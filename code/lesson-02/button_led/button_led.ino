// Lesson 02, Part D — button controls the LED (core build)
// Wiring: pin 8 -> 220 ohm -> LED anode; LED cathode -> GND.
//         button between pin 2 and GND (INPUT_PULLUP: pressed = LOW).

const int LED_PIN = 8;
const int BUTTON_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // built-in pull-up: no resistor needed
}

void loop() {
  int state = digitalRead(BUTTON_PIN);

  if (state == LOW) {          // LOW = pressed (pull-up logic!)
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
