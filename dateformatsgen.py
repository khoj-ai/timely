import csv
import os
from datetime import datetime, timedelta

# Define the CSV file name
csv_file = 'datestemp.csv'

# Function to generate date pairs
def generate_date_pairs():
    pairs = []
    for year in range(2000, 2051):  # Years from 2000 to 2050
        start_date = datetime(year, 1, 1)  # Starting from Jan 1, 2024 for this example

        for i in range(366):  # Assuming a leap year to cover all dates
            current_date = start_date + timedelta(days=i)
            day = current_date.day
            month = current_date.month
            year = current_date.year % 100  # Last two digits of the year

            standard_date = current_date.strftime('%m/%d')
            standard_date_with_year = current_date.strftime('%m/%d/%y')

            formats_without_year = [
                f"{month}/{day}",
                f"{month:02d}/{day}",
                f"{month}/{day:02d}",
                f"{month:02d}/{day:02d}",
                current_date.strftime('%b %d').replace(" 0", " "),  # Jan 1
                current_date.strftime('%B %d').replace(" 0", " "),  # January 1
            ]

            formats_with_year = [
                f"{month}/{day}/{year:02d}",
                f"{month:02d}/{day}/{year:02d}",
                f"{month}/{day:02d}/{year:02d}",
                f"{month:02d}/{day:02d}/{year:02d}",
            ]

            # Add pairs without year
            for fmt in formats_without_year:
                pairs.append((fmt, standard_date+"/xx-"+standard_date+"/xx"))

            # Add pairs with year
            for fmt in formats_with_year:
                pairs.append((fmt, standard_date_with_year+"-"+standard_date_with_year))

    return pairs

# Generate the pairs
date_pairs = generate_date_pairs()

# Check if the file exists
file_exists = os.path.isfile(csv_file)

# Open the CSV file in append mode
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # If the file doesn't exist, write the header
    if not file_exists:
        writer.writerow(['Value', 'Computed'])
    
    # Write the pairs
    writer.writerows(date_pairs)

print(f"Added {len(date_pairs)} pairs to {csv_file}")
