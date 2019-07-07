import numpy as np
import pandas as pd


def update_IOB_dict(tag, IOB_dict):
    '''
    Vowpal Wabbit requires number labels associated with IOB style tags. IOB_dict keeps track of IOB tags to number labels. If it encounters a new tag, it will update the IOB tags. Per Vowpal Wabbit instructions, O (outside of entities) are 1, B (the first word of an entity) are even numbers, I (other words in the entity) are odd numbers. B & I tags of the same entity must be consecutive labels. For example, if B-protein is 2, I-protein is 3, and O is 1. 
    IN: 
    tag - IOB style tag of a token.
    IOB_dict - a dictionary of IOB tags to number labels
    OUT: IOB_dict - an updated dictionary if it encountered a new tag, otherwise the same dictionary.
    '''
    if tag not in IOB_dict:
        IOB = tag.split('-')[0]
        tag_type = tag.split('-')[-1]
        max_label = max(IOB_dict.values())
        if IOB == 'B':
            IOB_dict[tag] = max_label+1
            IOB_dict['I-'+tag_type] = max_label+2
        elif IOB == 'I':
            IOB_dict['B-'+tag_type] = max_label+1
            IOB_dict[tag] = max_label+2
        else: 
            print(doc_id, words_i, tag)
    else: 
        pass
    return IOB_dict
    

def vw_row_out(text, IOB_tag, token):
    '''
    Converts text, number label, and SpaCy token to Vowpal Wabbit input format. 
    [Label] |[Name of feature] [Feature] |[Name of feature] [Feature] | ...
    IN: 
    text - word
    IOB_tag - number label from IOB_dict
    token - SpaCy token
    OUT: row - Vowpal Wabbit compliant data row for each word
    '''
    vw_text = text.replace(':', ';').replace('|', '/')
    row_tag_text = '%s |text %s ' %(IOB_tag, vw_text)

    features = {'lemma': token.lemma_.replace(':', ';').replace('|', '/'), 
                'pos': token.pos_.replace(':', ';').replace('|', '/'), 
                'tag': token.tag_.replace(':', ';').replace('|', '/'), 
                'dep': token.dep_.replace(':', ';').replace('|', '/'),
                'ent': token.ent_type_.replace(':', ';').replace('|', '/')
               }
    booleans = {'title': token.is_title, 
                'lower': token.is_lower, 
                'upper': token.is_upper, 
                'alpha': token.is_alpha, 
                'stop': token.is_stop}
    
    feature_fills = []
    for k, v in features.items():
        feature_fills.append(k)
        feature_fills.append(v)
    boolean_fills = []
    for k, v in booleans.items():
        boolean_fills.append(k)
        if v == True:
            boolean_fills.append(1)
        else:
            boolean_fills.append(0)
            
    row_features = '|%s %s '*int(len(features)) % tuple(feature_fills) 
    row_booleans = '|%s:%s '*int(len(booleans)) % tuple(boolean_fills) 
    row = row_tag_text + row_features + row_booleans
    
    return row


def make_vw_txt(filename, list_of_doc_ids, data_dict, IOB_dict = {'O': 1}):
    '''
    Generates train txt file or test txt file.
    IN: 
    filename - name of txt file that will be generated
    list_of_doc_ids - list of doc ids in train set or test set 
    data_dict - dictionary of doc_ids: {'doc': paragraph of words, 'words': dictionary of {'word_index': {'text': word, 'tag': BIO tag, 'token': SpaCy token}}}
    IOB_dict - You an provide the IOB_dict from the train txt file so that the test txt file will have matching labels. Also useful if you want to train/text on 1 entity at a time. Or you can just let the function generate a new IOB_dict.
    OUT: a IOB_dict so you can keep track of the entity tags to the number labels. 
    '''
    f = open(filename, 'w')
    for doc_id in list_of_doc_ids:
        f.write('1 | -DOCSTART- | -X-\n')
        words = data_dict[doc_id]['words']
        for index, words_i in enumerate(words.keys()):
            tag = words[words_i]['tag']
            text = words[words_i]['text']
            token = words[words_i]['token']
            if text == '\n':
                f.write('\n')
            else:
                IOB_dict = update_IOB_dict(tag, IOB_dict)
                row = vw_row_out(text, IOB_dict[tag], token)
                f.write(row+'\n')
    f.close
    return IOB_dict