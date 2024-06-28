from datasets import load_dataset

ds = load_dataset("sentence-transformers/wikihow")
with open("csv/wiki_gradient_v2.txt", "a") as file:
    for i in range(0, 30000):
        query = ds['train'][i]['summary']
        doc = ds['train'][i]['text']
        try:
            query.replace("\n", "")
            file.write(f"{query}|{doc}|1\n")
        except:
            print("Error at ", i)