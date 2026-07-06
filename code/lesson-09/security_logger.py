# Lesson 09, Layer 1 — motion detection + alarm + CSV log
# PIR OUT->GPIO27 (PIR powered from external 5V rail; COMMON GROUND with Pi pin 9!)
# Buzzer + ->GPIO22, alarm LED->GPIO17 (via 330), status LED->GPIO23 (via 330)
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
