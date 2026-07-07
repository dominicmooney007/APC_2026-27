# Lesson 12 — Whisplay Mini-Project: Single-Button Game

> Take a working game apart, understand its loop, and rebuild it as *your* game. **Third graded build.**

**Platform:** Whisplay
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 11](lesson-11-whisplay-io.md) — button events, LED, audio, PIL→LCD

## The brief

The driver repo ships two complete single-button games — play them first:

```bash
cd Whisplay/example
sudo python3 flappy_bird.py     # short press = flap
sudo python3 jump_game.py       # hold to charge, release to jump
```

Your job is **not** to write a game from scratch. It's the more realistic skill: **take working code you didn't write, understand it, and change it into something meaningfully yours.** Pick one game as your base and modify it.

## Requirements (what gets graded)

| # | Requirement |
|---|---|
| 1 | At least **three meaningful modifications** (see tiers below) — cosmetic-only doesn't count |
| 2 | You can **explain the game loop** of your base game: where input is read, where state updates, where the frame is drawn |
| 3 | Game is **winnable/losable** and restartable without rerunning the script |
| 4 | Code in the repo format + a `CHANGES.md` listing what you changed and where |
| 5 | Someone else **playtests** your game in the final 20 minutes |

**Modification tiers** (mix at least one Tier 2+):

- **Tier 1 (easy):** new colours/graphics, new sounds (Lesson 11 skills!), different speeds/gravity, new title screen.
- **Tier 2 (real):** scoring change (combo, multiplier), difficulty ramp over time, lives system, obstacles that behave differently, LED reacts to game state (danger = red).
- **Tier 3 (ambitious):** new mechanic (moving gaps, power-ups), two-phase gameplay, persistent high score saved to a file.

## Today's plan (~120 min)

| Time | Phase | What you're doing |
|---|---|---|
| ~15 min | Play & pick | Play both games; choose your base |
| ~25 min | Read | Map the game loop (worksheet below); plan your 3 mods |
| ~55 min | Mod | Change → run → test, one modification at a time |
| ~20 min | Playtest | Swap seats, play each other's games, demo |
| ~5 min | Submit | Code + `CHANGES.md` to the repo/hand-in |

## Reading someone else's code (the worksheet)

Before changing anything, find and note the line numbers where your base game:

1. …reads the **button** (look for `on_button_press` / `button_pressed`)
2. …updates the **world** (position, velocity, obstacles — usually inside `while` loop math)
3. …detects **collision / game over**
4. …**draws the frame** (look for `draw_image` and the PIL drawing before it)
5. …plays a **sound**
6. …tracks the **score**

!!! tip "Change one number first"
    Before your real mods, change one constant (gravity, speed, a colour) and rerun. Two minutes, and now you *know* your edit-run loop works and roughly how the code responds. Then start the real work.

!!! warning "Copy the file first"
    Work on `my_game.py`, not the original — you want a known-good version to diff against when something breaks:
    ```bash
    cp flappy_bird.py my_game.py
    ```

## Check your work

- All three mods present and demonstrable, one of them Tier 2+.
- Cold start works: reboot the Pi, run the game, everything (screen, sound, LED, button) still behaves.
- Your `CHANGES.md` matches what the playtester actually experienced.

## Extension / challenge

Finished with time to spare? **High-score persistence** (write to a file, survive restarts, show on the title screen) is the most satisfying Tier 3 — small enough to finish, real enough to demo.

!!! note "Where this leads"
    The [`whisplay-ai-chatbot`](https://github.com/PiSugar/whisplay-ai-chatbot) project (GPL-3.0) turns this same HAT into a push-to-talk voice AI assistant. Heavy setup (Node + Python + API keys) puts it out of scope this semester, but it's a legitimate capstone stretch if you want one — talk to me.

## Code

- Your base: `Whisplay/example/flappy_bird.py` or `jump_game.py` — © PiSugar, [Apache-2.0](https://github.com/PiSugar/Whisplay/blob/main/LICENSE). Keep the attribution comment at the top of your modified file.
- [`code/lesson-12/CHANGES-template.md`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-12/CHANGES-template.md) — the required change log format.

**Next up:** [Lesson 13 — Mini-capstone: proposal & build](lesson-13-capstone-build.md)
