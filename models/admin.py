
class Admin:

    __connection = None
    __cursor = None

    def __init__(self,connection):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

    def get_users(self):
        self.__cursor.execute(
            """SELECT u.id,name,surname,username,mail,city.cityname,school.schoolname,gender.type FROM users AS u JOIN gender ON u.gender = gender.id JOIN school ON u.school = school.id JOIN city ON u.city = city.id""")
        return self.__cursor.fetchall()

    def get_username_by_id(self,user_id):
        self.__cursor.execute("""SELECT username from users WHERE id=%s""",[user_id])
        return self.__cursor.fetchone()



    def del_user(self,user_id):
        username=self.get_username_by_id(user_id=user_id)
        self.__cursor.execute("""DELETE FROM userlogin WHERE username=%s""",[username])
        self.__cursor.execute("""DELETE FROM profilepic WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM follow WHERE follow.follower=%s or following=%s""", [user_id,user_id])
        self.__cursor.execute("""DELETE FROM posts WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM postlikes WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM postcomments WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM interests WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM hiddenposts WHERE userid=%s""", [user_id])
        self.__cursor.execute(
            """DELETE FROM users WHERE id=%s""",[user_id]
        )
    def update_user(self,email,school_id,user_id):
        self.__cursor.execute("""UPDATE users SET mail=%s,school=%s WHERE id=%s""",[email,school_id,user_id])
