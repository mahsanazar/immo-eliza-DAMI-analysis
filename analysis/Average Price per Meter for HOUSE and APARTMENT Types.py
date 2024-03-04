import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Assuming df is your DataFrame containing the data

# Calculate price per meter
df['price_per_meter'] = df['price_main'] / df['surface']

# Filter the DataFrame for 'HOUSE' and 'APARTMENT' types
filtered_df = df[df['type'].isin(['HOUSE', 'APARTMENT'])]

# Calculate the average price per meter for each type
average_price_per_meter = filtered_df.groupby('type')['price_per_meter'].mean()

# Plotting the average price per meter for each type
plt.figure(figsize=(8, 6))
average_price_per_meter.plot(kind='bar', color=['blue', 'green'])
plt.title('Average Price per Meter for HOUSE and APARTMENT Types')
plt.xlabel('Type')
plt.ylabel('Average Price per Meter')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
