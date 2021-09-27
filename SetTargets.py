import pymysql
import variables
from lib.Bot import Bot 

# Pick Variables
db_host=variables.db_host
db_user=variables.db_user
db_passwd=variables.db_passwd
db_name=variables.db_name

connection = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
cursor = connection.cursor()

bot=Bot()

rows=bot.SetFollowTargets(cursor,connection)
rows=bot.SetLikeTargets(cursor,connection)
rows=bot.PopulateUserbase(cursor,connection)


connection.close()