import tweepy 

# personal credentials (will be moved to the config file) 
my_consumer_key =''
my_consumer_secret=''
my_access_token=''
my_access_token_secret=''

# connection  
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

# sending message
my_api.update_status(status='This is my sample message sent via Twitter API')
