# Course code, by lesson

Each `lesson-NN/` folder holds the code for that lesson — the lesson pages on the course site link directly to these files.

## Spare / extension material

A few files aren't referenced by any lesson page. They're kept as **extra material** for students who want more, or as alternatives if your kit has the parts:

| File | What it is | Needs |
|---|---|---|
| `lesson-03/rgb_mixer/` | Colour mixing with three PWM channels | RGB LED (or 3 LEDs) |
| `lesson-04/tmp36_read/` | Analog temperature (raw → volts → °C) | TMP36 sensor |
| `lesson-04/distance_dial/` | Ultrasonic distance drives a servo dial | HC-SR04 + servo |
| `lesson-04/l298n_motor/` | Motor demo with direction reversing | L298N + DC motor |
| `lesson-05/parking_sensor_starter/` | Alternative Lesson 5 starter (no LCD) | HC-SR04 + LED |
| `lesson-09/logger.py`, `plot_data.py` | Analog logging/plotting (vs. motion) | MCP3008 + pot |
| `lesson-09/webapp.py`, `webapp_led_control.py` | Analog-sensor web page + LED control | MCP3008 |

Note: some spare sketches use older pin choices — always check the header comment against your wiring.
