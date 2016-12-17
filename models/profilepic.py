
class ProfilePic:
    __connection= None
    __cursor= None
    savable =False
    def __init__(self,picid=None,connection=None,link=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if picid:
            self.picid = picid
            self.get_picture()
        self.link = link

        if link and picid:
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection



    def get_picture(self):
        self.__cursor.execute("""SELECT link FROM PROFILEPIC WHERE userid =%s""",[self.picid])
        data= self.__cursor.fetchone()
        if data:
            self.link=data[0]


    def update_pic(self):
        self.__cursor.execute("""UPDATE profilepic SET link=%s WHERE userid =%s""",[self.link,self.picid])
        self.__connection.commit()

    def save(self):
        self.__cursor.execute("""INSERT INTO profilepic (USERID,LINK) VALUES (%s,%s)""",[self.picid, self.link])

    def delete(self):
        self.__cursor.execute("""DELETE FROM profilepic WHERE userid =%s""",[self.picid])
        self.__connection.commit()


