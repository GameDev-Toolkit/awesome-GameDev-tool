<div align="center">

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

# Contributing to awesome-GameDev-tool

**Found something missing or broken? Open a pull request — that is the whole process.**

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/pulls)
[![Link check](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/actions/workflows/link-check.yml/badge.svg)](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/actions/workflows/link-check.yml)

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

</div>

You do **not** need to open an issue first, and you do not need to ask anyone. If you know the
tool and you have the link, you know enough to send a PR. A maintainer reviews it, fixes the small
stuff if needed, and merges.

## The 2-minute version

1. Open [README.md](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/blob/main/README.md)
   and click the ✏️ pencil icon ("Edit this file"). GitHub forks the repo for you.
2. Press `Ctrl+F`, find the right subsection, and add **one line** in alphabetical order.
3. Click **Commit changes**, then **Create a new branch for this commit and start a pull request**.

That's it. CI checks your link automatically, and a maintainer merges it. If the line is not
perfect, we will polish it in review — bad formatting is never a reason to close a PR.

## The entry format

One line per entry, alphabetised inside its subsection:

```markdown
- **[Name](https://example.com)** – One sentence about what it does and who it is for. `TAG`
```

Real example:

```markdown
- **[Aseprite](https://www.aseprite.org)** – The industry favourite: layers, onion skin, tags, tilesets and a powerful CLI. `PAID` `OSS`
```

**Good:**

```markdown
- **[LDtk](https://ldtk.io)** – Modern, friendly level editor with auto-layers, entities and a JSON format. `OSS` `FREE`
```

**Not good:**

- `- [SuperTool](https://supertool.io) — tool` — no bold, no tags, says nothing.
- `- **[SuperTool](https://supertool.io)** – The best engine ever!!` — hype instead of facts.
- `- **[SuperTool](https://supertool.io?ref=me)** – ...` — tracking parameter.

The details: en dash `–` between name and description (not a hyphen), one factual sentence of
about 120 characters or less, no marketing words, tags in backticks at the end.

## Tags

| Tag | When to use it |
| :-- | :-- |
| `OSS` | Source code is public (GitHub, GitLab, SourceForge…) and it can be built |
| `FREE` | Free to use, but closed source |
| `FREEMIUM` | Free tier exists, paid plans or royalties for more |
| `PAID` | Requires payment (one-time or subscription) |
| `WEB` | Runs in the browser, nothing to install |
| `AI` | Uses generative AI |

Not sure? Leave them off — a maintainer will add them. A wrong tag is worse than no tag.

## Where does the entry go?

Put it under the section matching what the tool **is**, not what it is made with:

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

Two sections fit? Pick the one a reader would search first, and add it **only once**.

## What belongs here

A tool, service, library, portal or resource a game developer would realistically use **while
making a game** — engines and libraries, art/audio/animation software, asset stores, QA and CI,
backend and monetization services, learning resources and communities.

It should be useful to more than one person, still working, and reachable without an invite-only
beta.

**Please don't add:** unreleased products with only a landing page, links to articles *about* a
tool instead of the tool, link farms and "top 10 tools" listicles, paid courses dressed up as free
resources, duplicates (search the name and the domain first), or anything NSFW, pirated or of
unclear legal status.

> **Asset rips:** sites like The Models Resource are handy for study, but their assets are not
> licensed for shipping. If you add one, say so in the description.

## Link rules

1. **HTTPS, canonical URL** — `https://godotengine.org`, not a `/download/linux/` subpage or a
   redirecting `http://` version.
2. **Link to the thing itself**, not to an article about it and not to a search result.
3. **Official site first**; for open-source projects the repository is fine and often more stable.
4. **No dead links** — open it in a private window before submitting.
5. **No shorteners, no tracking** (`utm_*`, `?ref=`, `fbclid`, `gclid`, `bit.ly`).
6. If the site is alive but blocks bots (Cloudflare, login wall), add it to
   [`.linksignore`](.linksignore) **with a reason** in the same PR:

```
https://example.com/*    # Cloudflare blocks automated clients, verified by hand 2026-10
```

## Prefer the terminal?

```bash
gh repo fork GameDev-Toolkit/awesome-GameDev-tool --clone
cd awesome-GameDev-tool
git checkout -b add-my-tool
# edit README.md
python3 scripts/check_links.py README.md   # optional, needs Python 3.9+, no dependencies
git commit -am "Add LibreSprite to pixel art editors"
git push -u origin add-my-tool
gh pr create --fill
```

Name the PR `Add <Tool>` or `Fix <what>`, and tell us in one or two sentences **why** you like the
tool. Personal experience beats a feature list.

## A whole new category?

Welcome, if it earns its place: at least **5–8 solid entries** that fit nowhere else. Use
`## N. Title` and `### N.M Subtitle`, add it in pipeline order (engines → art → audio → design →
tech → business → learning), and mention it in the PR — we will handle numbering and the table of
contents together with you.

## Review and merge

- A maintainer reviews PRs **weekly**, usually much faster.
- CI (`link-check`) runs on every PR and must pass.
- Small, focused PRs merge quickly; a PR that reformats 300 lines will be asked to split.
- No news for two weeks? Ping it with a comment — no hard feelings.
- We may tweak your description, tags or position. That is normal, not a rejection.

## Not ready to open a PR?

That's fine. [Open an issue](https://github.com/GameDev-Toolkit/awesome-GameDev-tool/issues/new/choose)
with the tool or the dead link and someone will turn it into a PR. But honestly — editing one line
on GitHub is less work than writing an issue.

## Code of conduct

Be decent to each other. Harassment, gatekeeping and "just learn to code" snark are not welcome.
Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Maintainers may remove comments, commits or
contributions that violate it.

<div align="center">

<img src="image/line-svg-3D444D-alg.svg" alt="" width="100%">

**Thanks for making this list better.** 🎮

<sub>Inspired by the [Awesome](https://awesome.re) manifesto.</sub>

</div>
