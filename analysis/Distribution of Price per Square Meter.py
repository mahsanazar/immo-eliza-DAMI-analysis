import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np

pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x))

# Specify the file paths
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
    #print(df)
except Exception as e:
    print("Error:", e)
#print(df.describe(include='all'))
#print(df.info())

# Plotting bedrooms and price

# Calculate price per square meter
df['price_per_sqm'] = df['price_main'] / df['surface']
# Filter out non-finite values from the 'price_per_sqm' column
price_per_sqm_filtered = df['price_per_sqm'][np.isfinite(df['price_per_sqm'])]

# Plot the histogram with filtered data
plt.figure(figsize=(10, 6))
plt.hist(price_per_sqm_filtered, bins=20, color='skyblue', alpha=0.7)
plt.title('Distribution of Price per Square Meter')
plt.xlabel('Price per Square Meter')
plt.ylabel('bedrooms')
plt.grid(True)
plt.show()

# plotting price per type of house


price_per_type = df.groupby('type')['price_main'].mean()
# Plot the histogram 
plt.figure(figsize=(10, 6))
plt.hist
plt.title('Distribution of Price per Square Meter')
plt.xlabel('Price per Square Meter')
plt.ylabel('bedrooms')
plt.grid(True)
plt.show()