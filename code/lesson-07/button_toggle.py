# Lesson 07, Part D (core build) — debounced toggle in 10 lines
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2, pull_up=False, bounce_time=0.05)   # debouncing = one argument

def flip():
    led.toggle()
    state = "ON" if led.is_lit else "OFF"
    print(f"LED is now {state}")

button.when_pressed = flip
pause()
