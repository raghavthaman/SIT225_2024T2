import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def load_and_clean_data(filename):
    """Load and clean data, handling column names"""
    df = pd.read_csv(filename)
    df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()
    return df

try:
    # Load data
    df = load_and_clean_data('dht22_data.csv')
    
    # Apply aggressive filtering (remove top/bottom 10%)
    lower = df['Temperature'].quantile(0.10)
    upper = df['Temperature'].quantile(0.90)
    strong_filtered = df[(df['Temperature'] >= lower) & (df['Temperature'] <= upper)]
    
    # Prepare data
    X = strong_filtered[['Temperature']]
    y = strong_filtered['Humidity']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate predictions
    test_temps = np.linspace(X.min()[0], X.max()[0], 100).reshape(-1, 1)
    predictions = model.predict(test_temps)
    
    # Create plot with DARK GREEN crosses
    plt.figure(figsize=(12, 7), facecolor='white')  # Larger figure with white background
    
    # Dark green crosses (using hex code #006400)
    plt.scatter(X, y, 
                marker='x',
                color='#006400',  # Dark green color
                s=70,            # Slightly larger markers
                linewidths=1.8,   # Thicker crosses
                alpha=0.8,        # Less transparency
                label='Filtered Data (10% outliers removed)')
    
    # Enhanced trend line
    plt.plot(test_temps, predictions, 
             color='#E63946',     # Scientific red
             linewidth=2.5, 
             linestyle='-',
             label='Regression Trend')
    
    # Styling
    plt.xlabel('Temperature (°C)', fontsize=12, fontweight='bold')
    plt.ylabel('Humidity (%)', fontsize=12, fontweight='bold')
    plt.title('Temperature vs Humidity (10% Outliers Removed)', 
              fontsize=14, pad=20, fontweight='bold')
    
    # Custom legend
    legend = plt.legend(frameon=True, framealpha=0.9, 
                        edgecolor='black', fontsize=10)
    legend.get_frame().set_facecolor('#F8F9FA')  # Light gray background
    
    # Grid and axes
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#F8F9FA')  # Light gray plot background
    
    # Save high-quality image
    plt.savefig('temperature_humidity_dark_green.png', 
                dpi=350, 
                bbox_inches='tight',
                facecolor='white')
    
    # Print results
    print("\n" + "="*50)
    print("Aggressive Filtering Results (10% outliers removed)")
    print("="*50)
    print(f"\nData points remaining: {len(strong_filtered)}/{len(df)}")
    print(f"Temperature range: {X.min()[0]:.1f}°C to {X.max()[0]:.1f}°C")
    print("\nRegression Model:")
    print(f"  Slope: {model.coef_[0]:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    print(f"  Equation: Humidity = {model.coef_[0]:.4f}*Temperature + {model.intercept_:.4f}")
    print(f"\nModel Performance:")
    print(f"  R-squared: {model.score(X, y):.4f}")
    print(f"  Standard Error: {np.sqrt(np.mean((y - model.predict(X))**2)):.4f}")
    
    plt.show()

except Exception as e:
    print(f"\nERROR: {str(e)}")
    print("Please verify:")
    print("1. 'dht22_data.csv' exists in the current directory")
    print("2. The file contains 'Temperature' and 'Humidity' columns")
    print("3. The data is properly formatted (comma-separated values)")