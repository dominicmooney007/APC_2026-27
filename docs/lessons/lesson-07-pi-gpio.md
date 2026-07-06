# Lesson 07 — Raspberry Pi: Python, Thonny & GPIO

> Write Python on the Pi itself and control real hardware through the GPIO pins — blink an LED, then make a button drive it with event callbacks.

**Platform:** Raspberry Pi 5
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 6](lesson-06-pi-intro.md) — booting, terminal, proper shutdown; [Lesson 1](lesson-01-foundations.md) — LED + resistor wiring

## Learning objectives

- Run Python in **Thonny** on the Pi (no compile, no upload — just Run).
- Locate pins on the Pi's **40-pin GPIO header** and explain BCM numbering ("GPIO17" ≠ "physical pin 17").
- Blink an LED with `gpiozero`'s `LED` class.
- Read a button with the `Button` class two ways: polling in a loop, and **event callbacks** (`when_pressed`) — using a pull-**down** this time, the mirror image of the Arduino's pull-up.
- Contrast the Pi workflow with the Arduino workflow you already know.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~20 min | A | Thonny tour + first Python on the Pi |
| ~25 min | B | GPIO header + wire and blink an LED |
| ~30 min | C | Button input: polling, then callbacks |
| ~35 min | D | **Core build:** button-toggled LED, the Python way |
| ~10 min | — | Check-out + shutdown |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Pi 5 + screen/keyboard/mouse | 1 | |
| Breadboard + jumper wires | 1 | **Female-to-male** jumpers for the Pi header |
| LED + 330 Ω resistor | 1 | 330 Ω on the Pi (3.3 V pins) |
| Push button | 1 | Same tactile switch as Lesson 2 |

**Software:** Thonny (pre-installed on the Pi) + the `gpiozero` library (pre-installed on Raspberry Pi OS).

!!! warning "The Pi's pins are 3.3 V — and fragile"
    Arduino pins forgive a lot; **Pi pins don't**. Never connect 5 V to a GPIO pin, and always wire with the power off. A blown GPIO pin is forever.

---

## Part A — Thonny & Python on the Pi (~20 min)

Open **menu → Programming → Thonny**. Type in the editor:

```python
print("Hello from the Pi!")

for i in range(5):
    print(i, i * i)
```

Click **Run** (or F5), save as `~/apc/lesson-07/hello.py` when asked. Output appears in the Shell pane below.

Feel the difference from Arduino: no board selection, no port, no compile-and-upload. The code runs **on the same machine you're typing on**. Stop a runaway program with the red **Stop** button.

---

## Part B — The GPIO header + blink (~25 min)

The Pi's 40-pin header carries GPIO pins, 3.3 V, 5 V, and grounds. We name pins by their **GPIO (BCM) number** — the same names `gpiozero` uses. Keep a [pinout diagram](https://pinout.xyz) open; **GPIO17 is physical pin 11**, and physical pins 6, 9, 14, 20, 25, 30, 34, 39 are all ground.

### Wiring

**Shut down and unplug power first.**

| From | To |
|---|---|
| **GPIO17** (physical pin 11) | 330 Ω resistor → LED **anode** (long leg) |
| LED **cathode** | Any **GND** pin (e.g. physical pin 9) |

### The code

```python
from gpiozero import LED
from time import sleep

led = LED(17)          # GPIO17 — the BCM number, not the physical pin

while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
```

Run it. Compare line-for-line with Arduino Blink: `pinMode` → `LED(17)`, `digitalWrite` → `.on()`/`.off()`, `delay(500)` → `sleep(0.5)`, `loop()` → `while True:`.

### ✅ Checkpoint B

Change it to blink SOS (3 short, 3 long, 3 short — then repeat). Hint: write a `def blink(duration):` function so you don't repeat yourself. That's a thing C++ made harder.

---

## Part C — Button input, two ways (~30 min)

### Wiring

**Power off.** Button between **3.3 V** (physical pin 1) and **GPIO2** (physical pin 3). This is the opposite arrangement from the Arduino: there, the pin idled HIGH (pull-up) and pressing pulled it LOW; here we tell `gpiozero` to hold the pin LOW (pull-**down**) and pressing pulls it HIGH. Either works — the code just has to know which.

### Way 1 — polling (the Arduino way)

```python
from gpiozero import LED, Button

led = LED(17)
button = Button(2, pull_up=False)   # pull-down: pressed = HIGH.
                                    # And is_pressed just means pressed — no LOW/HIGH gymnastics!

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
```

### Way 2 — event callbacks (the Python way)

```python
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2, pull_up=False)

button.when_pressed = led.on      # run this WHEN it happens
button.when_released = led.off

pause()    # keep the program alive, waiting for events
```

Same behaviour, no loop: you *declare what should happen*, and `gpiozero` watches the hardware for you. This style scales much better once three sensors and two outputs are in play.

!!! note "Where did debouncing go?"
    `Button(2, pull_up=False, bounce_time=0.05)` — one argument replaces Lesson 2's whole millis-timing dance. Libraries are compressed experience.

---

## Part D — Core build: toggle, the Python way (~35 min)

Lesson 2's toggle extension took careful edge-and-bounce logic in C++. Rebuild it in Python:

```python
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2, pull_up=False, bounce_time=0.05)

def flip():
    led.toggle()                       # gpiozero even gives us toggle()
    state = "ON" if led.is_lit else "OFF"
    print(f"LED is now {state}")       # your serial-monitor habit, Pi style

button.when_pressed = flip
pause()
```

### ✅ Check your work

**Success looks like:** each press flips the LED once — crisply, no double-flips — and the Shell prints the state each time.

!!! warning "`GPIODeviceError: pin already in use`?"
    A previous run still owns the pin. Press Thonny's red **Stop** button, then Run again. (Only one program can hold a GPIO pin at a time.)

!!! warning "Button does nothing?"
    Check you wired **GPIO2 = physical pin 3** (not physical pin 2!), and the other button leg to **3.3 V, never 5 V**. The pinout diagram is not optional; every Pi wiring bug starts here.

---

## Extension / challenge

1. **Hold to dim** — move the LED to **GPIO18** (physical pin 12 — a hardware PWM pin), swap `LED` for `PWMLED`, and make holding the button ramp brightness up and down. (`PWMLED(18).value` takes 0.0–1.0.)
2. **Reaction game, ported** — if you built Lesson 5's reaction timer, rewrite it in Python with `time.time()` and callbacks. Compare line counts.
3. **Two-button dimmer** — one button brightens, one dims, with the level printed on each press.

## Code

All code in [`code/lesson-07/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-07):

- [`blink.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-07/blink.py) — Part B
- [`button_polling.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-07/button_polling.py) / [`button_callbacks.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-07/button_callbacks.py) — Part C
- [`button_toggle.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-07/button_toggle.py) — Part D core build
- [`pwm_dimmer.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-07/pwm_dimmer.py) — Extension 1 starter

**Next up:** [Lesson 8 — Raspberry Pi: analog (ADC), I2C & SPI](lesson-08-pi-buses.md)
