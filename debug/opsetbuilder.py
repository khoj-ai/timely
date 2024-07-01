import csv
from datetime import datetime

def parse_date(date_str):
    """
    Parse date string in format 'MM/DD/YYYY' or 'MM/DD/YY' to datetime object.
    """
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return datetime.strptime(date_str, '%m/%d/%y')

def is_within_range(date, start, end):
    """
    Check if date is within the range [start, end].
    """
    return start <= date <= end

# Dictionary to store results
mega_bins = {}

# Read CSV file and process rows
with open('csv/bulk.csv') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if exists
    for row in reader:
        if "Computed" in row or "xx" in row[1]:
            continue
        
        current_id = row[0]
        date_range = row[1]
        start_date_str, end_date_str = date_range.split("-")
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        
        found = False
        
        # Check against existing mega_bins
        for key, value in mega_bins.items():
            if is_within_range(start_date, value[0], value[1]) or is_within_range(end_date, value[0], value[1]):
                mega_bins[key].append(current_id)
                found = True
                break
        
        if not found:
            # Create new entry in mega_bins
            mega_bins[current_id] = [start_date, end_date]

print(mega_bins)
