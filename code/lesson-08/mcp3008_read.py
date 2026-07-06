# Lesson 08, Part B (core build) — read analog via MCP3008 over SPI
# Wiring (see lesson page for the full pin table):
#   MCP3008: VDD+VREF->3.3V, AGND+DGND->GND,
#   CLK->GPIO11, DOUT->GPIO9, DIN->GPIO10, CS->GPIO8
#   Pot: outer legs -> 3.3V and GND, middle -> CH0 (chip pin 1)
from gpiozero import MCP3008
from time import sleep

pot = MCP3008(channel=0)      # CH0, SPI CE0 by default

while True:
    print(f"raw: {pot.value:.3f}   volts: {pot.value * 3.3:.2f}")
    sleep(0.2)
