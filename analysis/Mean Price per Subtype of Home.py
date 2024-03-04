import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np

pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x))

# Specify the file paths
input_excel_file_path = r"C:\Users\afshi\Documents\GitHub\immo-eliza-DAMI-analysis\data\cleaned\version 3 data.xlsx"
try:
    df = pd.read_excel(input_excel_file_path)
    #print(df)
except Exception as e:
    print("Error:", e)
price_per_subtype = df.groupby('subtype')['price_main'].mean()

# Plot the bar plot
plt.figure(figsize=(10, 6))
plt.bar(price_per_subtype.index.astype(str), price_per_subtype.values, color='skyblue')

plt.title('Mean Price per Subtype of Home')
plt.xlabel('Subtype of Home')
plt.ylabel('Mean Price')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
# Set y-tick labels to price_per_subtype values
#plt.yticks(price_per_subtype.values, price_per_subtype.values)
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()