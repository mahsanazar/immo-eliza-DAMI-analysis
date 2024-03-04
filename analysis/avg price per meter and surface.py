import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\cleanedexcel_immo_77k.xlsx"
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
#print(df['Surface Category'])

# Calculate price per meter
df['Price per Meter'] = df['price_main'] / df['surface']

# Group by surface category and calculate mean price per meter
price_per_meter_category = df.groupby('Surface Category')['Price per Meter'].mean()

# Calculate counts per surface category
counts_per_category = df['Surface Category'].value_counts()

# Define the desired order of categories
desired_order = [
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

# Reindex the DataFrame based on the desired order
price_per_meter_category = price_per_meter_category.reindex(desired_order)
counts_per_category = counts_per_category.reindex(desired_order)

# Plot the bar plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot mean price per meter
price_per_meter_category.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_ylabel('Mean Price per Meter', color='skyblue')

# Create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()
counts_per_category.plot(kind='bar', color='orange', alpha=0.5, ax=ax2)  # Plot counts
ax2.set_ylabel('Counts', color='orange')

plt.title('Mean Price per Meter and Counts per Surface Category of Home')
plt.xlabel('Surface Category')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()
