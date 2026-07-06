# Lesson 11, Part B — button events (same pattern as gpiozero callbacks)
# Run from Whisplay/example:  sudo python3 button_events.py
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
