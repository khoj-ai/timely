import csv
from datetime import datetime
from datasets import load_dataset
import random

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

def scorer(date):
    month, day, year = map(int, date.split('/'))
    if year < 100:  # Assuming two-digit years are 2000s
        year += 2000
    score = year * 10000 + month * 100 + day * 1
    return score

def is_similar(start_date1, end_date1, start_date2, end_date2):
    start_score1 = scorer(start_date1)
    end_score1 = scorer(end_date1)
    start_score2 = scorer(start_date2)
    end_score2 = scorer(end_date2)
    return (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2) or (start_score1 <= start_score2 <= end_score1) or (start_score1 <= end_score2 <= end_score1)

def gradient(start_date1, end_date1, start_date2, end_date2):
    if is_similar(start_date1, end_date1, start_date2, end_date2):
        return 1
    score_diff = min(abs(scorer(start_date1) - scorer(end_date2)), abs(scorer(end_date1) - scorer(start_date2)))
    if score_diff > 200:
        return 0
    return 1 - score_diff / 200

dataset = open("csv/gradients_test.csv", "w", newline="")
writer = csv.writer(dataset, delimiter="|")
writer.writerow(["Query", "Document", "Score"])

value_computed_dict = {}
with open('csv/bulk.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        if "Computed" in row or "xx" in row[1]:
            continue
        value_computed_dict[row[0]] = row[1]

gradient_count = 30000
i = 0
values = list(value_computed_dict.keys())
while i < gradient_count:
    query = random.choice(values)
    if (query.count("/") == 2 and random.random() < 0.5):
        continue
    document = value_computed_dict[query].split("-")[0]
    month, day, year = map(int, document.split('/'))
    if random.random() < 0.7:
        month = str(random.randint(1, 12)).zfill(2)
    if random.random() < 0.1:
        year = str(random.randint(2000, 2021))
    if random.random() < 0.8:
        day = str(random.randint(1, 28)).zfill(2)
    startd = f"{month}/{day}/{year}"
    #make sure each item in startd is 2 digits
    vals = startd.split("/")
    for j in range(len(vals)):
        vals[j] = vals[j].zfill(2)
    startd = "/".join(vals)
    #create an artificial end date that doesn't break any rules. eg. start date < end date and if start date is day 28 end date has to 28. if its 27 end date can be 28 or 27 etc
    endd = startd
    startq, endq = value_computed_dict[query].split("-")
    score = gradient(startq, endq, startd, endd)
    # if score == 0 and random.random() < 0.4:
    #     continue
    # if score == 1 and random.random() < 0.5:
    #     continue
    #remove /n from query and startd
    query = query.replace("\n", "")
    startd = startd.replace("\n", "")
    if score != 0 and score < 0.95:
        writer.writerow([query, startd, score])
    i += 1


        



