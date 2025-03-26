import pandas as pd
from sklearn.linear_model import LinearRegression

# Load data - FIXED escape sequence warning
df = pd.read_csv('dht22_data.csv')
df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()

# Prepare data (X = Temperature, y = Humidity)
X = df[['Temperature']]
y = df['Humidity']

# Train model
model = LinearRegression()
model.fit(X, y)

# Print model coefficients
print("Linear Regression Model Trained:")
print(f"Slope (Coefficient): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"Equation: Humidity = {model.coef_[0]:.4f} * Temperature + {model.intercept_:.4f}")

# Additional diagnostics
r2 = model.score(X, y)
print(f"R-squared: {r2:.4f} (Explains {r2*100:.1f}% of variance)")