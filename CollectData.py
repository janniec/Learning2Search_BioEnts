import numpy as np
import pandas as pd



def collect_lines_from_file(filename):
    '''
    Data is Medline abstracts broken into lines of words & tags.
    Creates a dictionary key with Medline doc_ids.
    Grabs lines of words & tegs into a list & assigns as value to Medline doc_ids.
    IN: filename - path to data
    OUT: dictionary with Medline doc_ids as keys and lists of lines as values.
    '''
    file = open(filename, 'r')
    txtfiles = {}
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
    
    