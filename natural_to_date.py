import csv
from datetime import datetime
from datasets import load_dataset
import random
import time
random.seed(time.time())

def get_dates(date_str):
    """
    This function takes a date string in the format "MM/DD/YYYY"
    and returns a datetime object.
    """
    date_range = date_str.split("-")
    
    if len(date_range) != 2:
        raise ValueError("Input date string is not in the correct format 'MM/DD/YYYY-MM/DD/YYYY' or 'MM/DD/YY-MM/DD/YY'")
    
    date1_str = date_range[0].strip()
    date2_str = date_range[1].strip()
    
    # Check the length of the year part to determine the format
    year_length = len(date1_str.split("/")[-1])
    
    if year_length == 2:
        date_format = '%m/%d/%y'
    elif year_length == 4:
        date_format = '%m/%d/%Y'
    else:
        raise ValueError("Year part of the date is not in a recognized format")
    
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    
    return date1, date2

from functools import lru_cache

@lru_cache(maxsize=None)
def scorer(date):
    #get month day and year from date time object
    month = date.month
    day = date.day
    year = date.year
    #month, day, year = map(int, date.split('/'))
    if year < 100:  # Assuming two-digit years are 2000s
        year += 2000
    score = year * 10000 + month * 100 + day * 1
    return score

def is_similar(start_date1, end_date1, start_date2, end_date2):
    if abs(start_date1.year-start_date2.year) > 2:
        return False
    # Check for overlap directly using datetime comparisons
    return (start_date2 <= start_date1 <= end_date2) or (start_date2 <= end_date1 <= end_date2)


# Load data from CSV files into dictionaries
def load_data(file_path, data_dict):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if "Computed" in row or "xx" in row[1]:
                continue
            data_dict[row[0]] = row[1]

def generate_hash_map(data_dict):
    hash_map = {}
    for key, date_str in data_dict.items():
        start_date, end_date = get_dates(date_str)
        hash_map[key] = (scorer(start_date), scorer(end_date))
    return hash_map


# File paths for your CSV files
seasons_file = 'csv/seasons.csv'
dates_file = 'csv/dates_updated.csv'
lastx_file = 'csv/lastx_updated.csv'
relatives_dates_file = 'csv/relatives_dates_updated.csv'
months_file = 'csv/months.csv'

# Initialize dictionaries
season_dict = {}
dates_dict = {}
lastx_dict = {}
relativedate_dict = {}
monthsdict = {}

# Load data into dictionaries while skipping unwanted rows
load_data(seasons_file, season_dict)
load_data(dates_file, dates_dict)
load_data(lastx_file, lastx_dict)
load_data(relatives_dates_file, relativedate_dict)
load_data(months_file, monthsdict)

# Date formats to use
date_formats = ['%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y-%m-%d', '%m-%d-%Y']

#writing to file titled csv/natural_to_date.csv
file = open('csv/natural_to_date.csv', 'w', newline='')
writer = csv.writer(file, delimiter='|')
writer.writerow(['Value', 'Computed'])

rows = []
for i in range(5):
    for season_key, season_date in season_dict.items():
        season_start, season_end = get_dates(season_date)
        #generate a date between the two datetime objects
        random_date = season_start + (season_end - season_start) * random.random()
        date_format = random.choice(date_formats)
        rows.append([season_key, random_date.strftime(date_format)])

for date_key, date_str in dates_dict.items():
    start_date, end_date = get_dates(date_str)
    random_date = start_date + (end_date - start_date) * random.random()
    date_format = random.choice(date_formats)
    rows.append([date_key, random_date.strftime(date_format)])

#for i in range(3):
#print lastx size
print(len(lastx_dict), "lastx size")
for lastx_key, lastx_date in lastx_dict.items():
    lastx_start, lastx_end = get_dates(lastx_date)
    random_date = lastx_start + (lastx_end - lastx_start) * random.random()
    date_format = random.choice(date_formats)
    rows.append([lastx_key, random_date.strftime(date_format)])

print(len(relativedate_dict), "relativedate size")
for relative_key, relative_date in relativedate_dict.items():
    relative_start, relative_end = get_dates(relative_date)
    random_date = relative_start + (relative_end - relative_start) * random.random()
    date_format = random.choice(date_formats)
    rows.append([relative_key, random_date.strftime(date_format)])

#for i in range(3):
for month_key, month_date in monthsdict.items():
    month_start, month_end = get_dates(month_date)
    random_date = month_start + (month_end - month_start) * random.random()
    date_format = random.choice(date_formats)
    rows.append([month_key, random_date.strftime(date_format)])

random.shuffle(rows)
writer.writerows(rows)
print(f"wrote {len(rows)} rows to natural_to_date.csv")