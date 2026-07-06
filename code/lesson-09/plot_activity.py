# Lesson 09, Layer 2 — activity graph from the motion log
# Install first: sudo apt install python3-matplotlib
import csv
from datetime import datetime
import matplotlib.pyplot as plt

times, states = [], []
with open("motion_log.csv") as f:
    for row in csv.DictReader(f):
        times.append(datetime.fromisoformat(row["timestamp"]))
        states.append(int(row["motion"]))

plt.figure(figsize=(10, 3))
plt.fill_between(times, states, step="post", alpha=0.6)
plt.title("Motion activity — bench station")
plt.xlabel("Time")
plt.yticks([0, 1], ["quiet", "MOTION"])
plt.tight_layout()
plt.savefig("activity.png")
plt.show()
