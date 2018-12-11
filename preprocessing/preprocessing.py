#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 18:04:06 2018

@author: dmitriitiron
"""

import csv
import unidecode
import io
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import read_lexicon_source
import numpy as np
import datetime
from sklearn.neighbors import KNeighborsClassifier
import random
import pandas as pd


lemmatizer = WordNetLemmatizer()
file_name = "more_tags_2.csv"

stop_words = [',', '"', "''", "'", '.', ';', '``', '...', '%', '-', '(', ')', ':', '!', '?', '[', ']', '', '#']
punctuation = string.punctuation

# removes links and @tags, and tokenizes
def clean(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r"@\S+", "", tweet)
    tokens = word_tokenize(tweet)
    clean_tokens = []
    for word in tokens:
        lemma = lemmatizer.lemmatize(word)
        clean_tokens.append(str(lemma))
    return clean_tokens


#returns the text with all encoded lower case characters
def encode(text):
    text_array = []
    clean_text = ""
    for character in text:
        try:
            decoded = unidecode.unidecode(character)
        except UnicodeEncodeError:
            decoded = " "
        except UnicodeDecodeError:
            decoded = " "
        if decoded not in punctuation:
            text_array.append(decoded.lower())
        clean_text = "".join(text_array)
    return clean_text



def make_trimmed_w2v_file(path_orig, path_new, unique_tokens):
    counter = 0
    with open(path_new,'w') as output:
        with open(path_orig, 'r') as source:
            lines = source.readlines()
            
            output.write(str(lines[0])) 
            
            for line in lines:
                #print (line)
                word = line.split()[0]
                if word in unique_tokens:
                    output.write(line)
                    print(word)
                counter+=1
                if (counter % 50) == 0:
                    print(str(datetime.datetime.now()), " that's ", counter)
    return 1
        


def create_sent_scores(data, df):
    counter =0
    sent_scores = []
    for row in data:
        sent_vectors= []
        #print(row[3])
        for token in row[2]:
            if token in df['tokens'].tolist():
                sent_vectors.append(np.asarray(df.loc[df['tokens'] == token].values.tolist()[0][1:]))
                #print(len(sent_vectors), token)
                
        counter+=1
        if (counter % 50) == 0:
            print(str(datetime.datetime.now()), " that's ", counter)
            
        sent_score = np.average(np.asarray(sent_vectors), axis=0).tolist()
        sent_scores.append(sent_score)
        row.append(sent_score)
    return data


def split_data(data,max_train,train_lim_0,train_lim_pos,train_lim_neg,test_lim_0):
    
    train_x, train_y, train_ids, unlabelled_x, unlabelled_y,unlabelled_ids, test_x, test_y, test_ids = [],[],[],[],[],[],[],[],[]
    
    
    count0=0
    count_pos=0
    count_neg=0
    
    for row in data:
        tag = row[1]
        sent_score = row[5]
        tweet_id = row[0]
        if tag == 'n':
            unlabelled_x.append(sent_score)
            unlabelled_ids.append(tweet_id)
        else:
            if len(train_x) >max_train-1:
                test_x.append(sent_score)
                test_y.append(tag)
                test_ids.append(tweet_id)
            
            else:
                
                if (tag == '0' and train_y.count('0')<train_lim_0) or (tag== '1' and train_y.count('1') < train_lim_pos) or (tag=='-1' and train_y.count('-1')<train_lim_neg):
                    train_x.append(sent_score)
                    train_y.append(tag)
                    train_ids.append(tweet_id)
                    
                    if tag =='0':
                        count0+=1
                    elif tag == '-1':
                        count_neg+=1
                    else:
                        count_pos +=1
                    
                else:
                    if tag == '0':
                        if test_y.count('0')<test_lim_0:
                            test_x.append(sent_score)
                            test_y.append(tag)
                            test_ids.append(tweet_id)
                    else:
                        test_x.append(sent_score)
                        test_y.append(tag)
                        test_ids.append(tweet_id)
                    
    return train_x, train_y, train_ids, unlabelled_x, unlabelled_y,unlabelled_ids, test_x, test_y, test_ids



def evaluate_method1(tokenized_tweets, pos_dict, neg_dict):
    binary_vals = [1,0]
    thresh_vals = [1,2,3,4,5,6]
    
    
    
    best_accuracy=[0,0,0]
    token_dict = {}
    for binary_val in binary_vals:
        for thresh_val in thresh_vals:
            num_of_neut = 0
            binary = binary_val
            thresh = thresh_val
            correct_preds = 0
            total_preds = 0
            
            for tweet in tokenized_tweets:
                if not tweet[0]=='0':#(tweet[0] == '0' and num_of_neut<100) or :
                    score = 0
                    tag_pred = None
                    # compute scoreof the tweet
                    for word in tweet[1]:
                        if word in pos_dict:
                            if binary ==1:
                                score +=1
                            else:
                                score+=pos_dict[word]
                            #print(word, pos_dict[word])
                            if word in token_dict:
                                token_dict[word][0] +=1
                            else:
                                token_dict[word] =[1, 'pos', pos_dict[word]]
                                
                        elif word in neg_dict:
                            if binary ==1:
                                score-=1
                            else:
                                score-=neg_dict[word]
                            #print(word, neg_dict[word])
                            
                            if word in token_dict:
                                token_dict[word][0] +=1
                            else:
                                token_dict[word] =[1,'neg', neg_dict[word]]
    
                    
                    # assign tag according to the chosen thresholds
                    if score <= (0-thresh):
                        tag_pred = '-1'
                    elif score >= (0+thresh):
                        tag_pred = '1'
                    else:
                        tag_pred = '0'
                    
                    if tweet[0]=='0':
                        num_of_neut +=1
                        
                    if tag_pred == tweet[0]:
                        correct_preds+=1
                        #print("correct: ", ' '.join(tweet[1]), tag_pred, tweet[0], '\n======')
                    #else:
                        #print("incorrect: ", ' '.join(tweet[1]), tag_pred, tweet[0], '\n======')
                    total_preds+=1
                    
                   # print(tag_pred,tweet[0],'\n=====================\n')
                    
            accuracy = float(float(correct_preds)/total_preds)
            print(binary_val, thresh_val,accuracy)
            print (correct_preds, total_preds)
            if accuracy > best_accuracy[0]:
                best_accuracy = [accuracy,binary_val, thresh_val]
    return best_accuracy, token_dict
            
    
    


with io.open(file_name, 'r') as csv_file:
    reader = csv.reader(csv_file)
    data = []
    print("PREPROCESSING DATA")
    for i,row in enumerate(reader):
        encoded_tweet = encode(row[2])
        clean_tweet = clean(encoded_tweet)
        row[2] = clean_tweet
        time_period = row[3]
        row[3] = " ".join(clean_tweet)
        row.append(time_period)
        if i != 0:
            data.append(row)

pos_dict, neg_dict = read_lexicon_source.read_lexicon('NRC-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
scored = []
tokenized_tweets = []

any_tokens = 0
unique_tokens = []
for row in data:
    if row[1] != 'n':
        tokenized_tweets.append([row[1],row[2]])
    for token in row[2]:
        if not token in unique_tokens:
            unique_tokens.append(token)
        any_tokens+=1

#make_trimmed_w2v_file('new_w2v_file.txt', 'trimmed_w2v.txt', unique_tokens)

w2v = pd.read_csv('trimmed_w2v.txt', sep=' ')

# create the list of vectors for each sentence append as the last value in row in data, return data
data = create_sent_scores(data, w2v)

train_x, train_y, train_ids, unlabelled_x, unlabelled_y,unlabelled_ids, test_x, test_y, test_ids = split_data(data,220,60,80,60,60)

for n_val in [1,2,3,4,5,6,7,8,9,10]:
    
    clf = KNeighborsClassifier(n_neighbors=n_val, weights='distance', p=2)
    
    clf.fit(train_x, train_y)
    
    pred_y = clf.predict(test_x)
        
    from sklearn.metrics import accuracy_score,f1_score
    
    accuracy = accuracy_score(test_y, pred_y)
    f1_result = f1_score(test_y, pred_y, average='macro')
    print("num neighbors: ", n_val, "accuracy: ", accuracy, "f1: ", f1_result)
        

best_accuracy,token_dict = evaluate_method1(tokenized_tweets,pos_dict,neg_dict)

            

    