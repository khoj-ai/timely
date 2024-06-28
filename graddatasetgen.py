import csv
from datasets import load_dataset
import random

ds = load_dataset("sentence-transformers/wikihow")
#Query Document Score
file = open("csv/gradients_test.csv", "r", newline="")
reader = csv.reader(file, delimiter="|")
header = next(reader)
file_to_write = open("csv/ungradient_data.csv", "w", newline="")
writer = csv.writer(file_to_write, delimiter="|")
writer.writerow("Query|Document")

doc_templates_end = [" Created {val}", " Published {val}", " Written {val}", " Released {val}", " Posted {val}"]
doc_templates_start = ["Created {val} ", "Published {val} ", "Written {val} ", "Released {val} ", "Posted {val} "]

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
j = 0
i = 0
while j < 30000-2:
    #make sure there is a next. if there is no next break
    try:
        row = next(reader)
    except:
        break
    query = row[0]
    document = row[1]
    score = row[2]
    start_or_end = random.randint(0, 1)
    #format doc
    if start_or_end == 0:
        doc_template = random.choice(doc_templates_start)
    else:
        doc_template = random.choice(doc_templates_end)
    document = doc_template.format(val=document)
    document = modify_doc(i, document, start_or_end)
    #format query
    start_or_end = random.randint(0, 1)
    if start_or_end == 0:
        query = modify_query(i, query, 0)
    else:
        query = modify_query(i, query, 1)
    try:
        #replace /n from query and document
        query = query.replace("\n", "")
        document = document.replace("\n", "")
        writer.writerow([query, document])
        i += 1
        j += 1
    except:
        i += 1
    