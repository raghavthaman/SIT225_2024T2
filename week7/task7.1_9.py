import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def load_and_clean_data(filename):
    """Load and clean data, handling column names"""
    df = pd.read_csv(filename)
    # Clean column names by removing units and extra spaces
    df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()
    return df

try:
    # Load data
    print("Loading data files...")
    original_df = load_and_clean_data('dht22_data.csv')
    filtered_df = load_and_clean_data('filtered_data.csv')
    
    # Verify required columns exist
    print("\nChecking data structure...")
    print("Original data columns:", original_df.columns.tolist())
    print("Filtered data columns:", filtered_df.columns.tolist())
    
    if 'Temperature' not in original_df.columns or 'Humidity' not in original_df.columns:
        raise KeyError("Required columns not found in original data")
    if 'Temperature' not in filtered_df.columns or 'Humidity' not in filtered_df.columns:
        raise KeyError("Required columns not found in filtered data")

    # Prepare data
    X_orig = original_df[['Temperature']]
    y_orig = original_df['Humidity']
    X_filt = filtered_df[['Temperature']]
    y_filt = filtered_df['Humidity']

    # Train models
    print("\nTraining models...")
    original_model = LinearRegression().fit(X_orig, y_orig)
    filtered_model = LinearRegression().fit(X_filt, y_filt)

    # Generate comparison range
    temp_range = np.linspace(
        min(X_orig.min()[0], X_filt.min()[0]),
        max(X_orig.max()[0], X_filt.max()[0]),
        100
    ).reshape(-1, 1)

    # Create comparison plot with crosses
    print("\nCreating comparison plot...")
    plt.figure(figsize=(10, 6))
    
    # Original data as red crosses
    plt.scatter(X_orig, y_orig, 
                marker='x',  # This changes dots to crosses
                color='red',
                s=50,        # Size of markers
                linewidths=1.5,  # Thickness of cross lines
                alpha=0.6,
                label='All Data (Original)')
    
    # Filtered data as blue crosses
    plt.scatter(X_filt, y_filt, 
                marker='x',  # Crosses for filtered data too
                color='blue',
                s=50,
                linewidths=1.5,
                alpha=0.8,
                label='Filtered Data')
    
    # Trend lines
    plt.plot(temp_range, original_model.predict(temp_range), 
             'r--', label='Original Trend')
    plt.plot(temp_range, filtered_model.predict(temp_range), 
             'b-', linewidth=2, label='Filtered Trend')
    
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.title('Impact of Outlier Removal on Linear Regression (Cross Markers)')
    plt.legend()
    plt.grid(True)
    plt.savefig('model_comparison_crosses.png', dpi=300, bbox_inches='tight')
    
    # Print model comparison
    print("\n=== Model Comparison Results ===")
    print(f"Original Model: Humidity = {original_model.coef_[0]:.4f}*Temperature + {original_model.intercept_:.4f}")
    print(f"Filtered Model: Humidity = {filtered_model.coef_[0]:.4f}*Temperature + {filtered_model.intercept_:.4f}")
    print(f"\nChange in slope: {filtered_model.coef_[0] - original_model.coef_[0]:.4f}")
    print(f"Change in intercept: {filtered_model.intercept_ - original_model.intercept_:.4f}")
    
    # Calculate and print R-squared values
    r2_orig = original_model.score(X_orig, y_orig)
    r2_filt = filtered_model.score(X_filt, y_filt)
    print(f"\nOriginal Model R-squared: {r2_orig:.4f}")
    print(f"Filtered Model R-squared: {r2_filt:.4f}")
    
    # Show plot
    plt.show()

except FileNotFoundError as e:
    print(f"\nERROR: File not found - {str(e)}")
    print("Please ensure both 'dht22_data.csv' and 'filtered_data.csv' exist in the current directory")
    
except KeyError as e:
    print(f"\nERROR: Missing column - {str(e)}")
    print("Please check your CSV files contain columns named 'Temperature' and 'Humidity'")
    print("Current columns in original data:", original_df.columns.tolist() if 'original_df' in locals() else "Not loaded")
    print("Current columns in filtered data:", filtered_df.columns.tolist() if 'filtered_df' in locals() else "Not loaded")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    print("An unexpected error occurred. Please check your data and try again.")