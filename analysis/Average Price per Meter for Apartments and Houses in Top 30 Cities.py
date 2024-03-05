import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Define the DataFrame df
df['locality'] = df['locality'].replace({'Antwerpen': 'Antwerp'})

# Group by locality (city) and count the number of homes for each city
homes_per_city = df['locality'].value_counts()

# Sort cities by the number of homes in descending order and select the top thirty cities
top_thirty_cities = homes_per_city.sort_values(ascending=False).head(30)

# Filter the DataFrame to include only the top thirty cities
df_top_thirty_cities = df[df['locality'].isin(top_thirty_cities.index)]

# Filter the DataFrame for apartments and houses separately
df_apartment = df_top_thirty_cities[df_top_thirty_cities['type'] == 'APARTMENT']
df_house = df_top_thirty_cities[df_top_thirty_cities['type'] == 'HOUSE']

# Calculate price per meter for apartments and houses separately
df_apartment['price_per_meter'] = df_apartment['price_main'] / df_apartment['surface']
df_house['price_per_meter'] = df_house['price_main'] / df_house['surface']

# Create pivot tables to visualize the average price per meter for apartments and houses
pivot_table_apartment = pd.pivot_table(df_apartment, values='price_per_meter', index='locality', aggfunc='mean')
pivot_table_house = pd.pivot_table(df_house, values='price_per_meter', index='locality', aggfunc='mean')

# Merge the pivot tables to include only cities with available data for both types
merged_pivot_table = pd.merge(pivot_table_apartment, pivot_table_house, on='locality', suffixes=('_apartment', '_house'), how='inner')

# Plotting the merged pivot table as bar plots
plt.figure(figsize=(12, 8))

merged_pivot_table.plot(kind='bar', color=['skyblue', 'lightgreen'])
plt.title('Average Price per Meter for Apartments and Houses in Top 30 Cities')
plt.xlabel('City')
plt.ylabel('Average Price per Meter')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()

plt.show()
