# Lesson 07, Part B — blink an LED with gpiozero
# Wiring: GPIO17 (physical pin 11) -> 330 ohm -> LED anode; cathode -> GND
from gpiozero import LED
from time import sleep

led = LED(17)          # GPIO17 — BCM number, not the physical pin

while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
