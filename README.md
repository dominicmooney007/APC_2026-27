# Advanced Physical Computing 2026–27

Course materials and code for **Advanced Physical Computing (APC)**, Semester 1 — a high-school elective that takes students from basic electronics through Arduino, the Raspberry Pi 5, and the Whisplay HAT, ending in a mini-capstone build.

Everything students need lives here: lesson pages with wiring diagrams and troubleshooting tips, and all the code they download, organized by lesson. The lessons are written in Markdown and published as an interactive site with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Live site:** https://dominicmooney007.github.io/APC_2026-27/ *(available after first deploy)*

## Who this is for

- **Students** — work through the lessons on the live site. Each page has copy-pasteable code, wiring tables, and fixes for common mistakes. Grades and deadlines live in Schoology, which links out to each lesson here in order.
- **Teachers reusing or adapting the course** — clone the repo, edit the Markdown in `docs/`, and republish. The lesson template and per-lesson code folders make it straightforward to add or swap activities.

No prior experience is assumed; Lesson 1 covers safety, basic electronics, and how to get the code.

## What's inside

The 14 lessons of Semester 1 progress across three hardware platforms:

| Lessons | Unit | Platform | Language / tools |
|---|---|---|---|
| 1 | Foundations — safety & electronics | — | — |
| 2–5 | Arduino | Arduino Uno | C++ / Arduino IDE |
| 6–9 | Raspberry Pi 5 | Raspberry Pi 5 | Python / Thonny |
| 10–12 | Whisplay HAT | Whisplay on the Pi | Python |
| 13–14 | Mini-capstone | Any | — |

## Repository layout

```
mkdocs.yml          # site config + nav (nav order = Schoology link order)
docs/               # all lesson pages (Markdown = single source of truth)
  lessons/          # one page per lesson, chronological
  appendix/         # reference guides by hardware platform
  assets/           # images, diagrams, GIFs
code/               # code students download, foldered by lesson
templates/          # reusable lesson-page template
```

## For maintainers

Preview and build the site locally:

```bash
pip install mkdocs-material   # one-time setup
mkdocs serve                  # live preview at http://127.0.0.1:8000
mkdocs build                  # build static site into site/
```

Publish to GitHub Pages:

```bash
mkdocs gh-deploy
```

This builds the site and pushes it to the `gh-pages` branch, which GitHub Pages serves automatically (first time only: **Settings → Pages → Deploy from branch → `gh-pages`**). Then paste each lesson's live URL into Schoology in chronological order.

## Licensing notes

- Whisplay driver + examples: [Apache-2.0](https://github.com/PiSugar/Whisplay)
- whisplay-ai-chatbot (stretch/capstone): [GPL-3.0](https://github.com/PiSugar/whisplay-ai-chatbot)
