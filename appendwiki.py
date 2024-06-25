from datasets import load_dataset

ds = load_dataset("sentence-transformers/wikihow")
with open("csv/wikidateaware_v4_mini.txt", "a") as file:
    for i in range(1500, 3501):
        query = ds['train'][i]['summary']
        doc = ds['train'][i]['text']
        try:
            file.write(f"{query}|{doc}\n")
        except:
            print("Error at ", i)