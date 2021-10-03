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

my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

bot=Bot()

users=bot.GetFollowersToBeGreeted(cursor)
for u in users:
    user_id=u[0]
    name=u[1]
    first_name=name.split()[0]
    rows=bot.SetMessageToSend(cursor,connection,user_id,first_name)
    status=2
    table='followers'
    bot.updateStatus(cursor,connection,user_id,status,table)




