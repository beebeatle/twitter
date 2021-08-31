import tweepy 

# personal details 
my_consumer_key =''
my_consumer_secret=''
my_access_token=''
my_access_token_secret=''

my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

my_api.update_status(status='This is my sample message sent via Twitter API')