#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 23:05:18 2018

@author: dmitriitiron
"""

import requests
import json
import os


endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/collectCanTweets.json" 

headers = {"Authorization":"Bearer AAAAAAAAAAAAAAAAAAAAAB258wAAAAAAj1oNmI3Jdh6Kdb9wWEaeDz%2BrBJc%3DV4ZkRpxynsqUjsCSFifyti2hMSkhy4nuzxotaYND5hehMzMg3c", "Content-Type": "application/json"}  

data = '{"query":"(canada (legalize OR legalization OR #legalize OR #legalization OR weed OR cannabis OR marijuana OR pot) place_country:CA lang:en)", "fromDate": "201612010000", "toDate": "201712010000","maxResults": 100,"next":"eyJhdXRoZW50aWNpdHkiOiI2YzRhNzQ1ODViZDI1ZTMwODA5MDg4YjYzMWRjODllMDgwMjc2ZTliMGE2N2IxMzIwNTgwMGJmMDE4NmU0MGQ4IiwiZnJvbURhdGUiOiIyMDE2MTIwMTAwMDAiLCJ0b0RhdGUiOiIyMDE3MTIwMTAwMDAiLCJuZXh0IjoiMjAxNzExMTYyMTIxMjYtOTMxMjcxMDE0NjIwNjA2NDYzLTAifQ=="}'
indexes = []
for item in os.listdir("/Users/dmitriitiron/twitter-files/saved_loads"):
    if "saved_load" in item:
        index = int(item.split('saved_load')[0])
        indexes.append(index)

response = requests.post(endpoint,data=data,headers=headers).json()

load = json.dumps(response, indent = 2)
counter = max(indexes) +1
with open("saved_loads/"+str(counter)+'saved_load.json','w') as output:
    output.write(load)

for item in response['results']:
    if 'extended_tweet' in item:
        print(item['extended_tweet']['full_text'], ' || ',str(item['place']), ' || ',str(item['geo']), ' || ', str(item['created_at']), ' || ', "\n ===================\n")
    else:
        print(item['text'], ' || ',str(item['place']), ' || ',str(item['geo']), ' || ', str(item['created_at']), ' || ', "\n ===================\n")
print('\n====================\n',response['next'])