// Lesson 04, Part D (core build) — distance display + proximity beeper
// HC-SR04: Trig->9, Echo->10. LCD: SDA->A4, SCL->A5.
// Passive buzzer: + -> pin 8, - -> GND.

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
