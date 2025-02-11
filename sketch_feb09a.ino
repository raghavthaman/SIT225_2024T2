#include <DHT.h>

#define DHTPIN 2         // Pin where the DHT22 data line is connected
#define DHTTYPE DHT22    // Define sensor type as DHT22

DHT dht(DHTPIN, DHTTYPE);  // Create a DHT object

void setup() {
  Serial.begin(9600);
  dht.begin();  // Initialize DHT sensor
}

void loop() {
  // Wait a few seconds between readings
  delay(2000);
  
  // Reading temperature or humidity takes about 250 milliseconds
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if readings failed and exit early
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print the values to the Serial Monitor
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
}
