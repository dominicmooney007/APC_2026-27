# Lesson 09, Layer 3 — live security status in the browser
# On the phone (same Wi-Fi): http://<pi-address>:5000  (hostname -I)
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
