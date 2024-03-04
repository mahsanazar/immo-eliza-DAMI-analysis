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
    elif 100<= surface <200:
        return "100-150"
    elif 150<= surface< 250:
        return "150-200"
    elif 250<= surface< 300:
        return "250-300"
    elif 300<= surface< 350:
         return "300-350"
    elif 350<= surface<400:
         return "350-400"
    elif 450<= surface<500:
         return "450-500"
    elif 550<=surface<600:
         return "550-600"
    else:
        return "Greater than 600"

# Apply categorization to create a new column
df['Surface Category'] = df['surface'].apply(categorize_surface)

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
    elif condition ==0 :
        return "non specific"

# Apply categorization to create a new column
df['Condition Category'] = df['condition'].apply(categorize_condition)

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

# Group by Surface Category and Condition Category, then count the occurrences
grouped_counts = df.groupby(['Surface Category', 'Condition Category']).size().unstack(fill_value=0)

# Reindex the DataFrame based on the desired order of surface categories
grouped_counts = grouped_counts.reindex(surface_category_order)

# Plot a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(grouped_counts, annot=True, fmt='d', cmap="YlGnBu")
plt.title('Counts of Condition Categories for Each Surface Category')
plt.xlabel('Condition Category')
plt.ylabel('Surface Category')
plt.tight_layout()
plt.show()
