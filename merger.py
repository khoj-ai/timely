import os
import glob
import pandas as pd

# Directory where the CSV files are located
input_dir = 'csv'

# Output CSV file path
output_file = 'csv/bulk.csv'

# Search for all CSV files in the input directory
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# List to store all the dataframes from individual CSVs
dfs = []

# Iterate over each CSV file
for csv_file in csv_files:
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # Append DataFrame to the list
    dfs.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dfs, ignore_index=True)

# Write the combined DataFrame to a single CSV file
combined_df.to_csv(output_file, index=False)

print(f'Combined CSV file saved to: {output_file}')
