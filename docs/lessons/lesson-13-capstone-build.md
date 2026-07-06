# Lesson 13 — Mini-Capstone: Proposal & Build

> Your project, your platform, your idea — scoped tight enough to demo next lesson.

**Platform:** Any (Arduino, Pi, or Whisplay)
**Estimated time:** ~120 min hands-on (plus Lesson 14 to finish)
**Prerequisites:** The whole semester

## The brief

Design and build an original physical computing project on any platform from the course. You have **today plus most of Lesson 14** — roughly 3.5 hours of build time total. That's enough for something real, and not enough for something sprawling. Scope accordingly.

## Step 1 — The proposal (first ~25 min, required sign-off)

Fill in the proposal template (one per person or pair) and get it signed off **before touching hardware**:

- **Goal (one sentence):** "A device that ___."
- **Platform & why:** Arduino / Pi / Whisplay — and why it fits this idea.
- **Inputs and outputs:** which sensors, which actuators/displays/sounds.
- **The core loop:** what does it sense → decide → do, once a second?
- **Milestone 1 (today, minute 60):** the smallest demonstrable slice.
- **Milestone 2 (today, end):** input and output connected end-to-end.
- **Done means:** 2–3 bullet success criteria you'll be judged against.
- **Risk:** the one part most likely to eat your time, and your fallback.

!!! tip "The scope test"
    If your idea needs hardware we haven't used, a library nobody's installed, or more than one 'I hope this works' — shrink it. Strong capstones are usually *one clever behaviour, done well*: a graded build from earlier in the semester, combined with one new twist, is a perfectly good skeleton.

!!! warning "Out of scope"
    The Whisplay AI voice assistant (API keys, Node setup) and anything needing hardware the lab doesn't stock. Ask if unsure — *before* the proposal is signed.

## Step 2 — Build with checkpoints (~90 min)

Work in the order that kills risk fastest:

1. **Riskiest piece first.** Your proposal names it — prove it works in isolation before building around it.
2. **Milestone 1 by minute 60.** If you miss it, that's the signal to invoke your fallback *now*, not at minute 110.
3. **Commit as you go.** Code + a `README.md` in your project folder in the repo: goal, wiring table, how to run. Documentation is part of the grade — write it while you remember why things are the way they are.

## Check your work (end of today)

- [ ] Proposal signed off
- [ ] Riskiest component proven
- [ ] Milestone 2: end-to-end path works, even if rough
- [ ] Project folder in the repo with code + README started

Whatever state you're in, **note your next three tasks** in the README before pack-up — future-you starts Lesson 14 with zero warm-up time.

## Code

- [`code/lesson-13/proposal-template.md`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-13/proposal-template.md) — copy into your project folder and fill in.
- [`code/lesson-13/project-README-template.md`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-13/project-README-template.md) — the documentation skeleton.

**Next up:** [Lesson 14 — Mini-capstone: demo day & reflection](lesson-14-capstone-demo.md)
