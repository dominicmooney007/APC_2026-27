# Lesson 07, Extension 1 (starter) — hold the button to ramp brightness
# LED moved to GPIO18 (physical pin 12) — a hardware PWM pin
from gpiozero import PWMLED, Button
from time import sleep

led = PWMLED(18)        # PWM on any pin — .value takes 0.0 to 1.0
button = Button(2, pull_up=False)

level = 0.0
direction = +1

while True:
    if button.is_pressed:
        level += 0.02 * direction
        if level >= 1.0 or level <= 0.0:
            direction *= -1                 # bounce at the ends
            level = max(0.0, min(1.0, level))
        led.value = level
    sleep(0.02)
    # Your turn: print the level when it changes (not every loop!)
