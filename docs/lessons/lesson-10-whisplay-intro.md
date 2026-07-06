# Lesson 10 — Meet the Whisplay HAT

> Mount a HAT that gives your Pi a colour LCD, speaker, mic, button and RGB LED — install its driver, verify every part works, then put your own graphics on the screen from Python.

**Platform:** Whisplay (PiSugar Whisplay HAT on the Raspberry Pi 5)
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 8](lesson-08-pi-buses.md) — I2C/SPI concepts; [Lesson 6](lesson-06-pi-intro.md) — terminal & `git clone`

## The big idea

A **HAT** (Hardware Attached on Top) is a board that plugs onto the Pi's 40-pin header. The Whisplay packs on: a **240×280 colour LCD**, a **speaker + microphone** (WM8960 codec), a **physical button**, and an **RGB LED**. Under the hood it uses the buses from Lesson 8: **SPI** drives the screen, **I2C + I2S** drive the audio. Nothing magic — just everything you've learned, soldered onto one board.

## Learning objectives

- Mount a HAT safely on the 40-pin header.
- Install the Whisplay driver and verify all five subsystems with the built-in hardware test.
- Explain what the driver installed and why (SPI display, I2C/I2S audio overlays).
- Use the `WhisplayBoard` Python class to control the backlight and fill the screen.
- Render text and shapes with **Pillow (PIL)** and push them to the LCD.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~15 min | A | Mount the HAT (power off!) |
| ~25 min | B | Install the driver + reboot + hardware test |
| ~25 min | C | First light: backlight & fill the screen from Python |
| ~40 min | D | **Core build:** your own status screen (PIL → LCD) |
| ~15 min | — | Check-out + extension |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Raspberry Pi 5 + peripherals | 1 | |
| PiSugar Whisplay HAT | 1 | Handle by the edges — ESD rules apply |
| Internet connection on the Pi | — | For cloning the driver repo |

---

## Part A — Mount the HAT (~15 min)

1. **Shut the Pi down properly and unplug power.** (Lesson 6 rule — it matters most right now.)
2. Line the HAT's 40-pin socket up with the Pi's header — all 40 pins, no overhang.
3. Press down evenly on both ends until seated.
4. Have a partner confirm no pins are bent or missed **before** power goes back on.

!!! warning "A crooked HAT can kill both boards"
    Off-by-one-row mounting puts 5 V where the HAT expects ground. Double-check alignment — this is the one hardware step of the semester with real stakes.

---

## Part B — Install the driver & test everything (~25 min)

The screen, codec and LED need driver support. The installer enables the right buses (I2C and I2S are switched on automatically — Lesson 8 explains what those are) and sets up the WM8960 audio driver:

```bash
git clone https://github.com/PiSugar/Whisplay.git --depth 1
cd Whisplay
sudo bash install_driver.sh
sudo reboot
```

After reboot, run the full hardware test:

```bash
cd Whisplay/example
pip install -r requirements.txt --break-system-packages
sudo bash run_test.sh
```

### ✅ Checkpoint B

The test walks through **screen → LED → speaker → button → mic** with on-screen instructions and a final summary. All five say **OK**? You have a verified board. Anything says CHECK — flag it now, not in Lesson 12.

!!! note "Recognise the buses?"
    Run `i2cdetect -y 1` (Lesson 8) — the WM8960 codec now appears on the I2C bus. The LCD is on SPI. The HAT is Lesson 8 made real.

---

## Part C — First light from Python (~25 min)

The driver repo ships a Python class, `WhisplayBoard` (in `runtime/whisplay.py`), that wraps the whole board. Save this **inside the `Whisplay/example` folder** (so Python can find the driver) as `first_light.py`:

```python
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard

board = WhisplayBoard()
board.set_backlight(80)          # 0–100 %

# Colours are 16-bit "RGB565" numbers:
RED, GREEN, BLUE = 0xF800, 0x07E0, 0x001F

for colour in [RED, GREEN, BLUE]:
    board.fill_screen(colour)
    time.sleep(1)

board.fill_screen(0x0000)        # black
board.cleanup()                  # always release the hardware when done
```

```bash
sudo python3 first_light.py
```

!!! note "Why `sudo`, and why RGB565?"
    The driver talks to `/dev/spidev` and GPIO character devices — that needs root. And the LCD speaks **RGB565**: 16 bits per pixel (5 red + 6 green + 5 blue) instead of the usual 24. Part D hides that behind a helper.

### ✅ Checkpoint C

Screen steps red → green → blue → black. You control 67,200 pixels from Python.

---

## Part D — Core build: your own status screen (~40 min)

Drawing pixel-by-pixel is misery. The workflow every real Whisplay program uses (including the games in Lesson 12): **draw with Pillow (PIL) on an image in memory, convert to RGB565 bytes, push the whole frame at once.**

```python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard
from PIL import Image, ImageDraw, ImageFont

board = WhisplayBoard()
board.set_backlight(80)
W, H = board.LCD_WIDTH, board.LCD_HEIGHT          # 240 x 280

def rgb565_bytes(image):
    """Convert a PIL image to the LCD's RGB565 byte format."""
    rgb = image.convert("RGB")
    out = bytearray()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = rgb.getpixel((x, y))
            v = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            out += bytes([(v >> 8) & 0xFF, v & 0xFF])
    return bytes(out)

# --- draw your screen here ---
img = Image.new("RGB", (W, H), (15, 20, 30))
draw = ImageDraw.Draw(img)
font_big = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
font_small = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

draw.rounded_rectangle((10, 10, W - 10, H - 10), radius=16,
                       outline=(80, 160, 255), width=3)
draw.text((25, 40), "YOUR NAME", fill=(255, 255, 255), font=font_big)
draw.text((25, 90), "Adv. Physical Computing", fill=(160, 200, 255), font=font_small)
draw.ellipse((90, 150, 150, 210), fill=(80, 160, 255))
# -----------------------------

board.draw_image(0, 0, W, H, rgb565_bytes(img))
input("Press Enter to exit...")
board.cleanup()
```

Make it yours: name, a shape, different colours — anything, as long as you've changed the drawing code, not just run it.

### ✅ Check your work

**Success looks like:** your design, sharp and stable on the LCD, colours roughly matching what you intended.

!!! warning "`ModuleNotFoundError: whisplay`?"
    Your script isn't next to the `runtime` folder — the `sys.path.append` line assumes you're in `Whisplay/example`. Either move the script there or fix the path.

!!! warning "Colours look wrong / swapped?"
    You've probably hand-built the RGB565 conversion and mixed up the bit-shifts. Use the `rgb565_bytes` helper exactly as given.

!!! warning "Blank screen but no errors?"
    Backlight. `board.set_backlight(80)` before you judge anything else.

---

## Extension / challenge

1. **Live clock** — redraw the screen once a second with the current time (`datetime.now().strftime("%H:%M:%S")`). Notice the redraw flicker? That's why games build the *whole* frame in PIL first and push once.
2. **Play a video** — the driver repo ships `play_mp4.py` (`sudo apt install ffmpeg` first, then follow the README to grab the sample clip). Watch a video play on a chip you wired concepts for in Lesson 8.

## Code

All code in [`code/lesson-10/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-10):

- [`first_light.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-10/first_light.py) — Part C
- [`status_screen.py`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-10/status_screen.py) — Part D core build

Driver and examples © PiSugar, [Apache-2.0](https://github.com/PiSugar/Whisplay/blob/main/LICENSE) — course snippets adapt their patterns with attribution.

**Next up:** [Lesson 11 — Whisplay: buttons, RGB LED & audio](lesson-11-whisplay-io.md)
