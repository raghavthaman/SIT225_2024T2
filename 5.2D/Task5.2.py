import paho.mqtt.client as mqtt  # MQTT library for communication with broker
import json  # Library for parsing JSON-formatted messages

# MQTT connection details for HiveMQ broker
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883  # Secure MQTT port
mqttUser = "raghavthaman"  # MQTT username
mqttPassword = "Raghav@3006MQTT"  # MQTT password
topic = "sensor/gyro"  # Topic to subscribe to for gyroscope data

# Callback function triggered when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")  # Successful connection
        client.subscribe(topic)  # Subscribe to the gyroscope topic
    else:
        print(f"Connection failed with code {rc}")  # Print error code on failure

# Callback function triggered when a message is received from the broker
def on_message(client, userdata, message):
    payload = message.payload.decode()  # Decode incoming message
    try:
        data = json.loads(payload)  # Parse JSON payload
        x = data.get('x', 0)  # Extract x value (default to 0 if missing)
        y = data.get('y', 0)  # Extract y value
        z = data.get('z', 0)  # Extract z value
        print(f"Gyroscope Data - x: {x:.2f}, y: {y:.2f}, z: {z:.2f}")  # Print formatted output
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")  # Handle and display JSON errors

# Initialize MQTT client using protocol version 5
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  

# Set MQTT authentication credentials
client.username_pw_set(mqttUser, mqttPassword)

# Enable TLS encryption for secure communication
client.tls_set()

# Register callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker and start the loop to listen for incoming messages
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_forever()  # Keep the script running to continuously receive data