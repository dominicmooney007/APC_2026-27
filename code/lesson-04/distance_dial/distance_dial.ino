// Lesson 04, Part D (core build) — distance-controlled servo dial
// HC-SR04: Trig->7, Echo->6. Servo signal->9. Both share 5V/GND.

#include <Servo.h>

const int TRIG_PIN = 7;
const int ECHO_PIN = 6;
Servo dial;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dial.attach(9);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distanceCm = duration / 58.0;

  // 5 cm (close) -> 180 deg ... 50 cm (far) -> 0 deg
  int angle = map(constrain(distanceCm, 5, 50), 5, 50, 180, 0);
  dial.write(angle);

  Serial.print(distanceCm);
  Serial.print(" cm -> ");
  Serial.println(angle);
  delay(100);
}
