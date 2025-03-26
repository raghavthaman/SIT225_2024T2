import pandas as pd

# Load and clean data - fixed escape sequence warning
df = pd.read_csv('dht22_data.csv')
df.columns = df.columns.str.replace(r' \(.*\)', '', regex=True).str.strip()

# Remove top/bottom 5% temperatures
lower = df['Temperature'].quantile(0.05)
upper = df['Temperature'].quantile(0.95)
filtered_df = df[(df['Temperature'] >= lower) & (df['Temperature'] <= upper)]

# Save filtered data
filtered_df.to_csv('filtered_data.csv', index=False)

# Print summary
print(f"Original data: {len(df)} points")
print(f"Filtered data: {len(filtered_df)} points (removed {len(df)-len(filtered_df)})")
print(f"New temperature range: {filtered_df['Temperature'].min():.1f}°C to {filtered_df['Temperature'].max():.1f}°C")