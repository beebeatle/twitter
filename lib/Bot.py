class Bot:

    def GetAccountIdsForLike(self,cursor,limit):
        accounts=[]
        Sql="SELECT twitter_id,code FROM Accounts where code!=twitter_id and enabled!=2 limit "+str(limit)
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
        sql="SELECT id FROM messages where message_id='"+str(id)+"'"
        print (sql)
        records=cursor.execute(sql)
        return cursor.fetchone() is not None

    def saveMessage(self,cursor,connection,id,text):
        try:
            text.encode("utf8")
            sql="insert into messages (message_id,message_text) values ('"+str(id)+"','"+text+"')"
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
