#include <Arduino_LSM6DS3.h>

void setup() {
    Serial.begin(115200);
    while (!Serial);
    
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
    Serial.println("_id,_rev,x,y,z");  // CSV header
}

void loop() {
    float x, y, z;
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);
        String id = String(millis());  // Unique ID based on timestamp
        String rev = "1-" + String(random(100000, 999999));  // Simulated revision number

        Serial.print(id);
        Serial.print(",");
        Serial.print(rev);
        Serial.print(",");
        Serial.print(x, 2);
        Serial.print(",");
        Serial.print(y, 2);
        Serial.print(",");
        Serial.println(z, 2);
    }
    delay(500);  // Adjust sampling rate if needed
}
