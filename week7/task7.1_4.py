import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load data and model (from Step 3)
df = pd.read_csv('dht22_data.csv')
df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()
X = df[['Temperature']]
y = df['Humidity']

# Train model
model = LinearRegression().fit(X, y)

# Generate 100 test temperatures between min and max
test_temps = np.linspace(X.min().iloc[0], X.max().iloc[0], 100).reshape(-1, 1)
test_temps_df = pd.DataFrame(test_temps, columns=['Temperature'])  # Ensure feature names match
predicted_humidity = model.predict(test_temps_df)

# Save predictions to CSV
predictions = pd.DataFrame({
    'Test_Temperature': test_temps.flatten(),
    'Predicted_Humidity': predicted_humidity
})
predictions.to_csv('predictions.csv', index=False)

print("Generated 100 test predictions:")
print(predictions.head())
