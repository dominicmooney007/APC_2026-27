# Lesson 04 — Arduino: Sensors & Actuators

> Measure the real world (distance, temperature & humidity), show it on an LCD, and move things (servos, motors) — the building blocks of last year's parking sensor and auto-gate, and of your Lesson 5 project.

**Platform:** Arduino
**Estimated time:** ~120 min hands-on
**Prerequisites:** [Lesson 3](lesson-03-arduino-analog.md) — `analogRead`, PWM, Serial Monitor, `map()`

## Learning objectives

- Wire and read an HC-SR04 ultrasonic distance sensor, and convert echo time to centimetres.
- Read temperature **and** humidity from a DHT22 using a library.
- Print live readings on a 1602 I2C LCD — output a person can read without a laptop.
- Sweep an SG90 servo to a chosen angle with the `Servo` library.
- Explain why DC motors need external power and a driver board (L298N) — and never wire one straight to a pin.

## Today's plan (~120 min)

| Time | Part | What you're doing |
|---|---|---|
| ~25 min | A | Ultrasonic distance (HC-SR04) |
| ~20 min | B | Temperature & humidity (DHT22) |
| ~20 min | C | The I2C LCD: readings without a laptop |
| ~40 min | D | **Core build:** distance display with proximity beeper |
| ~15 min | — | Check-out + extensions (servo gate, L298N fan demo) |

## What you'll need

| Item | Qty | Notes |
|---|---|---|
| Arduino + USB + breadboard | 1 | |
| HC-SR04 ultrasonic sensor | 1 | 4 pins: VCC, Trig, Echo, GND |
| DHT22 temperature/humidity sensor | 1 | 3-pin module |
| 1602 LCD with I2C backpack | 1 | Address 0x27 (or 0x3F) |
| Passive buzzer | 1 | Plays tones via `tone()` |
| Micro servo (SG90) | 1 | For the extension |
| Jumper wires | ~12 | |
| *(Extension)* DC motor/fan + L298N driver + battery pack | 1 | Teacher demo station |

**Software:** Arduino IDE + two libraries (Part B/C tell you which).

---

## Part A — Ultrasonic distance (HC-SR04) (~25 min)

The HC-SR04 works like a bat: it chirps (ultrasound), listens for the echo, and the round-trip **time** gives the distance: **distance (cm) = duration × 0.034 / 2** (sound travels ~340 m/s, and the ping goes there *and* back).

### Wiring

**Unplug USB first.**

| HC-SR04 pin | To |
|---|---|
| VCC | Arduino **5V** |
| Trig | Arduino **pin 9** |
| Echo | Arduino **pin 10** |
| GND | Arduino **GND** |

### The sketch

```cpp
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Send a 10 microsecond chirp
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Time the echo, convert to cm
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  delay(100);
}
```

### ✅ Checkpoint A

Hold a book flat in front of the sensor. Verify readings at roughly **10 cm, 30 cm, 50 cm** against a ruler.

!!! warning "Readings of 0 or absurdly huge?"
    The echo never came back: target too close (<2 cm), too far (>4 m), or angled so the sound bounced away. Aim at something flat and face-on. Soft things (hoodies!) absorb sound.

---

## Part B — Temperature & humidity (DHT22) (~20 min)

The DHT22 measures temperature *and* humidity and sends both digitally on one wire — too complex to decode by hand, so we use a **library** (your first).

**Install:** Sketch → Include Library → Manage Libraries → search **"DHT sensor library"** (Adafruit) → Install (accept the companion "Adafruit Unified Sensor" when offered).

### Wiring

| DHT22 pin | To |
|---|---|
| VCC (+) | Arduino **5V** |
| Data | Arduino **pin 2** |
| GND (−) | Arduino **GND** |

### The sketch

```cpp
#include <DHT.h>

const int DHT_PIN = 2;
DHT dht(DHT_PIN, DHT22);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float tempC = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(tempC) || isnan(humidity)) {
    Serial.println("Read failed - check wiring");
  } else {
    Serial.print(tempC);
    Serial.print(" C   ");
    Serial.print(humidity);
    Serial.println(" %");
  }
  delay(2000);   // DHT22 needs ~2 s between reads
}
```

### ✅ Checkpoint B

Read room temperature, then breathe on the sensor — watch humidity jump and temperature climb. Notice the DHT22 refuses to be rushed: one reading every 2 seconds is its speed limit.

---

## Part C — The I2C LCD (~20 min)

The Serial Monitor needs a laptop. The **1602 LCD** (16 characters × 2 rows) makes your device readable on its own — and it connects over **I2C**, so it needs just 2 signal wires.

**Install:** Library Manager → search **"LiquidCrystal I2C"** (Frank de Brabander) → Install.

### Wiring

| LCD pin | To |
|---|---|
| VCC | Arduino **5V** |
| GND | Arduino **GND** |
| SDA | Arduino **A4** |
| SCL | Arduino **A5** |

### The sketch

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Address 0x27, 16 columns, 2 rows. If blank, try 0x3F.
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);      // column 0, row 0
  lcd.print("Hello APC!");
  lcd.setCursor(0, 1);      // column 0, row 1
  lcd.print("LCD is alive");
}

void loop() {
}
```

!!! warning "Backlight on but no text?"
    Two classic fixes: change `0x27` to `0x3F` (two common addresses), or adjust the **contrast potentiometer** on the back of the I2C backpack with a small screwdriver.

### ✅ Checkpoint C

Your text on the LCD, then: make row 2 show a number that counts up once per second (`lcd.print(millis() / 1000)` — but you'll need `lcd.setCursor` in `loop()` and a `delay`).

---

## Part D — Core build: distance display + proximity beeper (~40 min)

Combine A + C, plus the passive buzzer: **LCD shows live distance; the buzzer beeps when something gets too close.** This is the heart of last year's parking-sensor project — this year you're building it yourself.

**Add the buzzer:** positive (+) leg → **pin 8**, negative (−) leg → **GND**.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int trigPin = 9;
const int echoPin = 10;
const int buzzerPin = 8;
const int ALERT_CM = 15;          // beep when closer than this

LiquidCrystal_I2C lcd(0x27, 16, 2);

long readDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  lcd.init();
  lcd.backlight();
  lcd.print("Distance Sensor");
  delay(1500);
  lcd.clear();
}

void loop() {
  long distance = readDistanceCm();

  lcd.setCursor(0, 0);
  lcd.print("Dist: ");
  lcd.print(distance);
  lcd.print(" cm   ");            // trailing spaces erase old digits

  lcd.setCursor(0, 1);
  if (distance < ALERT_CM) {
    lcd.print("!! TOO CLOSE !! ");
    tone(buzzerPin, 880, 100);    // 880 Hz beep, 100 ms
  } else {
    lcd.print("Range clear     ");
  }

  Serial.println(distance);
  delay(150);
}
```

### ✅ Check your work

**Success looks like:** distance updates live on the LCD; walk your hand in and at 15 cm the second row flips and the buzzer chirps; pull away and it clears.

!!! warning "Buzzer silent?"
    `tone()` needs a **passive** buzzer (the open-backed one in your kit). Also check the + leg is on pin 8 — buzzers have polarity.

!!! warning "LCD shows stale digits (like '9 cm' becoming '99 cm')?"
    `lcd.print` doesn't erase. Print trailing spaces after the value — see the sketch — or `lcd.clear()` sparingly (it flickers).

---

## Extension / challenge

1. **Faster = closer** — make the beeps repeat faster as distance shrinks (map distance → gap between `tone()` calls). Now it's a real parking sensor.
2. **Auto gate** — add the SG90 servo (signal → **pin 6**, red → 5V, brown → GND). First run [`servo_sweep/servo_sweep.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/servo_sweep/servo_sweep.ino) to see the `Servo` library move it to 0°/90°/180°. Then the build: when something stays closer than 30 cm, the "gate" opens (90°); when clear for 5 s it closes. Last year's class built exactly this — after you've tried, compare with [`auto_gate/auto_gate.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/auto_gate/auto_gate.ino), which shows a proper state machine.
3. **Climate station** — swap the ultrasonic for the DHT22: LCD row 1 = temperature, row 2 = humidity.
4. **L298N fan (demo station)** — DC motors drink more current than a pin can supply and kick back voltage spikes, so they get **external battery power** and a **driver board**. Try [`l298n_fan/l298n_fan.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/l298n_fan/l298n_fan.ino): speed via PWM on ENA (pin 5), direction via IN1/IN2 (pins 7/4).

## Code

All sketches in [`code/lesson-04/`](https://github.com/REPLACE-USERNAME/apc-2026-27/tree/main/code/lesson-04):

- [`ultrasonic_read/ultrasonic_read.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/ultrasonic_read/ultrasonic_read.ino) — Part A
- [`dht22_read/dht22_read.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/dht22_read/dht22_read.ino) — Part B
- [`lcd_hello/lcd_hello.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/lcd_hello/lcd_hello.ino) — Part C
- [`distance_display/distance_display.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/distance_display/distance_display.ino) — Part D core build
- [`servo_sweep/servo_sweep.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/servo_sweep/servo_sweep.ino) + [`auto_gate/auto_gate.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/auto_gate/auto_gate.ino) — Extension 2
- [`l298n_fan/l298n_fan.ino`](https://github.com/REPLACE-USERNAME/apc-2026-27/blob/main/code/lesson-04/l298n_fan/l298n_fan.ino) — Extension 4 (demo)

**Next up:** [Lesson 5 — Arduino mini-project](lesson-05-arduino-project.md)
