#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>

// Wi-Fi Credentials
const char SSID[] = "Fastway";       // Replace with your Wi-Fi name
const char PASS[] = "1234567890";    // Replace with your Wi-Fi password

// Wi-Fi connection handler
WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

// Sensor Variables
float x, y, z;  
bool alarmTriggered = false;  // Alarm status variable

// Threshold for triggering an alarm
const float THRESHOLD = 2.0;  // Adjust based on sensitivity needs

void setup() {
  Serial.begin(115200);
  
  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Define Cloud Properties with Correct Permission Syntax
  ArduinoCloud.addProperty(x, Permission::Read);
  ArduinoCloud.addProperty(y, Permission::Read);
  ArduinoCloud.addProperty(z, Permission::Read);
  ArduinoCloud.addProperty(alarmTriggered, Permission::ReadWrite);

  // Initialize IMU (LSM6DS3 Accelerometer)
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("Setup complete!");
}

void loop() {
  ArduinoCloud.update(); // Sync cloud variables

  // Read accelerometer data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    
    // Print accelerometer readings
    Serial.print("X: "); Serial.print(x, 2);
    Serial.print(" | Y: "); Serial.print(y, 2);
    Serial.print(" | Z: "); Serial.println(z, 2);
    
    // Detect sudden movement (emergency condition)
    if (abs(x) > THRESHOLD || abs(y) > THRESHOLD || abs(z) > THRESHOLD) {
      alarmTriggered = true;  // Set alarm
      Serial.println("ALARM TRIGGERED!");
    } else {
      alarmTriggered = false; // Reset alarm if no motion detected
    }
  }

  delay(500);  // Delay for smooth data capture
}
