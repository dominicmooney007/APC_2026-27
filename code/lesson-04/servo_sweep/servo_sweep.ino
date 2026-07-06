// Lesson 04, Extension 2 warm-up — servo basics with the Servo library
// Brown->GND, Red->5V, Orange (signal)->pin 6

#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(6);
}

void loop() {
  myServo.write(0);      // degrees
  delay(1000);
  myServo.write(90);
  delay(1000);
  myServo.write(180);
  delay(1000);
}
