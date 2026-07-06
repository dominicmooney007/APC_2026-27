// Lesson 05 — parking sensor STARTER (deliberately incomplete)
// =============================================================
// WHAT IT DOES: reads HC-SR04 distance; you add the alert logic.
// WIRING: HC-SR04 VCC->5V, Trig->7, Echo->6, GND->GND
//         LED: pin 8 -> 220 ohm -> LED -> GND
// =============================================================
// This shows the REQUIRED project structure: header comment,
// named constants, and serial output that tells the story.

const int TRIG_PIN = 7;
const int ECHO_PIN = 6;
const int LED_PIN = 8;

const float NEAR_CM = 10.0;   // tune these!
const float MID_CM  = 25.0;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  return pulseIn(ECHO_PIN, HIGH) / 58.0;
}

void loop() {
  float d = readDistanceCm();

  // TODO 1: three zones -> three behaviours
  //   d < NEAR_CM          : LED solid ON
  //   NEAR_CM..MID_CM      : LED blinking (how fast?)
  //   d > MID_CM           : LED off
  // TODO 2: Serial.println the zone name, not just the number
  // TODO 3 (stretch): blink FASTER as d shrinks (map() is your friend)

  Serial.print(d);
  Serial.println(" cm  |  zone: ???");
  delay(100);
}
