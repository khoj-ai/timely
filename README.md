![image](https://github.com/khoj-ai/timely/assets/62105787/d860dc91-8706-4d80-9aca-7a50b3348f9e)
# Introduction
At Khoj, we develop open-source personalized AI solutions that enable users to extract useful information from various documents. To find relevant documents for a given query, embeddings models are commonly used. However, most of these models struggle with temporal reasoning. For instance, if asked "Where was I last summer?", the model might not necessarily find documents with dates within that specific time period. This limitation is significant, given the importance of time and date in language and daily life.

To address this problem, we propose **Timely**, a comprehensive pipeline for date-aware dataset generation, model fine-tuning, and benchmarking.

# Technical Details
For details related to dataset generation, model training and benchmarking as well as general findings and techniques refer to our technical report: [technical report].

# Dataset Generation
To replicate dataset generation use the following steps:
1. Run all files ending in "gen.py" (excluding gradientgen, benchgen, and datasetgen) to generate date tuple csv files
2. Run `py date_to_date.py`
3. Run `py natural_to_date.py`
4. Run `py natural_tuples.py` rerunning `lastxgen.py` and `relativedategen.py` with a smaller sample size for improved speed.
5. Run `py datasetgen2.py`. This will create a csv file in datasets titled `datasets/wiki_date_aware_diverse_v4.csv`. Change as necessary
6. Convert this csv file to a .txt file and run it through `dataset_linter.py`
7. The output text file can be used in training.

# Model Training
1. Start a Google Colab Instance with an A100 for optimal speed
2. Upload the desired `.txt` dataset
3. Open the `training.ipynb` notebook.
4. Adjust batch size and other parameters as necessary
5. **IMPORTANT: ** After pip installation, use the command at the end of the notebook to refresh pip installations.
6. Run all other lines starting at the python imports

# Benchmarking
1. Load the desired benchmark and trained model
2. Run all code blocks in `testing.ipynb`

# Questions
For any questions or suggestions feel free to contact team@khoj.dev
