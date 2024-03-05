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
df_top_thirty_cities = df[df['locality'].isin(top_thirty_cities.index)].copy()

# Define function to categorize surface
def categorize_surface(surface):
    if surface < 50:
        return "Less than 50"
    elif 50 <= surface < 100:
        return "50 - 100"
    elif 100 <= surface < 200:
        return "100-150"
    elif 150 <= surface < 250:
        return "150-200"
    elif 250 <= surface < 300:
        return "250-300"
    elif 300 <= surface < 350:
        return "300-350"
    elif 350 <= surface < 400:
        return "350-400"
    elif 450 <= surface < 500:
        return "450-500"
    elif 550 <= surface < 600:
        return "550-600"
    else:
        return "Greater than 600"

# Apply categorization to create a new column using .loc to avoid the warning
df_top_thirty_cities.loc[:, 'Surface Category'] = df_top_thirty_cities['surface'].apply(categorize_surface)

# Group by Surface Category and locality (city), then count the occurrences
grouped_counts = df_top_thirty_cities.groupby(['Surface Category', 'locality']).size().unstack(fill_value=0)

# Specify the order of surface categories
surface_categories_order = [
    "Less than 50",
    "50 - 100",
    "100-150",
    "150-200",
    "250-300",
    "300-350",
    "350-400",
    "450-500",
    "550-600",
    "Greater than 600"
]

# Sort the grouped_counts DataFrame based on the order of surface categories
grouped_counts_sorted = grouped_counts.reindex(surface_categories_order)

# Plot each surface category and save each plot separately
for surface_category in surface_categories_order:
    surface_distribution = grouped_counts_sorted.loc[surface_category].sort_values()
    plt.figure(figsize=(10, 6))
    surface_distribution.plot(kind='bar', color='skyblue')
    plt.title(f'Distribution of Home Surface Types in Top Thirty Cities ({surface_category})')
    plt.xlabel('City')
    plt.ylabel('Number of Homes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'distribution_surface_{surface_category}.png')  # Save each plot with a unique filename
    plt.close()  # Close the plot to release memory

# Combine all saved plots into one image
import glob
import cv2

# Get all saved plot filenames
plot_filenames = glob.glob('distribution_surface_*.png')

# Combine plots into one image horizontally
images = [cv2.imread(filename) for filename in plot_filenames]
combined_image = cv2.hconcat(images)

# Save the combined image
cv2.imwrite('combined_distribution_surface_types.png', combined_image)
