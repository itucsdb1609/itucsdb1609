
class Login:

    __connection = None
    __cursor = None
    def __init__(self,username,password,connection):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
            self.username=username
            self.password=password

    def authenticator(self):
        self.__cursor.execute("""SELECT username,admin from userlogin WHERE username=%s AND password=%s """,[self.username,self.password])
        user = self.__cursor.fetchone()
        if user:
            return user
        else:
            return False
