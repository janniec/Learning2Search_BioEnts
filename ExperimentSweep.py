import numpy as np
import pandas as pd
import os
import itertools
import datetime

import vwCommands as vwc
import evaluatePredictions as ep


def experiment_sweep(train_address, num_labels, rollin_list, rollout_list,\
                     epoch_list, lr_list, affix_list, history_list, neighbor_list):
    '''
    To find the best parameters for training data:
    1. Provide ranges of each paramaters.  
    2. Start DateTime timer.  
    3. Create an experiment dataframe to track combination of parameters and scores.  
    4. Print status updates.  
    5. Train Vowpal Wabbit models on train file & predict on test file.   
    6. Evaluate predictions utilizing skLearn.   
    7. Log in dataframe.  
    8. End DateTime timer and prints duration.  
    9. Output dataframe sorted on descending F1 score. 
    IN:
    train_address - where to import the training data from.
    num_labels - number of classes in the dataset.
    rollin_list - 'learn' or 'ref'.
    rollout_list - 'learn', 'mix', 'ref', 'none'.
    epoch_list - range of passes over training data.
    lr_list - range of step sizes to convergance in stochastic gradient descent.
    affix_list - range of prefixes/suffixes of features to train on.
    history_list - range of previous features to train on.
    neighbor_list - reange of neighboring predictions to train on.
    OUT: Experiment dataframe sorted on descending F1 Scores
    '''
    starttime = datetime.datetime.now()
    print('Start:\t', starttime)  
    
    num_combos = len(list(itertools.product(rollin_list, rollout_list,\
                                            epoch_list, lr_list, \
                                            affix_list, history_list, neighbor_list)))
    
    experiment_log = pd.DataFrame(columns = ['rollin', 'rollout', \
                                             'learnrate', 'epochs',\
                                             'affix', 'history', 'neighbor',\
                                             'precision', 'recall', 'fscore'])
    
    for index, combo in enumerate(itertools.product(rollin_list, rollout_list,\
                     epoch_list, lr_list, affix_list, \
                     history_list, neighbor_list)):
        if index % 50 == 0:
            print(index, '\t', str(float(index)/float(num_combos)), '% done')
        
        try:
            experiment_log.loc[index, 'rollin'] = combo[0]
            experiment_log.loc[index, 'rollout'] = combo[1]
            experiment_log.loc[index, 'epochs'] = combo[2] 
            experiment_log.loc[index, 'learnrate'] = combo[3]           
            experiment_log.loc[index, 'affix'] = combo[4]
            experiment_log.loc[index, 'history'] = combo[5]
            experiment_log.loc[index, 'neighbor'] = combo[6]
            
            fscore, precision, recall = vwc.single_experiment(train_address, num_labels, \
                  combo[0], combo[1], \
                  combo[2], combo[3], combo[4], combo[5], combo[6])

            experiment_log.loc[index, 'precision'] = precision.mean()
            experiment_log.loc[index, 'recall'] = recall.mean()
            experiment_log.loc[index, 'fscore'] = fscore.mean()
            
        except: print(index, combo)
 
    endtime = datetime.datetime.now()
    print('End:\t', endtime)
    print('Duration:\t', endtime-starttime)
    
    return experiment_log.sort_values(by='fscore', ascending=False).reset_index(drop=True)            