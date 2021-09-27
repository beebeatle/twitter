from typing import Text
import requests
import json

# personal details 
import variables
import settings

from lib.Twitter import Twitter 


my_bearer_token=variables.my_bearer_token

headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }

twitter=Twitter()

message_id=1439748567908954112
text=twitter.getDetailsOfMessage(message_id,headers)
print(text["user"]["id"],text["user"]["screen_name"])