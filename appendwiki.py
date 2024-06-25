from datasets import load_dataset

ds = load_dataset("sentence-transformers/wikihow")
with open("csv/wikidateaware_v3_mini.txt", "a") as file:
    for i in range(501, len(ds['train'])):
        query = ds['train'][i]['summary']
        doc = ds['train'][i]['text']
        try:
            file.write(f"{query}|{doc}\n")
        except:
            print("Error at ", i)