import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load and filter data
df = pd.read_csv('dht22_data.csv')
df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()
filtered_df = df[(df['Temperature'] >= df['Temperature'].quantile(0.05)) & 
                (df['Temperature'] <= df['Temperature'].quantile(0.95))]

# Prepare data
X = filtered_df[['Temperature']]
y = filtered_df['Humidity']

# Train model
model = LinearRegression()
model.fit(X, y)

# Generate predictions
test_temps = np.linspace(df['Temperature'].min(), df['Temperature'].max(), 100)
predictions = model.predict(test_temps.reshape(-1, 1))

# Create plot with dark blue crosses
plt.figure(figsize=(10, 6), facecolor='white')
plt.scatter(X, y,
            marker='x',
            color='#00008B',  # Dark blue
            s=60,
            linewidths=1.5,
            alpha=0.7,
            label='Filtered Data (5% removed)')

plt.plot(test_temps, predictions,
         'r-',
         linewidth=2,
         label='Trend Line')

plt.xlabel('Temperature (°C)', fontsize=12)
plt.ylabel('Humidity (%)', fontsize=12)
plt.title('Temperature vs Humidity (5% Outliers Removed)', fontsize=14)
plt.legend(framealpha=0.9)
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('filtered_5percent_darkblue.png', dpi=300, bbox_inches='tight')

# Print results
print("5% Outliers Removed Analysis:")
print(f"Data points: {len(filtered_df)} (removed {len(df)-len(filtered_df)})")
print(f"Temperature range: {X.min()[0]:.1f}°C to {X.max()[0]:.1f}°C")
print(f"Model: Humidity = {model.coef_[0]:.4f}*Temperature + {model.intercept_:.4f}")
print(f"R-squared: {model.score(X, y):.4f}")

plt.show()
