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
    
    # Initialize variables
    start_date = None
    end_date = None
    year = current_date_obj.year
    
    # Option for weeks
    if option == "last week":
        # Find the most recent Sunday
        most_recent_sunday = current_date_obj - timedelta(days=current_date_obj.weekday() + 1)
        # Last week's start date is the Sunday 7 days before the most recent Sunday
        start_date = most_recent_sunday - timedelta(days=7)
        # Last week's end date is the Saturday before the most recent Sunday
        end_date = most_recent_sunday - timedelta(days=1)
    elif option == "this week":
        # Find the most recent Sunday
        most_recent_sunday = current_date_obj - timedelta(days=current_date_obj.weekday() + 1)
        # This week's start date is the Sunday
        start_date = most_recent_sunday
        # This week's end date is current day
        end_date = current_date_obj
    elif option == "this month":
        # Get first day of current month
        start_date = current_date_obj.replace(day=1)
        # Get last day of current month
        end_date = current_date_obj
    elif option == "last month":
        # Get last month and year
        last_month = current_date_obj.month - 1
        last_year = year
        if last_month == 0:
            last_month = 12
            last_year -= 1
        
        # Get first day of last month
        start_date = current_date_obj.replace(year=last_year, month=last_month, day=1)
        # Get last day of last month
        next_month = start_date.month % 12 + 1
        next_month_year = start_date.year + (start_date.month // 12)
        end_date = datetime(next_month_year, next_month, 1).date() - timedelta(days=1)
    
    elif option == "last year":
        last_year = year - 1
        start_date = datetime(last_year, 1, 1).date()
        end_date = datetime(last_year, 12, 31).date()
    
    elif option == "middle of last year":
        last_year = year - 1
        start_date = datetime(last_year, 5, 1).date()
        end_date = datetime(last_year, 8, 31).date()
    
    elif option in ["beginning of last year", "early of last year", "start of last year", "early last year"]:
        last_year = year - 1
        start_date = datetime(last_year, 1, 1).date()
        end_date = datetime(last_year, 4, 30).date()
    
    elif option in ["end of last year", "late last year", "last of last year", "end last year", "late of last year"]:
        last_year = year - 1
        start_date = datetime(last_year, 9, 1).date()
        end_date = datetime(last_year, 12, 31).date()
    elif option == "last winter":
        #change winter to Winter if random swap
        if random.randint(0, 1) == 1:
            option = option.replace("winter", "Winter")
        last_year = year - 1
        start_date = datetime(last_year, 12, 1).date()
        end_date = datetime(last_year, 2, 28).date()
    elif option == "last summer":
        if random.randint(0, 1) == 1:
            option = option.replace("summer", "Summer")
        last_year = year - 1
        start_date = datetime(last_year, 6, 1).date()
        end_date = datetime(last_year, 8, 31).date()
    elif option == "last spring":
        if random.randint(0, 1) == 1:
            option = option.replace("spring", "Spring")
        last_year = year - 1
        start_date = datetime(last_year, 3, 1).date()
        end_date = datetime(last_year, 5, 31).date()
    elif option == "last fall":
        if random.randint(0, 1) == 1:
            option = option.replace("fall", "Fall")
        last_year = year - 1
        start_date = datetime(last_year, 9, 1).date()
        end_date = datetime(last_year, 11, 30).date()
    #check if option is a day of the week
    elif option in ["last monday", "last tuesday", "last wednesday", "last thursday", "last friday", "last saturday", "last sunday"]:
        # Convert the day name to a number (0 = Monday, 6 = Sunday)
        day_to_num = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
                    "friday": 4, "saturday": 5, "sunday": 6}
        target_day = option.split(" ")[-1]
        target_day_num = day_to_num[target_day]
        
        # Calculate the number of days to go back
        days_back = (current_date_obj.weekday() - target_day_num) % 7
        if days_back == 0:
            days_back = 7  # If it's the same day, we want last week's occurrence
        
        # Calculate the date of the last occurrence of the target day
        result_date = current_date_obj - timedelta(days=days_back)
        
        # Return formatted string
        return f"{option} current date:{current_date_obj.strftime('%m/%d/%Y')},{result_date.strftime('%m/%d/%Y')}-{result_date.strftime('%m/%d/%Y')}"
    else:
        # Option not recognized
        raise ValueError("Invalid option")
    
    return f"{option} current date:{current_date_obj.strftime('%m/%d/%Y')},{start_date.strftime('%m/%d/%Y')}-{end_date.strftime('%m/%d/%Y')}"
# Example usage
current_date = "12/12/2024"
option = "last year"

date_range = get_date_range(current_date, option)
print(date_range)


import random
import csv
with open('csv/lastx_updated.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Value', 'Computed'])
    options = [ "last month", 
                "last year", 
                "middle of last year",
                "beginning of last year", 
                "end of last year", 
                "start of last year", 
                "early last year", 
                "last week", 
                "this week", 
                "this month",
                "last winter",
                "last summer",
                "last spring",
                "last fall",
                "last monday",
                "last tuesday",
                "last wednesday",
                "last thursday",
                "last friday",
                "last saturday",
                "last sunday", ]
    i = 0
    while i < 10000:
        year = random.randint(2001, 2099)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        current_date = f"{month}/{day}/{year}"
        option = random.choice(options)
        date_range = get_date_range(current_date, option)
        if date_range == "":
            continue
        gen = random.randint(0, 3)
        #skip last thursday.... type queries every once in a while (any day of the week)
        if option in ["last monday", "last tuesday", "last wednesday", "last thursday", "last friday", "last saturday", "last sunday"]:
            if gen < 2:
                continue
        if "last year" in option and option != "last year" and gen == 1:
            option = option.replace("last year", str(year - 1))
            writer.writerow([f"{option}", date_range.split(",")[1]])
            i += 1
        else:
            writer.writerow([f"{option} today:{current_date}", date_range.split(",")[1]])
            i += 1

