# Lesson 11, Part D (core build) — press-to-talk voice memo
# Hold button = record (red LED); release = play back (green LED).
# Run from Whisplay/example:  sudo python3 voice_memo.py
# Find your wm8960 card number with:  aplay -l   (then fix CARD below)
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
