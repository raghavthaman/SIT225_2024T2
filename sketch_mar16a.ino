#include <WiFiNINA.h>
#include <WiFiSSLClient.h>  // Correct secure client for Nano 33 IoT
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>  

const char* ssid = "RAGHAV 7432";  // Ensure this is a 2.4GHz network
const char* password = "g3C6?713";
const char* mqttServer = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud";
const int mqttPort = 8883;
const char* mqttUser = "raghavthaman";  // Use correct HiveMQ Cloud username
const char* mqttPassword = "Raghav@3006MQTT";  // Use correct password

WiFiSSLClient wifiClient;  // Correct secure client for Nano 33 IoT
PubSubClient client(wifiClient);

void setup() {
    Serial.begin(115200);
    delay(2000);
    Serial.println("Publishing message...");
    Serial.println("Connecting to Wi-Fi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\nConnected to Wi-Fi!");

    client.setServer(mqttServer, mqttPort);
    
    while (!client.connected()) {
        Serial.println("Connecting to MQTT...");
        if (client.connect("ArduinoNano33", mqttUser, mqttPassword)) {
            Serial.println("Connected to MQTT!");
        } else {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying...");
            delay(2000);
        }
    }

    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
}

void loop() {
    float x, y, z;
    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(x, y, z);

        String payload = "{\"x\":" + String(x) + ",\"y\":" + String(y) + ",\"z\":" + String(z) + "}";
        client.publish("sensor/gyro", payload.c_str());
    }
    delay(500);
}
