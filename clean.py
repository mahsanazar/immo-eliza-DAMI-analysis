import pandas as pd
import os
import numpy as np 
from datetime import datetime
import re
import shutil # Import shutil module for file operations

# Define the path to the raw dataset
raw_data_path = 'data/raw/row_immoweb_data0403.csv' 

# Define the path to the clean dataset folder
clean_data_folder = 'data/cleaned/'

# Ensure the cleaned data folder exists
if not os.path.exists(clean_data_folder):
    os.makedirs(clean_data_folder)

# Current timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# Full path to the new file with timestamp
clean_data_path = os.path.join(clean_data_folder, f'row_data_20240304_cleaned_{timestamp}.csv')

# Define the final clean data file path
final_clean_data = 'final_clean/row_data_20240304_clean.csv'

# Define the function for loading the dataset
def load_dataset(file_path):
    # Load dataset into DataFrame
    df = pd.read_csv(file_path, encoding='latin-1') 
    return df

def clean_dataset(df):
    # Replace empty strings and strings that only contain whitespace with NaN for all columns
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # Correct the column name if there is a semicolon or unexpected character
    df.columns = df.columns.str.replace(r'[;]+$', '', regex=True)

    # Calculate the number of duplicate rows before dropping them
    duplicate_rows = df.duplicated().sum()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Drop rows with any missing values in specific columns (if these columns must not have missing values)
    cols_with_missing_values = ['id', 'locality', 'postalcode', 'price_main']
    df = df.dropna(subset=cols_with_missing_values)

    # Debugging: Check data types before conversion
    print("Data types before conversion:\n", df.dtypes)

    # Convert all columns with float type that have whole numbers to Int64
    for col in df.select_dtypes(include=['float']).columns:
        # Create a mask for all non-NaN entries that have only one digit after the decimal point, which is '0'
        mask = df[col].notna() & (df[col] % 1 == 0)
        # Apply the mask and convert to Int64
        df.loc[mask, col] = df.loc[mask, col].astype('Int64')

        # Remove '.0' suffix from numbers in all numeric columns
        if df[col].dtype == 'float64':
            df[col] = df[col].apply(lambda x: re.sub(r'\.0$', '', str(x)) if pd.notnull(x) else x)

    # Debugging: Check data types after conversion
    print("Data types after conversion:\n", df.dtypes)

    # Convert boolean columns to 0 and 1
    boolean_columns = [col for col in df.columns if df[col].dtype == bool]
    for col in boolean_columns:
        df[col] = df[col].astype(int)

    # Remove leading and trailing spaces from string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Replace empty strings resulted from stripping with NaN for string columns
    string_columns = df.select_dtypes(include=['object']).columns
    df[string_columns] = df[string_columns].replace(r'^\s*$', np.nan, regex=True)

    # Check each column and replace empty values with NaN
    for col in df.columns:
        # If column is numeric, replace non-existent values with NaN
        if df[col].dtype == 'float64' or df[col].dtype == 'int64':
            df[col] = df[col].replace(0, np.nan)
        # If column is not numeric (and hence is categorical), replace empty strings with NaN
        else:
            df[col] = df[col].replace('', np.nan)

    return df, duplicate_rows  # Return the DataFrame and the number of duplicate rows


# Load the raw dataset
df_raw = load_dataset(raw_data_path)

# Clean the dataset, Unpack the returned DataFrame and duplicate row count
df_cleaned, duplicate_rows = clean_dataset(df_raw)  

# Save the cleaned dataset with a timestamp to create a new file each run
df_cleaned.to_csv(clean_data_path, index=False, na_rep='nan')

# Debugging: Print a sample of the DataFrame after conversion
print("Sample data after conversion:\n", df_cleaned.head())

# Output the path to confirm where the cleaned CSV has been saved
print(f"Cleaned data saved to: {clean_data_path}")

# Print a summary of NaN counts per column right after cleaning
print(df_cleaned.isna().sum())

# Print the number of duplicate rows
print(f"Duplicate rows: {duplicate_rows}")

# Copy the latest cleaned dataset to the final clean data file path
shutil.copy(clean_data_path, final_clean_data)
