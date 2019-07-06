import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

def collect_labels(test_address):
    with open(test_address) as f:
        contents = f.readlines()
    all_labels = []
    sentence = []
    for line in contents:
        if line == '\n':
            all_labels.append(sentence)
            sentence = []
        else:
            sentence.append(line.split(' ')[0])
    all_labels.append(sentence)     
    return all_labels

def collect_predictions(pred_address):
    with open(pred_address) as f:
        contents = f.readlines()
    all_preds = []
    for sent in contents:
        all_preds.append(sent.split(' ')[:-1])
    return all_preds


def evaluate(test_address, pred_address, label_set):

    all_labels = collect_labels(test_address)   
    all_preds = collect_predictions(pred_address)
    
    labels = [item for sublist in all_labels for item in sublist]
    preds = [item for sublist in all_preds for item in sublist]
    
    if len(labels)!= len(preds):
#         print('labels:', len(labels))
#         print('preds :', len(preds))
        precision = len(preds)
        recall = len(labels)
        fscore = 0
        support = 0
        print('NOT LINING UP')
    else:
        precision, recall, fscore, support = precision_recall_fscore_support(labels, preds, average=None, labels=label_set) 

    return precision, recall, fscore, support