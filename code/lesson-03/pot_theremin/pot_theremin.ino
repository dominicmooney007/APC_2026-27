// Lesson 03, Extension 2 — pot theremin
// Pot: left->5V, middle->A0, right->GND
// Passive buzzer: + leg -> pin 8, - leg -> GND

const int POT_PIN = A0;
const int BUZZER_PIN = 8;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(POT_PIN);
  int pitch = map(raw, 0, 1023, 200, 2000);   // Hz
  tone(BUZZER_PIN, pitch);
  Serial.println(pitch);
  delay(20);
  // Your turn: add noTone() below a threshold so full-left = silence.
}
