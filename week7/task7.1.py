import serial
import csv
import time

# Serial port configuration (Update PORT if needed)
SERIAL_PORT = "COM7"  # For Windows (Check Device Manager)
# SERIAL_PORT = "/dev/ttyUSB0"  # For Linux
# SERIAL_PORT = "/dev/tty.usbmodem14101"  # For macOS
BAUD_RATE = 9600

# CSV file setup
CSV_FILENAME = "dht22_data.csv"
HEADER = ["Temperature (°C)", "Humidity (%)"]

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow connection to establish
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

# Open CSV file for writing
with open(CSV_FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(HEADER)  # Write column headers

    print("Collecting data... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode("utf-8").strip()  # Read data from serial
            if line:
                try:
                    temp, humid = map(float, line.split(","))  # Parse data
                    writer.writerow([temp, humid])  # Save to CSV
                    print(f"Saved: Temperature={temp}°C, Humidity={humid}%")
                except ValueError:
                    print("Invalid data received:", line)
    except KeyboardInterrupt:
        print("\nData collection stopped.")

# Close serial connection
ser.close()