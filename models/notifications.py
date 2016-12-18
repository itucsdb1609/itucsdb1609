
class Notifications:

    __connection = None
    __cursor = None
    user_id = None
    search = None
    def __init__(self,username,connection):
        self.__connection = connection
        self.__cursor=connection.cursor()
        if username:
            self.username=username
            self.get_user_id()
        if self.user_id:
            self.search=True

    def get_all_likes(self):
        if self.search:
            self.__cursor.execute("""SELECT u.username,p.link from postlikes as pl JOIN users as u on pl.userid=u.id JOIN posts as p on pl.postid=p.id WHERE p.userid=%s ORDER BY pl.id desc""",[self.user_id])
            return self.__cursor.fetchall()

    def get_all_comments(self):
        if self.search:
            self.__cursor.execute(
                """SELECT u.username,p.link from postcomments as pc JOIN users as u on pc.userid=u.id JOIN posts as p on pc.postid=p.id WHERE p.userid=%s ORDER BY pc.id desc""",
                [self.user_id])
            return self.__cursor.fetchall()

    def get_user_id(self):
        self.__cursor.execute("""SELECT id from users WHERE username=%s""",[self.username])
        uid=self.__cursor.fetchone()
        if uid:
            self.user_id=uid
