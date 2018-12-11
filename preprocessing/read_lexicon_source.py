#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 16:35:09 2018

@author: dmitriitiron
"""

import time
def read_lexicon(path):
    pos_dict = {}
    neg_dict = {}
    
    
    
    with open(path,'r') as source:
        emotions = []
        old_word = ""
        for line in source.readlines():
            word = line.split('\t')[0]
            emotion = line.split('\t')[1]
            value = line.split('\t')[2]
            
                
           # print('----\n',word, old_word, emotion, value, emotions)
            if not ('1' in value or '0' in value):
                print("something is wrong with ",word)
            
#            if word == 'abuse':
#                print (word,emotion,value)
#            
            
            if word == old_word:
                if '1' in value: 
                    emotions.append(emotion)
            
            else:
                if 'negative' in emotions:
                    count = 1
                    for emotion_ in emotions:
                        if emotion_ == 'sadness' or emotion_ == 'fear' or emotion_ == 'disgust' or emotion_ == 'anger':
                            count +=1
                    neg_dict[old_word] = count
#                    if old_word == 'abuse':
#                        print (emotions,count)
                    
                elif 'positive' in emotions:
                    count = 1
                    for emotion_ in emotions:
                        if emotion_ == 'anticipation' or emotion_ == 'joy' or emotion_ == 'surprise' or emotion_ == 'trust':
                            count +=1
                    pos_dict[old_word] = count
                
                emotions = []
                old_word = word
                if '1' in value: 
                    emotions.append(emotion)
#                print(word, old_word, emotion, value, emotions, '\n-----\n')

    return pos_dict,neg_dict



