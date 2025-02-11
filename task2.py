import serial
import time
import csv
from datetime import datetime

arduino = serial.Serial('COM7', 9600, timeout=1)

# Open the CSV file for writing
with open('accelerometer_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'X', 'Y', 'Z'])  # CSV headers

    # Collect data for a specified duration
    start_time = time.time()
    while True:
        try:
            # Read data from Arduino (accelerometer readings)
            line = arduino.readline().decode('utf-8').strip()
            if line:
                # Get the current timestamp in YYYYMMDDHHMMSS format
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                # Split the data into X, Y, Z values
                data = line.split(',')
                # Write the timestamp and data to the CSV file
                writer.writerow([timestamp] + data)
                print(f"{timestamp}: {data}")  # Print to console
            time.sleep(1)  # Adjust sleep time for your sampling frequency
        except KeyboardInterrupt:
            break

# Close the serial connection when done
arduino.close()
