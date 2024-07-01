import csv
import os
from datetime import datetime, timedelta

# Define the CSV file name
csv_file = 'date_ranges.csv'

# Function to generate date range pairs
def generate_date_range_pairs():
    pairs = []

    # Define month abbreviations and their corresponding numbers
    months = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    months_extended = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Iterate over each month and year directly
    for year in range(2000, 2051):  # Years from 2000 to 2050
        for month_str, month_num in months.items():
            # Calculate the start and end dates of the month
            start_date = datetime(year, month_num, 1).strftime('%m/%d/%Y')
            
            if month_num == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month_num + 1, 1) - timedelta(days=1)
            
            end_date_str = end_date.strftime('%m/%d/%Y')

            # Generate different input formats
            input_formats = [
                f"{month_str} '{str(year%100).rjust(2, '0')}",
                f"{month_str} of {year}",          # Jan of 2024
                f"{month_str} {year}",             # Jan 2024
                f"{year} {month_str}",             # 2024 Jan
                f"{month_str} {year}"              # January 2024
            ]

            # Append each input format to pairs
            for input_str in input_formats:
                pairs.append((input_str, f"{start_date}-{end_date_str}"))
        for month_str, month_num in months_extended.items():
            # Calculate the start and end dates of the month
            start_date = datetime(year, month_num, 1).strftime('%m/%d/%Y')
            
            if month_num == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month_num + 1, 1) - timedelta(days=1)
            
            end_date_str = end_date.strftime('%m/%d/%Y')

            # Generate different input formats
            input_formats = [
                f"{month_str} '{str(year%100).rjust(2, '0')}",
                f"{month_str} of {year}",          # Jan of 2024
                f"{month_str} {year}",             # Jan 2024
                f"{year} {month_str}",             # 2024 Jan
                f"{month_str} {year}"              # January 2024
            ]

            # Append each input format to pairs
            for input_str in input_formats:
                pairs.append((input_str, f"{start_date}-{end_date_str}"))

    return pairs

# Generate the pairs
date_range_pairs = generate_date_range_pairs()

# Check if the file exists
file_exists = os.path.isfile(csv_file)

# Open the CSV file in append mode
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # If the file doesn't exist, write the header
    if not file_exists:
        writer.writerow(['Value', 'Computed'])
    
    # Write the pairs
    writer.writerows(date_range_pairs)

print(f"Added {len(date_range_pairs)} pairs to {csv_file}")
