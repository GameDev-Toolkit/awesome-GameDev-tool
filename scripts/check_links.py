#!/usr/bin/env python3
"""
check_links.py — find dead links in this awesome list.

Scans Markdown files for links (inline links, autolinks, reference definitions
and HTML href/src attributes), then requests every unique URL concurrently and
reports the ones that are broken.

Zero dependencies: Python 3.9+ standard library only.

Usage
-----
    python3 scripts/check_links.py                    # check all Markdown files
    python3 scripts/check_links.py README.md          # check one file
    python3 scripts/check_links.py --jobs 32          # more parallelism
    python3 scripts/check_links.py --report report.md --json report.json
    python3 scripts/check_links.py --fail-on-blocked  # strict mode for CI
    python3 scripts/check_links.py --list             # just list every URL

Exit codes
----------
    0  no broken links (blocked links are warnings unless --fail-on-blocked)
    1  at least one broken link
    2  bad usage / nothing to check

Notes
-----
* 401/403/405/429/999 and similar "go away, robot" responses are reported as
  BLOCKED, not BROKEN: the site is alive, it just refuses automated clients.
  Use `--fail-on-blocked` if you want those to fail the build as well.
* Rules in `.linksignore` are skipped, e.g. `https://x.com/*  # blocks bots`.
  Every rule should carry a short `# reason`.
* Local (relative) links are verified against the filesystem, so a broken
  `CONTRIBUTING.md` reference is caught too.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import fnmatch
import json
import os
import random
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Sequence

VERSION = "1.1.0"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 "
    "awesome-gamedev-tool-link-checker/" + VERSION
)

# Statuses that mean "the page exists but does not want bots".
BLOCKED_STATUSES = {401, 403, 405, 406, 409, 418, 429, 451, 999}
# Statuses that make a GET worth trying after a failed HEAD.
RETRY_WITH_GET = {400, 401, 403, 405, 406, 411, 429, 501}

DEFAULT_FILES = ("README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md")
MARKDOWN_GLOBS = ("*.md", "docs/*.md", "docs/**/*.md")


# --------------------------------------------------------------------------- #
# Markdown parsing
# --------------------------------------------------------------------------- #

INLINE_LINK_RE = re.compile(r"(?<!\!)\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*(<[^>]*>|[^()\s]+)(?:\s+[\"'][^\"']*[\"'])?\s*\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(\s*(<[^>]*>|[^()\s]+)")
AUTOLINK_RE = re.compile(r"<((?:https?|ftp)://[^>\s]+)>")
BARE_URL_RE = re.compile(r"(?<![\w(<\"'=])(https?://[^\s<>\"'`\])]+)")
HTML_ATTR_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


@dataclass
class Link:
    url: str
    file: str
    line: int
    text: str = ""


def _strip_code(text: str) -> str:
    """Blank out fenced code blocks and inline code, keeping line numbers stable."""
    text = CODE_FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), text)


def extract_links(text: str, filename: str, include_images: bool) -> list[Link]:
    cleaned = _strip_code(text)
    lines = cleaned.splitlines()
    found: list[Link] = []

    patterns = [INLINE_LINK_RE, AUTOLINK_RE, HTML_ATTR_RE, REF_DEF_RE]
    if include_images:
        patterns.insert(0, IMAGE_RE)

    for lineno, line in enumerate(lines, start=1):
        # Skip headings-with-anchors only sections? No: capture everything.
        seen_on_line: set[str] = set()
        for pattern in patterns:
            for match in pattern.finditer(line):
                url = match.group(1) if match.groups() else match.group(0)
                if pattern is HTML_ATTR_RE:
                    url = match.group(1)
                elif pattern in (INLINE_LINK_RE, IMAGE_RE) and url.startswith("<"):
                    url = url[1:-1]
                url = url.strip()
                if not url or url in seen_on_line:
                    continue
                seen_on_line.add(url)
                found.append(Link(url=url, file=filename, line=lineno))
        if not include_images:
            for match in BARE_URL_RE.finditer(line):
                url = match.group(1).rstrip(".,;:")
                if url in seen_on_line:
                    continue
                seen_on_line.add(url)
                found.append(Link(url=url, file=filename, line=lineno))
    return found


# --------------------------------------------------------------------------- #
# .linksignore
# --------------------------------------------------------------------------- #

@dataclass
class IgnoreRule:
    pattern: str
    reason: str = ""


def load_ignore_rules(path: Path) -> list[IgnoreRule]:
    rules: list[IgnoreRule] = []
    if not path.is_file():
        return rules
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)
        entry = line[0].strip()
        if not entry or entry.startswith("#"):
            continue
        reason = line[1].strip() if len(line) > 1 else ""
        rules.append(IgnoreRule(entry, reason))
    return rules


def is_ignored(url: str, rules: Sequence[IgnoreRule]) -> bool:
    for rule in rules:
        if fnmatch.fnmatchcase(url, rule.pattern) or rule.pattern in url:
            return True
    return False


# --------------------------------------------------------------------------- #
# HTTP checking
# --------------------------------------------------------------------------- #

@dataclass
class Result:
    url: str
    status: str                     # OK | BROKEN | BLOCKED | IGNORED | LOCAL_MISSING
    code: int | None = None
    detail: str = ""
    final_url: str = ""
    occurrences: list[Link] = field(default_factory=list)
    elapsed: float = 0.0
    rechecked: bool = False


class Checker:
    def __init__(self, timeout: float, retries: int, per_host: int, verify_ssl: bool):
        self.timeout = timeout
        self.retries = retries
        self.per_host = per_host
        self._host_locks: dict[str, threading.Semaphore] = {}
        self._lock = threading.Lock()
        if verify_ssl:
            self.context = ssl.create_default_context()
        else:
            self.context = ssl.create_default_context()
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=self.context),
            urllib.request.HTTPRedirectHandler(),
        )

    def _host_sem(self, url: str) -> threading.Semaphore:
        host = urllib.parse.urlsplit(url).netloc.lower() or "?"
        with self._lock:
            sem = self._host_locks.get(host)
            if sem is None:
                sem = threading.Semaphore(self.per_host)
                self._host_locks[host] = sem
            return sem

    def _request(self, url: str, method: str) -> tuple[int | None, str, str]:
        """Return (status_code, final_url, error_message)."""
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "identity",
            "Connection": "close",
        }
        request = urllib.request.Request(url, method=method, headers=headers)
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                if method == "GET":
                    response.read(2048)
                return response.status, response.geturl(), ""
        except urllib.error.HTTPError as exc:
            exc.close()
            return exc.code, url, ""
        except urllib.error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, socket.timeout):
                return None, url, "timeout"
            return None, url, f"connection error: {reason}"
        except (socket.timeout, TimeoutError):
            return None, url, "timeout"
        except ssl.SSLError as exc:
            return None, url, f"ssl error: {exc}"
        except Exception as exc:  # noqa: BLE001 - last-resort guard
            return None, url, f"{type(exc).__name__}: {exc}"

    def check(self, url: str) -> tuple[str, int | None, str, str]:
        started = time.monotonic()
        code, final_url, error = 200, url, ""
        sem = self._host_sem(url)

        for attempt in range(self.retries + 1):
            with sem:
                code, final_url, error = self._request(url, "HEAD")
                if code is None or code in RETRY_WITH_GET:
                    code, final_url, error = self._request(url, "GET")

            if code is not None and code not in (429, 500, 502, 503, 504, 522, 524):
                break
            if attempt < self.retries:
                backoff = (2 ** attempt) + random.uniform(0, 0.4)
                time.sleep(min(backoff, 8))

        elapsed = time.monotonic() - started
        if code is None:
            return "BROKEN", None, error or "unreachable", final_url
        if 200 <= code < 400:
            detail = "" if final_url.rstrip("/") == url.rstrip("/") else f"redirects to {final_url}"
            return "OK", code, detail, final_url
        if code in BLOCKED_STATUSES:
            return "BLOCKED", code, "refuses automated clients", final_url
        if code in (408, 425, 500, 502, 503, 504):
            return "BROKEN", code, "server error after retries", final_url
        return "BROKEN", code, "", final_url


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def is_local(url: str) -> bool:
    return not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) and not url.startswith("#")


def normalise_local(url: str) -> str:
    return urllib.parse.unquote(url.split("#", 1)[0].split("?", 1)[0])


def resolve_local(url: str, base: Path) -> Path:
    return (base / normalise_local(url)).resolve()


def looks_like_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))


def collect_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if ".git" not in p.parts))
        elif path.is_file():
            files.append(path)
        else:
            print(f"warning: {raw} does not exist, skipping", file=sys.stderr)
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def default_file_list() -> list[str]:
    candidates: list[str] = []
    for name in DEFAULT_FILES:
        if Path(name).is_file():
            candidates.append(name)
    for pattern in MARKDOWN_GLOBS:
        candidates.extend(sorted(str(p) for p in Path(".").glob(pattern)))
    unique: list[str] = []
    for path in candidates:
        if path not in unique:
            unique.append(path)
    return unique


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def print_section(title: str, results: Sequence[Result], *, show_detail: bool) -> None:
    print(f"\n{title} ({len(results)})")
    print("-" * max(len(title) + 6, 40))
    for res in sorted(results, key=lambda r: r.url):
        label = f"HTTP {res.code}" if res.code else res.detail or "error"
        print(f"  {res.url}  [{label}]")
        if show_detail:
            for link in res.occurrences[:6]:
                print(f"      {link.file}:{link.line}")
            if len(res.occurrences) > 6:
                print(f"      … and {len(res.occurrences) - 6} more")
        elif res.detail and res.status == "OK":
            print(f"      {res.detail}")


def write_markdown_report(path: Path, results: Sequence[Result], stats: dict) -> None:
    broken = [r for r in results if r.status == "BROKEN"]
    slow = [r for r in results if r.status == "SLOW"]
    blocked = [r for r in results if r.status == "BLOCKED"]
    lines = [
        "# Link check report",
        "",
        f"- Checked: **{stats['checked']}** unique links in {stats['files']} file(s)",
        f"- OK: **{stats['ok']}**",
        f"- Broken: **{len(broken)}**",
        f"- Blocked (bot protection, not dead): **{len(blocked)}**",
        f"- Slow (timed out even after re-check): **{len(slow)}**",
        f"- Ignored: **{stats['ignored']}**",
        "",
    ]
    if broken:
        lines += ["## Broken links", "", "| URL | Status | Where |", "| :-- | :-- | :-- |"]
        for res in broken:
            where = ", ".join(f"{l.file}:{l.line}" for l in res.occurrences[:3])
            lines.append(f"| {res.url} | {res.code or res.detail} | {where} |")
        lines.append("")
    if slow:
        lines += ["## Slow links", "", "Timed out twice — probably fine, worth a manual look.", ""]
        for res in slow:
            lines.append(f"- {res.url}")
        lines.append("")
    if blocked:
        lines += ["## Blocked links", "", "Sites that refuse automated clients — verify by hand.", ""]
        for res in blocked:
            lines.append(f"- {res.url} (HTTP {res.code})")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="check_links.py",
        description="Check every link in this awesome list and report the dead ones.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python3 scripts/check_links.py\n"
            "  python3 scripts/check_links.py README.md --jobs 16\n"
            "  python3 scripts/check_links.py --report report.md --json report.json\n"
        ),
    )
    parser.add_argument("paths", nargs="*", help="Markdown files or directories (default: all *.md)")
    parser.add_argument("--jobs", type=int, default=24, help="parallel requests (default: 24)")
    parser.add_argument("--per-host", type=int, default=2, help="max parallel requests per host (default: 2)")
    parser.add_argument("--timeout", type=float, default=20.0, help="request timeout in seconds (default: 20)")
    parser.add_argument("--retries", type=int, default=2, help="retries for flaky responses (default: 2)")
    parser.add_argument("--ignore-file", default=".linksignore", help="path to the ignore file")
    parser.add_argument("--no-ignore", action="store_true", help="ignore the .linksignore rules")
    parser.add_argument("--include-images", action="store_true", help="also check image sources")
    parser.add_argument("--fail-on-blocked", action="store_true", help="treat blocked links as failures")
    parser.add_argument(
        "--recheck",
        action="store_true",
        help="re-check failures serially before reporting them (kills flaky CI runs)",
    )
    parser.add_argument("--no-insecure-ssl", action="store_true", help="verify TLS certificates strictly")
    parser.add_argument(
        "--fail-on-timeout",
        action="store_true",
        help="fail when a link times out even after the re-check",
    )
    parser.add_argument(
        "--annotations",
        action="store_true",
        help="emit GitHub Actions annotations for broken links (used in CI)",
    )
    parser.add_argument("--report", metavar="PATH", help="write a Markdown report")
    parser.add_argument("--json", metavar="PATH", help="write a JSON report")
    parser.add_argument("--list", action="store_true", help="only list the URLs that would be checked")
    parser.add_argument("--quiet", action="store_true", help="only print problems")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    targets = args.paths or default_file_list()
    files = collect_files(targets)
    if not files:
        print("error: no Markdown files to check", file=sys.stderr)
        return 2

    base_dir = Path.cwd()
    rules: list[IgnoreRule] = [] if args.no_ignore else load_ignore_rules(Path(args.ignore_file))

    links: list[Link] = []
    local_links: list[Link] = []
    for file in files:
        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = file.read_text(encoding="utf-8", errors="replace")
        for link in extract_links(text, str(file), args.include_images):
            url = link.url
            if url.startswith("#") or url.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            if is_local(url):
                local_links.append(link)
            elif looks_like_url(url):
                links.append(link)

    # Collapse duplicates, remembering where each one appeared.
    by_url: dict[str, list[Link]] = {}
    for link in links:
        by_url.setdefault(link.url, []).append(link)

    ignored_urls = {u: occ for u, occ in by_url.items() if is_ignored(u, rules)}
    pending = {u: occ for u, occ in by_url.items() if u not in ignored_urls}

    # Local file references.
    local_missing: list[Result] = []
    for link in local_links:
        if not resolve_local(link.url, base_dir).exists():
            local_missing.append(
                Result(url=link.url, status="LOCAL_MISSING", detail="file not found", occurrences=[link])
            )

    if args.list:
        for url in sorted(by_url):
            print(url)
        return 0

    if not args.quiet:
        print(f"Checking {len(pending)} unique links in {len(files)} file(s) "
              f"with {args.jobs} workers …", file=sys.stderr)

    checker = Checker(
        timeout=args.timeout,
        retries=args.retries,
        per_host=max(1, args.per_host),
        verify_ssl=not args.no_insecure_ssl,
    )

    results: list[Result] = []
    done = 0
    total = len(pending)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {pool.submit(checker.check, url): url for url in pending}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                status, code, detail, final_url = future.result()
            except Exception as exc:  # noqa: BLE001
                status, code, detail, final_url = "BROKEN", None, f"{type(exc).__name__}: {exc}", url
            results.append(
                Result(url=url, status=status, code=code, detail=detail,
                       final_url=final_url, occurrences=pending[url])
            )
            done += 1
            if not args.quiet and (done % 25 == 0 or done == total):
                print(f"  … {done}/{total}", file=sys.stderr)

    results.extend(local_missing)

    if args.recheck:
        suspects = [r for r in results if r.status == "BROKEN"][:60]
        if suspects:
            print(f"Re-checking {len(suspects)} suspect link(s) …", file=sys.stderr)
            slow = Checker(
                timeout=max(args.timeout, 60.0),
                retries=2,
                per_host=1,
                verify_ssl=not args.no_insecure_ssl,
            )
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                again = {pool.submit(slow.check, r.url): r for r in suspects}
                for future in concurrent.futures.as_completed(again):
                    res = again[future]
                    try:
                        status, code, detail, final_url = future.result()
                    except Exception as exc:  # noqa: BLE001
                        continue
                    was_broken = status == "BROKEN"
                    res.status, res.code, res.detail, res.final_url = status, code, detail, final_url
                    res.rechecked = True
                    if not was_broken:
                        print(f"  recovered on recheck: {res.url}", file=sys.stderr)

        # A site that never answers is not necessarily dead — most often it is
        # just slow or rate-limiting CI. Report those separately.
        for res in results:
            if res.rechecked and res.status == "BROKEN" and res.detail == "timeout":
                res.status = "SLOW"

    broken = [r for r in results if r.status in ("BROKEN", "LOCAL_MISSING")]
    blocked = [r for r in results if r.status == "BLOCKED"]
    slow = [r for r in results if r.status == "SLOW"]
    ok = [r for r in results if r.status == "OK"]
    redirects = [r for r in ok if r.detail]

    if not args.quiet:
        print_section("BROKEN LINKS", broken, show_detail=True)
        if slow:
            print_section("SLOW (timed out, verify by hand)", slow, show_detail=False)
        if blocked:
            print_section("BLOCKED (alive, but refusing bots)", blocked, show_detail=False)
        if redirects:
            print_section("REDIRECTS (consider updating)", redirects, show_detail=False)

    stats = {
        "checked": len(results),
        "files": len(files),
        "ok": len(ok),
        "broken": len(broken),
        "blocked": len(blocked),
        "ignored": len(ignored_urls),
        "slow": len(slow),
    }

    print(
        f"\nSummary: {stats['checked']} checked · {stats['ok']} ok · "
        f"{stats['broken']} broken · {stats['blocked']} blocked · "
        f"{stats['slow']} slow · {stats['ignored']} ignored",
        file=sys.stderr if args.quiet else sys.stdout,
    )

    if args.annotations:
        # GitHub renders these next to the offending line in a failing PR.
        for res in broken[:20]:
            link = res.occurrences[0] if res.occurrences else None
            where = f" file={link.file},line={link.line}" if link else ""
            reason = f"HTTP {res.code}" if res.code else (res.detail or "unreachable")
            print(f"::error{where},title=Broken link::{res.url} ({reason})")
        for res in blocked[:10]:
            link = res.occurrences[0] if res.occurrences else None
            where = f" file={link.file},line={link.line}" if link else ""
            print(f"::warning{where},title=Link blocked for bots::{res.url} (HTTP {res.code})")
        for res in slow[:10]:
            link = res.occurrences[0] if res.occurrences else None
            where = f" file={link.file},line={link.line}" if link else ""
            print(f"::warning{where},title=Slow link (verify by hand)::{res.url} timed out twice")

    if args.report:
        write_markdown_report(Path(args.report), results, stats)
        print(f"Markdown report written to {args.report}", file=sys.stderr)
    if args.json:
        payload = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stats": stats,
            "broken": [
                {
                    "url": r.url,
                    "status": r.status,
                    "code": r.code,
                    "detail": r.detail,
                    "locations": [f"{l.file}:{l.line}" for l in r.occurrences],
                }
                for r in broken
            ],
            "blocked": [{"url": r.url, "code": r.code} for r in blocked],
            "slow": [{"url": r.url, "detail": r.detail} for r in slow],
            "redirects": [
                {"url": r.url, "final_url": r.final_url} for r in redirects
            ],
        }
        Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"JSON report written to {args.json}", file=sys.stderr)

    if broken:
        return 1
    if args.fail_on_timeout and slow:
        return 1
    if args.fail_on_blocked and blocked:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
