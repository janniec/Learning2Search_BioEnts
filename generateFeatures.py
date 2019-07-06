import numpy as np
import pandas as pd
import spacy
nlp = spacy.load('en')



def split_text_to_match_tokens(old_dict):
    new_dict = {}
    for doc_id in old_dict.keys():
        new_dict[doc_id]={'doc': old_dict[doc_id]['doc'], 'words':{}}
#         print('****', doc_id, '*****')
        words = old_dict[doc_id]['words']
        spacy_tokens = nlp(old_dict[doc_id]['doc'])
        offset = 0
        for word_i in words.keys():
            index = word_i + offset
            tag = words[word_i]['tag'] 
            word = words[word_i]['text']
            token = spacy_tokens[index]  
            new_dict[doc_id]['words'][index]={}
            if len(word.strip()) > len(token.text.strip()):
                word = words[word_i]['text'].strip()[:len(token.text.strip())]

                new_dict[doc_id]['words'][index] = {'token': token, 'text': word, 'tag': tag}

                remaining_word = words[word_i]['text'].strip()[len(token.text.strip()):]
                offset +=1
                index = word_i + offset
                new_dict[doc_id]['words'][index]={}
                token = spacy_tokens[index] 
                if tag.startswith('B'):
                    tag_type = tag.split('-')[-1]
                    tag = 'I-'+tag_type
                while len(remaining_word.strip()) > len(token.text.strip()):
                    word = remaining_word.strip()[:len(token.text.strip())]

                    new_dict[doc_id]['words'][index] = {'token': token, 'text': word, 'tag': tag}

                    remaining_word = remaining_word.strip()[len(token.text.strip()):]
                    offset +=1
                    index = word_i + offset
                    new_dict[doc_id]['words'][index]={}
                    token = spacy_tokens[index] 
                if len(remaining_word.strip()) == len(token.text.strip()):
                    word = remaining_word.strip()

                    new_dict[doc_id]['words'][index] = {'token': token, 'text': word, 'tag': tag}

            else:

                new_dict[doc_id]['words'][index] = {'token': token, 'text': word, 'tag': tag} 
    return new_dict