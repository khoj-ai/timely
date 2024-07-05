import csv
from datetime import datetime
from datasets import load_dataset
import random

def get_dates(date_str):
    """
    This function takes a date string in the format "MM/DD/YYYY"
    and returns a datetime object.
    """
    dateRange = date_str.split("-")
    try:
        date1 = datetime.strptime(dateRange[0], '%m/%d/%y')
        date2 = datetime.strptime(dateRange[1], '%m/%d/%y')
    except ValueError:
        date1 = datetime.strptime(dateRange[0], '%m/%d/%Y')
        date2 = datetime.strptime(dateRange[1], '%m/%d/%Y')
    return date1, date2

value_computed_dict = {}
mega_bins = {}
count = 0
with open('csv/bulk.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        value_computed_dict[row[0]] = row[1]
        if "Computed" in row or "xx" in row[1]:
            continue
        if "/" not in row[0]:
            mega_bins[row[0]] = []
        count += 1

from functools import lru_cache

@lru_cache(maxsize=None)
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
    # if abs(start_score1.year-start_score2.year) > 1:
    #     return False
    return (start_score2 <= start_score1 <= end_score2) or (start_score2 <= end_score1 <= end_score2)

# Store the keys in a list once to avoid repeated list conversion
value_keys = list(value_computed_dict.keys())
mega_keys = list(mega_bins.keys())
print("bins: ", len(mega_keys))
for i in range(400000):
    val = random.choice(value_keys)
    val_computed = value_computed_dict[val]

    # Skip if "Computed" is in the value
    if "Computed" in val_computed:
        continue
    
    val_split = val_computed.split("-")
    start_date1, end_date1 = val_split[0], val_split[1]

    if "xx" in val_computed:
        j = 0
        for key in mega_keys:
            if j > 3000:
                break
            j += 1
            
            key_computed = value_computed_dict[key]
            dates = key_computed.split("-")
            start_date2, end_date2 = dates[0], dates[1]
            year_part = start_date2.split("/")[2].zfill(2)

            mod_start_date1 = start_date1.replace("xx", year_part)
            mod_end_date1 = end_date1.replace("xx", year_part)

            if is_similar(mod_start_date1, mod_end_date1, start_date2, end_date2):
                mega_bins[key].append(val)
                break
    else:
        j = 0
        for key in mega_keys:
            if j > 500:
                break
            j += 1
            
            key_computed = value_computed_dict[key]
            dates = key_computed.split("-")
            start_date2, end_date2 = dates[0], dates[1]

            if is_similar(start_date1, end_date1, start_date2, end_date2):
                mega_bins[key].append(val)

    if i % 10000 == 0:
        print("mega bin processing:", i)
# # print(mega_bins)
# #print mega bin of May 2019
# print(f"May 2019: {mega_bins["May 2019"]}")

ds = load_dataset("sentence-transformers/wikihow")
# for val in ds['train']:
#     print(val['text'])
# print(ds['train'][0]['text'])

@lru_cache(maxsize=None)
def modify_query(i, text, start_or_end):
    summary = ds['train'][i]['summary']
    if start_or_end == 0:
        if summary.endswith('.') or summary.endswith('?'):
            summary = summary[:-1]
        return summary + " " + text
    else:
        summary = summary[0].lower() + summary[1:]
        return text + " " + summary

@lru_cache(maxsize=None)
def modify_doc(i, text, start_or_end):
    doc = ds['train'][i]['text']
    if start_or_end == 0:
        if doc.endswith('.') or doc.endswith('?'):
            doc = doc[:-1]
        return doc + " " + text
    else:
        if random.randint(0, 1) == 0:
            text = text.lower()
        doc = doc[0].lower() + doc[1:]
        return text + " " + doc


month_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
doc_templates_end = [" Created {val}", " Published {val}", " Written {val}", " Released {val}", " Posted {val}"]
doc_templates_start = ["Created {val} ", "Published {val} ", "Written {val} ", "Released {val} ", "Posted {val} "]

dataset = open("datasets/wikihow_data_aware_v6.csv", "w", newline="")
writer = csv.writer(dataset, delimiter="|")
writer.writerow(["Query", "Document"])

i = 0
total_queries = 960000
j=0
rows = []
random.seed(datetime.now().timestamp())
keys_val = list(value_computed_dict.keys())
while j < total_queries:
    if i > 70000:
        i = 0
    if j % 10000 == 0:
        print("processing: ", j)
    val = random.choice(keys_val)
    if "Computed" in value_computed_dict[val]:
        continue
    if ("xx" in value_computed_dict[val] or val.count("/") == 2) and random.randint(0,100) > 90:
        start_or_end = random.randint(0, 1)
        query_text = modify_query(i, val, start_or_end)
        if val.count("/") == 1:
            start_date = value_computed_dict[val].split("-")[0]
            #set year to random year
            random_year = str(random.randint(0, 49)).zfill(2)
            start_date = start_date.replace("xx", random_year)
            start_or_end = random.randint(0, 1)
            if start_or_end == 0:
                start_date = random.choice(doc_templates_end).format(val=start_date)
            else:
                start_date = random.choice(doc_templates_start).format(val=start_date)
            doc_text = modify_doc(i, start_date, start_or_end)
        elif "xx" in value_computed_dict[val]:
            #remove year occasionally
            start_date = value_computed_dict[val].split("-")[0]
            #set year to random year
            random_year = str(random.randint(0, 49)).zfill(2)
            start_date = start_date.replace("xx", random_year)
            start_or_end = random.randint(0, 1)
            if start_or_end == 0:
                start_date = random.choice(doc_templates_end).format(val=start_date)
            else:
                start_date = random.choice(doc_templates_start).format(val=start_date)
            doc_text = modify_doc(i, start_date, start_or_end)
        else:
            start_date = value_computed_dict[val].split("-")[0]
            start_or_end = random.randint(0, 1)
            if start_or_end == 0:
                start_date = random.choice(doc_templates_end).format(val=start_date)
            else:
                start_date = random.choice(doc_templates_start).format(val=start_date)
            doc_text = modify_doc(i, start_date, start_or_end)
        try:
            #remove newline from doc_text
            doc_text = doc_text.replace("\n", "")
            #encode query and doc text into ascii
            rows.append([query_text, doc_text])
            i += 1
            j += 1
            # print(j)
        except:
            # print("error for ", val)
            i += 1
            continue
    elif any(month in val for month in month_short):
        start_or_end = random.randint(0, 1)
        query_text = modify_query(i, val, start_or_end)
        start_date = value_computed_dict[val].split("-")[0]
        if "xx" in start_date:
            random_year = str(random.randint(0, 49)).zfill(2)
            if random.randint(0, 1) == 0:
                start_date = start_date.replace("xx", random_year)
            else:
                start_date = start_date.replace("xx", "")
        #change day to random day from 01 to 26
        random_day = str(random.randint(1, 26)).zfill(2)
        start_date = start_date.split("/")
        start_date[1] = random_day
        start_date = "/".join(start_date)
        start_or_end = random.randint(0, 1)
        if start_or_end == 0:
            start_date = random.choice(doc_templates_end).format(val=start_date)
        else:
            start_date = random.choice(doc_templates_start).format(val=start_date)
        doc_text = modify_doc(i, start_date, start_or_end)
        try:
            doc_text = doc_text.replace("\n", "")
            rows.append([query_text, doc_text])
            i += 1
            j += 1
        except:
            # print("error for ", val)
            i += 1
            continue
    elif val in mega_keys:
        for k in range(10):
            if "current date" in val:
                val = val.replace(" current date:", ". Today:")
                val = val.replace("current date:", ". Today:")
            if mega_bins[val] == []:
                continue
            start_or_end = random.randint(0, 1)
            query_text = modify_query(i, val, start_or_end)
            selected_val = random.choice(mega_bins[val])
            start_or_end = random.randint(0, 1)
            if start_or_end == 0:
                formatted_val = random.choice(doc_templates_end).format(val=selected_val)
            else:
                formatted_val = random.choice(doc_templates_start).format(val=selected_val)
            doc_text = modify_doc(i, formatted_val, start_or_end)
            try:
                doc_text = doc_text.replace("\n", "")
                row.append([query_text, doc_text])
                i += 1
                j += 1
            except:
                # print("error for ", val)
                i += 1
                continue
            val = random.choice(mega_keys)
for row in rows:
    try:
        writer.writerow(row)
    except:
        continue
# reinforce Winter, Summer, Spring, Fall, Monsoon by artificially adding more entries to the dataset
i = 0
j = 0
num_reinforcements = 320000
reinforcements = ["Winter", "Summer", "Spring", "Fall", "Monsoon"]
season_dict = {}
for keys in mega_keys:
    if i > 70000:
        i = 0
    if i == num_reinforcements:
        break
    if any(reinforcement in keys for reinforcement in reinforcements):
        j = 0 
        season_dict[keys] = []
        while j < 6:
            val = random.choice(value_keys)
            val_split = value_computed_dict[val].split("-")
            if "Computed" in value_computed_dict[val]:
                continue       
            start_date1, end_date1 = val_split[0], val_split[1]
            dates = value_computed_dict[keys].split("-")
            start_date2, end_date2 = dates[0], dates[1]
            year_part = start_date2.split("/")[2].zfill(2)
            start_date1 = start_date1.replace("xx", year_part)
            end_date1 = end_date1.replace("xx", year_part)
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                # print(start_date1, end_date1, start_date2, end_date2)
                season_dict[keys].append(val)
                j += 1
                i += 1
        #print(f"Reinforced {keys} with {j} entries")
i = 0
j = 0
num_reinforcements = 320000
season_list = list(season_dict.keys())
while j < num_reinforcements:
    if j % 10000 == 0:
        print("processing: ", j)
    if i > 70000:
        i = 0
    key = random.choice(season_list)
    val = random.choice(season_dict[key])
    # print(key,val)
    if "xx" in value_computed_dict[val]:
        if random.randint(0, 1) == 0:
            val = val.replace("xx", str(random.randint(0, 49)).zfill(2))
        else:
            val = val.replace("xx", "")
    start_or_end = random.randint(0, 1)
    query_text = modify_query(i, key, start_or_end)
    selected_val = val
    start_or_end = random.randint(0, 1)
    #random swap key and selected_val
    if start_or_end == 0:
        formatted_val = random.choice(doc_templates_start).format(val=selected_val)
    else:
        formatted_val = random.choice(doc_templates_end).format(val=selected_val)
    doc_text = modify_doc(i, formatted_val, start_or_end)
    try:
        doc_text = doc_text.replace("\n", "")
        writer.writerow([query_text, doc_text])
        i += 1
        j += 1
    except:
        #print("error for ", val)
        i += 1

#similar process with reinforcement for strings that have "current date:" in them
i = 0
j = 0
num_reinforcements = 320000
reinforcements = ["current date:"]
current_date_dict = {}  
# print(mega_bins)
for keys in value_computed_dict.keys():
    if i > 70000:
        i = 0
    if i == num_reinforcements:
        break
    if any(reinforcement in keys for reinforcement in reinforcements):
        j = 0 
        current_date_dict[keys] = []
        while j < 6:
            val = random.choice(value_keys)
            val_split = value_computed_dict[val].split("-")
            if "Computed" in value_computed_dict[val]:
                continue       
            start_date1, end_date1 = val_split[0], val_split[1]
            dates = value_computed_dict[keys].split("-")
            start_date2, end_date2 = dates[0], dates[1]
            year_part = start_date2.split("/")[2].zfill(2)
            start_date1 = start_date1.replace("xx", year_part)
            end_date1 = end_date1.replace("xx", year_part)
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                #print(start_date1, end_date1, start_date2, end_date2)
                current_date_dict[keys].append(val)
                j += 1
                i += 1
        #print(f"Reinforced {keys} with {j} entries")

i = 0
j = 0
num_reinforcements = 320000
# print("keys date dict: ", len(current_date_dict.keys()))
while j < num_reinforcements:
    if j % 10000 == 0:
        print("processing: ", j)
    if i > 70000:
        i = 0
    key = random.choice(list(current_date_dict.keys()))
    val = random.choice(current_date_dict[key])
    # print(key,val)
    if "xx" in value_computed_dict[val]:
        if random.randint(0, 1) == 0:
            val = val.replace("xx", str(random.randint(0, 49)).zfill(2))
        else:
            val = val.replace("xx", "")
    start_or_end = random.randint(0, 1)
    query_text = modify_query(i, key, start_or_end)
    selected_val = val
    start_or_end = random.randint(0, 1)
    if start_or_end == 0:
        formatted_val = random.choice(doc_templates_start).format(val=selected_val)
    else:
        formatted_val = random.choice(doc_templates_end).format(val=selected_val)
    doc_text = modify_doc(i, formatted_val, start_or_end)
    try:
        doc_text = doc_text.replace("\n", "")
        writer.writerow([query_text, doc_text])
        i += 1
        j += 1
    except:
        # print("error for ", val)
        i += 1

#throw in standard query and doc pairs
num_standard = 160000
i = 0
j = 0
while j < num_standard:
    if i > 70000:
        i = 0
    query = modify_query(i, "", 0)
    doc = modify_doc(i, "", 0)
    try:
        doc = doc.replace("\n", "")
        writer.writerow([query, doc])
        i += 1
        j += 1
    except:
        # print("error for ", val)
        i += 1
    
