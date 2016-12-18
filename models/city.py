
class City:

    __connection = None
    __cursor = None
    savable=False

    def __init__(self, connection,city_name=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.name=city_name

        if city_name and not self.search_city_by_name():
            self.savable=True



    def get_all_cities(self):
        self.__cursor.execute("""SELECT * from city """)
        return self.__cursor.fetchall()

    def search_city_by_name(self):
        self.__cursor.execute("""SELECT id from city WHERE cityname=%s""",[self.name])
        city=self.__cursor.fetchone()
        if city:
            return city
        else:
            return False

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT into city (cityname) VALUES (%s)""",[self.name])
