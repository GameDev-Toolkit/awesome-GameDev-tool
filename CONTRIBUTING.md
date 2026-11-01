<div align="center">

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

# Contributing to awesome-GameDev-tool

**One good tool you love is worth more than ten random links.**

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/pulls)
[![Link check](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/actions/workflows/link-check.yml/badge.svg)](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/actions/workflows/link-check.yml)

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

</div>

Thanks for helping out! This list only stays useful because people like you fix dead links,
add the tool that saved their project, and argue politely about categories.

There are three ways to contribute, in ascending order of effort:

| I want to… | Do this |
| :-- | :-- |
| Report a dead or wrong link | [Open an issue](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/issues/new?title=Dead%20link:%20) with the URL |
| Suggest a tool quickly | [Open an issue](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/issues/new?title=Add:%20) — someone will turn it into a PR |
| Add it yourself | Follow this guide and open a pull request (2 minutes, promise) |

## Contents

- [What belongs here](#what-belongs-here)
- [What does not belong here](#what-does-not-belong-here)
- [Where to put your entry](#where-to-put-your-entry)
- [The entry format](#the-entry-format)
- [Tags and the legend](#tags-and-the-legend)
- [Link rules](#link-rules)
- [Add an entry: step by step](#add-an-entry-step-by-step)
- [Adding a whole new category](#adding-a-whole-new-category)
- [Check your links locally](#check-your-links-locally)
- [Pull request checklist](#pull-request-checklist)
- [Review and merge](#review-and-merge)
- [Code of conduct](#code-of-conduct)

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

## What belongs here

A tool, service, library, portal or resource that a game developer would realistically
use **while making a game**:

- engines, frameworks and libraries
- art, audio, animation and level-design software
- asset libraries and marketplaces
- QA, profiling, CI and version control
- backend, analytics, monetization and publishing services
- learning resources, communities, jams and reference material

The tool should be **useful to more than one person**, **still maintained or still working**,
and **reachable without an invite-only beta**.

## What does not belong here

- ❌ Your own unreleased product with a landing page and no download
- ❌ Abandoned tools whose site no longer resolves (see [link rules](#link-rules))
- ❌ Affiliate, referral or tracked links (`?ref=`, `utm_*`, shorteners like `bit.ly`)
- ❌ Link farms, SEO listicles, or "top 10 tools" articles
- ❌ Paid courses disguised as free resources
- ❌ Anything NSFW, pirated, or of unclear legal status (asset rips are a grey area — see below)
- ❌ Duplicates: search the README first (`Ctrl+F` on the tool name and on the domain)

> **Asset rips:** sites like The Models Resource are useful for study and reverse engineering,
> but the assets are not licensed for shipping. If you add such a site, say so in the description.

## Where to put your entry

Find the section that matches what the tool *is*, not what it is *made with*:

| The tool is… | Section |
| :-- | :-- |
| A complete engine with an editor | [1. Game Engines](README.md#1-game-engines) |
| A code library you build on | [2. Frameworks and Libraries](README.md#2-frameworks-and-libraries) |
| Pixel art, painting, UI or vector design | [3. 2D Art and Pixel Art](README.md#3-2d-art-and-pixel-art) |
| 3D modelling, texturing, rigging, voxels | [4. 3D Art and Modeling](README.md#4-3d-art-and-modeling) |
| Shaders, particles, VFX | [5. VFX, Shaders and Rendering](README.md#5-vfx-shaders-and-rendering) |
| Tilemaps, terrain, world and map making | [6. Level Design and World Building](README.md#6-level-design-and-world-building) |
| Music, SFX, voice, audio middleware | [7. Audio and Music](README.md#7-audio-and-music) |
| Free/paid asset stores, icons, textures | [8. Assets, Textures and Icons](README.md#8-assets-textures-and-icons) |
| Storyboards, cutscenes, video editing | [9. Animation, Cinematics and Video](README.md#9-animation-cinematics-and-video) |
| Writing, lore and worldbuilding | [10. Narrative, Dialogue and Writing](README.md#10-narrative-dialogue-and-writing) |
| Design docs, prototyping, tabletop | [11. Game Design and Prototyping](README.md#11-game-design-and-prototyping) |
| PICO-8, retro consoles, homebrew | [12. Fantasy Consoles and Retro Dev](README.md#12-fantasy-consoles-and-retro-dev) |
| Generative AI, procedural generation | [13. AI and Procedural Generation](README.md#13-ai-and-procedural-generation) |
| Netcode, lobbies, backend, hosting | [14. Multiplayer, Networking and Backend](README.md#14-multiplayer-networking-and-backend) |
| Analytics, LiveOps, ads, payments | [15. Analytics, LiveOps and Monetization](README.md#15-analytics-liveops-and-monetization) |
| Stores, PR, marketing, festivals | [16. Publishing, Stores and Marketing](README.md#16-publishing-stores-and-marketing) |
| Testing, profiling, crash reporting | [17. QA, Debugging and Profiling](README.md#17-qa-debugging-and-profiling) |
| Build systems, CI, version control | [18. Build, CI/CD and Version Control](README.md#18-build-cicd-and-version-control) |
| Editors, IDEs, coding assistants | [19. Programming Tools and IDEs](README.md#19-programming-tools-and-ides) |
| Physics, math, serialization, GPU APIs | [20. Core Libraries, Physics and Math](README.md#20-core-libraries-physics-and-math) |
| Translation and accessibility | [21. Localization and Accessibility](README.md#21-localization-and-accessibility) |
| Courses, docs, other awesome lists | [22. Learning and Documentation](README.md#22-learning-and-documentation) |
| Forums, news, game jams | [23. Communities, News and Game Jams](README.md#23-communities-news-and-game-jams) |
| Generic dev utilities | [24. Everyday Utilities](README.md#24-everyday-utilities) |

If two sections fit, pick the one a reader would search first, and **only add it once**.

## The entry format

Every entry is a single line, alphabetised inside its subsection:

```markdown
- **[Name](https://example.com)** – One sentence about what it does and who it is for. `TAG`
```

Real example:

```markdown
- **[Aseprite](https://www.aseprite.org)** – The industry favourite: layers, onion skin, tags, tilesets and a powerful CLI. `PAID` `OSS`
```

Rules for the line:

1. **`- `** then the name in `**[Name](url)**` — bold and linked.
2. Use an **en dash** `–` (not a hyphen `-`) between name and description.
3. Description: **one sentence, max ~120 characters**, sentence case, no trailing period rules —
   just be consistent with the neighbours (descriptions here end with a period).
4. No marketing fluff ("revolutionary", "best-in-class", "game-changing").
   Say what it *does*: "Node-based procedural texture generator for Godot".
5. End with tags in backticks, separated by spaces: `` `OSS` `FREE` ``.
6. Keep the line under ~200 characters so it stays readable in diffs.

### Good vs. not good

| ✅ Good | ❌ Why not |
| :-- | :-- |
| `- **[LDtk](https://ldtk.io)** – Modern, friendly level editor with auto-layers, entities and a JSON format. \`OSS\` \`FREE\`` | — |
| `- **[SuperTool](https://supertool.io)** – The best game engine!!` | Hype instead of facts, no tags |
| `- [SuperTool](https://supertool.io) — tool` | No bold, no tags, three-word description |
| `- **[SuperTool](https://supertool.io?ref=me)** – ...` | Referral parameter |

## Tags and the legend

Use these exact tags — they match the [legend in the README](README.md#legend):

| Tag | When to use it |
| :-- | :-- |
| `OSS` | Source code is public (GitHub, GitLab, SourceForge…) and it can be built |
| `FREE` | Free to use, but closed source |
| `FREEMIUM` | Free tier/version exists, paid plans or royalties for more |
| `PAID` | Requires payment (one-time or subscription) |
| `WEB` | Runs in the browser, nothing to install |
| `AI` | Uses generative AI |

Not sure? Leave the tags off — a maintainer will add them. A wrong tag is worse than no tag.

## Link rules

CI checks every link, but please do your part:

1. **HTTPS, canonical URL.** Use `https://godotengine.org`, not `https://godotengine.org/download/linux/`
   or a redirecting `http://` version.
2. **Link to the thing itself**, not to an article about it, not to a Google search result.
3. **Prefer the official site**; for open-source projects a GitHub/GitLab **repository** is fine
   (and often more stable than a marketing site).
4. **No dead links.** Open the URL in a private window before submitting. If it 404s, don't add it.
5. **No URL shorteners or tracking parameters** (`utm_*`, `?ref=`, `fbclid`, `gclid`).
6. **Platform stores are acceptable** for games/tools that only exist there (e.g. an itch.io app),
   but point at the store page, not an affiliate link.
7. **Anchors are fine** if the target section exists (`https://example.com/docs#install`).

If a link is alive but blocks bots (Cloudflare, login walls), add it to
[`.linksignore`](.linksignore) **with a reason** in the same PR:

```
https://example.com/*    # Cloudflare blocks automated clients, verified by hand 2026-10
```

## Add an entry: step by step

### 1. Fork and clone

```bash
gh repo fork GameDev-Toolkit/awesome-GameDev-tool --clone
cd awesome-GameDev-tool
git checkout -b add-my-tool
```

<details>
<summary>No <code>gh</code>? Use the web UI instead</summary>

1. Open [README.md](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/blob/main/README.md).
2. Click the ✏️ pencil icon ("Edit this file").
3. GitHub forks the repository for you automatically.
4. Make your change, then choose **Create a new branch for this commit and start a pull request**.

</details>

### 2. Find the right subsection

Open `README.md`, press `Ctrl+F`, and search for a nearby tool to find the right block.
Sections look like this:

```markdown
### 3.1 Pixel Art Editors

- **[Aseprite](https://www.aseprite.org)** – ...
- **[LibreSprite](https://libresprite.github.io)** – ...
```

### 3. Insert your line alphabetically

Ignore case and punctuation when sorting; `**` and `[` don't count.

```diff
 - **[GraphicsGale](https://graphicsgale.com/us/)** – Long-standing pixel and animation editor, now freeware. `FREE`
+- **[LibreSprite](https://libresprite.github.io)** – Free fork of the last open-source Aseprite, actively maintained. `OSS` `FREE`
 - **[Pixelorama](https://github.com/Orama-Interactive/Pixelorama)** – Free, cross-platform pixel editor with animation and infinite canvas. `OSS` `FREE`
```

### 4. Check that your change is clean

```bash
git diff                     # one added line, nothing else
python3 scripts/check_links.py README.md
```

### 5. Commit and push

```bash
git commit -am "Add LibreSprite to pixel art editors"
git push -u origin add-my-tool
gh pr create --fill
```

Write the PR title as `Add <Tool>` or `Fix <what>`. In the description, tell us **why** you like
the tool — one or two sentences is plenty.

## Adding a whole new category

New top-level categories are welcome, but they need to earn their place:

1. There are **at least 5–8 solid entries** that don't fit anywhere else.
2. It gets a number, a title, and a one-line blockquote intro, in the same style as the others.
3. It is added in the right place in the **Contents** list and in **CONTRIBUTING.md's section map**
   (this file), otherwise the two documents drift apart.
4. Use `## N. Title` for the category and `### N.M Subtitle` for subsections.
5. Match the existing order: sections run roughly along the production pipeline
   (engines → art → audio → design → tech → business → learning).

## Check your links locally

The repository ships with a dependency-free checker:

```bash
python3 scripts/check_links.py                 # everything
python3 scripts/check_links.py README.md       # just the list
python3 scripts/check_links.py --jobs 32       # faster (be kind to small sites)
python3 scripts/check_links.py --list          # show URLs without checking
python3 scripts/check_links.py --fail-on-blocked --report report.md
```

Requires **Python 3.9+**. It reports:

- **BROKEN** — 404, 410, DNS failure, TLS failure after retries → must be fixed
- **BLOCKED** — 401/403/429 (`refusing bots`) → not necessarily dead, verify by hand
- **UNVERIFIED** — timed out twice, or the network died → usually a slow host, worth checking by hand
- **REDIRECTS** — works, but the canonical URL moved → nice to update

Failures are automatically re-checked before they are reported, so one slow host will not
turn a PR red. Use `--fail-on-unverified` if you want network-level failures to fail the run too.

Exit code is `1` if anything is broken, so you can wire it into your own pre-commit hook:

```bash
printf '#!/bin/sh\npython3 scripts/check_links.py README.md\n' > .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## Pull request checklist

Copy this into your PR description:

```markdown
- [ ] The tool is new (searched the list for its name and domain)
- [ ] It is in the correct section and alphabetical position
- [ ] The line follows the format: `- **[Name](url)** – Description. \`TAG\``
- [ ] The link is HTTPS, canonical, and opens in a private window
- [ ] No affiliate/tracking parameters, no URL shorteners
- [ ] Description is one factual sentence, no marketing language
- [ ] `python3 scripts/check_links.py README.md` passes
- [ ] I have used this tool (or verified it works today)
```

## Review and merge

- A maintainer reviews PRs **weekly** (usually much faster).
- CI (`link-check`) runs on every PR and must pass.
- Small, focused PRs are merged quickly. A PR that reformats 300 lines will be asked to split.
- If your PR goes quiet for more than two weeks, ping it with a comment — no hard feelings.

We may edit your description for tone, tags or position. That's normal and not a rejection.

## Code of conduct

Be decent to each other. Harassment, gatekeeping and "just learn to code" snark are not welcome.
Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Maintainers may remove comments, commits
or contributions that violate it.

<div align="center">

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

**Thanks for making this list better.** 🎮

<sub>Inspired by the [Awesome](https://awesome.re) manifesto.</sub>

</div>
