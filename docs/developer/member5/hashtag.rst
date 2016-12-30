Hashtags
^^^^^^^^

I create a post object and I fill this with HTML tags


.. code-block:: python

class Hashtag:
    __connection = None
    __cursor = None

    def __init__(self, connection,hid=None, name=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.name = name
        self.hid = hid

    def get_hashtags(self):
        self.__cursor.execute("""SELECT id,hashtagname from hashtag""")
        return self.__cursor.fetchall()


    def get_hashtag_by_name(self):
        self.__cursor.execute("""SELECT id from hashtag WHERE hashtagname=%s""",[self.name])
        hashtag= self.__cursor.fetchone()
        if hashtag:
            return hashtag
        else:
            return False

    def save(self):
        if not self.get_hashtag_by_name():
            self.__cursor.execute("""INSERT into hashtag (hashtagname) VALUES (%s)""",[self.name])

    def delete(self):
        self.__cursor.execute("""DELETE FROM hashtag WHERE id=%s""", [self.hid])