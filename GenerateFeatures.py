import numpy as np
import pandas as pd
import spacy
nlp = spacy.load('en')



def grab_tagged_tokened_text_from_lines(dict_of_txtlines):

    ''' 
    For each line within each dictionary value, group words back into a paragraph structure and processes the paragraph with SpaCy and returns Spacy Tokens. 
    Please note that that SpaCy breaks down the paragraphs even further than the dataset broke down the words. For example: in the dataset, 1 line contained "high-dose". SpaCy tokenized this as ["high", "-", "dose"]. As such, the data dictionary has been reorganized to match the SpaCy breakdown. 
    IN: dictionary of doc_ids: list of lines
    OUT: dictionary of doc_ids: {{'word_index': {'text': word, 'tag': BIO tag, 'token': SpaCy token}}} 
    '''
    data = {}
    for doc_id in dict_of_txtlines.keys():
        paragraph = ' '.join([bio.split('\t')[0]\
                                     for bio in dict_of_txtlines[doc_id]])
        spacy_tokens = nlp(paragraph)
        words = [{'text': line.split('\t')[0], 'tag': line.split('\t')[-1][:-1]}\
                 for index, line in enumerate(dict_of_txtlines[doc_id])]
        data[doc_id]={}
        offset = 0
        for word_i, word_dict in enumerate(words):
            index = word_i + offset
            tag = word_dict['tag'] 
            word = word_dict['text']
            token = spacy_tokens[index]  
            data[doc_id][index]={}
            if len(word.strip()) > len(token.text.strip()):
                word = word_dict['text'].strip()[:len(token.text.strip())]

                data[doc_id][index] = {'token': token, 'text': word, 'tag': tag}

                remaining_word = word_dict['text'].strip()[len(token.text.strip()):]
                offset +=1
                index = word_i + offset
                data[doc_id][index]={}
                token = spacy_tokens[index] 
                if tag.startswith('B'):
                    tag_type = tag.split('-')[-1]
                    tag = 'I-'+tag_type
                while len(remaining_word.strip()) > len(token.text.strip()):
                    word = remaining_word.strip()[:len(token.text.strip())]

                    data[doc_id][index] = {'token': token, 'text': word, 'tag': tag}

                    remaining_word = remaining_word.strip()[len(token.text.strip()):]
                    offset +=1
                    index = word_i + offset
                    data[doc_id][index]={}
                    token = spacy_tokens[index] 
                if len(remaining_word.strip()) == len(token.text.strip()):
                    word = remaining_word.strip()

                    data[doc_id][index] = {'token': token, 'text': word, 'tag': tag}

            else:

                data[doc_id][index] = {'token': token, 'text': word, 'tag': tag} 
    return data