import requests
import json

class Twitter:

    def GetUserDetailsById(self,userId,headers):
        urlUser="https://api.twitter.com/2/users/"+str(userId)
        response = requests.get(urlUser, headers=headers)
        json_data = json.loads(response.text)
        return json_data["data"]["username"]