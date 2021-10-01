from typing import Text
import requests
import json
import tweepy 

import logging
import pymysql

# personal details 
import variables
import settings
import sys

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

text='test2'
recipient_id='52366299'
status='@artembatkivskyi Indeed!'
in_reply_to_status_id='1437928558735790088'

my_api.update_status(status, in_reply_to_status_id)
#API.update_status(status, *, in_reply_to_status_id, auto_populate_reply_metadata, exclude_reply_user_ids, attachment_url, media_ids, possibly_sensitive, lat, long, place_id, display_coordinates, trim_user, card_uri)