from datetime import date, datetime, timedelta

def get_date_range(current_date, option):
  """
  This function takes the current date and an option ("last month" or "last year")
  and returns a formatted string with the date range for that option.
  """

  # Handle different date formats using datetime.strptime
  try:
    current_date_obj = datetime.strptime(current_date, "%m/%d/%Y").date()
  except ValueError:
    raise ValueError("Invalid date format. Please use MM/DD/YYYY.")

  # Calculate year based on parsed date object
  year = current_date_obj.year

  if option == "last month":
    # Get last month and year
    last_month = current_date_obj.month - 1
    last_year = year
    if last_month == 0:
      last_month = 12
      last_year -= 1

    # Get first day of last month
    start_date = current_date_obj.replace(month=last_month, day=1)

    # Get last day of last month (using timedelta)
    end_date = start_date + timedelta(days = 25)  # Subtract 1 day for last day

  elif option == "last year":
    last_year = year - 1
    start_date = current_date_obj.replace(year=last_year, day=1, month=1)
    end_date = current_date_obj.replace(year=last_year, day=31, month=12)  # Last day of last year
  elif option == "middle of last year":
    last_year = year - 1
    start_date = current_date_obj.replace(year=last_year, day=1, month=5)
    end_date = current_date_obj.replace(year=last_year, day=31, month=8)
  elif option == "beginning of last year":
    last_year = year - 1
    start_date = current_date_obj.replace(year=last_year, day=1, month=1)
    end_date = current_date_obj.replace(year=last_year, day=30, month=4)
  elif option == "end of last year":
    last_year = year - 1
    start_date = current_date_obj.replace(year=last_year, day=1, month=9)
    end_date = current_date_obj.replace(year=last_year, day=31, month=12)
  else:
    raise ValueError("Invalid option. Choose 'last month' or 'last year'.")

  return f"{option} current date:{current_date_obj.strftime('%m/%d/%y')},{start_date.strftime('%m/%d/%y')}-{end_date.strftime('%m/%d/%y')}"

# Example usage
current_date = "12/12/2024"
option = "last year"

date_range = get_date_range(current_date, option)
print(date_range)


import random
import csv
with open('lastx.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Value', 'Computed'])
    for i in range(1200):
        year = random.randint(2000, 2050)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        current_date = f"{month}/{day}/{year}"
        option = random.choice(["last month", "last year", "middle of last year", "beginning of last year", "end of last year"])
        date_range = get_date_range(current_date, option)
        gen = random.randint(0, 3)
        if "last year" in option and option != "last year" and gen == 1:
            option = option.replace("last year", str(year - 1))
            writer.writerow([f"{option}", date_range.split(",")[1]])
        else:
            writer.writerow([f"{option} current date: {current_date}", date_range.split(",")[1]])

