# Lesson 09, Extension 1 — arm/disarm the station from the phone
# Status LED (GPIO23) = armed indicator; alarm only fires when armed.
from gpiozero import MotionSensor, LED, Buzzer
from datetime import datetime
from flask import Flask

pir = MotionSensor(27)
alarm_led = LED(17)
status_led = LED(23)
buzzer = Buzzer(22)
app = Flask(__name__)
state = {"armed": True, "last_motion": "never"}

def intruder():
    state["last_motion"] = datetime.now().strftime("%H:%M:%S")
    if state["armed"]:
        alarm_led.on()
        buzzer.beep(on_time=0.1, off_time=0.1, n=3)

pir.when_motion = intruder
pir.when_no_motion = alarm_led.off
status_led.on()

@app.route("/")
def home():
    motion = pir.motion_detected and state["armed"]
    colour = "#c62828" if motion else ("#2e7d32" if state["armed"] else "#555")
    label = "MOTION DETECTED" if motion else ("ARMED" if state["armed"] else "DISARMED")
    return f"""
    <html>
      <head><meta http-equiv="refresh" content="2"></head>
      <body style="font-family: sans-serif; text-align: center;
                   background: {colour}; color: white;">
        <h1>Security station</h1>
        <p style="font-size: 3em;">{label}</p>
        <p>Last motion: {state["last_motion"]}</p>
        <p><a style="color:white" href="/arm">ARM</a> |
           <a style="color:white" href="/disarm">DISARM</a></p>
      </body>
    </html>
    """

@app.route("/arm")
def arm():
    state["armed"] = True
    status_led.on()
    return '<meta http-equiv="refresh" content="0; url=/">'

@app.route("/disarm")
def disarm():
    state["armed"] = False
    status_led.off()
    alarm_led.off()
    return '<meta http-equiv="refresh" content="0; url=/">'

app.run(host="0.0.0.0", port=5000)
