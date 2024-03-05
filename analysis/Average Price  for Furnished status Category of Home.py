import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Define function to categorize condition
def categorize_furnished(isFurnished):
    if isFurnished == 0:
        return "not furnished"
    elif isFurnished==1:
        return"is furnished"
    else:
        return "non specific"

# Apply categorization to create a new column
df['Furnished Category'] = df['isFurnished'].apply(categorize_furnished)

# Calculate price per meter
df['Price per Meter'] = df['price_main'] / df['surface']

# Group by condition category and calculate mean price per meter
price_per_meter_category = df.groupby('Furnished Category')['Price per Meter'].mean()

# Convert the index to strings
price_per_meter_category.index = price_per_meter_category.index.astype(str)

# Check if the DataFrame is empty or contains NaN values
# Check if the DataFrame is empty or contains NaN values
if price_per_meter_category.empty or price_per_meter_category.isnull().values.any():
    print("Error: Empty or NaN values found in the DataFrame.")
else:
    print("Data for plotting:", price_per_meter_category)
    # Plot the bar plot if the DataFrame is valid
    plt.figure(figsize=(10, 6))
    price_per_meter_category.plot(kind='bar', color='skyblue')
    plt.title('Average Price per meter for Furnished/non furnished status Category of Home')
    plt.xlabel(' Furnished Category')
    plt.ylabel('Average Price ')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

