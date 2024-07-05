from datasets import load_dataset
import random

ds = load_dataset("sentence-transformers/wikihow")

doc_templates_end = [" Created {val}", " Published {val}", " Written {val}", " Released {val}", " Posted {val}"]
doc_templates_start = ["Created {val} ", "Published {val} ", "Written {val} ", "Released {val} ", "Posted {val} "]

#open BENCHMARK_PARAM.csv in reading mode so we can extract date values
import csv 
with open("benchmarks/BENCHMARK_PARAM.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)
    dates = []
    for row in reader:
        dates.append(row[0])

i = 80000
with open("benchmarks/BENCHMARK.csv", "w", encoding="utf-8") as file:
    for line in dates:
        query_date, doc1_date, doc2_date, score = line.split("|")
        while True:
            try:
                query = str(ds['train'][i]['summary'])
                query = query.replace("\n", "")
                #randomly add query_date to start or end
                start_or_end = random.randint(0, 1)
                if start_or_end == 0:
                    query = query_date + " " + query
                else:
                    #remove punctuation from the end of the query
                    query = query.rstrip(".?")
                    query = query + " " + query_date
                    #readd punctuation
                    # query = query + "?"
                break  # Exit the loop if there's no issue
            except (IndexError, KeyError) as e:
                print(f"Skipping i={i} due to error: {e}")
                i += 1  # Increment i and try again
                if i >= len(ds['train']):
                    raise Exception("Reached end of dataset without finding a valid entry.")
        #pick either start or end and format the docs
        start_or_end = random.randint(0, 1)
        if start_or_end == 0:
            doc_template = random.choice(doc_templates_start)
        else:
            doc_template = random.choice(doc_templates_end)
        doc1_date = doc_template.format(val=doc1_date)
        doc2_date = doc_template.format(val=doc2_date)
        context = str(ds['train'][i]['text'])
        context = context.replace("\n", "")
        if start_or_end == 0:
            doc1 = doc1_date + context
            doc2 = doc2_date + context
        else:
            doc1 = context + doc1_date
            doc2 = context + doc2_date
        try:
            #remove any "|" from query doc1 and doc2
            query = query.replace("|", "")
            doc1 = doc1.replace("|", "")
            doc2 = doc2.replace("|", "")
            file.write(f"{query}|{doc1}|{doc2}|{score}\n")
        except Exception as e:
            print(f"Error writing to file for i={i}: {e}")
        i += 1  # Move to the next entry in ds['train']
