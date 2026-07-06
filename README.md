# Advanced Physical Computing 2026–27

Course materials **and** code for APC Semester 1 (Arduino + Raspberry Pi 5 + Whisplay HAT), published as an interactive site with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Live site:** https://REPLACE-USERNAME.github.io/apc-2026-27/ *(update after first deploy)*

## Layout

```
mkdocs.yml          # site config + nav (nav order = Schoology link order)
docs/               # all lesson pages (Markdown = single source of truth)
  lessons/          # one page per lesson, chronological
  appendix/         # cross-links by hardware platform
  assets/           # images, diagrams, GIFs
code/               # code students download, foldered by lesson
templates/          # reusable lesson-page template
```

## Working on the site

```bash
# one-time setup
pip install mkdocs-material

# live-preview while editing (http://127.0.0.1:8000)
mkdocs serve

# build the static site into site/
mkdocs build
```

## Publishing to GitHub Pages

```bash
mkdocs gh-deploy
```

That builds the site and pushes it to the `gh-pages` branch; GitHub Pages serves it automatically (repo **Settings → Pages → Deploy from branch → `gh-pages`**, first time only). Then paste each lesson's live URL into Schoology in chronological order.

Before first deploy, replace `REPLACE-USERNAME` in `mkdocs.yml`, `README.md`, and the lesson pages with the real GitHub username/org (search the repo for `REPLACE-USERNAME`).

## Licensing notes

- Whisplay driver + examples: [Apache-2.0](https://github.com/PiSugar/Whisplay)
- whisplay-ai-chatbot (stretch/capstone): [GPL-3.0](https://github.com/PiSugar/whisplay-ai-chatbot)
