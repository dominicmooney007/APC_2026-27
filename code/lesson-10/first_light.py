# Lesson 10, Part C — first light: backlight + fill the screen
# Run from Whisplay/example:  sudo python3 first_light.py
# Uses the PiSugar Whisplay driver (Apache-2.0): github.com/PiSugar/Whisplay
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard

board = WhisplayBoard()
board.set_backlight(80)          # 0-100 %

# Colours are 16-bit "RGB565" numbers:
RED, GREEN, BLUE = 0xF800, 0x07E0, 0x001F

for colour in [RED, GREEN, BLUE]:
    board.fill_screen(colour)
    time.sleep(1)

board.fill_screen(0x0000)        # black
board.cleanup()                  # always release the hardware when done
