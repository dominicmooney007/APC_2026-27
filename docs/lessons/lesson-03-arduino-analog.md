# Lesson 03 — Arduino: Analog Input, PWM & Serial

> Read a knob and a light sensor as numbers, fade an LED with PWM, and watch your data live in the Serial Monitor and Plotter.

**Platform:** Arduino
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 2](lesson-02-arduino-digital.md) — uploading sketches, digital I/O, breadboard LED circuit

## Learning objectives

- Read a voltage with `analogRead` and explain the 0–1023 range.
- Use `Serial.begin` / `Serial.println` and the Serial Monitor to see live values — your #1 debugging tool from now on.
- Use the Serial **Plotter** to graph a sensor in real time.
- Output "in-between" levels with `analogWrite` (PWM) and explain why it only works on `~` pins.
- Use `map()` to connect an input range to an output range — the pattern behind almost every device this semester.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~25 min | A | Potentiometer + `analogRead` + Serial Monitor |
| ~20 min | B | Serial Plotter: see your data as a graph |
| ~25 min | C | PWM: fade an LED with `analogWrite` |
| ~35 min | D | **Core build:** knob-controlled LED brightness (`map()`) |
| ~15 min | — | Check-out + extensions |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Arduino + USB cable | 1 | |
| Breadboard + jumper wires | 1 | |
| Potentiometer (10 kΩ) | 1 | The knob |
| Passive buzzer | 1 | For the extension — plays tones |
| LED + 220 Ω resistor | 1 | From Lesson 2 |

**Software:** Arduino IDE.

---

## Part A — Analog input: the potentiometer (~25 min)

Digital pins know two states. **Analog pins (A0–A5) measure a voltage** and report it as a number from **0 (0 V) to 1023 (5 V)**.

### Wiring

**Unplug USB first.** The potentiometer has three legs:

| Pot leg | To |
|---|---|
| Left | Arduino **5V** |
| Middle (wiper) | Arduino **A0** |
| Right | Arduino **GND** |

### The sketch

```cpp
const int POT_PIN = A0;

void setup() {
  Serial.begin(9600);         // open the serial connection to the Mac
}

void loop() {
  int value = analogRead(POT_PIN);   // 0–1023
  Serial.println(value);             // send it to the Serial Monitor
  delay(100);
}
```

Upload, then open **Tools → Serial Monitor** and set the speed to **9600 baud** (bottom-right). Turn the knob and watch the numbers.

### ✅ Checkpoint A

Find the knob positions that give you roughly **0**, **512**, and **1023**. What voltage does 512 correspond to?

!!! tip "Serial is your multimeter"
    From today on, when a circuit misbehaves, your first move is `Serial.println` the value you *think* you have. Guessing is slower than looking.

---

## Part B — The Serial Plotter (~20 min)

Close the Serial Monitor and open **Tools → Serial Plotter** — same data, live graph. Turn the knob and watch the wave. This graph view becomes essential in Lesson 4, when readings come from a sensor you *can't* turn by hand.

### ✅ Checkpoint B

Make three distinct "signals" on the plot: a slow sine-like wave, a square-ish wave (snap the knob end to end), and a flat line at roughly half. Screenshot the best one — first entry for your project journal.

---

## Part C — Analog output: PWM (~25 min)

`digitalWrite` gives you ON or OFF. **PWM** (pulse-width modulation) fakes in-between levels by switching ON/OFF very fast — the fraction of time spent ON sets the brightness. `analogWrite(pin, 0–255)` does this on the pins marked **`~`** (3, 5, 6, 9, 10, 11).

Rewire your LED (with its 220 Ω resistor) to **pin 9**, then:

```cpp
const int LED_PIN = 9;   // must be a ~ PWM pin

void setup() {
  // no pinMode needed for analogWrite, but it doesn't hurt
}

void loop() {
  for (int level = 0; level <= 255; level++) {   // fade up
    analogWrite(LED_PIN, level);
    delay(5);
  }
  for (int level = 255; level >= 0; level--) {   // fade down
    analogWrite(LED_PIN, level);
    delay(5);
  }
}
```

!!! note "Two different scales — deliberately"
    `analogRead` gives **0–1023**; `analogWrite` takes **0–255**. They're different hardware (10-bit ADC in, 8-bit PWM out). Connecting them is Part D's job.

---

## Part D — Core build: knob controls brightness (~35 min)

Wire **both** circuits at once: pot on A0 (Part A) and LED on pin 9 (Part C). Now connect input to output with `map()`:

```cpp
const int POT_PIN = A0;
const int LED_PIN = 9;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(POT_PIN);              // 0–1023
  int brightness = map(raw, 0, 1023, 0, 255); // rescale to 0–255

  analogWrite(LED_PIN, brightness);

  Serial.print(raw);
  Serial.print(" -> ");
  Serial.println(brightness);
  delay(50);
}
```

### ✅ Check your work

**Success looks like:** the LED smoothly follows the knob — fully off at one end, fully bright at the other — and the Serial Monitor shows both numbers moving together.

!!! warning "LED only ever on or off?"
    You're probably on a non-`~` pin — `analogWrite` on those acts like digital. Move the LED to 3, 5, 6, 9, 10, or 11.

!!! warning "Values jumpy or stuck?"
    Stuck at 0 or 1023: the wiper (middle leg) isn't in A0, or one outer leg is loose. Jittery by ±2–3: that's normal ADC noise — real sensors wiggle.

---

## Extension / challenge

1. **Reverse it** — knob up = LED *dimmer*. One argument change. Which one?
2. **Theremin** — wire the passive buzzer (+ leg → pin 8, − leg → GND) and turn knob position into pitch: `tone(8, map(raw, 0, 1023, 200, 2000));`. Congratulations, you've built an instrument. Starter in [`pot_theremin.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-03/pot_theremin/pot_theremin.ino).
3. **Fade patterns** — combine Part C and Part D: the knob sets the *speed* of the auto-fade instead of the brightness directly. Trickier than it sounds.

## Code

All sketches in [`code/lesson-03/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-03):

- [`pot_read/pot_read.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-03/pot_read/pot_read.ino) — Parts A & B
- [`led_fade/led_fade.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-03/led_fade/led_fade.ino) — Part C
- [`pot_brightness/pot_brightness.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-03/pot_brightness/pot_brightness.ino) — Part D core build
- [`pot_theremin/pot_theremin.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-03/pot_theremin/pot_theremin.ino) — Extension 2

**Next up:** [Lesson 4 — Arduino: sensors & actuators](lesson-04-arduino-sensors.md)
