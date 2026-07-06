# Lesson 11, Part A — RGB LED colours and fades
# Run from Whisplay/example:  sudo python3 rgb_led.py
import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "runtime"))
from whisplay import WhisplayBoard

board = WhisplayBoard()

board.set_rgb(255, 0, 0)        # red   (r, g, b — each 0-255)
time.sleep(1)
board.set_rgb(0, 255, 0)        # green
time.sleep(1)

# Smooth transition: fade to blue over half a second
board.set_rgb_fade(0, 0, 255, duration_ms=500)
time.sleep(1)

board.set_rgb(0, 0, 0)          # off
board.cleanup()
