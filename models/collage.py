
class Collage:

    __connection = None
    __cursor = None
    savable=False

    def __init__(self, connection,collage_name=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.name=collage_name

        if collage_name and not self.search_collage_by_name():
            self.savable=True



    def get_all_collages(self):
        self.__cursor.execute("""SELECT * from school """)
        return self.__cursor.fetchall()

    def search_collage_by_name(self):
        self.__cursor.execute("""SELECT id from school WHERE school.schoolname=%s""",[self.name])
        collage=self.__cursor.fetchone()
        if collage:
            return collage
        else:
            return False

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT into school (schoolname) VALUES (%s)""",[self.name])
