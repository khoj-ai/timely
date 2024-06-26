from datasets import load_dataset

ds = load_dataset("sentence-transformers/wikihow")
with open("csv/wiki_gradient_v1.txt", "a") as file:
    for i in range(0, 120100):
        query = ds['train'][i]['summary']
        doc = ds['train'][i]['text']
        try:
            file.write(f"{query}|{doc}|1\n")
        except:
            print("Error at ", i)