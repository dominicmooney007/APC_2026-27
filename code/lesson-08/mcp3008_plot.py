# Lesson 08, Extension 3 — live plot of an MCP3008 channel
# Install first: sudo apt install python3-matplotlib
from gpiozero import MCP3008
import matplotlib.pyplot as plt

sensor = MCP3008(channel=0)
values = []

plt.ion()                                  # interactive mode: live updates
fig, ax = plt.subplots()

while True:
    values.append(sensor.value)
    values = values[-100:]                 # keep the last 100 readings
    ax.clear()
    ax.plot(values)
    ax.set_ylim(0, 1)
    ax.set_title("Live sensor (last 100 readings)")
    plt.pause(0.1)
