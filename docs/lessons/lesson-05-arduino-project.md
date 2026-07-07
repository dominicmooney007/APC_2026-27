# Lesson 05 — Arduino Mini-Project: Interactive Reactive Device

> Design and build one device that senses something, decides something, and does something. **First graded build.**

**Platform:** Arduino
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lessons 2–4](lesson-02-arduino-digital.md) — everything so far

## The brief

Build a device that follows the pattern behind all physical computing:

**INPUT** (a sensor you choose) → **LOGIC** (decisions in your code) → **OUTPUT** (something a person can see, hear, or watch move)

You have everything you need: buttons, the pot, DHT22, HC-SR04 for input; LEDs, the LCD, the buzzer, servo, and (at the demo station) the L298N fan for output; `if`/`map()`/serial for the logic in between.

## Requirements (what gets graded)

| # | Requirement |
|---|---|
| 1 | At least **one sensor input** and **one physical output** |
| 2 | Logic that makes a *decision* — not just input piped straight to output |
| 3 | `Serial.println` debugging output showing the device's state |
| 4 | Code in the class repo format: named sketch folder, comment header saying what it does and how it's wired |
| 5 | A working **demo** in the last 15 minutes |

!!! note "Working & simple beats ambitious & broken"
    A finished two-component device demos better than an unfinished four-component one. Scope small; extend if time remains.

## Project ideas (pick one or invent your own)

- **Parking sensor, finished** — take Lesson 4's core build further: beep rate scales with distance, LCD shows a zone bar, knob adjusts the alert threshold.
- **Auto gate** — HC-SR04 + servo + LCD: gate opens when a "vehicle" approaches, closes 5 s after it clears, LCD narrates the state. (Last year's class favourite — build your own version, then compare with the state-machine starter.)
- **Smart fan** — DHT22 + L298N fan: fan kicks in above a set temperature, speed scales with heat, LCD shows temp + fan %. Knob overrides manually.
- **Climate alarm** — DHT22 + buzzer + LCD: alert when humidity or temperature leaves a healthy range; different tones for different problems.
- **Reaction-time game** — LED + button + LCD scoreboard: random delay, LED on, measure `millis()` until press; best time on the LCD.
- **Instrument** — pot + buzzer theremin from Lesson 3, upgraded: button toggles scales/modes, LCD shows the note.

## Today's plan (~120 min)

| Time | Phase | What you're doing |
|---|---|---|
| ~15 min | Plan | Sketch the idea: what's IN, what's OUT, what's the rule in between? Get a thumbs-up before wiring. |
| ~30 min | Wire | Breadboard the circuit. Power off while wiring — as always. |
| ~50 min | Code | Build in slices: sensor printing to serial *first*, then output, then the logic. |
| ~15 min | Demo | Show it working; explain one problem you hit and how you found it. |
| ~10 min | Submit | Sketch folder into the class repo/hand-in. |

!!! tip "Build in slices, not all at once"
    Get the sensor printing believable numbers to serial before you write any logic. Half of all project bugs are actually wiring bugs you'd have caught in 30 seconds of `Serial.println`.

!!! tip "Catch-up option"
    If you never finished a core build from Lessons 2–4, finishing it *is* a valid project base — e.g. the Lesson 4 distance dial with zones added becomes the parking sensor.

## Check your work

Before you call it done:

- Unplug it, plug it back in — does it still work from a cold start?
- Does the serial output tell the story of what it's doing?
- Can you explain every line of your sketch? (You'll be asked about one.)

## Extension / challenge

Finished early? Add a **second output mode** (e.g. the parking sensor gets a "night mode" toggled by a button), or make the thresholds adjustable with the pot instead of hard-coded.

## Code

- [`code/lesson-05/smart_fan_starter/`](https://github.com/dominicmooney007/APC_2026-27/tree/main/code/lesson-05/smart_fan_starter) — a deliberately *incomplete* starter for the smart fan showing the required structure (comment header, state via serial). Don't copy it — outdo it.
- [`code/lesson-04/auto_gate/`](https://github.com/dominicmooney007/APC_2026-27/tree/main/code/lesson-04/auto_gate) — the auto-gate state machine, if that's your base.

**Next up:** [Lesson 6 — Raspberry Pi 5: Linux & remote access](lesson-06-pi-intro.md)
