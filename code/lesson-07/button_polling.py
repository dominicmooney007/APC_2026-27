# Lesson 07, Part C (way 1) — button by polling, the Arduino way
# Wiring: LED as blink.py; button between 3.3V (pin 1) and GPIO2 (pin 3)
from gpiozero import LED, Button

led = LED(17)
button = Button(2, pull_up=False)     # internal pull-down: pressed = HIGH

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
