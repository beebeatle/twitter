from typing import Text
import requests
import json
import tweepy 

import logging
import pymysql

# personal details 
import variables
import settings
import sys

from lib.Bot import Bot 

my_consumer_key = variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

# authentication of consumer key and secret 
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
# Authentication of access token and secret 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)


bot=Bot()
rows=bot.GetMessagesToSend(cursor)

count=0
for row in rows:
    if count < 10:
        count=count+1
        id=row[0]
        user_id=row[1]
        text=row[2]
        print (str(count)+".","Id: ",id)

        try:
            flag=my_api.send_direct_message(user_id, text)
            print ("Set as Sent")
            status=2
            bot.UpdateMessageSentStatus(cursor,connection,id,status,'')
        except tweepy.TweepError as e:
            status=3
            print ("Error captured and saved")
            e_s=str(e)[1:-1]
            e_j=json.dumps(e_s)
            ej=json.loads(e_j)
            bot.UpdateMessageSentStatus(cursor,connection,id,status,ej)
