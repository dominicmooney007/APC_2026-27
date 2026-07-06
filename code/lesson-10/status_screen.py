# Lesson 10, Part D (core build) — draw with PIL, push to the LCD
# Run from Whisplay/example:  sudo python3 status_screen.py
# Uses the PiSugar Whisplay driver (Apache-2.0): github.com/PiSugar/Whisplay
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
