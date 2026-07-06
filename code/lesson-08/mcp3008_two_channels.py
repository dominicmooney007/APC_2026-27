# Lesson 08, Extension 2 — two analog channels at once
# Pot middle -> CH0 (chip pin 1); second pot middle -> CH1 (chip pin 2)
from gpiozero import MCP3008
from time import sleep

pot = MCP3008(channel=0)
pot2 = MCP3008(channel=1)

while True:
    print(f"pot1: {pot.value:.3f}   pot2: {pot2.value:.3f}")
    sleep(0.2)
