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

# Pick Variables
host=variables.database_host
user=variables.database_user
passwd=variables.database_passwd
database=variables.database

my_consumer_key = variables.my_consumer_key
my_consumer_secret= variables.my_consumer_secret
my_access_token= variables.my_access_token
my_access_token_secret=variables.my_access_token_secret
my_bearer_token=variables.my_bearer_token

# Pick Settings
FollowersLimit=settings.FollowersLimit
LogFileName=settings.LogFileName

# authentication of consumer key and secret 
my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
# Authentication of access token and secret 
my_auth.set_access_token(my_access_token, my_access_token_secret) 
my_api = tweepy.API(my_auth)

#logging.basicConfig(filename='Log/TwitterBot.log', encoding='utf-8',level=logging.INFO,format='%(asctime)s -%(levelname)s-%(message)s')

logging.basicConfig(handlers=[logging.FileHandler(LogFileName,'w', 'utf-8')],level=logging.INFO,format='%(asctime)s -%(levelname)s-%(message)s')

connection = pymysql.connect(host="localhost", user="root", passwd="", database="twitter")
cursor = connection.cursor()

headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+my_bearer_token+''
    }
    

### Like function
def SendLike (tweetId,userID,userName,ref_user_name,run_id):
    try:
        APIResponse=my_api.create_favorite(tweetId)
        print (APIResponse.text)
    except:
        print("Something went wrong")
        logMessage="Error Like "+userName+"/"+userID+" "+tweetId
        logging.info(logMessage)
        result=0
    else:
        print("Nothing went wrong. Logging activities now")
        logMessage="Sent Like "+userName+"/"+userID+" "+tweetId
        logging.info(logMessage)
        result=1

        try:
            SqlQ="INSERT INTO activities(type, target_user_id,target_user_name,message_id,ref_user_name,message_text,run_id) \
                VALUES ('like','"+userID+"','"+userName+"','"+tweetId+"','"+ref_user_name+"','"+messageText+"','"+run_id+"')"
            print (SqlQ)
            cursor.execute(SqlQ)
        except:
            SqlQ="INSERT INTO activities(type, target_user_id,target_user_name,message_id,ref_user_name,message_text,run_id) \
             VALUES ('like','"+userID+"','"+userName+"','"+tweetId+"','"+ref_user_name+"','Text Encoding Error','"+run_id+"')"
            print (SqlQ)
            cursor.execute(SqlQ)
        finally:
            connection.commit()



    return result


def RunRegister(input,command):
    SqlQ="INSERT INTO runs (input,command) values ('"+input+"','"+command+"')"
    print (SqlQ)

    cursor.execute(SqlQ)
    connection.commit()

    return cursor.lastrowid

def RunUpdate(run_id,users_count,messages_count,likes_count):
    SqlQ="update runs set users_count='"+users_count+"', messages_count='"+messages_count+"',  likes_count='"+likes_count+"' where id='"+run_id+"'"
    print (SqlQ)

    cursor.execute(SqlQ)
    connection.commit()

    return cursor


def GetAccounts():
    accounts=[]
    Sql="SELECT code FROM Accounts"
    records=cursor.execute(Sql)
    rows = cursor.fetchall()
    return rows
  #  i=0
   # for row in rows:
    #    accounts[i]=row[0]
     #   i=i+1
    #return accounts

def GetUserDetails(userName):
    urlUser="https://api.twitter.com/2/users/by/username/"+userName
    response = requests.get(urlUser, headers=headers)
    json_data = json.loads(response.text)
    userID=json_data["data"]["id"]
    return userID
    
def GetUserDetailsById(userId):
    urlUser="https://api.twitter.com/2/users/"+str(userId)
    response = requests.get(urlUser, headers=headers)
    json_data = json.loads(response.text)
    return json_data["data"]["username"]

def getMessages(userId):
    url = "https://api.twitter.com/2/users/"+userId+"/tweets?max_results=5"
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    return json_data
# Functions Definition is Complete


accountsTotal=0
accounts=GetAccounts()

i=0
for acc in accounts:
    print (acc[0])
    userNameInput=acc[0]
    accountsTotal=accountsTotal+1
    i=i+1
    if i>0:
        break
    

command=sys.argv[0]
#userNameInput=sys.argv[1]
ref_user_name=userNameInput


# Converts Name into ID
userIdInput=GetUserDetails(userNameInput)

# Print Intake from User
print ("User Name",userNameInput)
print ("User ID",userIdInput)

run_id=str(RunRegister(userNameInput,command))

# Get Followers of the given User
friends=my_api.followers_ids(userIdInput)
FriendsCount=len(friends)

print ("Total Followers captured: ",FriendsCount)

# Get Users (Followers)
#MyFollowers=my_api.followers()

# Walk through Followers
MyCount=0
totalLikes=0
skippedMany=0
skippedDM=0
messagesTotal=0
likeFail=0
for i in friends:
    
    if MyCount >= FollowersLimit:
        break

    MyCount=MyCount+1  
    userId=str(i)
    userName=GetUserDetailsById(userId)
    
    
    print("\n--------",MyCount,".",userName,userId,"\n")

    json_data = getMessages(userId)
   
    myCountM=0
    
# Walk through Messages  
    tweetId=""
    myCountLikes=0
    
    try:
        CountMessages=len(json_data["data"])
        print ("Messages captured for the user:", CountMessages)
    except:
        print ("No Messages detected")
        continue
    
    # Process given Message
    for m in json_data["data"]:
        messagesTotal=messagesTotal+1
        # Connect to the database


        myCountM=myCountM+1
        tweetId=m["id"]
        print("\n",myCountM,tweetId)

        messageText=m["text"]
        messageText.encode("utf8")
        print(messageText)
        logMessage="Received "+userName+"/"+userId+" "+tweetId+" : "+messageText
        logging.info(logMessage)
              
        try:
            SqlQ="INSERT INTO activities(type, target_user_id,target_user_name,message_id,ref_user_name,message_text,run_id) \
                VALUES ('read','"+userId+"','"+userName+"','"+tweetId+"','"+ref_user_name+"','"+messageText+"','"+run_id+"')"
            print (SqlQ)
            cursor.execute(SqlQ)
        except:
            SqlQ="INSERT INTO activities(type, target_user_id,target_user_name,message_id,ref_user_name,message_text,run_id) \
             VALUES ('read','"+userId+"','"+userName+"','"+tweetId+"','"+ref_user_name+"','Text Encoding Error','"+run_id+"')"
            print (SqlQ)
            cursor.execute(SqlQ)
        finally:
            connection.commit()



        # Check type of message if it's a DM or RT
        if "@" in messageText:
            print("@ Found!")
            logMessage="Skipped @ "+userName+"/"+userId+" "+tweetId
            logging.info(logMessage)
            skippedDM=skippedDM+1
        else:
            if myCountLikes > 0:
                print("Skipped Like: Too Much for the session for this user")
                logMessage="Skipped Too Many "+userName+"/"+userId+" "+tweetId
                logging.info(logMessage)
                skippedMany=skippedMany+1
                continue 
            else:
                print ("Sending a like")
                result=SendLike (tweetId,userId,userName,ref_user_name,run_id)
                print ("Result:",result)
                if result>0:
                    myCountLikes=myCountLikes+1
                    totalLikes=totalLikes+1
                else:
                    likeFail=likeFail+1



print ("Summary for the Run: \
    \nRun ID: "+str(run_id)+" \
    \nAccounts processed "+str(accountsTotal)+" \
    \nUsers processed "+str(MyCount)+" \
    \nMessaged retrieved: "+str(messagesTotal)+" \
    \nSkipped DM RT "+str(skippedDM)+" \
    \nSkipped - Too Many:  "+str(skippedMany)+"\
    \nLikes not accepted  "+str(likeFail)+"\
    \nLiked New: "+str(totalLikes)+" \
")

RunUpdate(str(run_id),str(MyCount),str(messagesTotal),str(totalLikes))



connection.close()

#END