import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import pandas as pd

# MQTT connection details
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883
mqttUser = "raghavthaman"
mqttPassword = "Raghav@3006MQTT"
topic = "sensor/gyro"

# MongoDB connection details
mongoClient = MongoClient("mongodb://localhost:27017/")
db = mongoClient["sensor_data"]
collection = db["gyroscope"]

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
        print(f"Received: {data}")

        # Insert data into MongoDB
        collection.insert_one(data)
        print("Data inserted into MongoDB")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Function to query MongoDB and save data to CSV
def save_to_csv():
    data = list(collection.find())
    df = pd.DataFrame(data)
    df.to_csv("gyroscope_data.csv", index=False)
    print("Data saved to gyroscope_data.csv")

# Function to clean data and remove non-numeric or empty fields
def clean_data():
    df = pd.read_csv("gyroscope_data.csv")
    df = df.dropna()  # Remove rows with missing values
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric
    df.to_csv("cleaned_gyroscope_data.csv", index=False)
    print("Data cleaned and saved to cleaned_gyroscope_data.csv")

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
client.username_pw_set(mqttUser, mqttPassword)
client.tls_set()  # Enable SSL/TLS for secure connection

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start listening
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_start()  # Start loop in a non-blocking way

# Collect data for 30 minutes (1800 seconds)
import time
time.sleep(1800)  # Adjust time as needed

# Stop MQTT loop and disconnect
client.loop_stop()
client.disconnect()

# Save data to CSV and clean it
save_to_csv()
clean_data()