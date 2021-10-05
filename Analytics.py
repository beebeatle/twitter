import pymysql
import variables
from lib.Data import Data 

# Pick Variables
db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

data=Data()

messageSourced=data.GetMessagesSourced(cursor)
messageLiked=data.GetMessagesLiked(cursor)
messageRetweeted=data.GetMessagesRetweeted(cursor)
usersFollowed=data.GetUsersFollowed(cursor)

print ("Messages sourced:",messageSourced)
print ("Messages liked:",messageLiked)
print ("Messages retweeted:",messageRetweeted)
print ("Users followed:",usersFollowed)


connection.close()