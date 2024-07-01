import csv
from datetime import datetime

def get_dates(date_str):
    """
    This function takes a date string in the format "MM/DD/YYYY"
    and returns a datetime object.
    """
    dateRange = date_str
    dateRange = dateRange.split("-")
    try:
        date1 = datetime.strptime(dateRange[0], '%m/%d/%y')
        date2 = datetime.strptime(dateRange[1], '%m/%d/%y')
    except ValueError:
        date1 = datetime.strptime(dateRange[0], '%m/%d/%Y')
        date2 = datetime.strptime(dateRange[1], '%m/%d/%Y')
    return date1, date2

# Dictionary to store counts of differences
difference_counts = {}
value_computed_dict = {}
mega_bins = {}
count = 0
with open('csv/bulk.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        value_computed_dict[row[0]] = row[1]
        if "Computed" in row or "xx" in row[1]:
            continue
        date1, date2 = get_dates(row[1])
        difference = (date2 - date1).days
        
        if difference in difference_counts:
            difference_counts[difference] += 1
        else:
            difference_counts[difference] = 1
        #if the difference is higher than 100 then make a new key in the mega_bins dictionary with row[0]
        if difference > 60:
            mega_bins[row[0]] = []
        count += 1

def scorer(date):
    month, day, year = date.split('/')
    if int(year) > 1000:
        year = int(year) % 100
    return int(year) * 365 + int(month) * 30 + int(day)

def is_similar(start_date1, end_date1, start_date2, end_date2):
    start_score1 = scorer(start_date1)
    end_score1 = scorer(end_date1)
    start_score2 = scorer(start_date2)
    end_score2 = scorer(end_date2)
    # if "06/01/2019" in start_date2:
    #     print('-----------------------------------')
    #     print(start_date1, end_date1, start_date2, end_date2)
    #     print(start_score1, end_score1, start_score2, end_score2)
    # true if start score 1 is between start score 2 and end score 2 or end score 1 is between start score 2 and end score 2
    return (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2)
   

#iterate over the rows again but this time we will be filling in mega_bins with the rows that had differences under 100
import random
for i in range(1000):
    val = random.choice(list(value_computed_dict.keys()))
    if "Computed" in value_computed_dict[val]:
        continue
    if "xx" in value_computed_dict[val]:
        start_date1 = value_computed_dict[val].split("-")[0]
        end_date1 = value_computed_dict[val].split("-")[1]
        for key in mega_bins.keys():
            start_date2 = value_computed_dict[key].split("-")[0]
            end_date2 = value_computed_dict[key].split("-")[1]
            #replace xx with year of start_date2 in start_date1
            if "xx" in start_date1:
                start_date1 = start_date1.replace("xx", start_date2.split("/")[2].zfill(2))
            if "xx" in end_date1:
                end_date1 = end_date1.replace("xx", start_date2.split("/")[2].zfill(2))
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                mega_bins[key].append(val)
    else:
        start_date1 = value_computed_dict[val].split("-")[0]
        end_date1 = value_computed_dict[val].split("-")[1]
        for key in mega_bins.keys():
            start_date2 = value_computed_dict[key].split("-")[0]
            end_date2 = value_computed_dict[key].split("-")[1]
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                mega_bins[key].append(val)
    if(i % 100 == 0):
        print(i) 
print(mega_bins["last year current date: 10/14/2010"])

#sample random data

