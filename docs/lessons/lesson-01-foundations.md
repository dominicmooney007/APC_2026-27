# Lesson 01 — Foundations: Course, Safety & Electronics

> Learn how this course works, how to handle electronics safely, and build your first working LED circuit on a breadboard.

**Platform:** — (no board yet — breadboard only)
**Estimated time:** ~120 min hands-on
**Prerequisites:** None. This is where everything starts.

## Learning objectives

- Navigate the course site and get code from the class GitHub repo (Download ZIP **and** `git clone`).
- Follow the lab's safety rules for electronics: ESD, powering safely, and "power off before wiring."
- Explain what a breadboard's rows and rails connect, and wire components on one.
- Use Ohm's law to choose a current-limiting resistor for an LED — and explain why the LED needs one.
- Build a working LED circuit from a schematic.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~20 min | A | Course site tour + get the code from GitHub |
| ~20 min | B | Lab safety & handling electronics |
| ~35 min | C | Electronics primer: breadboards, LEDs, resistors, Ohm's law |
| ~40 min | D | **Core build:** your first LED circuit |
| ~5 min | — | Check-out: show a working circuit |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Breadboard | 1 | Half-size or full-size |
| Breadboard power supply module | 1 | Set the output jumper to **3.3 V** |
| LED (red) | 1 | Long leg = anode (+) |
| Resistor, 220 Ω | 1 | Red-red-brown-gold |
| Jumper wires | 2–3 | Male–male |

**Software:** just a web browser today (this site + GitHub).

---

## Part A — This site, Schoology & GitHub (~20 min)

How the course fits together:

- **Schoology** = front door. Announcements, grades, deadlines, and a link to each lesson **in order**.
- **This site** = the actual lessons. Copy-pasteable code, wiring tables, troubleshooting.
- **The GitHub repo** = this site's source *plus* all code, foldered by lesson in [`code/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code).

### Get the code — two ways

**Option 1 — Download ZIP (no tools needed):** on the [repo page](https://github.com/REPLACE-USERNAME/apc-2026-27), click **Code → Download ZIP**, then unzip.

**Option 2 — Clone with git (what you'll use on the Pi later):**

```bash
git clone https://github.com/REPLACE-USERNAME/apc-2026-27.git
```

### ✅ Checkpoint A

Open `code/lesson-01/clone_check.py` from your downloaded/cloned copy. If you can read the message inside it, you're done with Part A.

!!! tip "Deeper git later"
    Today you only need to *get* code. Commits, branches, and pushing your own work come later in the semester.

---

## Part B — Lab safety & handling electronics (~20 min)

!!! warning "The one rule that covers most accidents"
    **Power off before you wire.** Never add, remove, or move a wire while the circuit is powered. Unplug first, rewire, check, then power up.

The rest of the safety picture:

- **Static (ESD):** touch something metal and grounded before handling boards or chips. Carry boards by their edges, not by the pins.
- **Power:** only use the supplies provided; check voltage settings **before** connecting anything (today: 3.3 V, not 5 V).
- **Components:** don't force parts into a breadboard; bent pins break. Resistors don't have a direction; LEDs and chips do.
- **Bench habits:** keep drinks away from the bench, keep loose wires tidy, and return parts to the kit sorted — the next class inherits your bench.
- **If something gets hot or smells burnt:** disconnect power immediately and tell your teacher. Don't touch the hot part.

---

## Part C — Electronics primer (~35 min)

### The breadboard

- Each **row of 5 holes** (a–e, or f–j) is connected together internally.
- The long **rails** down the sides (+ and −) run the full length — use them for power and ground.
- The **center trench** splits the two halves; nothing crosses it (that's what chips straddle).

### The LED

An LED only lets current flow one way:

- **Long leg = anode (+)** → toward positive.
- **Short leg = cathode (−)**, flat spot on the rim → toward ground.

Backwards won't damage it at these voltages — it just won't light.

### Why the resistor? (Ohm's law)

An LED barely resists current at all once it turns on. Connect it straight across the supply and it pulls far too much current — and burns out. The resistor limits the current. Ohm's law tells us how much:

**V = I × R**, rearranged: **R = V ÷ I**

For our circuit:

| Quantity | Value | Where it comes from |
|---|---|---|
| Supply voltage | 3.3 V | Power supply module setting |
| LED forward voltage | ~2.0 V | Red LED datasheet value |
| Voltage across resistor | 3.3 − 2.0 = **1.3 V** | What's left over |
| Target current | 10 mA (0.010 A) | Bright but safe |
| Resistor needed | 1.3 ÷ 0.010 = **130 Ω** | Ohm's law |

130 Ω isn't a standard value, so we round **up** to the nearest standard one: **220 Ω**. Rounding up means slightly less current — dimmer is safe, brighter is not.

!!! note "This calculation comes back constantly"
    Every LED you wire this semester — on the Arduino *and* the Pi — gets a current-limiting resistor, chosen exactly this way.

---

## Part D — Core build: your first LED circuit (~40 min)

The circuit: power supply **+3.3 V → resistor → LED → ground**.

### Wiring

| From | To |
|---|---|
| Power module +3.3 V output | Breadboard **+ rail** |
| Power module GND output | Breadboard **− rail** |
| + rail | Row 10 (jumper wire) |
| Row 10 | 220 Ω resistor → Row 15 |
| Row 15 | LED **long leg (anode)** |
| Row 16 | LED **short leg (cathode)** |
| Row 16 | − rail (jumper wire) |

### Steps

1. **Power off.** The power module stays unplugged until step 5.
2. Seat the power module on the breadboard ends and set its output jumper to **3.3 V**. Have a partner double-check the jumper.
3. Place the resistor and LED per the wiring table. Check the LED's long leg is on the resistor side.
4. Add the two jumper wires (+ rail → row 10, row 16 → − rail).
5. Compare against the table one more time — *then* plug in the power module.

### ✅ Check your work

**Success looks like:** the LED lights steadily, at comfortable-to-look-at brightness, and nothing is warm to the touch.

!!! warning "LED doesn't light?"
    In order of likelihood: **(1)** LED is backwards — flip it (power off first!). **(2)** A leg is in the wrong row — components must share a row to be connected. **(3)** Power module switch is off or the rail jumper is missing. **(4)** Dead LED — swap it (rare).

!!! warning "LED is very bright or the resistor is warm?"
    Power off immediately. You've probably skipped the resistor (LED straight to the rail) or the supply is set to 5 V. Fix, re-check, repower.

---

## Extension / challenge

Finished early? In order:

1. **Two LEDs in parallel** — each LED gets its *own* 220 Ω resistor. Why can't they share one? (Hint: what happens to the current through a shared resistor?)
2. **Recalculate for 5 V** — if the supply were 5 V instead of 3.3 V, what resistor would you need for the same 10 mA? Check your answer against the table method above.
3. **Read a schematic** — sketch this circuit using standard symbols (battery, resistor, LED) and have your teacher check it. Every wiring diagram this semester builds on this.

## Code

- [`code/lesson-01/clone_check.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-01/clone_check.py) — the Checkpoint A file proving you got the repo.
- [`code/lesson-01/resistor_calc.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-01/resistor_calc.py) — a little Ohm's-law calculator; a preview of the Python you'll run on the Pi from Lesson 7.

**Next up:** [Lesson 2 — Arduino: meet the board & digital I/O](lesson-02-arduino-digital.md)
