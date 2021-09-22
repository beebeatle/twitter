from typing import Text
import requests
import json

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

bot=Bot()
rows=bot.GetMessagesForClassification(cursor)

count=0
for row in rows:
    count=count+1
    id=row[0]
    text=row[1]
    print (str(count)+".","Id: ",id,"Message:",text)

    if "@" in text:
        print ("Direct message. Skip Retweet")
        status=3
        bot.UpdateMessageStatus(cursor,connection,id,status)
    else:
        print ("Regular update. Set for Retweet")
        status=1
        bot.UpdateMessageStatus(cursor,connection,id,status)

connection.close()