
class PostComments:

    __connection= None
    __cursor= None
    savable =False
    def __init__(self,pcid=None,connection=None,post_id=None,user_id=None,comment=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if pcid:
            self.pcid = pcid
            self.get_post_comment()
        self.post_id= post_id
        self.user_id= user_id
        self.comment = comment
        if post_id and user_id and len(comment)> 0:
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection


    def get_comment_by_user_id_and_post_id(self):
        self.__cursor.execute("""SELECT id,comment from postcomments WHERE userid =%s AND postid=%s ORDER BY id desc limit 1""",[self.user_id,self.post_id])
        post= self.__cursor.fetchone()
        if post:
            self.pcid= post[0]
            return  post[1]
        else:
            return False


    def get_post_comment(self):
        self.__cursor.execute("""SELECT userid,postid,comment FROM postcomments WHERE id =%s""",[self.pcid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.post_id=data[1]
            self.comment=data[2]

    def get_comments_by_post_id(self,post_id):
        self.__cursor.execute("""SELECT pc.id,u.username,pc.comment from postcomments as pc JOIN users as u ON pc.userid = u.id WHERE pc.postid= %s ORDER BY pc.id ASC """,[post_id])
        return self.__cursor.fetchall()

    def update_comment(self):
        self.__cursor.execute("""UPDATE postcomments SET comment=%s WHERE id=%s""",[self.comment,self.pcid])
        self.__connection.commit()

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT INTO postcomments (postid,userid,comment) VALUES (%s,%s,%s)""",[self.post_id,self.user_id,self.comment])
            self.__connection.commit()
            
    def delete(self):
        self.__cursor.execute("""DELETE FROM postcomments WHERE id=%s """,[self.pcid])
        self.__connection.commit()


