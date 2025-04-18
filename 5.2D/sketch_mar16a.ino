#include <WiFiNINA.h>               // Library for Wi-Fi connectivity (Nano 33 IoT)
#include <WiFiSSLClient.h>         // SSL client for secure communication
#include <PubSubClient.h>          // MQTT client library
#include <Arduino_LSM6DS3.h>       // Library for LSM6DS3 gyroscope sensor

// Wi-Fi and MQTT configuration
const char* ssid = "RAGHAV 7432";                    // Wi-Fi SSID (2.4GHz recommended)
const char* password = "g3C6?713";                   // Wi-Fi password
const char* mqttServer = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud";  // HiveMQ MQTT broker address
const int mqttPort = 8883;                           // Secure port for MQTT over SSL
const char* mqttUser = "raghavthaman";               // MQTT username
const char* mqttPassword = "Raghav@3006MQTT";        // MQTT password

// Create secure Wi-Fi and MQTT clients
WiFiSSLClient wifiClient;            // Secure Wi-Fi client for encrypted communication
PubSubClient client(wifiClient);     // MQTT client using the secure Wi-Fi client

void setup() {
    Serial.begin(115200);           // Start serial communication for debugging
    delay(2000);                    // Short delay for system stability

    Serial.println("Publishing message...");
    Serial.println("Connecting to Wi-Fi...");

    WiFi.begin(ssid, password);     // Connect to Wi-Fi

    // Wait until Wi-Fi is connected
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\nConnected to Wi-Fi!");

    // Set the MQTT broker server and port
    client.setServer(mqttServer, mqttPort);    

    // Attempt to connect to the MQTT broker
    while (!client.connected()) {
        Serial.println("Connecting to MQTT...");
        if (client.connect("ArduinoNano33", mqttUser, mqttPassword)) {
            Serial.println("Connected to MQTT!");
        } else {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying...");
            delay(2000); // Wait before retrying
        }
    }

    // Initialize the gyroscope (IMU)
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1); // Halt execution if IMU fails
    }
}

void loop() {
    float x, y, z; // Variables to store gyroscope readings

    // Check if gyroscope data is available
    if (IMU.gyroscopeAvailable()) {
        // Read gyroscope values
        IMU.readGyroscope(x, y, z);

        // Create JSON string with x, y, z values
        String payload = "{\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"z\":" + String(z) + "}";

        // Publish JSON data to MQTT topic "sensor/gyro"
        client.publish("sensor/gyro", payload.c_str());
    }

    delay(500); // Delay to control data sending rate (0.5 seconds)
}
