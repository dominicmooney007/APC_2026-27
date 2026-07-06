// Lesson 04, Part B — TMP36 temperature sensor
// Flat face toward you, legs down: left->5V, middle->A0, right->GND
// WARNING: backwards = it gets hot. Unplug and flip if so.

const int TEMP_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(TEMP_PIN);              // 0-1023
  float volts = raw * (5.0 / 1023.0);          // back to a real voltage
  float tempC = (volts - 0.5) * 100.0;         // 10 mV/degC, 500 mV offset

  Serial.print(tempC);
  Serial.println(" C");
  delay(500);
}
