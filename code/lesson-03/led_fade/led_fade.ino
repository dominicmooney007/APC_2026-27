// Lesson 03, Part C — fade an LED with PWM
// Wiring: pin 9 (~PWM) -> 220 ohm -> LED anode; cathode -> GND

const int LED_PIN = 9;   // must be a ~ PWM pin (3, 5, 6, 9, 10, 11)

void setup() {
}

void loop() {
  for (int level = 0; level <= 255; level++) {   // fade up
    analogWrite(LED_PIN, level);
    delay(5);
  }
  for (int level = 255; level >= 0; level--) {   // fade down
    analogWrite(LED_PIN, level);
    delay(5);
  }
}
