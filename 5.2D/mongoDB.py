import paho.mqtt.client as mqtt  # MQTT library for connecting to HiveMQ
import json  # For parsing JSON data
from pymongo import MongoClient  # MongoDB client for Python
import pandas as pd  # For data handling and cleaning

# MQTT connection details for HiveMQ broker
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883  # Secure port for MQTT
mqttUser = "raghavthaman"
mqttPassword = "Raghav@3006MQTT"
topic = "sensor/gyro"  # Topic for receiving gyroscope data

# Set up MongoDB client and specify database and collection
mongoClient = MongoClient("mongodb://localhost:27017/")  # Connect to local MongoDB
db = mongoClient["sensor_data"]  # Database name
collection = db["gyroscope"]  # Collection to store sensor readings

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)  # Subscribe to gyroscope topic
    else:
        print(f"Connection failed with code {rc}")

# Callback when a new message is received from the MQTT broker
def on_message(client, userdata, message):
    payload = message.payload.decode()  # Decode message from bytes to string
    try:
        data = json.loads(payload)  # Parse JSON data
        print(f"Received: {data}")

        # Insert the parsed data into MongoDB collection
        collection.insert_one(data)
        print("Data inserted into MongoDB")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Function to save collected MongoDB data into a CSV file
def save_to_csv():
    data = list(collection.find())  # Retrieve all documents from the collection
    df = pd.DataFrame(data)  # Convert to DataFrame
    df.to_csv("gyroscope_data.csv", index=False)  # Save to CSV file
    print("Data saved to gyroscope_data.csv")

# Function to clean the CSV data by removing invalid or missing values
def clean_data():
    df = pd.read_csv("gyroscope_data.csv")  # Load raw data
    df = df.dropna()  # Remove rows with missing values
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert all fields to numeric; invalid values become NaN
    df.to_csv("cleaned_gyroscope_data.csv", index=False)  # Save cleaned data
    print("Data cleaned and saved to cleaned_gyroscope_data.csv")

# Initialize MQTT client with version 5 API
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
client.username_pw_set(mqttUser, mqttPassword)  # Set credentials
client.tls_set()  # Enable secure TLS/SSL connection

# Assign the callback functions to the MQTT client
client.on_connect = on_connect
client.on_message = on_message

# Start connection to MQTT broker
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_start()  # Start MQTT loop in background (non-blocking)

# Collect gyroscope data for 30 minutes (1800 seconds)
import time
time.sleep(1800)  # Adjust duration if necessary

# Stop data collection and disconnect
client.loop_stop()
client.disconnect()

# Save the collected data to CSV and clean it
save_to_csv()
clean_data()