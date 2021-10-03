from typing import Text
import requests
import json
import pymysql

# personal details 
import variables
import settings
import logging

from lib.Twitter import Twitter 
from lib.Bot import Bot 

my_bearer_token=variables.my_bearer_token

# Pick Variables
db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()


headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }

twitter=Twitter()
bot=Bot()

bot.PopulateUserByFollowers(cursor,connection)

ids=bot.getUsersToEnrich(cursor)

count=0
for id in ids:

  if count > 10:
    break
  
  count=count+1
  print(count,id[0])
  userDetails=twitter.GetUserDetailsById(id[0],headers)
  print(userDetails['name'],userDetails['username'])
  bot.enrichUser(cursor,connection,id[0],userDetails['username'],userDetails['name'])

#message_id=1439748567908954112
#text=twitter.getDetailsOfMessage(message_id,headers)
#print(text["user"]["id"],text["user"]["screen_name"])