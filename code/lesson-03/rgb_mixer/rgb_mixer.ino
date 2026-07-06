// Lesson 03, Extension 3 — RGB colour mixing with three PWM channels
// Common-cathode RGB LED: R/G/B legs each through 220 ohm to pins 9/10/11,
// long leg (common cathode) to GND. (Or use three separate LEDs.)

const int R_PIN = 9;
const int G_PIN = 10;
const int B_PIN = 11;

void setColor(int r, int g, int b) {
  analogWrite(R_PIN, r);
  analogWrite(G_PIN, g);
  analogWrite(B_PIN, b);
}

void setup() {
}

void loop() {
  setColor(255, 0, 0);    delay(700);  // red
  setColor(0, 255, 0);    delay(700);  // green
  setColor(0, 0, 255);    delay(700);  // blue
  setColor(255, 120, 0);  delay(700);  // orange
  setColor(255, 0, 180);  delay(700);  // pink
  // Your turn: fade smoothly between colours instead of jumping.
}
