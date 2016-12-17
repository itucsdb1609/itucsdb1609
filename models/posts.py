
class posts:
    __connection= None
    __cursor= None
    savable =False
    def __init__(self,postid=None,connection=None,user_id=None,date=None,link=None,description=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if postid:
            self.postid = postid
            self.get_post()
        self.link = link
        self.date = date
        self.user_id = user_id
        self.description = description
        if link and user_id and postid:
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection


#     def get_post_by_user_id_and_post_id(self):
#         self.__cursor.execute("""SELECT id,comment from postcomments WHERE userid =%s AND postid=%s ORDER BY id desc limit 1""",[self.user_id,self.post_id])
#         post= self.__cursor.fetchone()
#         if post:
#             self.pcid= post[0]
#             return  post[1]
#         else:
#             return False


    def get_post(self):
        self.__cursor.execute("""SELECT userid,date,link,description FROM posts WHERE id =%s""",[self.postid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.date=data[1]
            self.link=data[2]
            self.description=data[3]

    def get_posts_by_userid(self,user_id):
        self.__cursor.execute("""Select id from posts where userid= %s ORDER BY date ASC """,[user_id])
        return self.__cursor.fetchall()

    def update_post(self):
        self.__cursor.execute("""UPDATE posts SET link=%s , DESCRIPTION=%s, date=%s WHERE id =%s""",[self.link,self.description,self.date,self.postid])
        self.__connection.commit()

    def save(self):
        self.__cursor.execute("""INSERT INTO POSTS (USERID,DATE,LINK,DESCRIPTION ) VALUES (%s,%s,%s,%s)""",[self.user_id, self.date, self.link, self.description])
    def delete(self):
        self.__cursor.execute("""DELETE FROM POSTS WHERE id =%s""",[self.postid])
        self.__connection.commit()


