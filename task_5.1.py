import serial
import json
import firebase_admin
from firebase_admin import credentials, db
import time

# Initialize Firebase
cred = credentials.Certificate("arduino-59447-firebase-adminsdk-fbsvc-a7fea71160.json")  # Add your Firebase credentials
firebase_admin.initialize_app(cred, {"databaseURL": "https://arduino-59447-default-rtdb.firebaseio.com/"})

# Open Serial Connection
ser = serial.Serial("COM7", 115200)  # Replace COMx with your Arduino port
ref = db.reference("gyroscope_data")

while True:
    try:
        line = ser.readline().decode().strip()
        x, y, z = map(float, line.split(","))
        timestamp = time.time()
        data = {"timestamp": timestamp, "x": x, "y": y, "z": z}
        ref.push(data)
        print("Uploaded:", data)
    except Exception as e:
        print("Error:", e)