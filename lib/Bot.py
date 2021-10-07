class Bot:

    def getUsersToEnrich(self,cursor):
        Sql="select user_id from users where name='' and status!='3'"
        records=cursor.execute(Sql)
        return cursor.fetchall()

    def enrichUser(self,cursor,connection,user_id,username,name):
        Sql="update users set name=\""+str(name)+"\", user_code='"+str(username)+"' where user_id='"+str(user_id)+"'"
        print(Sql)
        records=cursor.execute(Sql)
        connection.commit()

    def SetMessageToSend(self,cursor,connection,user_id,name):
        text="Hey "+name+"! Thank you for the follow. Have you seen any cool Low-Code apps recently that are worth sharing?"
        Sql="insert user_message (user_id, message, status) values ('"+str(user_id)+"','"+text+"','1')"
        print (Sql)
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        connection.commit()
        return rows

    def GetFollowers(self,cursor):
        Sql="SELECT user_id FROM followers"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetFollowersToBeGreeted(self,cursor):
        Sql="SELECT u.user_id, u.name, u.user_code FROM followers f \
            join users u on f.user_id=u.user_id\
                where f.status!='2' limit 5"
        records=cursor.execute(Sql)
        return cursor.fetchall()

    def InsertFollowers(self,cursor,connection,f):
        for i in f:
            Sql="insert into followers (user_id) values ('"+str(i)+"')"
            records=cursor.execute(Sql)
            print(Sql)
            connection.commit()
        

    def GetMessagesToSend(self,cursor):
        accounts=[]
        Sql="SELECT id, user_id, message FROM user_message where status=1"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def SetFollowTargets(self,cursor,connection):
        Sql="insert into user_follow (user_id,user_code, status) \
            SELECT distinct m.user_id, m.user_code, '1' as status FROM user_follow f RIGHT OUTER JOIN message m on m.user_id=f.user_id where m.user_id!='' and f.user_id is NULL"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        connection.commit()
        return rows

    def SetLikeTargets(self,cursor,connection):
        Sql="insert into message_like (message_id, status) \
            SELECT m.message_id, '1' as status FROM message m \
            left outer join message_like ml on ml.message_id=m.message_id \
            where ml.message_id is NULL"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        connection.commit()
        return rows

    def SetRetweetTargets(self,cursor,connection):
        Sql="insert into message_retweet (message_id, status) \
            SELECT m.message_id, '1' as status FROM message m left outer join message_retweet r on r.message_id=m.message_id  where r.message_id is NULL"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        connection.commit()
        return rows

    def PopulateUserByFollowers(self,cursor,connection):
        rows=''
        Sql="insert into users (user_id) \
            SELECT f.user_id FROM followers f left outer join users u on u.user_id=f.user_id where u.user_id is NULL"
        try:
            records=cursor.execute(Sql)
            connection.commit()
        except:
            print ("Error in PopulateUserbase")
        return rows

    def PopulateUserbase(self,cursor,connection):
        rows=''
        Sql="insert into users (user_id) \
            SELECT distinct m.user_id FROM message m left outer join users u on u.user_id=m.user_id where u.user_id is NULL"
        try:
            records=cursor.execute(Sql)
            rows = cursor.fetchall()
            connection.commit()
        except:
            print ("Error in PopulateUserbase")
        return rows

    def GetAccountIdsForLike(self,cursor,limit):
        accounts=[]
        Sql="SELECT twitter_id,code FROM Accounts where code!=twitter_id and enabled!=2 limit "+str(limit)
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetMessagesForLike(self,cursor):
        Sql="SELECT m.message_id, m.message_text, u.user_id, u.user_code \
        FROM message_like ml \
        join message m on m.message_id=ml.message_id \
        join users u on u.user_id=m.user_id \
        where ml.status=1"

        Sql="SELECT m.message_id, m.message_text, m.user_id, m.user_code \
        FROM message_like ml \
        join message m on m.message_id=ml.message_id \
        where ml.status=1"

        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetMessagesWithEmptyUsers(self,cursor):
        accounts=[]
        Sql="SELECT message_id FROM message_like where status=1"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetAccountsToLook(self,cursor):
        Sql="SELECT twitter_id, enabled FROM accounts where code=twitter_id order by weight desc limit 2"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def UpdateAccountDetailsById(self,cursor,connection,twitter_id,user_name):
        sql="update accounts set code='"+user_name+"' where twitter_id='"+twitter_id+"'"
        #print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def UpdateAccountDetailsByName(self,cursor,connection,twitter_id,user_name):
        sql="update accounts set twitter_id='"+twitter_id+"' where code='"+user_name+"'"
        #print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def GetAccounts(self,cursor):
        accounts=[]
        Sql="SELECT code FROM Accounts where enabled='1' order by weight desc"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetMessagesForRetweet(self,cursor):
        Sql="SELECT message_id FROM message_retweet where status='1' order by updated_at desc"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetUsersToFollow(self,cursor):
        Sql="SELECT user_id FROM user_follow where status='1'"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def GetMessagesForClassification(self,cursor):
        Sql="SELECT message_id, message_text FROM message where status='0'"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def UpdateMessageLikeStatus(self,cursor,connection,message_id,status):
        sql="update message_like set status='"+str(status)+"' where message_id='"+str(message_id)+"'"
        #print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def UpdateMessageRetweetStatus(self,cursor,connection,message_id,status):
        sql="update message_retweet set status='"+str(status)+"' where message_id='"+str(message_id)+"'"
        #print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def updateStatus(self,cursor,connection,user_id,status,table):
        sql="update "+table+" set status='"+str(status)+"' where user_id='"+str(user_id)+"'"
        print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def UpdateTargetStatus(self,cursor,connection,user_id,status):
        sql="update user_follow set status='"+str(status)+"' where user_id='"+str(user_id)+"'"
        print(sql)
        records=cursor.execute(sql)
        connection.commit()

    def UpdateMessageSentStatus(self,cursor,connection,id,status,resp_msg):
        resp_msg=str(resp_msg)
        #resp_msg=resp_msg.replace("'", "\'")
        sql="update user_message set status='"+str(status)+"',resp_msg=\""+str(resp_msg)+"\" where id='"+str(id)+"'"
        print(sql)
        records=cursor.execute(sql)
        connection.commit()


    def CheckAccount(self,cursor,account):
        sql="SELECT id FROM Accounts where twitter_id='"+account+"'"
        print(sql)
        records=cursor.execute(sql)
        row = cursor.fetchone()
        print (row)
        return row is not None

    def checkLink(self,cursor,acc_id_1,acc_id_2):
        acc_id_1=str(acc_id_1)
        acc_id_2=str(acc_id_2)
        sql="SELECT id FROM account_links where acc_id_1='"+acc_id_1+"' and acc_id_2='"+acc_id_2+"'"
        print(sql)
        records=cursor.execute(sql)
        row = cursor.fetchone()
        print (row)
        return row is not None        

    def checkLike(self,cursor,messageId):
        sql="SELECT id FROM activities where type='like' and message_id='"+messageId+"'"
        print (sql)
        records=cursor.execute(sql)
        return cursor.fetchone() is not None

    def checkUserLike(self,cursor,user_id):
        sql="SELECT id FROM activities where type='like' and target_user_id='"+user_id+"'"
        print (sql)
        records=cursor.execute(sql)
        return cursor.fetchone() is not None

    def InsertLink(self,cursor,connection,account,parent_code,parent_id):
        account=str(account)
        try:
            sql="insert into account_links (acc_id_1,acc_code_2,acc_id_2, link_type) values ('"+account+"','"+parent_code+"','"+parent_id+"','1')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error inserting a link: "+account)

        connection.commit()


    def checkMessage(self,cursor,id):
        sql="SELECT id FROM message where message_id='"+str(id)+"'"
        print (sql)
        records=cursor.execute(sql)
        return cursor.fetchone() is not None

    def saveMessage(self,cursor,connection,id,text,user_id,user_code):
        try:
            text.encode("utf8")
            sql="insert into message (message_id,message_text,user_id,user_code) values ('"+str(id)+"','"+text+"','"+str(user_id)+"','"+user_code+"')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error saving a message")

        connection.commit()

    def saveTargetFollower(self,cursor,connection,user_id,user_code):
        try:
            text.encode("utf8")
            sql="insert into target_follower (user_id,user_code) values ('"+str(user_id)+"','"+user_code+"')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error saving a message")

        connection.commit()

    def insertAccountAndLink(self,cursor,connection,account):
        try:
            sql="insert into Accounts (twitter_id,code) values ('"+account+"','"+account+"')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error inserting an Account: "+account)

        try:
            sql="insert into account_links (acc_id_1,acc_code_2, link_type) values ('"+account+"','luxoft','1')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error inserting a link: "+account)

        connection.commit()

    def insertAccounts(self,cursor,connection,accs):
        for i in accs:

            try:
                account=str(i[0])
            except:
                account=str(i)

            sql="SELECT id FROM Accounts where twitter_id='"+account+"'"
            print(sql)
            records=cursor.execute(sql)
            row = cursor.fetchone()
            print (row)
            if row is None:
                print ("Inserting into Accounts and Links: "+account)
                try:
                    sql="insert into Accounts (twitter_id,code) values ('"+account+"','"+account+"')"
                    print (sql)
                    resp=cursor.execute(sql)
                except:
                    print ("Error inserting: "+account)
            else:
                print ("Found in Accounts: "+account)
        connection.commit()
