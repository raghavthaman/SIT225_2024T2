import serial
import random
import time
from datetime import datetime

# Configure the serial connection
SERIAL_PORT = 'COM7'  # Change this to your Arduino's COM port
BAUD_RATE = 9600

# Initialize serial connection
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    time.sleep(2)  # Allow Arduino time to initialize
    print("Starting communication with Arduino...")
except Exception as e:
    print(f"Error initializing serial connection: {e}")
    exit(1)

try:
    while True:
        # Step 1: Generate and send a random number to Arduino
        number_to_send = random.randint(1, 10)
        arduino.write(f"{number_to_send}\n".encode('utf-8'))

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Sent to Arduino: {number_to_send}")

        # Step 2: Wait for Arduino's response
        response = arduino.readline().decode('utf-8').strip()
        
        if response:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Received from Arduino: {response}")

            # Step 3: Sleep for the number of seconds received
            try:
                sleep_time = int(response)
                if 0 <= sleep_time <= 10:  # Optional validation
                    print(f"Sleeping for {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    print("Sleep complete.")
                else:
                    print(f"Invalid sleep time received: {sleep_time}")
            except ValueError:
                print("Invalid number received from Arduino.")
        else:
            print(f"[{timestamp}] Warning: No response received from Arduino.")

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    arduino.close()
    print("Serial connection closed.")