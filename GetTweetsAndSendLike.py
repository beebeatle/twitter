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


headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }
    
userName=settings.userName

print ("Username: "+userName)

urlUser="https://api.twitter.com/2/users/by/username/"+userName

response = requests.get(urlUser, headers=headers)

json_data = json.loads(response.text)
userID=json_data["data"]["id"]
print (userID)

url = "https://api.twitter.com/2/users/"+userID+"/tweets"
response = requests.get(url, headers=headers)

json_data = json.loads(response.text)

# the result is a Python dictionary:
#print(json_data["meta"]["result_count"])

#print(json_data["data"][3]["text"])

for i in json_data["data"]:
    print(i["id"])
    tweetId=i["id"]
   # print ("\n")
    print(i["text"]+"\n-------------")
    APIResponse=my_api.create_favorite(tweetId)


#print(response.text)

print(response.status_code)
