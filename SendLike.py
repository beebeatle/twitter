import tweepy 
import variables

my_consumer_key = variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

# authentication of consumer key and secret 
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
# Authentication of access token and secret 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)
id='1442152151480950785'
try:
    APIResponse=my_api.create_favorite(id)
except:
    print ("Error")
#APIResponse=my_api.destroy_favorite(id)
#print (APIResponse)