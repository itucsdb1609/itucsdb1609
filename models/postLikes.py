
class PostLike:

    __connection= None
    __cursor= None
    savable =False
    accepted_like_types= ['heart', 'thumbs-up', 'thumbs-down', 'frown-o']
    def __init__(self,plid=None,connection=None,post_id=None,user_id=None,like_type=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if plid:
            self.plid = plid
            self.get_post_like()
        self.post_id= post_id
        self.user_id= user_id
        self.like_type = like_type
        if post_id and user_id and self.type_control():
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection

    def type_control(self):
        if self.like_type in self.accepted_like_types:
            return True
        return False

    def search_like_by_user_id_and_post_id(self):
        self.__cursor.execute("""SELECT id from postlikes WHERE userid =%s AND postid=%s""",[self.user_id,self.post_id])
        post= self.__cursor.fetchone()
        if post:
            self.plid= post[0]
            return True
        else:
            return False


    def get_post_like(self):
        self.__cursor.execute("""SELECT userid,postid,liketype FROM postlikes WHERE id =%s""",[self.plid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.post_id=data[1]
            self.like_type=data[2]

    def get_likes_by_post_id(self,post_id):
        self.__cursor.execute("""SELECT pl.id,u.username,pl.liketype from postlikes as pl JOIN users as u ON pl.userid = u.id WHERE pl.postid= %s """,[post_id])
        return self.__cursor.fetchall()

    def update_like_type(self):
        self.__cursor.execute("""UPDATE postlikes SET liketype =%s WHERE id=%s""",[self.like_type,self.plid])
        self.__connection.commit()

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT INTO postlikes (postid,userid,liketype) VALUES (%s,%s,%s)""",[self.post_id,self.user_id,self.like_type])
            self.__connection.commit()
            
    def delete(self):
        self.__cursor.execute("""DELETE FROM postlikes WHERE id=%s """,[self.plid])
        self.__connection.commit()



