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


dataset = open("benchmarks/BENCHMARK_PARAM.csv", "w", newline="")
writer = csv.writer(dataset, delimiter="|")
writer.writerow(["Query", "D1", "D2", "Score"])

value_computed_dict = {}
with open('csv/bulk.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        if "Computed" in row or "xx" in row[1]:
            continue
        value_computed_dict[row[0]] = row[1]

gradient_count = 10000
i = 0
values = list(value_computed_dict.keys())
while i < gradient_count:
    query = random.choice(values)
    if (query.count("/") == 2):
        continue
    document = value_computed_dict[query].split("-")[0]
    month, day, year = map(int, document.split('/'))
    if random.random() < 0.2:
        month = str(random.randint(1, 12)).zfill(2)
    if random.random() < 0.1:
        year = str(random.randint(2000, 2021))
    if random.random() < 0.8:
        day = str(random.randint(1, 28)).zfill(2)
    startd = f"{month}/{day}/{year}"
    #generate another startd using the same randomized logic
    month, day, year = map(int, document.split('/'))
    if random.random() < 0.2:
        month = str(random.randint(1, 12)).zfill(2)
    if random.random() < 0.1:
        year = str(random.randint(2000, 2021))
    if random.random() < 0.8:
        day = str(random.randint(1, 28)).zfill(2)
    init_startd = f"{month}/{day}/{year}"

    #score the doc date, startd, and init_startd. 1 if startd is closer to doc date than init_startd else 0
    if abs(scorer(startd) - scorer(document)) < abs(scorer(init_startd) - scorer(document)):
        score = 1
    else:
        score = 0

    vals = startd.split("/")
    for j in range(len(vals)):
        vals[j] = vals[j].zfill(2)
    startd = "/".join(vals)
    #SAME THING FOR init_startd
    vals = init_startd.split("/")
    for j in range(len(vals)):
        vals[j] = vals[j].zfill(2)
    init_startd = "/".join(vals)
    query = query.replace("\n", "")
    startd = startd.replace("\n", "")
    writer.writerow([query, startd, init_startd, score])
    i += 1

#open lastx and add 1000 of these using the same strategy
value_computed_dict = {}
with open('csv/lastx.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        if "Computed" in row or "xx" in row[1]:
            continue
        value_computed_dict[row[0]] = row[1]

gradient_count = 1000
i = 0
values = list(value_computed_dict.keys())
while i < gradient_count:
    query = random.choice(values)
    # if (query.count("/") == 2):
    #     continue
    document = value_computed_dict[query].split("-")[0]
    month, day, year = map(int, document.split('/'))
    if random.random() < 0.7:
        month = str(random.randint(1, 12)).zfill(2)
    if random.random() < 0.1:
        year = str(random.randint(2000, 2021))
    if random.random() < 0.8:
        day = str(random.randint(1, 28)).zfill(2)
    startd = f"{month}/{day}/{year}"
    #generate another startd using the same randomized logic
    month, day, year = map(int, document.split('/'))
    if random.random() < 0.7:
        month = str(random.randint(1, 12)).zfill(2)
    if random.random() < 0.1:
        year = str(random.randint(2000, 2021))
    if random.random() < 0.8:
        day = str(random.randint(1, 28)).zfill(2)
    init_startd = f"{month}/{day}/{year}"

    #score the doc date, startd, and init_startd. 1 if startd is closer to doc date than init_startd else 0
    if abs(scorer(startd) - scorer(document)) < abs(scorer(init_startd) - scorer(document)):
        score = 1
    else:
        score = 0

    vals = startd.split("/")
    for j in range(len(vals)):
        vals[j] = vals[j].zfill(2)
    startd = "/".join(vals)
    #SAME THING FOR init_startd
    vals = init_startd.split("/")
    for j in range(len(vals)):
        vals[j] = vals[j].zfill(2)
    init_startd = "/".join(vals)
    query = query.replace("\n", "")
    startd = startd.replace("\n", "")
    writer.writerow([query, startd, init_startd, score])
    i += 1




        



