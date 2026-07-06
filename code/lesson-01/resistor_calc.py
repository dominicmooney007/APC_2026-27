"""Lesson 01 — LED current-limiting resistor calculator (Ohm's law).

R = (supply voltage - LED forward voltage) / target current

Change the three values below and re-run to explore. This is a preview
of the Python you'll write on the Raspberry Pi from Lesson 7 onward.
"""

supply_v = 3.3    # volts — power supply module setting
led_forward_v = 2.0  # volts — typical red LED
target_current_a = 0.010  # amps (10 mA — bright but safe)

resistor_ohms = (supply_v - led_forward_v) / target_current_a

print(f"Supply: {supply_v} V, LED drop: {led_forward_v} V, target: {target_current_a * 1000:.0f} mA")
print(f"Minimum resistor: {resistor_ohms:.0f} Ω")
print("Round UP to the nearest standard value you have (e.g. 220 Ω).")
