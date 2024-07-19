from datasets import load_dataset
import random
import csv

ds = load_dataset("sentence-transformers/gooaq")

doc_templates_end = [" Created {val}", " Published {val}", " Written {val}", " Released {val}", " Posted {val}"]
doc_templates_start = ["Created {val} ", "Published {val} ", "Written {val} ", "Released {val} ", "Posted {val} "]

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

from functools import lru_cache
@lru_cache(maxsize=None)
def modify_query(i, text, start_or_end):
    summary = ds['train'][i]['question'].encode('utf-8').decode('utf-8')
    if start_or_end == 0:
        return f"{summary} {text}"
    else:
        return f"{text} {summary[0].lower()}{summary[1:]}"

@lru_cache(maxsize=None)
def modify_doc(i, text, start_or_end):
    doc = ds['train'][i]['answer'].encode('utf-8').decode('utf-8').replace('\n', "")
    if start_or_end == 0:
        return f"{doc} {text}"
    else:
        text = text.lower() if random.randint(0, 1) == 0 else text
        return f"{text} {doc[0].lower()}{doc[1:]}"

def convert_date_format(date_str):
    # Convert MM/DD/YY to YYYY-MM-DD assuming dates are in the 2000s
    month, day, year = date_str.split("/")
    #clean year to only have digits
    year = ''.join(filter(str.isdigit, year))
    if int(year) < 100:
        year = "20" + year
    if year == "200":
        print(date_str)
    return year + "-" + month.zfill(2) + "-" + day.zfill(2)

def move_current_date_to_start(input_string):
    loc_date_start = input_string.find("current date:")
    input_string = input_string.replace("current date:", "currentxdate:", 1)
    if loc_date_start == -1:
        return input_string
    loc_date_end = loc_date_start
    while input_string[loc_date_end] != ' ' and input_string[loc_date_end] != '|' and loc_date_end < len(input_string)-1:
        #print(input_string[loc_date_start:loc_date_end])
        loc_date_end += 1
    loc_date_end += 1
    date_str = input_string[loc_date_start:loc_date_end]
    date = date_str.split(":")[1].strip()
    new_date = convert_date_format(date)
    reformatted_string = input_string.replace(date_str, "")
    reformatted_string = "today:" + new_date + " " + reformatted_string
    return reformatted_string

with open("benchmarks/BENCHMARK_U.csv", "w", encoding="utf-8", newline="") as file:
    with open("benchmarks/BENCHMARK_U_original.csv", "w", encoding="utf-8", newline="") as file1:
        writer = csv.writer(file, delimiter='|')
        writer1 = csv.writer(file1, delimiter='|')
        i = 2500000
        sample_size = 10000
        j = 0
        while j < sample_size:
            type = random.randint(0, 10)
            if type < 3:
                data = natural_to_dates
            elif type < 6:
                data = dates_to_dates
            else:
                data = natural_to_natural
            key, val = random.choice(data)
            start_or_end = random.randint(0, 1)
            wrong_key, wrong_val = random.choice(data)
            if val.count("/") >= 1 and "year" not in key:
                wrong_val = val
                wrong_val = wrong_val.split("/")
                new_day = random.randint(1, 28)
                new_month = random.randint(1, 12)
                new_month = str(new_month).zfill(2)
                wrong_val[0] = new_month
                wrong_val[1] = str(new_day).zfill(2)
                wrong_val = "/".join(wrong_val)
            if val.count("/") >= 1 and "year" in key:
                wrong_val = val
                wrong_val = wrong_val.split("/")
                new_day = random.randint(1, 28)
                new_month = random.randint(1, 12)
                new_month = str(new_month).zfill(2)
                #rand val from -2 to 2 not inclusive of 0
                rand_val = 0
                while rand_val == 0:
                    rand_val = random.randint(-2, 2)
                new_year = rand_val + int(wrong_val[2])
                wrong_val[0] = new_month
                wrong_val[1] = str(new_day).zfill(2)
                wrong_val[2] = str(new_year)
                wrong_val = "/".join(wrong_val)
            query = modify_query(i, key, start_or_end)
            doc1 = modify_doc(i, val, start_or_end)
            doc2 = modify_doc(i, wrong_val, start_or_end)

            if "current date:" in doc1 or "current date:" in doc2:
                continue

            else: 
                standardquery = move_current_date_to_start(query).replace("  "," ")
            
            writer.writerow([standardquery, doc1, doc2, 1])
            writer1.writerow([query, doc1, doc2, 1])
            #writer.writerow([key,val,wrong_val,1])
            j += 1
            i += 1