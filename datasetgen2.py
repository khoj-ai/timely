import random
import csv
from functools import lru_cache
from datasets import load_dataset
from tqdm import tqdm

def load_csv_data(filename, delimiter):
    data = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            if "Computed" not in row:
                data.append((row[0], row[1]))
    return data

natural_to_dates = load_csv_data('csv/natural_to_date.csv', '|')
dates_to_dates = load_csv_data('csv/dates_to_dates.csv', ',')
natural_to_natural = load_csv_data('csv/natural_language_tuples.csv', '|')

ds = load_dataset("sentence-transformers/wikihow")

@lru_cache(maxsize=None)
def modify_query(i, text, start_or_end):
    summary = ds['train'][i]['summary'].encode('utf-8').decode('utf-8')
    if start_or_end == 0:
        return f"{summary} {text}"
    else:
        return f"{text} {summary[0].lower()}{summary[1:]}"

@lru_cache(maxsize=None)
def modify_doc(i, text, start_or_end):
    doc = ds['train'][i]['text'].encode('utf-8').decode('utf-8').replace('\n', "")
    if start_or_end == 0:
        return f"{doc} {text}"
    else:
        text = text.lower() if random.randint(0, 1) == 0 else text
        return f"{text} {doc[0].lower()}{doc[1:]}"

def write_to_csv(filename, data, mode='w'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        for row in tqdm(data, desc=f"Writing to {filename}", unit="row"):
            writer.writerow(row)

def generate_entries(data, count):
    entries = []
    for i, (key, val) in enumerate(tqdm(data, desc="Generating entries", unit="entry")):
        start_or_end = i % 2
        i = i % 70000
        entries.append([modify_query(i, key, start_or_end), modify_doc(i, val, start_or_end)])
    return entries[:count] if count else entries

# Generate entries
print("Generating natural language entries")
natural_entries = generate_entries(natural_to_natural, None)
print("Generating date entries")
date_entries = generate_entries(natural_to_dates, None)
print("Generating dates to dates entries")
dates_to_dates_entries = generate_entries(dates_to_dates, None)

# Write to CSV
output_file = 'datasets/wiki_data_aware_diverse_v2.csv'
print(f"Writing entries to {output_file}")
write_to_csv(output_file, natural_entries)
write_to_csv(output_file, date_entries, mode='a')
write_to_csv(output_file, dates_to_dates_entries, mode='a')

total_entries = sum(map(len, [natural_entries, date_entries, dates_to_dates_entries]))
print(f"Total entries written: {total_entries}")

print("adding plain entries")
entries = []
for i in range(70000):
    entries.append([ds['train'][i]['summary'], ds['train'][i]['text']])

for i in range(70000):
    random_month_str = str(random.randint(1, 12)).zfill(2)
    random_day_str = str(random.randint(1, 28)).zfill(2)
    random_year_str = str(random.randint(2000, 2021))
    random_date = f" current date:{random_month_str}/{random_day_str}/{random_year_str}"
    entries.append([ds['train'][i]['summary']+random_date, ds['train'][i]['text']])

write_to_csv(output_file, entries, mode='a')