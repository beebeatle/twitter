from typing import Text
import requests
import json
import tweepy 

# personal details 
import variables
import settings

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

MyCount=1

MyFollowers=my_api.followers()

for i in MyFollowers:
    print(MyCount,".",i.name,"\n")
    MyCount=MyCount+1  

