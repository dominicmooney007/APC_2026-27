// Lesson 02, Extensions 1-2 — toggle the LED on each press, debounced.
// Try building this yourself BEFORE reading! Same wiring as button_led.
//
// Two ideas here:
// 1. Toggle: act only when the button CHANGES from up to down (edge),
//    not while it's held (level).
// 2. Debounce: a real button "bounces" — it makes/breaks contact several
//    times in a few ms. We ignore changes within DEBOUNCE_MS of the last one.

const int LED_PIN = 8;
const int BUTTON_PIN = 2;
const unsigned long DEBOUNCE_MS = 50;

int ledState = LOW;
int lastReading = HIGH;              // HIGH = not pressed (pull-up)
unsigned long lastChangeTime = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int reading = digitalRead(BUTTON_PIN);

  // Only consider the reading if it's been stable long enough
  if (reading != lastReading && (millis() - lastChangeTime) > DEBOUNCE_MS) {
    lastChangeTime = millis();
    lastReading = reading;

    if (reading == LOW) {            // falling edge = new press
      ledState = !ledState;          // flip the remembered state
      digitalWrite(LED_PIN, ledState);
    }
  }
}
