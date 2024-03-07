import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Assuming df is your DataFrame containing the data

# Calculate price per meter
df['price_per_meter'] = df['price_main'] / df['surface']




# Filter the DataFrame for 'apartment' type and remove 'KOT' subtype
apartment_df = df[(df['type'] == 'APARTMENT') & (df['subtype'] != 'KOT')]

# Filter the DataFrame for 'house' type and remove '0' subtype
house_df = df[(df['type'] == 'HOUSE') & (df['subtype'] != 0)]
# Sort the values in the DataFrames by 'price_per_meter'
apartment_df_sorted = apartment_df.groupby('subtype')['price_per_meter'].mean().sort_values(ascending=False)
house_df_sorted = house_df.groupby('subtype')['price_per_meter'].mean().sort_values(ascending=False)

# Create bar plot for 'apartment' subtype
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
apartment_df.groupby('subtype')['price_per_meter'].mean().plot(kind='bar', color='blue')
plt.title('Average Price per Meter for Apartment Subtypes')
plt.xlabel('Subtype')
plt.ylabel('Average Price per Meter')

# Create bar plot for 'house' subtype
plt.subplot(1, 2, 2)
house_df.groupby('subtype')['price_per_meter'].mean().plot(kind='bar', color='green')
plt.title('Average Price per Meter for House Subtypes')
plt.xlabel('Subtype')
plt.ylabel('Average Price per Meter')

plt.tight_layout()
plt.show()
