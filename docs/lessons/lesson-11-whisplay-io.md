# Lesson 11 — Whisplay: Buttons, RGB LED & Audio

> Wire up the rest of the HAT from Python: button events, LED colours, and sound in and out through the onboard codec — everything Lesson 12's game needs.

**Platform:** Whisplay
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 10](lesson-10-whisplay-intro.md) — driver installed, hardware test passed, PIL → LCD workflow

## Learning objectives

- Drive the RGB LED with `set_rgb()` and smooth transitions with `set_rgb_fade()`.
- Handle the physical button with **event callbacks** (`on_button_press` / `on_button_release`) — the same pattern as gpiozero in Lesson 7.
- Play sound through the speaker and record from the mic using the WM8960 codec (`aplay` / `arecord`).
- Combine screen + LED + button + sound into one responsive program.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~20 min | A | RGB LED: colours and fades |
| ~25 min | B | Button events + LED + screen feedback |
| ~30 min | C | Audio out & audio in (speaker + mic) |
| ~35 min | D | **Core build:** press-to-talk voice memo |
| ~10 min | — | Check-out |

## What you'll need

Same rig as Lesson 10: Pi 5 + Whisplay HAT, driver installed. All scripts run from `Whisplay/example` with `sudo python3`.

---

## Part A — The RGB LED (~20 min)

```python
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard

board = WhisplayBoard()

board.set_rgb(255, 0, 0)        # red   (r, g, b — each 0–255)
time.sleep(1)
board.set_rgb(0, 255, 0)        # green
time.sleep(1)

# Smooth transition: fade to blue over half a second
board.set_rgb_fade(0, 0, 255, duration_ms=500)
time.sleep(1)

board.set_rgb(0, 0, 0)          # off
board.cleanup()
```

Familiar? It's Lesson 3's PWM colour mixing — the driver is doing `analogWrite` three times, in software, so you don't have to.

### ✅ Checkpoint A

Write a loop that fades through at least 4 colours of your choosing, smoothly, forever (until Ctrl-C).

---

## Part B — Button events (~25 min)

The Whisplay button uses the callback pattern you know from `gpiozero`:

```python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard
from signal import pause

board = WhisplayBoard()
board.set_backlight(80)

def pressed():
    board.set_rgb(0, 255, 0)
    print("DOWN")

def released():
    board.set_rgb(0, 0, 0)
    print("UP")

board.on_button_press(pressed)      # compare: button.when_pressed = ...
board.on_button_release(released)

pause()
```

### ✅ Checkpoint B

Extend it: each press cycles the LED **and** redraws the screen (Lesson 10's PIL workflow) to show a count of presses. Keep your `rgb565_bytes` helper handy — you'll reuse it every lesson now.

---

## Part C — Audio: out, then in (~30 min)

Audio doesn't need Python at all — Linux treats the WM8960 as a normal sound card. Find it, then use the standard ALSA tools:

```bash
aplay -l                 # list playback devices; find the card number of "wm8960"
```

**Play** (use your card number in place of `1`):

```bash
aplay -D plughw:1,0 /usr/share/sounds/alsa/Front_Center.wav
```

**Record 5 seconds, then play it back:**

```bash
arecord -D plughw:1,0 -f S16_LE -r 48000 -c 2 -d 5 memo.wav
aplay -D plughw:1,0 memo.wav
```

From Python, run the same commands with `subprocess`:

```python
import subprocess

CARD = "plughw:1,0"     # your wm8960 card number

def play(path):
    subprocess.run(["aplay", "-D", CARD, path])

def record(path, seconds):
    subprocess.run(["arecord", "-D", CARD, "-f", "S16_LE",
                    "-r", "48000", "-c", "2", "-d", str(seconds), path])
```

!!! warning "Silence?"
    1) Wrong card number — recheck `aplay -l`. 2) Volume — run `alsamixer`, select the wm8960 card with F6, and raise Speaker/Playback. 3) The hardware test in Lesson 10 passed audio, so the wiring is known-good — the problem is settings, not solder.

---

## Part D — Core build: press-to-talk voice memo (~35 min)

Combine all four subsystems: **hold the button to record (LED red), release to play it back (LED green), screen shows state.**

```python
import sys, os, subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard
from PIL import Image, ImageDraw, ImageFont
from signal import pause

board = WhisplayBoard()
board.set_backlight(80)
W, H = board.LCD_WIDTH, board.LCD_HEIGHT
CARD = "plughw:1,0"                     # <-- your wm8960 card
MEMO = "/tmp/memo.wav"
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

def rgb565_bytes(image):
    rgb = image.convert("RGB")
    out = bytearray()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = rgb.getpixel((x, y))
            v = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            out += bytes([(v >> 8) & 0xFF, v & 0xFF])
    return bytes(out)

def show(text, bg):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    d.text((30, 120), text, fill=(255, 255, 255), font=font)
    board.draw_image(0, 0, W, H, rgb565_bytes(img))

rec_proc = None

def start_recording():
    global rec_proc
    board.set_rgb(255, 0, 0)
    show("RECORDING", (120, 20, 20))
    rec_proc = subprocess.Popen(
        ["arecord", "-D", CARD, "-f", "S16_LE",
         "-r", "48000", "-c", "2", "-d", "30", MEMO])

def stop_and_play():
    global rec_proc
    if rec_proc:
        rec_proc.terminate()
        rec_proc.wait()
    board.set_rgb(0, 255, 0)
    show("PLAYING", (20, 100, 40))
    subprocess.run(["aplay", "-D", CARD, MEMO])
    board.set_rgb(0, 0, 0)
    show("READY", (15, 20, 30))

board.on_button_press(start_recording)
board.on_button_release(stop_and_play)

show("READY", (15, 20, 30))
print("Hold the button to record; release to play back. Ctrl-C to quit.")
pause()
```

### ✅ Check your work

**Success looks like:** hold → screen says RECORDING with red LED → speak → release → your voice plays back with green LED → back to READY. That's a complete interactive device: input, processing, three kinds of output.

!!! warning "Playback is silent but recording 'worked'?"
    Check `alsamixer` capture levels (F4 switches to capture view), and make sure you actually spoke *at the mic side of the board*.

---

## Extension / challenge

1. **Sound-effects board** — 3 short WAVs; each press cycles which one plays; screen shows the current sound's name.
2. **Level meter** — after recording, use Python's `wave` module to read the file and draw a simple loudness bar on the LCD.

## Code

All code in [`code/lesson-11/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-11):

- [`rgb_led.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-11/rgb_led.py) — Part A
- [`button_events.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-11/button_events.py) — Part B
- [`voice_memo.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-11/voice_memo.py) — Part D core build

Driver © PiSugar, [Apache-2.0](https://github.com/PiSugar/Whisplay/blob/main/LICENSE).

**Next up:** [Lesson 12 — Whisplay mini-project: single-button game](lesson-12-whisplay-game.md)
