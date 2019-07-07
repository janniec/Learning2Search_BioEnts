# Learning2Search_BioEnts
Named Entity Recognition on Biomedical Journals, using Vowpal Wabbit's Learning2Search.  
  
  
## Vowpal Wabbit & Learning2Search  
[Vowpal Wabbit](https://github.com/VowpalWabbit/vowpal_wabbit) is a fast and flexible open source system sponsored by Microsft Research. While capable of  many techniques, such as classification, regression, topic modeling or matrix factorization, at its core the system is based on sparse gradient descent, making it intrisically fast and easy to optimize ... once you figured out how to use it.  
  
[Learning2Search](https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Learning-to-Search-Sub-System) is Vowpal Wabbit's most mysterious technique. This subsystem promises a fast and easy way to solve structured prediction problems, such as dependancy parsing and entity recognition problems, through joint prediction with joint loss, a powerful approach to any text analysis.  
  
<img src="https://github.com/janniec/Learning2Search_BioMeds/blob/master/images/joint_prediction.png" alt="Dimensions" align="middle" height=300px>   
   
Learning2Search accomplishes this through three components in its algorithm, (1) a roll-in policy that determins how the model will train, (2) one-step deviations to make sequences of preditions, and (3) a roll-out policy that scores the sequences of predictions.  
  
<img src="https://github.com/janniec/Learning2Search_BioMeds/blob/master/images/rollinrollout.jpg" alt="Dimensions" align="middle" height=400px>  
  
The available policies are 'ref', which is akin to supervised learning, 'learn', which is akin to imitation learning, and 'mix' which is a 50/50 mixture of the 2 policies. Rolling-in with 'learn' is recommended, as 'mix' is not available as a rollin policy, and 'ref' gives inconsistent results, especially when there are sequences in the testing set not found in the training set. Assuming the roll-in policy is set to 'learn', rolling-out with 'learn' is akin to reinforcement learning and not recommended. Rolling-out with 'ref' may not converge on a local optimal score. Rolling in with 'learn' and rolling-out with 'mix' has shown the most consistent good performance. For more information, please [read this](https://arxiv.org/pdf/1502.02206.pdf) and [watch this](https://www.youtube.com/watch?v=ZMhO1FO_j0o).  
  
Depsite the wealth of information about the subsystem's performance and underlying algorithm, documentation on how to actually implement Learning2Search is minimal or outdated. Through reasearch, trial & error, and sheer grit, I have been able to piece together enough information to build custom entity recogintion models.  
  
  
## Data  
Data for this project came from the [Genia version 3.02 corpus](http://www.nactem.ac.uk/tsujii/GENIA/ERtask/report.html) which contains abstracts found on MEDLINE. The designated training set contained 2000 abstracts, while the designated testing set contained 404 abstracts.  All abstracts were hand-annotated, by the JNLPBA Project, according to 5 classes based on chemical classifications -- protein, cell-type, cell-line, RNA and DNA.    
   
Because the performance of NER models are so dependant on the cleanliness and consistency of the selected texts and annotations within the dataset, it is important to note the average performance of various models on the dataset.  In 2004, this dataset was created by the JNLPBA project and shared among eight participants to test the data on various systems, which included Support Vector Machines, several Markov Models, and Conditional Random Field. Below is the table of the mean performances across all 5 classes by each of the participants. For more information, please see the [Introduction to the Bio-Entity Recognition Task at JNLPBA](http://www.nactem.ac.uk/tsujii/GENIA/ERtask/shared_task_intro.pdf).   
   
|           	| Recall 	| Precision 	| F1 Score 	|
|-----------	|--------	|-----------	|----------	|
| Zho       	| 76.0   	| 69.4      	| 72.6     	|
| Fin       	| 71.6   	| 68.6      	| 70.1     	|
| Set       	| 70.3   	| 69.3      	| 69.8     	|
| Son       	| 67.8   	| 64.8      	| 66.3     	|
| Zha       	| 69.1   	| 61.0      	| 64.8     	|
| Ros       	| 67.4   	| 61.0      	| 64.0     	|
| Par       	| 66.5   	| 59.8      	| 63.0     	|
| Lee       	| 50.8   	| 47.6      	| 49.1     	|
| Base Line 	| 52.6   	| 43.6      	| 47.7     	|  
   
In 2018, the same dataset was used for a Deep Exhaustive Model  utilizing a long-short-term memory neural net ('DEM LSTM'). Below is the table of DEM LSTM's categorical performance on the GENIA testing set. For more information, please see the [Deep Exhaustive Model for Nested Named Entity Recognition](https://www.aclweb.org/anthology/D18-1309).  
  
| Label     	| Recall 	| Precision 	| F1Score 	|
|-----------	|--------	|-----------	|---------	|
| protein   	| 70.8   	| 94.1      	| 80.8    	|
| cell-line 	| 53.1   	| 94.6      	| 67.9    	|
| cell-type 	| 70.0   	| 88.4      	| 78.1    	|
| RNA       	| 57.1   	| 98.8      	| 72.4    	|
| DNA       	| 58.7   	| 92.6      	| 71.8    	|  

  
## Tools  
  * Vowpal Wabbit
  * SpaCy
  * SkLearn
  

## Pipeline
1. Collect lines of words and tags from the GENIA datasets.  
2. Group the words back together into text structure.  
3. Process the texts, utilizing SpaCy, to create features. 
4. Generate txt files with designated train data & test data.  
5. Train Vowpal Wabbit models on train file & predict on test file.  
6. Evaluate predictions utilizing skLearn.  
  
* In order to find the best parameters to fit the models on the data, please use the ExperimentSweep module.  
    1. Provide ranges of each paramaters.  
    2. Start DateTime timer.  
    3. Create an experiment dataframe to track combination of parameters and scores.  
    4. Print status updates.  
    5. Train Vowpal Wabbit models on train file & predict on test file.   
    6. Evaluate predictions utilizing skLearn.   
    7. Log in dataframe.  
    8. End DateTime timer and prints duration.  
    9. Output dataframe sorted on descending F1 score.  
  
  
## Models  
Learning2Search models are inherently multiclass, predicting [IOB tags](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)), the inside, outside, and beginning of each entity. For example, each non-entity word is tagged as "outside" with the 1 label. The first or only word of an entity is tagged as "beginning" with the 2 label (or even numbered label if the model is predicting multiple entities). Finally, the other words within the entity are tagged as "inside" with the 3 label (or odd numbered label if the model is predicting multiple entities).   
   
- Approach 1: a single model to predict 5 entities/ 11 classes. A model trained on only 2000 abstracts was insufficient to predict so many classes. See the evaluation table below.  Either the pattern of text between the entities needed to be more formulaic or we needed more data to predict the relationship among the classes.   
  
| Label     	| Recall 	| Precision 	| F1Score 	|
|-----------	|--------	|-----------	|---------	|
| All Classes  	| 48.8   	| 71.3      	| 53.7    	|  
  
- Approach 2: five separate models, one for each entity/ 3 classes. This method proved more successful. Categorical performance of each model is shown in the table below, along with the F1 scores of the recent DEM LSTM model as a bench mark.  
   
| Label     	| Recall 	| Precision 	| F1Score 	| DEM's F1s	|
|-----------	|--------	|-----------	|---------	|---------	|
| protein   	| 72.7   	| 80.6      	| 75.7    	| 80.8    	|
| cell-line 	| 76.5   	| 79.4      	| 77.3    	| 67.9    	|
| cell-type 	| 76.6   	| 92.6      	| 82.8    	| 78.1    	|
| RNA       	| 69.3   	| 95.1      	| 78.2    	| 72.4    	|
| DNA       	| 73.9   	| 91.8      	| 80.9    	| 71.8    	|  
  
In addition, the collective performance across all the classes has improved beyond the performance of the top participant of the JNLPBA Project, as shown in the table below.   
  
| Label     	| Recall 	| Precision 	| F1Score 	|
|-----------	|--------	|-----------	|---------	|
| All Classes  	| 73.8   	| 87.9      	| 79.0    	|  
| Zho       	| 76.0   	| 69.4      	| 72.6     	|  
    
    
## Next Steps  
Legacy versions of Learning2Search apparently had the capability to perform [Entity Relation Recognition](https://github.com/VowpalWabbit/vowpal_wabbit/tree/master/demo/entityrelation). Given that models have been separated to train and predict on 1 entity at a time. There is an opportunity to use the predictions generated from the more successful models, such as cell-type, as entity-relation features in weaker models, such as protein, to boost performance.  