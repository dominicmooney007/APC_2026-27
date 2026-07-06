# Lesson 07, Part C (way 2) — button by event callbacks, the Python way
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2, pull_up=False)

button.when_pressed = led.on      # run this WHEN it happens
button.when_released = led.off

pause()    # keep the program alive, waiting for events
