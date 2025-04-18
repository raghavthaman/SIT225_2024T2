import paho.mqtt.client as mqtt  # MQTT client for message communication
import json  # To parse and handle JSON payloads
import requests  # For HTTP requests to CouchDB
from requests.auth import HTTPBasicAuth  # For basic authentication with CouchDB
import pandas as pd  # For handling and cleaning CSV data

# MQTT connection details for HiveMQ broker
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883  # Secure port for MQTT
mqttUser = "raghavthaman"
mqttPassword = "Raghav@3006MQTT"
topic = "sensor/gyro"  # MQTT topic for gyroscope data

# CouchDB configuration
couchDB_url = "http://localhost:5984"
db_name = "sensor_data"
admin_user = "raghavthaman"
admin_password = "Raghav@3006couchDB"

# Create CouchDB database if it does not already exist
def create_db():
    try:
        response = requests.get(f"{couchDB_url}/{db_name}", auth=HTTPBasicAuth(admin_user, admin_password))
        if response.status_code != 200:
            print(f"Database '{db_name}' doesn't exist. Creating new one.")
            response = requests.put(f"{couchDB_url}/{db_name}", auth=HTTPBasicAuth(admin_user, admin_password))
            if response.status_code == 201:
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Failed to create database. Response: {response.text}")
        else:
            print(f"Database '{db_name}' already exists.")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to CouchDB: {e}")

# MQTT callback: triggered upon successful connection to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)  # Subscribe to sensor data topic
    else:
        print(f"Connection failed with code {rc}")

# MQTT callback: triggered when a message is received from the broker
def on_message(client, userdata, message):
    payload = message.payload.decode()  # Decode MQTT message
    try:
        data = json.loads(payload)  # Parse the JSON payload
        print(f"Received: {data}")

        # Insert data into CouchDB using HTTP POST
        response = requests.post(f"{couchDB_url}/{db_name}", json=data, auth=HTTPBasicAuth(admin_user, admin_password))
        if response.status_code == 201:
            print("Data inserted into CouchDB")
        else:
            print(f"Failed to insert data into CouchDB: {response.text}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Save all documents from CouchDB to a CSV file
def save_to_csv():
    response = requests.get(f"{couchDB_url}/{db_name}/_all_docs?include_docs=true", auth=HTTPBasicAuth(admin_user, admin_password))
    if response.status_code == 200:
        docs = response.json()['rows']
        data = [doc['doc'] for doc in docs]  # Extract documents from response
        df = pd.DataFrame(data)  # Convert to DataFrame
        df.to_csv("gyroscope_data.csv", index=False)  # Save raw data
        print("Data saved to gyroscope_data.csv")
    else:
        print(f"Failed to fetch data from CouchDB: {response.text}")

# Clean the saved CSV by removing non-numeric or empty fields
def clean_data():
    df = pd.read_csv("gyroscope_data.csv")  # Load raw data from CSV
    df = df.dropna()  # Drop rows with missing values
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric values
    df.to_csv("cleaned_gyroscope_data.csv", index=False)  # Save cleaned data
    print("Data cleaned and saved to cleaned_gyroscope_data.csv")

# Initialize MQTT client (version 3.1.1 by default)
client = mqtt.Client()
client.username_pw_set(mqttUser, mqttPassword)
client.tls_set()  # Enable SSL/TLS for secure communication

# Set callback functions for MQTT events
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker and start listening
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_start()  # Start non-blocking MQTT loop

# Create the CouchDB database if it doesn’t already exist
create_db()

# Collect sensor data for 30 minutes
import time
time.sleep(1800)  # Adjust collection time as needed

# Stop MQTT loop and disconnect from the broker
client.loop_stop()
client.disconnect()

# Save collected data to CSV and perform cleaning
save_to_csv()
clean_data()