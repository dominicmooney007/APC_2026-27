# Lesson 09, Layer 2 — graph the CSV log
# Install first: sudo apt install python3-matplotlib
import csv
from datetime import datetime
import matplotlib.pyplot as plt

times, values = [], []
with open("readings.csv") as f:
    for row in csv.DictReader(f):
        times.append(datetime.fromisoformat(row["timestamp"]))
        values.append(float(row["value"]))

plt.figure(figsize=(10, 4))
plt.plot(times, values)
plt.title("Light level over time")        # match YOUR sensor
plt.xlabel("Time")
plt.ylabel("Sensor value (0-1)")
plt.tight_layout()
plt.savefig("plot.png")
plt.show()
