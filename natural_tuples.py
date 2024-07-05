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

# do the above but first shuffle the dictionaries
season_keys = list(season_dict.keys())
random.shuffle(season_keys)
date_keys = list(dates_dict.keys())
random.shuffle(date_keys)

# Precompute and hash scores
season_hash_map = generate_hash_map(season_dict)
date_hash_map = generate_hash_map(dates_dict)


natural_language_tuples = set()
i = 0

# Pre-filter date_keys to avoid checking for '/' in the inner loop
filtered_date_keys = [date for date in date_keys if "/" not in date]

# Create a list of start and end scores for seasons and dates
season_scores = [(season, *season_hash_map[season]) for season in season_keys]
date_scores = [(date, *date_hash_map[date]) for date in filtered_date_keys]

#repeat for lastx and seasons
lastx_keys = list(lastx_dict.keys())
random.shuffle(lastx_keys)
lastx_hash_map = generate_hash_map(lastx_dict)

#seasons and lastx
for season in season_keys:
    start_score1, end_score1 = season_hash_map[season]
    for lastx in lastx_keys:
        start_score2, end_score2 = lastx_hash_map[lastx]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((season, lastx))
            # print(season, lastx)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("Season to lastx tuples generated. Size is now", len(natural_language_tuples))

#seasons and relatives
relatives_keys = list(relativedate_dict.keys())
#random.shuffle(relatives_keys)
relatives_hash_map = generate_hash_map(relativedate_dict)

for relatives in relatives_keys:
    start_score1, end_score1 = relatives_hash_map[relatives]
    for season in season_keys:
        start_score2, end_score2 = season_hash_map[season]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((relatives, season))
            # print(relatives, season)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("seasons to relatives tuples generated. Size is now", len(natural_language_tuples))

#seasons to months
months_keys = list(monthsdict.keys())
random.shuffle(months_keys)
months_hash_map = generate_hash_map(monthsdict)

for month in months_keys:
    start_score1, end_score1 = months_hash_map[month]
    for season in season_keys:
        start_score2, end_score2 = season_hash_map[season]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((month, season))
            # print(month, season)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("seasons to months tuples generated. Size is now", len(natural_language_tuples))

#relatives to dates
for relatives in relatives_keys:
    start_score1, end_score1 = relatives_hash_map[relatives]
    for date in date_keys:
        start_score2, end_score2 = date_hash_map[date]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((relatives, date))
            # print(relatives, date)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

#lastx to dates
for lastx in lastx_keys:
    start_score1, end_score1 = lastx_hash_map[lastx]
    for date in date_keys:
        start_score2, end_score2 = date_hash_map[date]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((lastx, date))
            # print(lastx, date)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

#months to dates
for month in months_keys:
    start_score1, end_score1 = months_hash_map[month]
    for date in date_keys:
        start_score2, end_score2 = date_hash_map[date]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((month, date))
            # print(month, date)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

#seasons to dates
for season in season_keys:
    start_score1, end_score1 = season_hash_map[season]
    for date in date_keys:
        start_score2, end_score2 = date_hash_map[date]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((season, date))
            # print(season, date)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

#lastx to months
for lastx in lastx_keys:
    start_score1, end_score1 = lastx_hash_map[lastx]
    for month in months_keys:
        start_score2, end_score2 = months_hash_map[month]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((lastx, month))
            # print(lastx, month)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("lastx to months tuples generated. Size is now", len(natural_language_tuples))

#lastx to seasons
for lastx in lastx_keys:
    start_score1, end_score1 = lastx_hash_map[lastx]
    for season in season_keys:
        start_score2, end_score2 = season_hash_map[season]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((lastx, season))
            # print(lastx, season)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("lastx to seasons tuples generated. Size is now", len(natural_language_tuples))

#relatives to months
for relatives in relatives_keys:
    start_score1, end_score1 = relatives_hash_map[relatives]
    for month in months_keys:
        start_score2, end_score2 = months_hash_map[month]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((relatives, month))
            # print(relatives, month)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

print("relatives to months tuples generated. Size is now", len(natural_language_tuples))

#relatives to seasons
for relatives in relatives_keys:
    start_score1, end_score1 = relatives_hash_map[relatives]
    for season in season_keys:
        start_score2, end_score2 = season_hash_map[season]
        if (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2):
            natural_language_tuples.add((relatives, season))
            # print(relatives, season)
            i += 1
            break
    if i % 1000 == 0:
        print(i)

#print a couple of samples from the tuples set
print("Random samples from the tuples set:")
#remember it is a set not a list
for i, tup in enumerate(random.sample(sorted(natural_language_tuples), 20)):
    print(tup)

#final length: 
print("Final length of the natural language tuples set is", len(natural_language_tuples))

#Save the natural language tuples set to a file at csv/natural_language_tuples.csv with delimiter '|'
with open('csv/natural_language_tuples.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(['Value', 'Computed'])
    for tup in natural_language_tuples:
        writer.writerow(tup)