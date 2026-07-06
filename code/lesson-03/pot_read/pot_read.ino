// Lesson 03, Parts A & B — read a potentiometer (or LDR divider) on A0
// Pot: left leg -> 5V, middle -> A0, right -> GND
// LDR: 5V -> LDR -> A0 + 10k -> GND (voltage divider)

const int POT_PIN = A0;

void setup() {
  Serial.begin(9600);         // open the serial connection to the Mac
}

void loop() {
  int value = analogRead(POT_PIN);   // 0-1023
  Serial.println(value);             // view in Serial Monitor or Plotter
  delay(100);
}
