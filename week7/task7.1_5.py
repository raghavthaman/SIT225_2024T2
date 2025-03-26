import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load original data and predictions
df = pd.read_csv('dht22_data.csv')
df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()
predictions = pd.read_csv('predictions.csv')

# Create plot with crosses for data points
plt.figure(figsize=(10, 6))

# Changed marker from dots to crosses (using 'x' marker)
plt.scatter(df['Temperature'], df['Humidity'], 
            color='blue', 
            marker='x',      # Cross markers
            s=50,           # Size of markers
            linewidths=1.5, # Thickness of cross lines
            label='Actual Data')

# Trend line - using correct column names from predictions
plt.plot(predictions['Test_Temperature'], predictions['Predicted_Humidity'], 
         color='red', 
         linewidth=2, 
         label='Trend Line')

plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.title('Temperature vs Humidity with Linear Regression Trend')
plt.legend()
plt.grid(True)
plt.savefig('trend_plot_crosses.png', dpi=300)
plt.show()

# Analysis
print("\nTrend Line Analysis:")
print("a) The trend line follows the general pattern but may deviate near extremes.")
print("b) Outliers are visible as points far from the red line (e.g., very humid cold days).")