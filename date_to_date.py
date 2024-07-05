import csv
import os
from datetime import datetime, timedelta

# Define the CSV file name
csv_file = 'csv/dates_to_dates.csv'

import random
from datetime import datetime, timedelta

def generate_random_date_pairs(sample_size=300000):
    pairs = []
    start_year = 2000
    end_year = 2050
    total_days = (datetime(end_year + 1, 1, 1) - datetime(start_year, 1, 1)).days
    
    formats_without_year = [
        # '{month}/{day}',
        # '{month:02d}/{day}',
        '{month}/{day:02d}',
        '{month:02d}/{day:02d}',
        '{short_month} {day}',  # Jan 1
        '{full_month} {day}',   # January 1
    ]
    
    formats_with_year = [
        # '{month}/{day}/{year:02d}',
        # '{month:02d}/{day}/{year:02d}',
        '{month:02d}/{day:02d}/{year:02d}',
        '{month:02d}/{day:02d}/{year:02d}',
        '{short_month} {day} {full_year}',   # Jan 1 2000
        '{full_year} {short_month} {day}',   # 2000 Jan 1
    ]
    
    for _ in range(sample_size):
        random_day = datetime(start_year, 1, 1) + timedelta(days=random.randint(0, total_days - 1))
        day = random_day.day
        month = random_day.month
        year = random_day.year % 100  # Last two digits of the year
        full_year = random_day.year
        short_month = random_day.strftime('%b')
        full_month = random_day.strftime('%B')
        
        standard_date = random_day.strftime('%m/%d')
        standard_date_with_year = random_day.strftime('%m/%d/%y')
        
        chosen_format_without_year = random.choice(formats_without_year)
        chosen_format_with_year = random.choice(formats_with_year)
        
        formatted_date_without_year = chosen_format_without_year.format(
            month=month, day=day, short_month=short_month, full_month=full_month
        )
        formatted_date_with_year = chosen_format_with_year.format(
            month=month, day=day, year=year, full_year=full_year, short_month=short_month
        )
        
        if random.randint(0,1) == 1:
            # Add pairs without year
            pairs.append((formatted_date_without_year, standard_date))
            
            # Add pairs with year
            pairs.append((formatted_date_with_year, standard_date_with_year))
        else:
            pairs.append((standard_date, formatted_date_without_year))
            pairs.append((standard_date_with_year,formatted_date_with_year))
    
    return pairs

# Generate the pairs
date_pairs = generate_random_date_pairs()

# Open the CSV file in append mode
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Value', 'Computed'])
    # Write the pairs
    writer.writerows(date_pairs)

print(f"Added {len(date_pairs)} pairs to {csv_file}")
