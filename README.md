### Introduction

This repository hosts code and datasets related to developing a fine-tuning pipeline for date-aware embeddings model.

### Overview Diagrams
![image](https://github.com/khoj-ai/timely/assets/62105787/8ddf3529-2d75-44e2-935a-672f21599889)
![image](https://github.com/khoj-ai/timely/assets/62105787/288f41da-cd6d-404a-9d71-0abb16c9e5ab)
![image](https://github.com/khoj-ai/timely/assets/62105787/29a9d99d-494a-47a6-952f-b3fb18898d70)


### Dataset Generation

To handle the wide variety of natural language dates different files ending in `gen.py` have been established. Each of these scripts generate pairings in the format **natural date,MM/DD/YY-MM/DD/YY** in a csv file in the folder `csv`. New scripts can also easily be added to create support for other natural language formats. Then the `merger.py` script can be called to combine all csv files into massive pairings repository that can be sampled called `bulk.csv`. After this `datasetgen.p`y can be modified and called to sample `bulk.csv` and produce datasets with different properties.

#### gen files
* holidaygen.py (Christmas, Thanksgiving, etc)
* dateformatsgen.py (4/4, 04/04/2024, 04/04/24, etc)
* monthgen.py (jan, feb, march, etc)
* relativedategen.py (x months ago, x years ago, x days ago)
* seasonsgen.py (winter, spring, monsoon, etc)
* lastxgen.py (last year, last month, etc)

### Training

To train the model for yourself use the notebooks in the `notebooks` folder ensuring the dataset is saved at some accessible location and the path appropriately modified in the code.


### Model Versions / Prototyping

#### v1

The aim of the first training run was to make a simple version of the wikihow dataset with natural date
formats to demonstrate that a base embeddings model is capable of giving documents with a better temporal match a higher similarity score. The dataset had roughly 5000 entries with 1/3 of the entries being infused with natural dates and MM/DD/YY format dates. This model was about 10% better on simple date matching but much better than the base models on more natural formats and for larger periods like seasons. This was due to the initial date matching generation having a much higher proprtion of standard dates. The random sampling of these date matches led to a dataset that was saturated with standard dates. MTEB scores in this test run were fairly similar to the original model suggesting that we weren't degrading the models general reasoning ability.

#### v2

During the v2 iteration the dataset was adjusted to be larger and more diverse in terms of supported date formats. From our testing we found that for strongly related dates such as "december" and "winter" the model had a stronger handling with 15-20% better performance on our benchmarks compared to the base model. It still suffered however on weakly related matches such as matching november as higher than april when talking about the winter. MTEB scores in this test run were fairly similar to the original model suggesting that we weren't degrading the models general reasoning ability.

#### v3

During this trial run we decided to explore possible methodologies to teach our model about weakly related pairings of temporal information. To do this, we create a new triplet dataset with query, document, and a score based on how close the dates were. While the results were promising for some specific test cases, there were many incorrect results we found while doing small tests with individual cases. The MTEB scores during this test run suffered horribly with a 25-30% degradation in performance compared to the base model. While some efforts were made to adjust the loss function (CosineSimilarity and AnglELoss) and to normalize the scoring based on original embeddings produced by the base model, MTEB scores only increased marginally and running our benchmarks revealed that the model was no better than the original model in terms of temporal reasoning. The exact cause of this significant degradation remains unknown but reading the technical report on nomic-embed-text-v1 (our base model) suggests that float scoring based triplets isn't a properly supported training paradigm for the model. We may revisit this training strategy with a different base model such as one from MixedBread.

#### v4

One interesting thing about the v2 model is that in some cases it was able to handle weakly matched pairings of dates. We decided to train a new model using the simple query, pair strategy of v2 but to introduce a small proportion of pairs that weren't direct matches and instead had dates that were loosely related. This was inspired by nomic's training system where the model is first trained on loosely related data and then contrastively finetuned on higher-quality strongly related data. This method seems to be successful as it lead to almost a 20% improvement on the weakly related benchmark compared to a 12% improvement on our v2 model compared to the base model. In fact, across all our benchmarks the v4 model is able to produce a 15-20% improvement compared to the base model compared to v2 which produces a 10-12% improvement.

#### v5
v5 is currently being developed but is using a similar approach to v4 with a much larger dataset, and standard pairing to prevent MTEB degradation.

#### notes
* Percent improvements are based on the original percent of the base model. For example if the base model has a score of 0.5 and the tuned model has a score of 0.75 this is labeled as a 25% improvement rather than a 50% improvement.
* Benchmarks are rough scores and can be changed as the benchmarks run on a relatively small sample size
* Small steps between model versions may have been omitted but general training arguments will be included below.



