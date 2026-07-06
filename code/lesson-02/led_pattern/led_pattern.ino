// Lesson 02, Extension 3 — LED chase pattern (starter)
// Wiring: pins 8, 9, 10, 11 -> each through its OWN 220 ohm resistor
//         -> LED anode; all LED cathodes -> GND.
// Challenge: make it bounce back and forth (Knight Rider style).

const int LED_PINS[] = {8, 9, 10, 11};
const int NUM_LEDS = 4;
const int STEP_MS = 120;

void setup() {
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], HIGH);
    delay(STEP_MS);
    digitalWrite(LED_PINS[i], LOW);
  }
  // Your turn: after the loop above, run the pattern in REVERSE
  // so the light bounces back instead of jumping to the start.
}
