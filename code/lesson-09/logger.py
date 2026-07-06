# Lesson 09, Layer 1 — append timestamped sensor readings to a CSV
from gpiozero import MCP3008
from datetime import datetime
from time import sleep

sensor = MCP3008(channel=0)
FILENAME = "readings.csv"

with open(FILENAME, "a") as f:
    if f.tell() == 0:                        # brand-new file? write a header
        f.write("timestamp,value\n")

while True:
    now = datetime.now().isoformat(timespec="seconds")
    value = round(sensor.value, 4)
    with open(FILENAME, "a") as f:
        f.write(f"{now},{value}\n")
    print(now, value)
    sleep(1)
