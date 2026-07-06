// Lesson 02, Parts B & C — Blink
// Blinks the onboard LED (pin 13). For Part C, change LED_PIN to 8
// and wire: pin 8 -> 220 ohm resistor -> LED anode; LED cathode -> GND.

const int LED_PIN = 13;  // onboard LED; change to 8 for your breadboard LED

void setup() {
  pinMode(LED_PIN, OUTPUT);   // declare the pin as an output
}

void loop() {
  digitalWrite(LED_PIN, HIGH);  // LED on
  delay(500);                   // wait 500 ms
  digitalWrite(LED_PIN, LOW);   // LED off
  delay(500);
}
