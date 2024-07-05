from datetime import datetime, timedelta
import holidays
import csv
import random

def daterange(month, day, year):
    # Create a datetime object for the given date
    date = datetime(year, month, day)
    
    # Calculate the start and end dates of the 14-day interval
    start_date = date - timedelta(days=10)  # 10 days before
    end_date = date + timedelta(days=10)    # 10 days after
    
    # Format the dates into the required string format
    interval_str = f"{start_date.month}/{start_date.day}/{start_date.year}-{end_date.month}/{end_date.day}/{end_date.year}"
    
    return interval_str

# Define possible date formats for specific holidays
date_formats = {
    "Christmas Day": [
        "{year} Christmas",
        "Christmas {year}",
        "Christmas '{year_short}",
        "'{year_short} Christmas"
    ],
    "Thanksgiving": [
        "{year} Thanksgiving",
        "Thanksgiving {year}",
        "Thanksgiving '{year_short}",
        "'{year_short} Thanksgiving"
    ],
    "New Year's Day": [
        "{year} New Year's Day",
        "New Year's Day {year}",
        "New Year's Day '{year_short}",
        "'{year_short} New Year's Day",
        "{year} New Year's",
        "New Year's {year}",
        "New Year's '{year_short}",
        "'{year_short} New Year's",
        "{year} New Years",
        "New Years {year}",
        "New Years '{year_short}",
        "'{year_short} New Years"
    ]
}

# Generate a list of all holidays
all_holidays = []
for year in range(2000, 2040):
    us_holidays = holidays.UnitedStates(years=year)
    for date, description in us_holidays.items():
        if "observed" not in description:
            all_holidays.append((date, description))

# Randomly sample holidays
sample_size = 1000  # Adjust this number to your needs
sampled_holidays = random.sample(all_holidays, min(sample_size, len(all_holidays)))

# Write to CSV
with open('csv/holidays_updated.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Description', 'Raw Date'])
    
    for holiday_date, description in sampled_holidays:
        year = holiday_date.year
        year_short = holiday_date.year % 100
        month = holiday_date.month
        day = holiday_date.day
        date_range = daterange(month, day, year)
        
        if description in date_formats:
            chosen_format = random.choice(date_formats[description])
            input_str = chosen_format.format(year=year, year_short=year_short)
        else:
            input_str = f"{year} {description}"
        
        writer.writerow([input_str, date_range])
