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

# Define the conditions
conditions = ['AS_NEW', 'GOOD', 'JUST_RENOVATED', 'TO_BE_DONE_UP', 'TO_RENOVATE', 'TO_RESTORE']

# Create a pivot table to visualize price per meter for each condition
pivot_table = pd.pivot_table(df, values='price_per_meter', index='condition', aggfunc='mean')

# Reorder the pivot table according to the specified conditions
pivot_table = pivot_table.reindex(conditions)

# Sort the pivot table in descending order of average price per meter
pivot_table_sorted = pivot_table.sort_values(by='price_per_meter', ascending=False)

# Plotting the sorted pivot table as a bar plot
plt.figure(figsize=(10, 6))
pivot_table_sorted.plot(kind='bar', color='skyblue')
plt.title('Average Price per Meter for Each Condition (Descending Order)')
plt.xlabel('Condition')
plt.ylabel('Average Price per Meter')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()