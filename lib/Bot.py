class Bot:

    def GetAccountsToLook(self,cursor):
        Sql="SELECT twitter_id FROM accounts where code=twitter_id limit 100"
        records=cursor.execute(Sql)
        rows = cursor.fetchall()
        return rows

    def UpdateAccountDetails(self,cursor,connection,twitter_id,user_name):
        sql="update accounts set code='"+user_name+"' where twitter_id='"+twitter_id+"'"
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


    def InsertLink(self,cursor,connection,account,parent_code,parent_id):
        account=str(account)
        try:
            sql="insert into account_links (acc_id_1,acc_code_2,acc_id_2, link_type) values ('"+account+"','"+parent_code+"','"+parent_id+"','1')"
            print (sql)
            resp=cursor.execute(sql)
        except:
            print ("Error inserting a link: "+account)

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
