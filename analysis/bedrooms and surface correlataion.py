import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

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

# Apply categorization to create a new column
df['Surface Category'] = df['surface'].apply(categorize_surface)

# Specify the desired order of surface categories
surface_category_order = [
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

# Group by Surface Category and calculate the mean number of bedrooms
grouped_means = df.groupby('Surface Category')['bedrooms'].mean().reindex(surface_category_order)

# Plot a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=grouped_means.index, y=grouped_means.values, palette='viridis')
plt.title('Average Number of Bedrooms per Surface Category')
plt.xlabel('Surface Category')
plt.ylabel('Average Number of Bedrooms')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
