import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Group by locality (city) and count the number of homes for each city
homes_per_city = df['locality'].value_counts()
print(homes_per_city)

# Sort cities by the number of homes in descending order and select the top ten cities
top_ten_cities = homes_per_city.sort_values(ascending=False).head(30)

# Plot the bar chart
plt.figure(figsize=(12, 8))
ax = top_ten_cities.plot(kind='bar', color='skyblue')

plt.title('Top Ten Cities with Most Number of Homes for Sale')
plt.xlabel('City')
plt.ylabel('Number of Homes')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels and align them to the right
plt.grid(True)
plt.tight_layout()

# Annotate the bars with the number of homes
for i, (city, num_homes) in enumerate(top_ten_cities.items()):
    ax.annotate(f"{num_homes}", (i, num_homes), textcoords="offset points", xytext=(0,10), ha='center')

plt.show()
