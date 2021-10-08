import requests
import json

class Twitter:

    def GetUserDetailsById(self,userId,headers):
        urlUser="https://api.twitter.com/2/users/"+str(userId)
        print(urlUser)
        try:
            response = requests.get(urlUser, headers=headers)
            json_data = json.loads(response.text)
            return json_data["data"]
        except:
            print (response.text)
            return False
        #print (response.code)
        print (response.text)
        

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

    def getDetailsOfMessage(self,message_id,headers):
        url = "https://api.twitter.com/1.1/statuses/show.json?id="+str(message_id)
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        return json_data

    def getFollowers(self,headers):
        url = "https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=LowCodeWins&count=5000"
        response = requests.get(url, headers=headers)
        json_data = json.loads(response.text)
        return json_data

        