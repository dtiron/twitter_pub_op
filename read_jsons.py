#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:37:53 2018

@author: dmitriitiron
"""

import os
import json
import emoji

folder_name = "/Users/dmitriitiron/twitter-files/saved_loads/"


with open('clean_tweets.tsv', 'w') as output:
    output.write('id\ttext\tcreation_time\tuser_loc\n')
    for item in os.listdir(folder_name):
        if "saved_load" in item:
            with open(folder_name+item, 'r') as input_f:
                json_encoded = input_f.read()
                decoded = json.loads(json_encoded)
                
                from_date = decoded['requestParameters']['fromDate']
                to_date = decoded['requestParameters']['toDate']
                print ("\n============================\n", from_date, to_date)
                
                
                for tweet in decoded['results']:
                    if 'extended_tweet' in tweet:
                        text = (tweet['extended_tweet']['full_text'])
                    else:
                        text = (tweet['text'])
                    
                    text = ' '.join(emoji.demojize(text).split())
                    
                    
                
                    creation_time = tweet['created_at']
                    id = str(tweet['id'])
                    if not tweet['user']['location'] == None:
                        user_loc = tweet['user']['location']
                    
                    line = id + '\t' + text + '\t' + creation_time + '\t' + user_loc +'\n'
                    output.write(line)
                    
                    
                

                