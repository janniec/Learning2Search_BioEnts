import numpy as np
import pandas as pd


def train_command(train_address, model_address, num_labels, \
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor):
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
    model_line = 'vw -i %s ' % model_address
    pred_line = '-p %s ' % pred_address
    raw_line = '-r %s ' % raw_address
    test_line = '-d %s ' % test_address
    
    vw_test = model_line+pred_line+raw_line+test_line+'-t '
    return(vw_test)