// Lesson 04, Extension 3 (DEMO STATION) — DC motor via L298N driver
// Motor -> L298N OUT1/OUT2. Battery pack -> L298N 12V + GND.
// L298N GND also to Arduino GND (shared ground is essential!).
// L298N IN1->4, IN2->5, ENA->9 (PWM = speed).
// NEVER wire a DC motor directly to an Arduino pin.

const int IN1 = 4;
const int IN2 = 5;
const int ENA = 9;   // PWM pin = speed control

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  // forward, half speed
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 128);
  delay(2000);

  // stop
  analogWrite(ENA, 0);
  delay(1000);

  // reverse, full speed
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 255);
  delay(2000);

  // stop
  analogWrite(ENA, 0);
  delay(1000);
}
