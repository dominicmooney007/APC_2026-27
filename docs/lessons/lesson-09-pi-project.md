# Lesson 09 — Raspberry Pi Mini-Project: Security Station

> Build a motion-sensing security station: log activity over time, plot it, and serve a live status page any phone on the network can open. **Second graded build.**

**Platform:** Raspberry Pi 5
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 7](lesson-07-pi-gpio.md) — gpiozero, LED & button wiring; [Lesson 6](lesson-06-pi-intro.md) — terminal

## The brief

Build a **security monitoring station** in three layers, each one a checkpoint:

1. **DETECT & LOG** — a PIR motion sensor watches the bench; every second, log whether motion is detected (with a real timestamp) to a CSV. Motion also fires the alarm LED + buzzer.
2. **PLOT** — load the CSV and produce an activity graph (a PNG you could put in an incident report).
3. **SERVE** — a tiny Flask web server shows live ARMED / MOTION status to any device on the class network.

This is the Pi doing what the Arduino *can't*: files, real timestamps, and a network.

## Requirements (what gets graded)

| # | Requirement |
|---|---|
| 1 | A CSV log with **timestamp + motion state**, at least 5 minutes long, showing real detections |
| 2 | A labelled activity plot (title, axis labels) generated from that CSV |
| 3 | A Flask page showing **live status**, reachable from another device |
| 4 | Physical alarm response: LED and buzzer react to motion |
| 5 | Code in the repo format + a working demo (plot + phone showing a live detection) |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Pi 5 + breadboard + jumpers | 1 | Female-to-male for the header |
| PIR motion sensor (HC-SR501) | 1 | Needs 5 V — see wiring |
| Breadboard power supply module | 1 | Set to **5 V** for the PIR |
| Active piezo buzzer | 1 | The one-tone kind |
| LED (alarm) + 330 Ω | 1 | GPIO17, as in Lesson 7 |
| LED (status, different colour) + 330 Ω | 1 | GPIO23 |

### Wiring — power off first

The PIR wants **5 V**, which the Pi's GPIO must never touch. Solution (same trick the class used last year): power it from the **breadboard power supply**, and give everything a **common ground**.

| Component | Power | Ground | Signal → Pi |
|---|---|---|---|
| Breadboard PSU (set to 5 V) | → + rail | → − rail | — |
| **Pi physical pin 9 (GND)** | — | → − rail | *(common ground — essential!)* |
| PIR sensor | + rail | − rail | OUT → **GPIO27** (pin 13) |
| Buzzer | — | − rail | + leg → **GPIO22** (pin 15) |
| Alarm LED | — | − rail | via 330 Ω → **GPIO17** (pin 11) |
| Status LED | — | − rail | via 330 Ω → **GPIO23** (pin 16) |

!!! warning "Two rules that protect your Pi"
    **Never connect the Pi's 5 V pins to the breadboard power rail** (two supplies fighting = dead Pi), and **never wire 5 V to a GPIO pin**. The PIR's OUT signal is safe — it swings low/high at logic level.

!!! note "PIR sensors need a warm-up"
    The HC-SR501 takes **30–60 seconds to stabilise** after power-on and may fire false triggers during that window. Power it early, be patient, and don't debug 'ghost motion' in the first minute.

## Today's plan (~120 min)

| Time | Layer | What you're doing |
|---|---|---|
| ~20 min | Wire | All four components + PSU; PIR warm-up while you read ahead |
| ~30 min | 1: Log | Detector logging to CSV, LED+buzzer responding |
| ~25 min | 2: Plot | Activity graph from the growing CSV |
| ~30 min | 3: Serve | Flask status page |
| ~15 min | Demo | Plot + live phone demo + submit |

---

## Layer 1 — Detect & log (~30 min)

`gpiozero` treats the PIR as a `MotionSensor` — callbacks, just like `Button`:

```python
# security_logger.py — motion detection + alarm + CSV log
from gpiozero import MotionSensor, LED, Buzzer
from datetime import datetime
from time import sleep

pir = MotionSensor(27)
alarm_led = LED(17)
status_led = LED(23)
buzzer = Buzzer(22)
FILENAME = "motion_log.csv"

def intruder():
    alarm_led.on()
    buzzer.beep(on_time=0.1, off_time=0.1, n=3)   # three short beeps
    print("MOTION at", datetime.now().strftime("%H:%M:%S"))

def all_clear():
    alarm_led.off()

pir.when_motion = intruder
pir.when_no_motion = all_clear

status_led.on()                    # station is armed
with open(FILENAME, "a") as f:
    if f.tell() == 0:
        f.write("timestamp,motion\n")

while True:                        # one row per second: 1 = motion, 0 = quiet
    now = datetime.now().isoformat(timespec="seconds")
    state = 1 if pir.motion_detected else 0
    with open(FILENAME, "a") as f:
        f.write(f"{now},{state}\n")
    sleep(1)
```

**Start it and leave it running** — it builds your 5-minute dataset while you write Layer 2 in a second Thonny window. Wave at the sensor now and then so the data has *shape*.

### ✅ Checkpoint 1

Motion → LED on + triple beep + `MOTION` in the Shell; `cat motion_log.csv` in a terminal shows rows of 0s with clusters of 1s where you waved.

!!! warning "Constant or random triggering?"
    Warm-up (wait a minute), sensitivity (the two orange dials on the HC-SR501 — try both at ~25%), or a hot air source (sunlight, a heater) in view. Point it somewhere boring.

---

## Layer 2 — Plot the activity (~25 min)

```bash
sudo apt install -y python3-matplotlib
```

```python
# plot_activity.py — activity graph from the motion log
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
```

### ✅ Checkpoint 2

A graph where you can *point at a block of MOTION* and say "that's when you walked past." An incident report, from your own sensor.

---

## Layer 3 — Serve the status (~30 min)

```python
# security_web.py — live security status in the browser
from gpiozero import MotionSensor, LED, Buzzer
from datetime import datetime
from flask import Flask

pir = MotionSensor(27)
alarm_led = LED(17)
buzzer = Buzzer(22)
app = Flask(__name__)
last_motion = {"time": "never"}

def intruder():
    alarm_led.on()
    buzzer.beep(on_time=0.1, off_time=0.1, n=3)
    last_motion["time"] = datetime.now().strftime("%H:%M:%S")

pir.when_motion = intruder
pir.when_no_motion = alarm_led.off

@app.route("/")
def home():
    motion = pir.motion_detected
    colour = "#c62828" if motion else "#2e7d32"
    label = "MOTION DETECTED" if motion else "ALL QUIET"
    return f"""
    <html>
      <head><meta http-equiv="refresh" content="2"></head>
      <body style="font-family: sans-serif; text-align: center;
                   background: {colour}; color: white;">
        <h1>Security station</h1>
        <p style="font-size: 3em;">{label}</p>
        <p>Last motion: {last_motion["time"]}</p>
      </body>
    </html>
    """

app.run(host="0.0.0.0", port=5000)      # 0.0.0.0 = visible to the network
```

Find your Pi's address with `hostname -I`, then on your phone (same Wi-Fi): `http://192.168.1.42:5000`.

!!! warning "Page won't load from the phone?"
    1) Phone on the same network as the Pi? 2) Did you use `host="0.0.0.0"`? 3) Typed `http://` not `https://`? 4) Is the app actually running (Thonny shows `Running on ...`)?

!!! warning "`pin already in use` when starting Flask?"
    Your Layer 1 logger still owns GPIO27. Stop it first — or (better challenge) merge logging *into* the web app.

### ✅ Checkpoint 3

Walk past the sensor while watching your phone: the page flips red with the timestamp. You built a networked security device.

---

## Extension / challenge

1. **Arm/disarm from the phone** — add `/arm` and `/disarm` routes and an `armed` flag; the status LED (GPIO23) shows the armed state, and the alarm only fires when armed. (Now it's genuinely last year's Smart Security System — with a web upgrade its builders didn't have.)
2. **Show the graph on the page** — serve `activity.png` with an `<img>` tag, regenerated periodically.
3. **Servo lockdown** — an SG90 (signal → GPIO18, powered from the 5 V rail) turns 90° to "lock the gate" whenever motion is detected while armed.

## Code

All code in [`code/lesson-09/`](https://github.com/dominicmooney007/APC_2026-27/tree/main/code/lesson-09):

- [`security_logger.py`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-09/security_logger.py) — Layer 1
- [`plot_activity.py`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-09/plot_activity.py) — Layer 2
- [`security_web.py`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-09/security_web.py) — Layer 3
- [`security_web_armable.py`](https://github.com/dominicmooney007/APC_2026-27/blob/main/code/lesson-09/security_web_armable.py) — Extension 1

**Next up:** [Lesson 10 — Meet the Whisplay HAT](lesson-10-whisplay-intro.md)
