import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
def plot_dht22_data():
    csv_file = "dht22_readings_1s.csv"
    df = pd.read_csv(csv_file, parse_dates=['Timestamp'])
    
    # Create a figure with two subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot temperature
    axes[0].plot(df['Timestamp'], df['Temperature (°C)'], label='Temperature (°C)', color='red')
    axes[0].set_ylabel('Temperature (°C)')
    axes[0].set_title('DHT22 Temperature Data')
    axes[0].legend()
    axes[0].grid()
    
    # Plot humidity
    axes[1].plot(df['Timestamp'], df['Humidity (%)'], label='Humidity (%)', color='blue')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Humidity (%)')
    axes[1].set_title('DHT22 Humidity Data')
    axes[1].legend()
    axes[1].grid()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run the function
plot_dht22_data()
