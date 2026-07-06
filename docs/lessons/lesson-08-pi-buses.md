# Lesson 08 — Raspberry Pi: Analog (ADC), I2C & SPI

> The Pi can't read analog signals — so we give it that superpower with an ADC chip over SPI, and meet the two bus protocols that most add-on hardware (including the Whisplay HAT) speaks.

**Platform:** Raspberry Pi 5
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 7](lesson-07-pi-gpio.md) — gpiozero, GPIO wiring; [Lesson 3](lesson-03-arduino-analog.md) — what analog input means

!!! tip "Pacing: one bus device is the win"
    This is the densest Pi session. The **core task is one working analog read via the MCP3008**. The I2C section is a demo/extension — done is better than both-half-done.

## The big idea

The Arduino had `analogRead` built in; the Pi 5 has **no analog input at all**. The fix — and the deeper lesson — is that computers talk to helper chips over shared **buses**:

| Bus | Wires | Feel | Today |
|---|---|---|---|
| **SPI** | 4 (+ select per device) | Fast, simple | MCP3008 ADC chip → analog restored |
| **I2C** | 2 (SDA + SCL) | Slower, but many devices on two wires | Scan the bus, read a sensor (demo) |

The Whisplay HAT you'll mount in Lesson 10 uses **both** (plus I2S for audio) — today explains what those letters mean.

## Learning objectives

- Explain why the Pi lacks analog input and what an ADC does.
- Enable SPI and I2C with `raspi-config`.
- Wire an MCP3008 and read a potentiometer with `gpiozero.MCP3008`.
- Scan the I2C bus with `i2cdetect` and explain device addresses.

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Pi 5 + breadboard + jumpers | 1 | Female-to-male for the header |
| MCP3008 ADC chip | 1 | 16-pin DIP — straddles the trench |
| Potentiometer (10 kΩ) | 1 | Same knob as the Arduino track |
| *(Demo)* Any I2C device | 1 | e.g. temperature/pressure sensor breakout |

---

## Part A — Enable the buses (~15 min)

```bash
sudo raspi-config
# Interface Options -> SPI -> enable
# Interface Options -> I2C -> enable
# Finish (reboot if prompted)
```

Verify:

```bash
ls /dev/spidev*   # should list spidev0.0, spidev0.1
ls /dev/i2c*      # should list /dev/i2c-1
```

---

## Part B — Core build: MCP3008 analog input (~55 min)

The MCP3008 is a **10-bit, 8-channel ADC**: eight analog inputs, values 0–1023 (the same resolution the Arduino had), reported to the Pi over SPI.

### Wiring — power off first

Chip straddling the trench, **notch/dimple to the left**; pins number 1–8 across the bottom (left→right), 9–16 across the top (right→left):

| MCP3008 pin | Name | To (Pi physical pin) |
|---|---|---|
| 16 | VDD | 3.3 V (pin 1) |
| 15 | VREF | 3.3 V (pin 1) |
| 14 | AGND | GND (pin 6) |
| 13 | CLK | GPIO11 / SCLK (pin 23) |
| 12 | DOUT | GPIO9 / MISO (pin 21) |
| 11 | DIN | GPIO10 / MOSI (pin 19) |
| 10 | CS | GPIO8 / CE0 (pin 24) |
| 9 | DGND | GND (pin 6) |
| 1 | CH0 | Potentiometer middle leg |

Pot outer legs → 3.3 V and GND (**3.3 V, not 5 V** — VREF is 3.3 V and the Pi is not 5 V-tolerant).

### The code

`gpiozero` already knows this chip:

```python
from gpiozero import MCP3008
from time import sleep

pot = MCP3008(channel=0)      # CH0, on SPI CE0 by default

while True:
    print(f"raw: {pot.value:.3f}   volts: {pot.value * 3.3:.2f}")
    sleep(0.2)
```

!!! note "0.0–1.0, not 0–1023"
    `gpiozero` normalizes ADC readings to a float 0.0–1.0. Multiply by 3.3 for volts, or by 1023 if you miss the Arduino numbers.

### ✅ Check your work

**Success looks like:** turn the pot end-to-end and the value sweeps ~0.00 → ~1.00 smoothly.

!!! warning "All zeros? All noise?"
    All **0.000**: SPI not enabled, CS on the wrong pin, or the chip is rotated 180° (check the notch!). Random jitter with nothing connected to CH0 is normal — a floating input reads garbage, same as the Arduino did.

Sanity experiment before moving on: move the CH0 wire to 3.3 V directly (should read ~1.000), then to GND (~0.000). Now you *know* what the rails look like through the ADC — useful calibration instinct for any analog sensor you meet later.

---

## Part C — I2C: the two-wire bus (demo / extension) (~25 min)

I2C carries many devices on two wires (SDA = data, SCL = clock, physical pins 3 & 5), each with its own **address**. With any I2C device wired (VCC→3.3 V, GND→GND, SDA→pin 3, SCL→pin 5):

```bash
sudo apt install -y i2c-tools
i2cdetect -y 1
```

You get a grid with a number like `76` — that device's address on the bus. Every I2C library asks for it. In Lesson 10, the Whisplay's audio codec appears on this same bus — run `i2cdetect` again then and you'll recognize it.

---

## Extension / challenge

1. **Analog dimmer, Pi edition** — combine today's pot reading with Lesson 7's `PWMLED` on GPIO18: `led.value = pot.value`. One line connects the two halves of everything you've learned this week.
2. **Two channels at once** — a second pot (borrow one) on CH1, print both. Eight channels is the MCP3008's whole point.
3. **Plot it** — Thonny's Shell scrolls; matplotlib doesn't. `sudo apt install python3-matplotlib`, then adapt [`mcp3008_plot.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-08/mcp3008_plot.py) — a live-updating graph, and a preview of Lesson 9.

## Code

All code in [`code/lesson-08/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-08):

- [`mcp3008_read.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-08/mcp3008_read.py) — Part B core build
- [`mcp3008_two_channels.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-08/mcp3008_two_channels.py) — Extension 2
- [`mcp3008_plot.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-08/mcp3008_plot.py) — Extension 3

**Next up:** [Lesson 9 — Raspberry Pi mini-project](lesson-09-pi-project.md)
