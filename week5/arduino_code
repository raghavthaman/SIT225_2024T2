#include <Arduino_LSM6DS3.h> // Include library for the LSM6DS3 gyroscope sensor

void setup() {
    Serial.begin(115200);  // Start serial communication at 115200 baud rate
    while (!Serial);       // Wait for serial connection to establish

    // Initialize the IMU (Inertial Measurement Unit) sensor
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");  // Print error message if initialization fails
        while (1);  // Halt execution if IMU is not found
    }
}

void loop() {
    float x, y, z;  // Variables to store gyroscope readings

    // Check if gyroscope data is available
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);  // Read gyroscope data for X, Y, and Z axes

        // Print gyroscope readings in CSV format (comma-separated values)
        Serial.print(x);
        Serial.print(",");
        Serial.print(y);
        Serial.print(",");
        Serial.println(z);  // Newline at the end to indicate a complete reading
    }

    delay(100);  // Delay for 100ms before next reading (adjust as needed)
}
