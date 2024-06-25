import csv
import os
from datetime import datetime, timedelta

# Define the CSV file name
csv_file = 'seasons_temp.csv'

# Function to generate date range for Winter
def generate_winter_date_range(year):
    base_month = 12  # December
    base_day = 1

    # Calculate the start and end dates based on the time period definition
    start_date = datetime(year, base_month, base_day).strftime('%m/%d/%Y')
    end_date = datetime(year + 1, 3, 1) - timedelta(days=1)  # End of February of the following year
    end_date_str = end_date.strftime('%m/%d/%Y')

    # Format the date range
    date_range = f"{start_date}-{end_date_str}"

    # Generate different input formats
    year_str = f"{year % 100:02}"  # Ensure two-digit year with leading zero if necessary
    input_formats = [
        f"Winter '{year_str}",
        f"Winter {year_str}",
        f"Winter {year}",
        f"{year} Winter"
    ]

    return [(input_str, date_range) for input_str in input_formats]

# Function to generate date range for Spring
def generate_spring_date_range(year):
    base_month = 3  # March
    base_day = 1

    # Calculate the start and end dates based on the time period definition
    start_date = datetime(year, base_month, base_day).strftime('%m/%d/%Y')
    end_date = datetime(year, 6, 1) - timedelta(days=1)  # End of May
    end_date_str = end_date.strftime('%m/%d/%Y')

    # Format the date range
    date_range = f"{start_date}-{end_date_str}"

    # Generate different input formats
    year_str = f"{year % 100:02}"  # Ensure two-digit year with leading zero if necessary
    input_formats = [
        f"Spring '{year_str}",
        f"Spring {year_str}",
        f"Spring {year}",
        f"{year} Spring"
    ]

    return [(input_str, date_range) for input_str in input_formats]

# Function to generate date range for Summer
def generate_summer_date_range(year):
    base_month = 6  # June
    base_day = 1

    # Calculate the start and end dates based on the time period definition
    start_date = datetime(year, base_month, base_day).strftime('%m/%d/%Y')
    end_date = datetime(year, 9, 1) - timedelta(days=1)  # End of August
    end_date_str = end_date.strftime('%m/%d/%Y')

    # Format the date range
    date_range = f"{start_date}-{end_date_str}"

    # Generate different input formats
    year_str = f"{year % 100:02}"  # Ensure two-digit year with leading zero if necessary
    input_formats = [
        f"Summer '{year_str}",
        f"Summer {year_str}",
        f"Summer {year}",
        f"{year} Summer"
    ]

    return [(input_str, date_range) for input_str in input_formats]

# Function to generate date range for Fall
def generate_fall_date_range(year):
    base_month = 9  # September
    base_day = 1

    # Calculate the start and end dates based on the time period definition
    start_date = datetime(year, base_month, base_day).strftime('%m/%d/%Y')
    end_date = datetime(year, 12, 1) - timedelta(days=1)  # End of November
    end_date_str = end_date.strftime('%m/%d/%Y')

    # Format the date range
    date_range = f"{start_date}-{end_date_str}"

    # Generate different input formats
    year_str = f"{year % 100:02}"  # Ensure two-digit year with leading zero if necessary
    input_formats = [
        f"Fall '{year_str}",
        f"Fall {year_str}",
        f"Fall {year}",
        f"{year} Fall"
    ]

    return [(input_str, date_range) for input_str in input_formats]

# Function to generate date range for Monsoon
def generate_monsoon_date_range(year):
    base_month = 6  # June
    base_day = 1

    # Calculate the start and end dates based on the time period definition
    start_date = datetime(year, base_month, base_day).strftime('%m/%d/%Y')
    end_date = datetime(year, 9, 30)  # End of September
    end_date_str = end_date.strftime('%m/%d/%Y')

    # Format the date range
    date_range = f"{start_date}-{end_date_str}"

    # Generate different input formats
    year_str = f"{year % 100:02}"  # Ensure two-digit year with leading zero if necessary
    input_formats = [
        f"Monsoon '{year_str}",
        f"Monsoon {year_str}",
        f"Monsoon {year}",
        f"{year} Monsoon"
    ]

    return [(input_str, date_range) for input_str in input_formats]

# Function to generate date range pairs for various seasons
def generate_date_range_pairs():
    pairs = []

    # Generate date ranges for Winter, Spring, Summer, Fall, and Monsoon
    for year in range(2001, 2051):  # Years from 2001 to 2050
        winter_pairs = generate_winter_date_range(year)
        spring_pairs = generate_spring_date_range(year)
        summer_pairs = generate_summer_date_range(year)
        fall_pairs = generate_fall_date_range(year)
        monsoon_pairs = generate_monsoon_date_range(year)
        
        pairs.extend(winter_pairs)
        pairs.extend(spring_pairs)
        pairs.extend(summer_pairs)
        pairs.extend(fall_pairs)
        pairs.extend(monsoon_pairs)

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
