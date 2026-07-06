# Lesson 09, Layer 3 — live sensor value in the browser
# On the phone (same Wi-Fi): http://<pi-address>:5000  (hostname -I)
from gpiozero import MCP3008
from flask import Flask

sensor = MCP3008(channel=0)
app = Flask(__name__)

@app.route("/")
def home():
    value = round(sensor.value, 3)
    return f"""
    <html>
      <head><meta http-equiv="refresh" content="2"></head>
      <body style="font-family: sans-serif; text-align: center;">
        <h1>Sensor station</h1>
        <p style="font-size: 4em;">{value}</p>
        <p>refreshes every 2 s</p>
      </body>
    </html>
    """

app.run(host="0.0.0.0", port=5000)      # 0.0.0.0 = visible to the network
