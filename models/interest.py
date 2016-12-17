
class Interest:

    __connection= None
    __cursor= None
    savable =False
    def __init__(self,iid=None,connection=None,interest_name=None,user_id=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if iid:
            self.iid = iid
            self.get_interest()
        self.user_id= user_id
        self.interest_name = interest_name
        if user_id and len(interest_name)> 0 and not self.interest_control_by_user_id_and_interest_name():
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection


    def get_interest_by_user_id_and_interest(self):
        self.__cursor.execute("""SELECT id from interests WHERE userid =%s AND interests.interest=%s ORDER BY id desc limit 1""",[self.user_id,self.interest_name])
        interest= self.__cursor.fetchone()
        if interest:
            self.iid= interest[0]
            return True
        else:
            return False


    def get_interest(self):
        self.__cursor.execute("""SELECT userid,interest FROM interests WHERE id =%s""",[self.iid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.interest_name=data[1]

    def get_interest_by_user_id(self,user_id):
        self.__cursor.execute("""SELECT i.id,i.interest from interests as i JOIN users as u ON i.userid = u.id WHERE i.userid= %s ORDER BY i.id ASC """,[user_id])
        return self.__cursor.fetchall()

    def interest_control_by_user_id_and_interest_name(self):
        self.__cursor.execute(
            """SELECT id from interests WHERE userid= %s AND interest=%s """,[self.user_id,self.interest_name])
        interest= self.__cursor.fetchone()
        if interest:
            return True
        else:
            return False


    def update_interest(self,new_name):
        if new_name != self.interest_name:
            self.__cursor.execute("""UPDATE interests SET interest=%s WHERE id=%s""",[new_name,self.iid])
            self.__connection.commit()

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT INTO interests (userid,interest) VALUES (%s,%s)""",[self.user_id,self.interest_name])

    def delete(self):
        self.__cursor.execute("""DELETE FROM interests WHERE id=%s """,[self.iid])
        self.__connection.commit()


