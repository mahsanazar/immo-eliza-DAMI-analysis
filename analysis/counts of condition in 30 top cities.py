import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Group by locality (city) and count the number of homes for each city
homes_per_city = df['locality'].value_counts()

# Sort cities by the number of homes in descending order and select the top thirty cities
top_thirty_cities = homes_per_city.sort_values(ascending=False).head(30)

# Filter the DataFrame to include only the top thirty cities
df_top_thirty_cities = df[df['locality'].isin(top_thirty_cities.index)]

# Define function to categorize condition
def categorize_condition(condition):
    if condition == "TO_BE_DONE_UP":
        return "TO_BE_DONE_UP"
    elif condition in ["JUST_RENOVATED", "TO_RENOVATE"]:
        return "JUST_RENOVATED"
    elif condition == 'GOOD':
        return "GOOD"
    elif condition == "AS_NEW":
        return "AS_NEW"
    elif condition == "TO_RESTORE":
        return "TO_RESTORE"

# Apply categorization to create a new column
df_top_thirty_cities['Condition Category'] = df_top_thirty_cities['condition'].apply(categorize_condition)

# Filter out the "non specific" category
df_filtered = df_top_thirty_cities[df_top_thirty_cities['Condition Category'] != 'non specific']

# Group by locality (city) and condition category, then count the occurrences
grouped_counts = df_filtered.groupby(['locality', 'Condition Category']).size().unstack(fill_value=0)

# Plot the distribution of condition categories for each city
grouped_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Distribution of Condition Categories in Top Thirty Cities (Excluding "non specific")')
plt.xlabel('City')
plt.ylabel('Number of Homes')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
