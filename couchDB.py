import paho.mqtt.client as mqtt
import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# MQTT connection details
mqttBroker = "27298008709441c5b8a12aac22fa02d9.s1.eu.hivemq.cloud"
mqttPort = 8883
mqttUser = "raghavthaman"
mqttPassword = "Raghav@3006MQTT"
topic = "sensor/gyro"

# CouchDB connection details
couchDB_url = "http://localhost:5984"
db_name = "sensor_data"
admin_user = "raghavthaman"  # Your admin username
admin_password = "Raghav@3006couchDB"  # Your admin password

# Create CouchDB database if not exists
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

        # Insert data into CouchDB
        response = requests.post(f"{couchDB_url}/{db_name}", json=data, auth=HTTPBasicAuth(admin_user, admin_password))
        if response.status_code == 201:
            print("Data inserted into CouchDB")
        else:
            print(f"Failed to insert data into CouchDB: {response.text}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Function to query CouchDB and save data to CSV
def save_to_csv():
    response = requests.get(f"{couchDB_url}/{db_name}/_all_docs?include_docs=true", auth=HTTPBasicAuth(admin_user, admin_password))
    if response.status_code == 200:
        docs = response.json()['rows']
        data = [doc['doc'] for doc in docs]
        df = pd.DataFrame(data)
        df.to_csv("gyroscope_data.csv", index=False)
        print("Data saved to gyroscope_data.csv")
    else:
        print(f"Failed to fetch data from CouchDB: {response.text}")

# Function to clean data and remove non-numeric or empty fields
def clean_data():
    df = pd.read_csv("gyroscope_data.csv")
    df = df.dropna()  # Remove rows with missing values
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric
    df.to_csv("cleaned_gyroscope_data.csv", index=False)
    print("Data cleaned and saved to cleaned_gyroscope_data.csv")

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(mqttUser, mqttPassword)
client.tls_set()  # Enable SSL/TLS for secure connection

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start listening
print("Connecting to broker...")
client.connect(mqttBroker, mqttPort)
client.loop_start()  # Start loop in a non-blocking way

# Create CouchDB database
create_db()

# Collect data for 30 minutes (1800 seconds)
import time
time.sleep(1800)  # Adjust time as needed

# Stop MQTT loop and disconnect
client.loop_stop()
client.disconnect()

# Save data to CSV and clean it
save_to_csv()
clean_data()
