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

# Pick Settings
LogFileName=settings.LogFileName

logging.basicConfig(handlers=[logging.FileHandler(LogFileName,'w', 'utf-8')],level=logging.INFO,format='%(asctime)s -%(levelname)s-%(message)s')

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }
    
#Counters
count=0

bot=Bot()
twitter=Twitter()

#accounts=bot.GetAccountsToLook(cursor)

query="LowCode"
rows=twitter.getMessageStream(headers,query)

for row in rows:
    count=count+1
    row_id=row["id"]
    row_text=row["text"]

    message_details=twitter.getDetailsOfMessage(row_id,headers)
    user_id=message_details["user"]["id"]
    user_code=message_details["user"]["screen_name"]

    print (str(count)+".","Id: ",row_id, "Text:",row_text,"User ID",user_id,"User code:",user_code)

    checkMessageFlag=bot.checkMessage(cursor,row_id)
    if checkMessageFlag is True:
        print ("Message already saved. Skipping")
    else:
        bot.saveMessage(cursor,connection,row_id,row_text,user_id,user_code)

connection.close()

#END