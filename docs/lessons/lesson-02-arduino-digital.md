# Lesson 02 — Arduino: Meet the Board & Digital I/O

> Upload your first sketch to an Arduino, learn how a C++ sketch is structured, and make a button control an LED.

**Platform:** Arduino (Uno or class board), programmed from a Mac over USB
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 1](lesson-01-foundations.md) — breadboard wiring, LED + resistor, "power off before wiring"

## Learning objectives

- Identify the key parts of the Arduino board: USB port, power, digital pins, GND, the onboard LED.
- Select the correct **board** and **port** in the Arduino IDE and upload a sketch.
- Explain the two-part structure of every sketch: `setup()` runs once, `loop()` runs forever.
- Use `pinMode`, `digitalWrite`, and `delay()` to control an output.
- Use `digitalRead` with `INPUT_PULLUP` to read a button, and use it to control an LED.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~15 min | A | Meet the board + IDE tour, board & port selection |
| ~25 min | B | Upload Blink; dissect `setup()` / `loop()` |
| ~25 min | C | Your own LED on a breadboard pin |
| ~40 min | D | **Core build:** button controls the LED |
| ~15 min | — | Check-out + extensions for fast finishers |

!!! note "The IDE is already installed"
    Your Mac already has the Arduino IDE set up — don't reinstall it. If it's missing, tell your teacher rather than downloading it yourself.

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Arduino board + USB cable | 1 | |
| Breadboard | 1 | From Lesson 1 |
| LED (any colour) | 1 | Long leg = anode (+) |
| Resistor, 220 Ω | 1 | For the LED |
| Push button (tactile switch) | 1 | 4-leg breadboard type |
| Jumper wires | 4–6 | Male–male |

**Software:** Arduino IDE (on the Mac).

---

## Part A — Meet the board & the IDE (~15 min)

Find these on your board before plugging anything in:

- **USB port** — power *and* programming come through here today.
- **Digital pins 0–13** — each can be an input or an output. (Avoid 0 and 1 for now — they're shared with USB communication.)
- **GND pins** — same job as the − rail in Lesson 1.
- **Onboard LED** — marked `L`, wired internally to **pin 13**. It's how we'll test without wiring anything.

Now plug the board in and open the IDE:

1. **Tools → Board** → select your board (e.g. *Arduino Uno*).
2. **Tools → Port** → select the port that mentions `usbmodem` or `usbserial`.

!!! warning "No port showing?"
    Try a different USB cable first — many are charge-only and can't carry data. Then try another USB port on the Mac. Still nothing? Ask.

---

## Part B — Blink: your first upload (~25 min)

Every Arduino program (a **sketch**) has the same skeleton:

```cpp
void setup() {
  // runs ONCE, when the board powers on or resets
}

void loop() {
  // runs FOREVER, top to bottom, over and over
}
```

That's the biggest difference from Python so far: you don't run the program — you **upload** it, and the board runs it on a loop until you upload something else.

Upload this — it blinks the onboard LED (pin 13):

```cpp
const int LED_PIN = 13;  // onboard LED

void setup() {
  pinMode(LED_PIN, OUTPUT);   // declare the pin as an output
}

void loop() {
  digitalWrite(LED_PIN, HIGH);  // LED on
  delay(500);                   // wait 500 ms
  digitalWrite(LED_PIN, LOW);   // LED off
  delay(500);
}
```

Click **Upload** (the → arrow). The board's TX/RX lights flicker during upload, then the `L` LED starts blinking.

### ✅ Checkpoint B

Change both `500`s to make it blink **twice as fast**, and upload again. If the blink speed changed, you own the upload workflow.

!!! tip "Compile vs. run"
    Upload = compile the C++ → flash it onto the board. Errors appear in the black console at the bottom *before* anything reaches the board. Read the **first** error line — the rest is usually noise.

---

## Part C — Your own LED on a breadboard (~25 min)

Now drive an external LED — same circuit as Lesson 1, but the Arduino pin replaces the power supply.

### Wiring

**Power off first: unplug the USB cable before wiring.**

| From | To |
|---|---|
| Arduino **pin 8** | 220 Ω resistor → breadboard row |
| Resistor's other end | LED **long leg (anode)** |
| LED **short leg (cathode)** | Arduino **GND** |

Change one line in your Blink sketch:

```cpp
const int LED_PIN = 8;  // was 13 — now your breadboard LED
```

Re-plug USB, upload, and your LED on the breadboard blinks.

!!! warning "LED not blinking?"
    Same checklist as Lesson 1: LED backwards, wrong row, or missing GND connection. Plus one new one: does the pin number in the sketch match the pin you actually wired?

---

## Part D — Core build: button controls the LED (~40 min)

### The wiring trick: `INPUT_PULLUP`

A button just connects two points when pressed. To read it reliably the pin needs a defined voltage when the button *isn't* pressed — otherwise it floats and reads randomly. The Arduino has built-in **pull-up resistors** we can switch on from code, which means:

- **Pressed** reads `LOW` — and **not pressed** reads `HIGH`. Backwards from what you'd guess. Remember it.

### Wiring

**Unplug USB first.** Keep the LED circuit from Part C.

| From | To |
|---|---|
| Button leg (one side) | Arduino **pin 2** |
| Button leg (other side) | Arduino **GND** |

!!! tip "Button legs come in pairs"
    The 4-leg buttons connect in pairs along the *sides*. If your button seems always-pressed or never-pressed, rotate it 90°.

### The sketch

```cpp
const int LED_PIN = 8;
const int BUTTON_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // built-in pull-up: no resistor needed
}

void loop() {
  int state = digitalRead(BUTTON_PIN);

  if (state == LOW) {          // LOW = pressed (pull-up logic!)
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

### ✅ Check your work

**Success looks like:** LED off normally; LED on **while** the button is held; off again on release. Instant response, no flicker.

!!! warning "LED logic reversed?"
    If the LED is on until you press: your `if` is checking `HIGH` instead of `LOW`. With a pull-up, **pressed = LOW**.

!!! warning "Nothing happens at all?"
    Check the button is straddling correctly (rotate it 90°), and that one leg really goes to GND. Then re-read the pin numbers in the sketch vs. your wiring.

---

## Extension / challenge

Finished the core build? In order:

1. **Toggle instead of hold** — one press turns the LED on, the next press turns it off. (You'll need a variable that *remembers* the LED state, and to act only when the button *changes* from up to down.) You'll likely discover the LED sometimes flips twice per press — that's **switch bounce**, and it's the next challenge.
2. **Debounce it** — ignore changes that happen within ~50 ms of the last one. Compare your approach with [`button_toggle_debounced.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/button_toggle_debounced/button_toggle_debounced.ino) after you've tried.
3. **LED pattern** — wire 2–3 more LEDs (each with its own 220 Ω resistor, pins 9–11) and make a chase/Knight-Rider pattern. Starter in [`led_pattern.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/led_pattern/led_pattern.ino).

## Code

All sketches for this lesson live in [`code/lesson-02/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-02):

- [`blink/blink.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/blink/blink.ino) — Parts B & C
- [`button_led/button_led.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/button_led/button_led.ino) — Part D core build
- [`button_toggle_debounced/button_toggle_debounced.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/button_toggle_debounced/button_toggle_debounced.ino) — Extensions 1–2
- [`led_pattern/led_pattern.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-02/led_pattern/led_pattern.ino) — Extension 3

**Next up:** [Lesson 3 — Arduino: analog input, PWM & serial](lesson-03-arduino-analog.md)
