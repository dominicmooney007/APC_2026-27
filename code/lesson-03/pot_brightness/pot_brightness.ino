// Lesson 03, Part D (core build) — knob controls LED brightness
// Pot on A0 (see pot_read), LED + 220 ohm on pin 9 (see led_fade)

const int POT_PIN = A0;
const int LED_PIN = 9;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(POT_PIN);              // 0-1023
  int brightness = map(raw, 0, 1023, 0, 255); // rescale to 0-255

  analogWrite(LED_PIN, brightness);

  Serial.print(raw);
  Serial.print(" -> ");
  Serial.println(brightness);
  delay(50);
}
