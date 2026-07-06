// Lesson 04, Part B — DHT22 temperature & humidity
// Library: "DHT sensor library" (Adafruit) + "Adafruit Unified Sensor"
// Wiring: VCC->5V, Data->pin 2, GND->GND

#include <DHT.h>

const int DHT_PIN = 2;
DHT dht(DHT_PIN, DHT22);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float tempC = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(tempC) || isnan(humidity)) {
    Serial.println("Read failed - check wiring");
  } else {
    Serial.print(tempC);
    Serial.print(" C   ");
    Serial.print(humidity);
    Serial.println(" %");
  }
  delay(2000);   // DHT22 needs ~2 s between reads
}
