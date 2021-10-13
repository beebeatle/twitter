from typing import Text
import requests
import json
import tweepy 
import pathlib

import logging
import pymysql

# personal details 
import variables
import settings
import sys

from lib.Bot import Bot 
from lib.Twitter import Twitter 

my_consumer_key = variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

logPath=variables.logPath

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

rows=my_api.followers()

twitter=Twitter()
bot=Bot()

headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }

folderPath=str(pathlib.Path().resolve())
logFileName=folderPath+''+logPath+'SaveFollower.log'
print(logFileName)
logging.basicConfig(handlers=[logging.FileHandler(logFileName,'w', 'utf-8')],level=logging.INFO,format='%(asctime)s -%(levelname)s-%(message)s')

fs=twitter.getFollowers(headers)
existingF=fs['ids']

print("Twitter: "+str(existingF))
logging.info("Twitter: "+str(existingF))

rows=bot.GetFollowers(cursor)
savedF=[]
count=0

for i in rows:
    savedF.append(int(i[0]))
#    count=count+1
#    print(count,i[0])
#    existingF.remove(i[0])

print("Database: "+str(savedF))
logging.info("Database: "+str(savedF))

existingFS=set(existingF)
savedFS=set(savedF)

dif1=existingFS.difference(savedFS)
dif2=savedFS.difference(existingFS)

print("Twitter difference from database:", dif1)
logging.info("Twitter difference from database:"+str(dif1))

print("Database difference from Twitter:", dif2)
logging.info("Database difference from Twitter:"+str(dif2))

bot.InsertFollowers(cursor,connection,dif1)






