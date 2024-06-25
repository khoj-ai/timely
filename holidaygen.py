
from datetime import date, datetime, timedelta 
import holidays 
import csv

def daterange(month, day, year):
    # Create a datetime object for the given date
    date = datetime(year, month, day)
    
    # Calculate the start and end dates of the 14-day interval
    start_date = date - timedelta(days=10)  # 7 days before
    end_date = date + timedelta(days=10)    # 7 days after
    
    # Format the dates into the required string format
    interval_str = f"{start_date.month}/{start_date.day}/{start_date.year}-{end_date.month}/{end_date.day}/{end_date.year}"
    
    return interval_str

#holidays.csv 
with open('holidays.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Description', 'Raw Date'])
  
for year in range(2000, 2040):
    for ptr in holidays.UnitedStates(years = year).items(): 
        year = ptr[0].year
        month = ptr[0].month
        day = ptr[0].day
        description = ptr[1]
        # Christmas 2024, 2024 Christmas, Christmas '24, '24 Christmas -> 12/15/2024-12/31/2024
        # make these 4 types of date formats 
        if "observed" in description:
            continue
        if description == "Christmas Day":
            date_range = daterange(month, day, year)
            input_formats = [
                f"Christmas {year}",
                f"{year} Christmas",
                f"Christmas '{year % 100:02}",
                f"'{year % 100:02} Christmas"
            ]
            with open('holidays.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                for input_str in input_formats:
                    writer.writerow([input_str, date_range])
        # Thanksgiving 2024, 2024 Thanksgiving, Thanksgiving '24, '24 Thanksgiving -> 11/01/2024-11/30/2024
        # make these 4 types of date formats 
        elif description == "Thanksgiving":
            date_range = daterange(month, day, year)
            input_formats = [
                f"Thanksgiving {year}",
                f"{year} Thanksgiving",
                f"Thanksgiving '{year % 100:02}",
                f"'{year % 100:02} Thanksgiving"
            ]
            with open('holidays.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                for input_str in input_formats:
                    writer.writerow([input_str, date_range])
        #  New Year's Day 2024, 2024 New Year's Day, New Year's Day '24, '24 New Year's Day -> 01/01/2024-01/01/2024
        # make these 4 types of date formats 
        elif description == "New Year's Day":
            date_range = daterange(month, day, year)
            input_formats = [
                f"New Year's Day {year}",
                f"{year} New Year's Day",
                f"New Year's Day '{year % 100:02}",
                f"'{year % 100:02} New Year's Day",
                f"New Year's {year}",
                f"{year} New Year's",
                f"New Year's '{year % 100:02}'",
                f"'{year % 100:02} New Year's",
                f"New Years {year}",
                f"{year} New Years",
                f"New Years '{year % 100:02}",
                f"'{year % 100:02} New Years",
            ]
            with open('holidays.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                for input_str in input_formats:
                    writer.writerow([input_str, date_range])
        else:
            date_range = daterange(month, day, year)
            with open('holidays.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([description, date_range])


        
