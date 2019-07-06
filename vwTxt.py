import numpy as np
import pandas as pd


def update_BIO_dict(tag, BIO_dict):
    if tag not in BIO_dict:
        BIO = tag.split('-')[0]
        tag_type = tag.split('-')[-1]
        max_label = max(BIO_dict.values())
        if BIO == 'B':
            BIO_dict[tag] = max_label+1
            BIO_dict['I-'+tag_type] = max_label+2
        elif BIO == 'I':
            BIO_dict['B-'+tag_type] = max_label+1
            BIO_dict[tag] = max_label+2
        else: 
            print(doc_id, words_i, tag)
    else: 
        pass
    return BIO_dict
    

def vw_row_out(text, BIO_tag, token):
    vw_text = text.replace(':', ';').replace('|', '/')
    row_tag_text = '%s |text %s ' %(BIO_tag, vw_text)

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


def make_vw_txt(filename, list_of_doc_ids, data_dict, BIO_dict = {'O': 1}):
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
                BIO_dict = update_BIO_dict(tag, BIO_dict)
                row = vw_row_out(text, BIO_dict[tag], token)
                f.write(row+'\n')
    f.close
    return BIO_dict