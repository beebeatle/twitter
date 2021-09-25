from typing import Text
import requests
import json
import tweepy 

# personal details 
import variables
import settings

from lib.Bot import Bot 

my_consumer_key =   variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

# authentication of consumer key and secret 
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
# Authentication of access token and secret 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)


bot=Bot()

accounts=bot.GetAccounts(cursor)

print ("Accounts selected:", len(accounts))

for acc in accounts:
    MyCount=0
    accountsTotal=accountsTotal+1
    userNameInput=acc[0] 
    print ("\n-------\n ["+str(accountsTotal)+"] ACCOUNT: ",userNameInput,"\n-------")
  

    # Converts Name into ID
    userIdInput=GetUserDetails(userNameInput)

    # Print Intake from User
    print ("User Name",userNameInput)
    print ("User ID",userIdInput)

    # Get Followers of the given User
    friends=my_api.followers_ids(userIdInput)
  #  bot.insertAccounts(cursor,connection,friends)
    activityCount=activityCount+1
    FriendsCount=len(friends)

    print ("Total Followers captured: ",FriendsCount)
    # Walk through Followers

    for i in friends:
        friendId=i
        #checkAccountFlag=bot.checkAccount(i)
        checkLinkFlag=bot.checkLink(cursor,friendId,userIdInput)
        if checkLinkFlag is False:
            print ("No Link detected. Inserting a new link")
            insertLinkFlag=bot.InsertLink(cursor,connection,friendId,userNameInput,userIdInput)
        else:
            print ("Existing Link detected for "+str(friendId)+" and "+str(userIdInput)+". No insert")
            
       


connection.close()
