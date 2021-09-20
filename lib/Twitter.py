import requests
import json

class Twitter:

    def GetUserDetailsById(self,userId,headers):
        urlUser="https://api.twitter.com/2/users/"+str(userId)
        try:
            response = requests.get(urlUser, headers=headers)
            json_data = json.loads(response.text)
        except:
            print (response.text)
        #print (response.code)
        print (response.text)
        return json_data["data"]["username"]

    def GetUserDetailsByName(self,userName,headers):
        urlUser="https://api.twitter.com/2/users/by/username/"+userName
        response = requests.get(urlUser, headers=headers)
        json_data = json.loads(response.text)
        userID=json_data["data"]["id"]
        return userID

    def getMessages(self,userId,headers):
        url = "https://api.twitter.com/2/users/"+userId+"/tweets?max_results=5&exclude=retweets,replies"
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        return json_data

    def getMessageStream(self,headers,query):
        url = "https://api.twitter.com/2/tweets/search/recent?query="+query
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        return json_data["data"]