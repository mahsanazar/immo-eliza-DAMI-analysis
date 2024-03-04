import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the Excel file
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\cleanedexcel_immo_77k.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
except Exception as e:
    print("Error:", e)

# Group by locality and calculate mean price per meter
mean_price_per_meter_locality = df.groupby('locality')['price_main'].mean()

# Sort localities based on mean price per meter in descending order
sorted_localities = mean_price_per_meter_locality.sort_values(ascending=False)

# Get the first ten most expensive localities
first_ten_expensive_localities = sorted_localities.head(10)

# Plot the bar chart
plt.figure(figsize=(10, 6))
bar_plot = first_ten_expensive_localities.plot(kind='bar', color='skyblue')
plt.title('Top 10 Most Expensive homes')
plt.xlabel('Locality')
plt.ylabel('Mean Price ')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels and align them to the right
plt.grid(True)

# Annotate each bar with its corresponding value
for i, v in enumerate(first_ten_expensive_localities):
    plt.text(i, v + 100, f'{v:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()
