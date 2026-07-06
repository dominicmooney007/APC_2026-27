// Lesson 05 — smart fan STARTER (deliberately incomplete)
// =============================================================
// WHAT IT DOES: reads DHT22 temperature; you add the fan logic.
// WIRING: DHT22 Data->2. LCD SDA->A4, SCL->A5.
//         L298N: ENA->5 (PWM), IN1->7, IN2->4, battery pack + shared GND.
// =============================================================
// This shows the REQUIRED project structure: header comment,
// named constants, and serial output that tells the story.

#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int DHT_PIN = 2;
const int motorENA = 5;
const int motorIN1 = 7;
const int motorIN2 = 4;

const float FAN_ON_C = 26.0;    // tune these!
const float FAN_MAX_C = 32.0;

DHT dht(DHT_PIN, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(motorIN1, OUTPUT);
  pinMode(motorIN2, OUTPUT);
  digitalWrite(motorIN1, HIGH);   // fixed direction
  digitalWrite(motorIN2, LOW);
  lcd.init();
  lcd.backlight();
}

void loop() {
  float tempC = dht.readTemperature();

  // TODO 1: below FAN_ON_C -> fan off (analogWrite 0)
  // TODO 2: between FAN_ON_C and FAN_MAX_C -> map() temp to speed 100..255
  // TODO 3: LCD row 0 = temperature, row 1 = fan state ("OFF" / "42%")
  // TODO 4: Serial.println the state the same way
  // TODO 5 (stretch): pot on A0 overrides to manual speed control

  Serial.print(tempC);
  Serial.println(" C  |  fan: ???");
  delay(2000);
}
