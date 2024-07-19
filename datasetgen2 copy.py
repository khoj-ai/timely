import random
import csv
from functools import lru_cache
from datasets import load_dataset
from tqdm import tqdm

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 
          'august', 'september', 'october', 'november', 'december']

def contains_month(text):
    text_lower = text.lower()
    return any(month in text_lower for month in MONTHS)

def contains_four_digit_year(text):
    for i in range(len(text) - 3):
        if text[i:i+4].isdigit():
            if i == 0 or not text[i-1].isdigit():
                if i+4 == len(text) or not text[i+4].isdigit():
                    # Check if it's surrounded by spaces or common punctuation
                    if i == 0 or text[i-1] in ' ,.?':
                        if i+4 == len(text) or text[i+4] in ' ,.?':
                            return True
    return False

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
doc_terms = ["Published {val}", "Created {val}", "Released {val}", "Written {val}"]
@lru_cache(maxsize=None)
def modify_query(i, text, start_or_end):
    summary = ds['train'][i]['question'].encode('utf-8').decode('utf-8')
    #remove question mark 
    summary = summary[:-1] if summary[-1] == '?' else summary
    if start_or_end == 0:
        return f"{summary} {text}?"
    else:
        return f"{text.capitalize()} {summary[0].lower()}{summary[1:]}?"

@lru_cache(maxsize=None)
def modify_doc(i, text, start_or_end):
    doc = ds['train'][i]['answer'].encode('utf-8').decode('utf-8').replace('\n', "")
    text = random.choice(doc_terms).format(val=text)
    if start_or_end == 0:
        return f"{doc} {text}"
    else:
        text = text.lower() if random.randint(0, 1) == 0 else text
        return f"{text} {doc[0].lower()}{doc[1:]}"

def write_to_csv(filename, data, mode='w'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        #chunk this into batches of 10000
        chunk_size = 10000
        for i in range(0, len(data), chunk_size):
            writer.writerows(data[i:i + chunk_size])

i = 0
def generate_entries(data, count, natural=False):
    global i
    entries = []
    for j, (key, val) in enumerate(tqdm(data, desc="Generating entries", unit="entry")):
        if random.randint(0, 1) == 0 and natural:
            key, val = val, key
        #if current date is in val swap key and val
        if "today:" in val:
            key, val = val, key
        start_or_end = j % 2
        #keep incrementing i if there is a 4 digit number in the query or document
        query = ds['train'][i]['question']
        doc = ds['train'][i]['answer']
        while True:
            if i >= len(ds['train']):
                i = 0  # Reset to avoid index out of range
            query = ds['train'][i]['question']
            doc = ds['train'][i]['answer'].replace('\n', '')
            if not contains_four_digit_year(query) and \
               not contains_four_digit_year(doc) and \
               not contains_month(query) and not contains_month(doc):
                break
            i += 1
                
        nquery = modify_query(i, key, start_or_end)
        ndoc = modify_doc(i, val, start_or_end)
        if "today:" in ndoc:
            print(ndoc)
        entries.append([nquery, ndoc])
        i += 1
    return entries[:count] if count else entries

# Generate entries
print("Generating natural language entries")
natural_entries = generate_entries(natural_to_natural, None, True)
print("Generating date entries")
date_entries = generate_entries(natural_to_dates, None)
print("Generating dates to dates entries")
dates_to_dates_entries = generate_entries(dates_to_dates, None)

# Write to CSV
output_file = 'datasets/gooaq_v1.csv'
print(f"Writing entries to {output_file}")
write_to_csv(output_file, natural_entries)
write_to_csv(output_file, date_entries, mode='a')
write_to_csv(output_file, dates_to_dates_entries, mode='a')

total_entries = sum(map(len, [natural_entries, date_entries, dates_to_dates_entries]))
print(f"Total entries written: {total_entries}")

print("adding plain entries")
entries = []
for i in range(200000):
    entries.append([ds['train'][i]['question'], ds['train'][i]['answer'].replace('\n', '')])

for i in range(200000):
    random_month_str = str(random.randint(1, 12)).zfill(2)
    random_day_str = str(random.randint(1, 28)).zfill(2)
    random_year_str = str(random.randint(2000, 2021))
    random_date = f" current date:{random_month_str}/{random_day_str}/{random_year_str}"
    entries.append([ds['train'][i]['question']+random_date, ds['train'][i]['answer'].replace('\n', '')])

write_to_csv(output_file, entries, mode='a')