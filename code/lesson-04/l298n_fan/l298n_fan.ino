// Lesson 04, Extension 4 (DEMO STATION) — DC fan via L298N driver
// Same wiring as last year's APC fan controller:
//   Motor -> L298N OUT1/OUT2. Battery pack -> L298N 12V + GND.
//   L298N GND also to Arduino GND (shared ground is essential!).
//   ENA->pin 5 (PWM = speed), IN1->pin 7, IN2->pin 4.
// NEVER wire a DC motor directly to an Arduino pin.

const int motorENA = 5;   // PWM pin for speed control
const int motorIN1 = 7;   // Motor direction 1
const int motorIN2 = 4;   // Motor direction 2

void setup() {
  pinMode(motorIN1, OUTPUT);
  pinMode(motorIN2, OUTPUT);
}

void loop() {
  // forward, half speed
  digitalWrite(motorIN1, HIGH);
  digitalWrite(motorIN2, LOW);
  analogWrite(motorENA, 128);
  delay(2000);

  // stop
  analogWrite(motorENA, 0);
  delay(1000);

  // forward, full speed
  analogWrite(motorENA, 255);
  delay(2000);

  // stop
  analogWrite(motorENA, 0);
  delay(1000);
}
