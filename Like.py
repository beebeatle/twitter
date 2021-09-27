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

from lib.Twitter import Twitter 
from lib.Bot import Bot 

# Pick Variables
db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

my_consumer_key = variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

LogFileName=settings.LogFileName

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

# authentication of consumer key and secret 
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
# Authentication of access token and secret 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

bot=Bot()
rows=bot.GetMessagesForLike(cursor)

print ("Total:",len(rows))

count=0
for row in rows:
    if count < 50:
        count=count+1
        id=row[0]
        text=row[1]
        user_code=row[3]
        print (str(count)+".","Id: ",id,"Text:",text, "User code:", user_code)
        try:
            likeFlag=my_api.create_favorite(id)
            #print (retweetFlag)
            print ("Set as Liked")
            status=2
            bot.UpdateMessageLikeStatus(cursor,connection,id,status)
        except:
            print ("Error. Set as Skipped")
            status=3
            bot.UpdateMessageLikeStatus(cursor,connection,id,status)

connection.close()