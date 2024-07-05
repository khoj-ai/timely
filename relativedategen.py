import random
from datetime import date, timedelta, datetime
import re
import csv

# Function to generate a random date between 2000-01-01 and 2050-12-31
def random_dategen():
    start_date = date(2000, 1, 1)
    end_date = date(2050, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

# Function to calculate last day of the month
def last_day_of_month(year, month):
    # Calculate next month and year
    next_month = month % 12 + 1
    next_year = year + (1 if next_month == 1 else 0)
    # Find the last day of the current month
    last_day = (datetime(next_year, next_month, 1) - timedelta(days=1)).strftime("%m/%d/%y")
    return last_day

# Regular expression to match dates in format MM/DD/YY
date_pattern = r'(\d{2})/(\d{2})/(\d{2})'

# Function to replace the date with last day of the month
def adjust_date(match):
    month = int(match.group(1))
    day = int(match.group(2))
    year = int(match.group(3))
    
    # Determine the full year from the two-digit year
    if year >= 40:
        full_year = year + 1900
    else:
        full_year = year + 2000
    
    last_day = last_day_of_month(full_year, month)
    return last_day

def get_last_day_of_month(start_date):
  """Finds the last day of the month for a given start date.

  Args:
      start_date: A datetime.date object representing any date within the month.

  Returns:
      A datetime.date object representing the last day of the month.
  """

  # Check if it's December, then handle it as a special case.
  if start_date.month == 12:
    return start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
  else:
    # For other months, use the previous approach.
    first_day_next_month = start_date.replace(month=start_date.month + 1, day=1)
    last_day_of_month = first_day_next_month - timedelta(days=1)
    return last_day_of_month

# Function to generate a random string in the specified format
def random_date_string(current_date):
    # Generate random timedelta in days, months or years
    time_units = ['days', 'months', 'years']
    time_unit = random.choice(time_units)
    if time_unit == 'days':
        max_days = min(30, (current_date - date(current_date.year, 1, 1)).days + 1)  # Maximum 30 days
        if max_days <= 1:
            random_value = 1  # If max_days is 0 or 1, set random_value to 1
        else:
            random_value = random.randint(1, max_days)  # up to 30 days
        start_date = current_date - timedelta(days=random_value)
        end_date = start_date
    elif time_unit == 'months':
        max_months = min(12, (current_date.year - 2000) * 12 + current_date.month - 1)  # Maximum 12 months (1 year)
        if max_months <= 1:
            random_value = 1  # If max_months is 0 or 1, set random_value to 1
        else:
            random_value = random.randint(1, max_months)  # up to 12 months

        months_to_subtract = random_value
        years_to_subtract = 0

        new_month = current_date.month - months_to_subtract
        new_year = current_date.year - years_to_subtract

        if new_month <= 0:
            # Calculate how many years to subtract
            years_to_subtract = abs(new_month) // 12 + 1
            new_year -= years_to_subtract
            new_month += years_to_subtract * 12

        start_date = current_date.replace(year=new_year, month=new_month, day=1)

        # Calculate end_date
        if current_date.month == 1:
            end_year = start_date.year - 1
            end_month = 12
            # Find the last day of the previous month
            end_day = (date(current_date.year, current_date.month, 1) - timedelta(days=1)).day
        else:
            end_year = start_date.year
            end_month = start_date.month - 1
            if end_month == 0:
                end_month = 12
                end_year -= 1
            end_day = min(start_date.day, (date(current_date.year, current_date.month - 1, 1) - timedelta(days=1)).day)

        end_date = date(end_year, end_month, end_day)
    else:  # years
        random_value = random.randint(1, 50)  # up to 50 years
        start_date = current_date.replace(year=current_date.year - random_value, month=1, day=1)
        # end_date = start_date.replace(year=start_date.year, day=31, month=12)
        end_date = current_date.replace(year=current_date.year - random_value, month=12, day=31)
    if time_unit != 'days' and time_unit != 'years':    
        end_date = get_last_day_of_month(start_date)
    # Format the dates
    start_date_str = start_date.strftime("%m/%d/%y")
    end_date_str = end_date.strftime("%m/%d/%y")
    
    # Generate the final string
    time_string = f"{random_value} {time_unit} ago,{start_date_str}-{end_date_str}"
    
    return time_string

# Main script to write CSV with modified dates
with open('csv/relatives_dates_updated.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Value', 'Computed'])

    for i in range(10000):
        # Get current date
        current_date = random_dategen()

        # Generate a random string
        random_string = random_date_string(current_date)
        entry = random_string.split(',')

        if "months ago" in entry[0]:
            # Adjust end date if month goes below January and subtract year by 1
            end_date_parts = entry[1].split('-')
            end_date_parts[1] = re.sub(date_pattern, adjust_date, end_date_parts[1])
            end_date_month, end_date_day, end_date_year = end_date_parts[1].split('/')

            if int(end_date_month) < 1:
                end_date_month = 12
                end_date_year = str(int(end_date_year) - 1)

            end_date_parts[1] = f"{end_date_month:02}/{end_date_day}/{end_date_year[-2:]}"

            entry[1] = '-'.join(end_date_parts)

        # Append current date to entry[0]
        entry[0] = f"{entry[0]} current date:{current_date.strftime('%m/%d/%y')}"

        # Write the modified entry to CSV
        writer.writerow(entry)
