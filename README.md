### Introduction

Current embeddings models don't compute embeddings consistently within the context of temporal information. When a query contains temporal information in natural language, documents are not embedded in such a way that they are closer if they have a better temporal match. The purpose of this pipeline is to establish datasets, benchmarks and fine-tuned models that are better in terms of their date arithmetic or date awareness when it comes to document retrieval using queries.

### Overview Diagrams
![image](https://github.com/khoj-ai/timely/assets/62105787/8ddf3529-2d75-44e2-935a-672f21599889)
![image](https://github.com/khoj-ai/timely/assets/62105787/288f41da-cd6d-404a-9d71-0abb16c9e5ab)
![image](https://github.com/khoj-ai/timely/assets/62105787/1d389611-a73e-4b33-9298-2fc33fd245a5)





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

One interesting thing about the v2 model is that in some cases it was able to handle weakly matched pairings of dates. We decided to train a new model using the simple query, pair strategy of v2 but to introduce a small proportion of pairs that weren't direct matches and instead had dates that were loosely related. This was inspired by nomic's training system where the model is first trained on loosely related data and then contrastively finetuned on higher-quality strongly related data. This method seems to be successful as it lead to almost a 20% improvement on the weakly related benchmark compared to a 12% improvement on our v2 model compared to the base model. In fact, across all our benchmarks the v4 model is able to produce a 15% improvement compared to the base model compared to v2 which produces a 10-12% improvement.

#### v5
During the v5 trial run we used a similar methodology to v4 but with a large amount of datapoints: ~440,000. We also removed the small proportion of weakly related date pairings because v5 achieved a 1% higher performance than v4 on our weak pairings benchmarks despite further fine tuning and adjustments. We also increased the amount of high quality natural language data which led to about a 20% improvement compared to the base model across benchmarks and notebly a 28% improvement on the standard benchmark.

#### v6
Currently in training. Same methodology as v5 but trained on A100, batch-size set to 64, and 2,000,000 data points. Large amount of non-date query doc pairings to try and combat MTEB degradation as we increase the number of data pairings and overall dataset size.

batch size 32
standard: 81% (86% v5)
hard: V6:  0.7570564516129032 V5:  0.7585685483870968
long: V6:  0.6913433382137628 V5:  0.6465959004392386 Original:  0.5021961932650073
Banking77Classification V6: 75% V5: 74%

batch size 16
standard:
V6:  0.8338368580060423
V5:  0.8600201409869084
V4:  0.7885196374622356
Original:  0.5861027190332326
V2:  0.7935548841893253

hard:
V6:  0.7424395161290323
V5:  0.7585685483870968
V4:  0.7086693548387096
Original:  0.5544354838709677
V2:  0.6789314516129032

long:
V6:  0.6524524158125915
V5:  0.6465959004392386
V4:  0.6932650073206442
Original:  0.5021961932650073
V2:  0.6278367496339677


#### v7 benchmarking
batch size 64, 900,000 data points, more diverse dataset

hard:
V7:  0.748991935483871
V5:  0.7585685483870968
Original:  0.5544354838709677

diverse benchmark: 

V7:  0.6866363636363636
V5:  0.6517272727272727
Original:  0.5149090909090909

diverse relative date focus:

V7:  0.809
V5:  0.8445
Original:  0.532

diverse easy:
V7:  0.987
V5:  0.952
Original:  0.638

diverse easy long:
V7:  0.992
V5:  0.9564
Original:  0.6637

diverse mini:
V7:  0.641
V5:  0.627
Original:  0.467

diverse date heavy:
V7:  0.99
V5:  0.967
Original:  0.674

diverse natural heavy:
V7:  0.99
V5:  0.943
Original:  0.653

diverse natural heavy and close dates:
V7:  0.909
V5:  0.841
Original:  0.666

diverse natural heavy and close dates extreme:
V7:  0.687
V5:  0.632
Original:  0.526

diverse natural heave and close dates medium (less subjective because randomization isn't applied to year long period where any date is fine:
V7:  0.808
V5:  0.72
Original:  0.56

diverse semistable (meaning I tried to remove inaccuracies and did some manual verification):
Fine Tuned nomic-embed-v7:  0.951
Fine Tuned nomic-embed-v5:  0.902
Fine Tuned nomic-embed-v2:  0.788
Original Nomic:  0.642

#### v8
1.6 million parameters, same strategy as v7, couple of cases included with date in query but matching to document wiht no date

##### diverse stable (10k)
Fine Tuned nomic-embed-v8:  0.9624
Fine Tuned nomic-embed-v7:  0.9634
Fine Tuned nomic-embed-v5:  0.9206
Fine Tuned nomic-embed-v2:  0.8254
Original Nomic:  0.6875



##### diverse base (10k)
* V8:  0.6476363636363637
* V7:  0.6866363636363636
* V5:  0.6517272727272727
* Original:  0.5149090909090909


##### diverse date heavy
- Fine Tuned nomic-embed-v8:  0.992
- Fine Tuned nomic-embed-v7:  0.99
- Fine Tuned nomic-embed-v5:  0.967
- Fine Tuned nomic-embed-v2:  0.868
- Original Nomic:  0.674

##### diverse semistable (meaning I tried to remove inaccuracies and did some manual verification):
- Fine Tuned nomic-embed-v8:  0.949
- Fine Tuned nomic-embed-v7:  0.951
- Fine Tuned nomic-embed-v5:  0.902
- Fine Tuned nomic-embed-v2:  0.788
- Original Nomic:  0.642

##### diverse close dates medium
* V8:  0.797
* V7:  0.808
* V5:  0.72
* Original:  0.56

#### diverse close dates standard

##### natural heavy
V8:  0.991
V7:  0.99
V5:  0.943
Original:  0.653

##### diverse hard:

V7:  0.748991935483871
V5:  0.7585685483870968
Original:  0.5544354838709677

##### diverse natural language period (season/month/etc in query):
Fine Tuned nomic-embed-v8:  0.6738911290322581
Fine Tuned nomic-embed-v7:  0.6759072580645161
Fine Tuned nomic-embed-v5:  0.6733870967741935
Fine Tuned nomic-embed-v2:  0.6169354838709677
Original Nomic:  0.4934475806451613

##### old benchmark (unreliable):
Fine Tuned nomic-embed-v8:  0.8197381671701913
Fine Tuned nomic-embed-v7:  0.8036253776435045
Fine Tuned nomic-embed-v5:  0.8600201409869084

##### old benchmark long (unreliable):
V8:  0.6453147877013177
V7:  0.6855783308931186
V6:  0.6524524158125915
V5:  0.6465959004392386
V4:  0.6932650073206442
Original:  0.5021961932650073
V2:  0.6278367496339677

#### v9

##### bench diverse stable (1k) (31.6% better than base model)
Fine Tuned nomic-embed-v9:  0.958041958041958
Fine Tuned nomic-embed-v7:  0.951
Fine Tuned nomic-embed-v5:  0.902
Original Nomic:  0.642

##### bench diverse stable (10k) (27.8% better than base model)
Fine Tuned nomic-embed-v9:  0.9656
Fine Tuned nomic-embed-v8:  0.9624
Fine Tuned nomic-embed-v7:  0.9634
Fine Tuned nomic-embed-v5:  0.9206
Fine Tuned nomic-embed-v2:  0.8254
Original Nomic:  0.6875

##### bench diverse standard
Fine Tuned nomic-embed-v9:  0.957
Fine Tuned nomic-embed-v7:  0.961
Fine Tuned nomic-embed-v5:  0.916
Original Nomic:  0.695

##### runtime speed
4 minutes, 60MB of data (same as nomic standard)

#### arctic v9 (small, medium, large)
switched to arctic v9 due to overall higher RAG score with small performance hit and smaller overall size. Arctic also has three model sizes which means we can easily create three different sizes based on the user's hardware. This is very important in ensuring we create a model that can be used across Khoj.

##### diverse stable
- Fine Tuned nomic-embed-v9:  0.9656
- Fine Tuned arctic-embed-m-v9:  0.9252
- Fine Tuned arctic-embed-l-v9:  0.9405

### 🔥 Final Results

#### diverse long (10k samples)
- Fine Tuned nomic-embed-v9:  0.9656
- nomic-embed-v1:  0.7016
- Fine Tuned arctic-embed-l-v9:  0.9405
- arctic-embed-l:  0.7302
- Fine Tuned arctic-embed-m-v9:  0.9252
- arctic-embed-m:  0.7598
- Fine Tuned arctic-embed-s-v9:  0.8939
- arctic-embed-s:  0.5862

#### diverse short (1k samples)
- Fine Tuned nomic-embed-v9:  0.958041958041958
- nomic-embed-v1:  0.6653346653346653
- Fine Tuned arctic-embed-l-v9:  0.9200799200799201
- arctic-embed-l:  0.7102897102897103
- Fine Tuned arctic-embed-m-v9:  0.8911088911088911
- arctic-embed-m:  0.7162837162837162
- Fine Tuned arctic-embed-s-v9:  0.8551448551448552
- arctic-embed-s:  0.5534465534465535

### notes
* Percent improvements are based on the original percent of the base model. For example if the base model has a score of 0.5 and the tuned model has a score of 0.75 this is labeled as a 25% improvement rather than a 50% improvement.
* Benchmarks are rough scores and haven't been built to be overly general at this point
* Small steps between model versions may have been omitted but general training arguments will be included below.

### in the works
- upgrade to title - wikipedia article dataset
- more formats of date
- times



### Contact
raghav@khoj.dev

