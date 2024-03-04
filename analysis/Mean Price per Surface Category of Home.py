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

# Group by surface category and calculate mean price
price_per_surface_category = df.groupby('Surface Category')['price_main'].mean()
print(price_per_surface_category)

# Plot the bar plot
plt.figure(figsize=(10, 6))
price_per_surface_category.plot(kind='bar', color='skyblue')
plt.title('Mean Price per Surface Category of Home')
plt.xlabel('Surface Category')
plt.ylabel('Mean Price')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()
