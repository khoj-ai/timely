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
        if "/" not in row[0]:
            mega_bins[row[0]] = []
        count += 1
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
for i in range(100000):
    val = random.choice(value_keys)
    val_split = value_computed_dict[val].split("-")
    
    if "Computed" in value_computed_dict[val]:
        continue
    
    start_date1, end_date1 = val_split[0], val_split[1]
    
    # If "xx" is present, modify start_date1 and end_date1
    if "xx" in value_computed_dict[val]:
        j = 0
        for key in mega_keys:
            j += 1
            if j > 500:
                break
            dates = value_computed_dict[key].split("-")
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
            j += 1
            if j > 500:
                break
            dates = value_computed_dict[key].split("-")
            start_date2, end_date2 = dates[0], dates[1]
            
            if is_similar(start_date1, end_date1, start_date2, end_date2):
                mega_bins[key].append(val)
                break
    
    if i % 100 == 0:
        print("mega bin processing:", i)
 
# print(mega_bins)
#print mega bin of May 2019
print(f"May 2019: {mega_bins["May 2019"]}")

ds = load_dataset("sentence-transformers/wikihow")
# for val in ds['train']:
#     print(val['text'])
# print(ds['train'][0]['text'])

def modify_query(i, text, start_or_end):
    summary = ds['train'][i]['summary']
    if start_or_end == 0:
        summary = summary.rstrip(".?")
        return summary + " " + text
    else:
        summary = summary[0].lower() + summary[1:]
        return text + " " + summary

def modify_doc(i, text, start_or_end):
    doc = ds['train'][i]['text']
    if start_or_end == 0:
        if random.randint(0, 1) == 0:
            text = text.lower()
        doc = doc.rstrip(".?")
        return doc + " " + text
    else:
        if random.randint(0, 1) == 0:
            text = text.lower()
        doc = doc[0].lower() + doc[1:]
        return text + " " + doc


month_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
doc_templates_end = [" Created {val}", " Published {val}", " Written {val}", " Released {val}", " Posted {val}"]
doc_templates_start = ["Created {val} ", "Published {val} ", "Written {val} ", "Released {val} ", "Posted {val} "]

dataset = open("csv/wikihow_date_aware_gradient_v1.csv", "w", newline="")
writer = csv.writer(dataset, delimiter="|")
writer.writerow(["Query", "Document", "Score"])

total_queries = 10000
j=0
while j < total_queries:
    if j % 10 == 0:
        print("processing: ", j)
    random.seed(datetime.now().timestamp())
    val = random.choice(list(value_computed_dict.keys()))
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
            writer.writerow([query_text, doc_text, 1])
            i += 1
            j += 1
        except:
            print("error for ", val)
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
            writer.writerow([query_text, doc_text, 1])
            i += 1
            j += 1
        except:
            print("error for ", val)
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
                writer.writerow([query_text, doc_text, 1])
                i += 1
                j += 1
            except:
                print("error for ", val)
                i += 1
                continue
            val = random.choice(mega_keys)
# reinforce Winter, Summer, Spring, Fall, Monsoon by artificially adding more entries to the dataset
i = 0
j = 0
num_reinforcements = 10000
reinforcements = ["Winter", "Summer", "Spring", "Fall", "Monsoon"]
season_dict = {}
for keys in mega_keys:
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
                print(start_date1, end_date1, start_date2, end_date2)
                season_dict[keys].append(val)
                j += 1
                i += 1
        print(f"Reinforced {keys} with {j} entries")
i = 0
j = 0
num_reinforcements = 10000
while j < num_reinforcements:
    key = random.choice(list(season_dict.keys()))
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
    if start_or_end == 0:
        formatted_val = random.choice(doc_templates_start).format(val=selected_val)
    else:
        formatted_val = random.choice(doc_templates_end).format(val=selected_val)
    doc_text = modify_doc(i, formatted_val, start_or_end)
    try:
        writer.writerow([query_text, doc_text, 1])
        i += 1
        j += 1
    except:
        print("error for ", val)
        i += 1

#similar process with reinforcement for strings that have "current date:" in them
i = 0
j = 0
num_reinforcements = 10000
reinforcements = ["current date:"]
current_date_dict = {}  
print(mega_bins)
for keys in value_computed_dict.keys():
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
                print(start_date1, end_date1, start_date2, end_date2)
                current_date_dict[keys].append(val)
                j += 1
                i += 1
        print(f"Reinforced {keys} with {j} entries")

i = 0
j = 0
num_reinforcements = 10000
print("keys date dict: ", len(current_date_dict.keys()))
while j < num_reinforcements:
    key = random.choice(list(current_date_dict.keys()))
    val = random.choice(current_date_dict[key])
    print(key,val)
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
        writer.writerow([query_text, doc_text, 1])
        i += 1
        j += 1
    except:
        print("error for ", val)
        i += 1
    
    
