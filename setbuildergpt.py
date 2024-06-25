import csv
from datetime import datetime
import multiprocessing
from functools import partial

def get_dates(date_str):
    date_range = date_str.split("-")
    try:
        date1 = datetime.strptime(date_range[0], '%m/%d/%y')
        date2 = datetime.strptime(date_range[1], '%m/%d/%y')
    except ValueError:
        date1 = datetime.strptime(date_range[0], '%m/%d/%Y')
        date2 = datetime.strptime(date_range[1], '%m/%d/%Y')
    return date1, date2

def scorer(date):
    month, day, year = date.split('/')
    return int(year) * 365 + int(month) * 30 + int(day)

def is_similar(start_date1, end_date1, start_date2, end_date2):
    start_score1 = scorer(start_date1)
    end_score1 = scorer(end_date1)
    start_score2 = scorer(start_date2)
    end_score2 = scorer(end_date2)
    return (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2)

def process_chunk(chunk, value_computed_dict, mega_bins):
    for val in chunk:
        if "Computed" in value_computed_dict[val['Value']] or "xx" in value_computed_dict[val['Value']]:
            continue
        start_date1, end_date1 = get_dates(value_computed_dict[val['Value']])
        for key in mega_bins.keys():
            start_date2, end_date2 = get_dates(value_computed_dict[key])
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                mega_bins[key].append(val['Value'])
    return mega_bins

if __name__ == '__main__':
    num_processes = multiprocessing.cpu_count()
    value_computed_dict = {}
    mega_bins = {}

    with open('csv/bulk.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value_computed_dict[row['Value']] = row['Computed']
            if "Computed" not in row['Computed'] and "xx" not in row['Computed']:
                difference = (get_dates(row['Computed'])[1] - get_dates(row['Computed'])[0]).days
                if difference > 60:
                    mega_bins[row['Value']] = []

    chunks = [list(value_computed_dict.keys())[i::num_processes] for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(partial(process_chunk, value_computed_dict=value_computed_dict, mega_bins=mega_bins), chunks)

    for result in results:
        for key, value_list in result.items():
            if isinstance(value_computed_dict[key], str) and ("Computed" in value_computed_dict[key] or "xx" in value_computed_dict[key]):
                continue
            if key in mega_bins:
                mega_bins[key].extend(value_list)
            else:
                mega_bins[key] = value_list

    print(mega_bins.get("last year current date: 10/14/2010", []))
