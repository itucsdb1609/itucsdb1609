from .collage import Collage
from .city import City

class Register:

    __connection= None
    __cursor= None
    savable=True
    error=''
    def __init__(self,connection,name, surname, email, username, city, collage,newcity, newcollage,gender, password,confirm):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

            self.name=name
            self.surname=surname
            self.email=email
            self.username=username
            self.city=city
            self.collage = collage
            self.newcity = newcity
            self.newcollage = newcollage
            self.password =password
            self.gender=gender
            self.confirm=confirm

            if self.name == '' or self.surname == '' or (self.email == '' or self.search_for_email()) or \
                    (self.username == '' or self.search_for_username()) or (self.city == 0 and len(self.newcity) == 0) or (
                    self.collage == 0 and len(self.newcollage) == 0) or self.password != self.confirm:
                self.savable = False


    def search_for_username(self):
        self.__cursor.execute("""SELECT id from users WHERE username =%s""" ,[self.username])
        user = self.__cursor.fetchone()
        if user:
            return True
        else:
            return False
    def search_id_for_username(self):
        self.__cursor.execute("""SELECT id from users WHERE username =%s""" ,[self.username])
        return self.__cursor.fetchone()

    def search_for_email(self):
        self.__cursor.execute("""SELECT id from users WHERE mail =%s""", [self.email])
        user = self.__cursor.fetchone()
        if user:
            return True
        else:
            return False

    def save(self):
        if self.savable:
            if self.city=='0':
                cityO = City(connection=self.__connection,city_name=self.newcity)
                cityO.save()
                self.city=cityO.search_city_by_name()
            if self.collage == '0':
                collageO = Collage(connection=self.__connection, collage_name=self.newcollage)
                collageO.save()
                self.collage = collageO.search_collage_by_name()
            self.__cursor.execute("""INSERT into users (username, name, surname, mail, gender, school, city) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                  [self.username,self.name,self.surname,self.email,self.gender,self.collage,self.city])
            self.__cursor.execute("""INSERT into userlogin (username, password) VALUES (%s,%s) """,[self.username,self.password])
            return True
        return False




