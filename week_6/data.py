import serial
import csv
import time

# Serial port configuration
SERIAL_PORT = "COM7"  # Your Arduino's serial port
BAUD_RATE = 115200
CSV_FILE = "gyroscope_data.csv"

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

# Open CSV file to store data
with open(CSV_FILE, "w", newline="") as file:
    writer = csv.writer(file)

    # Read and write header
    header = ser.readline().decode().strip()
    writer.writerow(header.split(","))

    print(f"Logging data to {CSV_FILE}... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode().strip()
            if line:
                writer.writerow(line.split(","))
                print(line)  # Display real-time readings
    except KeyboardInterrupt:
        print("\nData logging stopped.")
    finally:
        ser.close()
