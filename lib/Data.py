class Data:

    def GetMessagesLiked(self,cursor):
        Sql="SELECT count(distinct(id)) FROM message_like WHERE status=2 and updated_at >= now() - INTERVAL 1 DAY "
        cursor.execute(Sql)
        rows = cursor.fetchone()
        volume=rows[0]
        return volume

    def GetMessagesRetweeted(self,cursor):
        Sql="SELECT count(distinct(id)) FROM message_retweet WHERE status=2 and updated_at >= now() - INTERVAL 1 DAY "
        cursor.execute(Sql)
        rows = cursor.fetchone()
        volume=rows[0]
        return volume

    def GetUsersFollowed(self,cursor):
        Sql="SELECT count(distinct(id)) FROM user_follow WHERE status=2 and updated_at >= now() - INTERVAL 1 DAY "
        cursor.execute(Sql)
        rows = cursor.fetchone()
        volume=rows[0]
        return volume

    def GetMessagesSourced(self,cursor):
        Sql="SELECT count(distinct(id)) FROM message WHERE updated_at >= now() - INTERVAL 1 DAY "
        cursor.execute(Sql)
        rows = cursor.fetchone()
        volume=rows[0]
        return volume

