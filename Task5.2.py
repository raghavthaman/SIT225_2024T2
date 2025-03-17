import paho.mqtt.client as mqtt
import json

# MQTT connection details
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883
mqttUser = "raghavthaman"
mqttPassword = "Raghav@3006MQTT"
topic = "sensor/gyro"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, message):
    payload = message.payload.decode()
    try:
        data = json.loads(payload)
        x = data.get('x', 0)
        y = data.get('y', 0)
        z = data.get('z', 0)
        print(f"Gyroscope Data - x: {x:.2f}, y: {y:.2f}, z: {z:.2f}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Initialize client with protocol v5
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
client.username_pw_set(mqttUser, mqttPassword)
client.tls_set()  # Enable SSL/TLS for secure connection

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start listening
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_forever()