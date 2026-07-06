// Lesson 04, Extension 2 — automated gate (state machine)
// Adapted from last year's APC Auto Gate project.
// HC-SR04: Trig->9, Echo->10. Servo: signal->6, red->5V, brown->GND.
// LCD: SDA->A4, SCL->A5. Buzzer: + -> 8.
// Gate opens when something stays close, closes 5 s after it clears.

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

const int trigPin = 9;
const int echoPin = 10;
const int buzzerPin = 8;
const int servoPin = 6;

const int DETECTION_DISTANCE = 30;   // cm - "vehicle" detected
const int CLEAR_DISTANCE = 40;       // cm - considered gone
const unsigned long CLOSE_DELAY_MS = 5000;

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo gateServo;

enum GateState { GATE_CLOSED, GATE_OPEN };
GateState state = GATE_CLOSED;
unsigned long lastSeen = 0;

long readDistanceCm() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  return pulseIn(echoPin, HIGH) * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  gateServo.attach(servoPin);
  gateServo.write(0);                // closed position
  lcd.init();
  lcd.backlight();
  lcd.print("Auto Gate ready");
  delay(1000);
  lcd.clear();
}

void loop() {
  long d = readDistanceCm();

  lcd.setCursor(0, 0);
  lcd.print("Dist: ");
  lcd.print(d);
  lcd.print(" cm   ");

  if (state == GATE_CLOSED && d > 2 && d < DETECTION_DISTANCE) {
    state = GATE_OPEN;
    tone(buzzerPin, 660, 200);
    gateServo.write(90);             // open
    lastSeen = millis();
  }

  if (state == GATE_OPEN) {
    if (d < CLEAR_DISTANCE) {
      lastSeen = millis();           // still there - reset the timer
      lcd.setCursor(0, 1);
      lcd.print("GATE OPEN       ");
    } else {
      unsigned long waited = millis() - lastSeen;
      lcd.setCursor(0, 1);
      lcd.print("Closing in ");
      lcd.print((CLOSE_DELAY_MS - waited) / 1000 + 1);
      lcd.print("s  ");
      if (waited >= CLOSE_DELAY_MS) {
        state = GATE_CLOSED;
        tone(buzzerPin, 440, 200);
        gateServo.write(0);          // close
        lcd.setCursor(0, 1);
        lcd.print("GATE CLOSED     ");
      }
    }
  } else {
    lcd.setCursor(0, 1);
    lcd.print("GATE CLOSED     ");
  }

  delay(100);
}
