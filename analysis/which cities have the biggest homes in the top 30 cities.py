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

# Define function to categorize surface
def categorize_surface(surface):
    if surface < 50:
        return "Less than 50"
    elif 50 <= surface < 100:
        return "50 - 100"
    elif 100<= surface <150:
        return "100-150"
    elif 150<= surface< 200:
        return "150-200"
    elif 200<= surface< 250:
        return "200-250"
    elif 250<= surface< 300:
        return "250-300"
    elif 300<= surface< 350:
         return "300-350"
    elif 350<= surface<400:
         return "350-400"
    elif 400<=surface<450:
         return "400-450"
    elif 450<=surface<500:
         return "450-500"
    elif 500<=surface<550:
         return "500-550"
    elif 550<=surface<600:
         return "550-600"
    else:
        return "Greater than 600"

# Apply categorization to create a new column
df_top_thirty_cities['Surface Category'] = df_top_thirty_cities['surface'].apply(categorize_surface)

# Specify the desired order of surface categories
surface_category_order = ["100-150", "50 - 100", "150-200"]

# Group by 'locality' (city) and 'Surface Category', then count the occurrences
grouped_counts = df_top_thirty_cities.groupby(['locality', 'Surface Category']).size().unstack(fill_value=0)

# Reindex the DataFrame based on the desired order of surface categories
grouped_counts = grouped_counts.reindex(surface_category_order, axis=1)

# Plot the distribution of surface area within the top thirty cities for the specified surfaces
ax = grouped_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Distribution of Surface Area in Top Thirty Cities')
plt.xlabel('City')
plt.ylabel('Number of Homes')
plt.legend(title='Surface Category', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.tight_layout()



plt.show()
