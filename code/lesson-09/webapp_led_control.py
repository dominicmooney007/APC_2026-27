# Lesson 09, Extension 1 — the phone controls an LED too
# LED on GPIO17 as in Lesson 7. Visit /led/on and /led/off from the phone.
from gpiozero import MCP3008, LED
from flask import Flask

sensor = MCP3008(channel=0)
led = LED(17)
app = Flask(__name__)

@app.route("/")
def home():
    value = round(sensor.value, 3)
    led_state = "ON" if led.is_lit else "OFF"
    return f"""
    <html>
      <head><meta http-equiv="refresh" content="2"></head>
      <body style="font-family: sans-serif; text-align: center;">
        <h1>Sensor station</h1>
        <p style="font-size: 4em;">{value}</p>
        <p>LED is {led_state} —
           <a href="/led/on">on</a> | <a href="/led/off">off</a></p>
      </body>
    </html>
    """

@app.route("/led/on")
def led_on():
    led.on()
    return '<meta http-equiv="refresh" content="0; url=/">'

@app.route("/led/off")
def led_off():
    led.off()
    return '<meta http-equiv="refresh" content="0; url=/">'

app.run(host="0.0.0.0", port=5000)
