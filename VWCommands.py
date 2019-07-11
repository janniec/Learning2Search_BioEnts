import numpy as np
import pandas as pd
import os
import EvaluatePredictions as ep


def train_command(train_address, model_address, num_labels, \
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor):
    '''
    Outputs a string of commandline to train a Vowpal Wabbit model.
    Already set to call the Learning2Search subsystem with "--search_task".
    To build an NER model the task is already set to "sequencespan" 
    IN: 
    train_address - where to import the training data from.
    model_addres - where to save the trained model.
    num_labels - number of classes in the dataset.
    rollin - Rollin Policy, 'learn' is recommended.
    rollout - Rollout Policy, 'mix' or maybe 'ref' are recommended.
    epoch - number of passes over the training data.
    lr - step size to convergance in stochastic gradient descent.
    affix - trains on the prefixes/suffixes of features.
    history - trains on previous features.
    neighbor -  trains on neighboring predictions. 
    OUT: vw_train - string of commandline to train a Vowpal Wabbit model.
    '''
    
    label_line = 'vw --search %s ' % num_labels
    task_line = '--search_task sequencespan '
    rollin_line = '--search_rollin %s ' % rollin
    rollout_line = '--search_rollout %s ' % rollout
    epoch_line = '--passes %s ' % epochs
    learning_line = '--learning_rate %s ' % lr
    affix_line = '--affix -%sl,+%sl,-%sp,+%sp,-%st,+%st,-%sd,+%sd,-%se,+%se ' % tuple([affix]*10)
    spelling_line = '--spelling l,p,t,d,e '
    history_line = '--search_history_length %s ' % history
    neighbor_line = '--search_neighbor_features -%s:l,%s:l,-%s:p,%s:p,-%s:t,%s:t,-%s:d,%s:d,-%s:e,%s:e ' % tuple([neighbor]*10)
    cache_line = '-c '
    bytes_line = '-b 26 '
    model_line = '-f %s ' % model_address
    train_line = '-d %s' % train_address
    
    vw_train = label_line+task_line+\
    rollin_line+rollout_line+\
    epoch_line+learning_line+\
    affix_line+spelling_line+\
    history_line+cache_line+\
    neighbor_line+bytes_line+\
    model_line+train_line
    return(vw_train)  

def test_command(test_address, model_address, pred_address, raw_address):
    ''' 
    Outputs a string of commandline to test a Vowpal Wabbit model.
    IN:
    test_address - where to import the test data from.
    model_address - where to import the trained model from.
    pred_address - where to save the generated predictions.
    raw_address - where to save the generated confidence scores.
    OUT: vw_test - string of commandline to test a Vowpal Wabbit model. 
    '''
    model_line = 'vw -i %s ' % model_address
    pred_line = '-p %s ' % pred_address
    raw_line = '-r %s ' % raw_address
    test_line = '-d %s ' % test_address
    
    vw_test = model_line+pred_line+raw_line+test_line+'-t '
    return(vw_test)



def make_addresses(train_address):
    '''
    Outputs file addresses according to formulaic naming convention from train_address.
    '''
    address_path = train_address.split('/')[0]
    file_call = train_address.split('/')[-1].split('_')[0]
    
    test_address = address_path+'/%s_test.txt' % file_call
    model_address = address_path+'/%s_model.model' % file_call
    pred_address = address_path+'/%s_pred.txt' % file_call
    raw_address = address_path+'/%s_raw.txt' % file_call
    return test_address, model_address, pred_address, raw_address

def single_experiment(train_address, num_labels, \
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor):
    '''
    Trains a Vowpal Wabbit model, tests model, generates predictions and raw scores. 
    Evaluates predictions using SkLearn.
    train_address - where to import the training data from.
    num_labels - number of classes in the dataset.
    rollin - Rollin Policy, 'learn' is recommended.
    rollout - Rollout Policy, 'mix' or maybe 'ref' are recommended.
    epoch - number of passes over the training data.
    lr - step size to convergance in stochastic gradient descent.
    affix - trains on the prefixes/suffixes of features.
    history - trains on previous features.
    neighbor -  trains on neighboring predictions. 
    OUT: Scores from evaluation using SkLearn.
    '''
    test_address, model_address, pred_address, raw_address = make_addresses(train_address)
    
    vw_train = train_command(train_address, model_address, num_labels,\
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor)
    os.system(vw_train)
    vw_test = test_command(test_address, model_address, pred_address, raw_address)
    os.system(vw_test)
    
    label_set = [str(i) for i in list(range(1, num_labels+1))]
    precision, recall, fscore, support = ep.evaluate(test_address, pred_address, label_set)
    
    return fscore, precision, recall