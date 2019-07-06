import numpy as np
import pandas as pd



def collect_lines_from_file(filename):
    file = open(filename, 'r')
    txtfiles = {}
    medlines =  []
    dict_of_txtlines = {}
    for l in file:
        if l.startswith('###MEDLINE'):
            doc_id = l[11:-1]
            if doc_id in dict_of_txtlines:
                doc_id = l[11:-1]+'ABC'
            else: 
                pass
            dict_of_txtlines[doc_id] = []
        else: 
            dict_of_txtlines[doc_id].append(l)
    file.close()    
    print(len(list(dict_of_txtlines.keys())))
    return dict_of_txtlines
    
    
def grab_words_tags_from_lines(dict_of_txtlines):
    data = {}
    for doc_id in dict_of_txtlines.keys():
        lines = dict_of_txtlines[doc_id]
        doc = ' '.join([bio.split('\t')[0] for bio in lines])
        words = {index :{'text': line.split('\t')[0], 'tag': line.split('\t')[-1][:-1]} for index, line in enumerate(lines)}
        data[doc_id] = {'doc': doc, 'words': words}
    return data
