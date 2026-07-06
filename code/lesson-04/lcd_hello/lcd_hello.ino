// Lesson 04, Part C — 1602 I2C LCD hello
// Library: "LiquidCrystal I2C" (Frank de Brabander)
// Wiring: VCC->5V, GND->GND, SDA->A4, SCL->A5
// Blank screen? Try address 0x3F, or adjust the contrast pot on the backpack.

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);      // column 0, row 0
  lcd.print("Hello APC!");
  lcd.setCursor(0, 1);      // column 0, row 1
  lcd.print("LCD is alive");
}

void loop() {
}
