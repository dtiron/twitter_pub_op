#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:37:53 2018
@author: dmitriitiron
"""

import os
import json
import emoji
from dateutil import parser

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

oct16 = parser.parse("Oct 1 2016 00:00:00 +0000")
apr17 = parser.parse("Apr 1 2017 00:00:00 +0000")
oct17 = parser.parse("Oct 1 2017 00:00:00 +0000")
apr18 = parser.parse("Apr 1 2018 00:00:00 +0000")
oct18 = parser.parse("Oct 1 2018 00:00:00 +0000")
folder_name = "C:/Users/gaspa/PycharmProjects/550Final/Oct2017-Oct2018/"

def getPeriod(date):
    date_obj = parser.parse(date)
    if (date_obj > oct16) and (date_obj < oct18):
        if date_obj < apr17:
            period = '1'
        elif date_obj < oct17:
            period = '2'
        elif date_obj < apr18:
            period = '3'
        else:
            period = '4'
    else:
        raise Exception("tweet date out of bounds")
    return period


def formattedTweetLine(tweet):
    if 'extended_tweet' in tweet:
        raw_text = (tweet['extended_tweet']['full_text'])
    else:
        raw_text = (tweet['text'])

    raw_text_without_emojis = ' '.join(emoji.demojize(raw_text).split())
    text = raw_text_without_emojis.decode('utf-8').encode('utf-8')

    creation_time = getPeriod(tweet['created_at'])

    id = str(tweet['id'])

    if not tweet['user']['location'] == None:
        user_loc = tweet['user']['location']
    else:
        user_loc = "unknown_location"

    line = id + '\t' + text + '\t' + creation_time + '\t' + user_loc + '\n'
    return line


with open('clean_tweets.tsv', 'w') as output:
    output.write('id\ttext\tcreation_time\tuser_loc\n')
    for item in os.listdir(folder_name):
        if "saved_load" in item:
            with open(folder_name + item, 'r') as input_f:
                json_encoded = input_f.read()
                decoded = json.loads(json_encoded)

                from_date = decoded['requestParameters']['fromDate']
                to_date = decoded['requestParameters']['toDate']
                print ("\n============================\n", from_date, to_date)

                for tweet in decoded['results']:
                    output.write(formattedTweetLine(tweet))
