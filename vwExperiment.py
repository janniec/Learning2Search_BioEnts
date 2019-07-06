import numpy as np
import pandas as pd
import os
import itertools
import datetime

import vwCommands as vwc
import evaluatePredictions as ep


def make_addresses(train_address):
    address_path = train_address.split('/')[0]
    file_call = train_address.split('/')[-1].split('_')[0]
    
    test_address = address_path+'/%s_test.txt' % file_call
    model_address = address_path+'/%s_model.model' % file_call
    pred_address = address_path+'/%s_pred.txt' % file_call
    raw_address = address_path+'/%s_raw.txt' % file_call
    return test_address, model_address, pred_address, raw_address


def single_test(train_address, num_labels, \
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor):
    test_address, model_address, pred_address, raw_address = make_addresses(train_address)
    
    vw_train = vwc.train_command(train_address, model_address, num_labels,\
                  rollin, rollout, \
                  epochs, lr, affix, history, neighbor)
    os.system(vw_train)
#     ! eval {vw_train}
    vw_test = vwc.test_command(test_address, model_address, pred_address, raw_address)
    os.system(vw_test)
#     ! eval {vw_test}
    
    label_set = [str(i) for i in list(range(1, num_labels+1))]
    precision, recall, fscore, support = ep.evaluate(test_address, pred_address, label_set)
    
    return fscore, precision, recall


def experiment_sweep(train_address, num_labels, rollin_list, rollout_list,\
                     epoch_list, lr_list, affix_list, history_list, neighbor_list):
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
            
            fscore, precision, recall = single_test(train_address, num_labels, \
                  combo[0], combo[1], \
                  combo[2], combo[3], combo[4], combo[5], combo[6])

            experiment_log.loc[index, 'precision'] = precision.mean()
            experiment_log.loc[index, 'recall'] = recall.mean()
            experiment_log.loc[index, 'fscore'] = fscore.mean()
            
        except: print(index, combo)
 
    endtime = datetime.datetime.now()
    print('End:\t', endtime)
    print('Duration:\t', endtime-starttime)
    
    return experiment_log            