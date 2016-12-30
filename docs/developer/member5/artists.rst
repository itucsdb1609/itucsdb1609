Add POSTS,FOLLOW,PROFILEPICTURE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I create a post object and I fill this with HTML tags

.. code-block:: python


class Artists:
    __connection = None
    __cursor = None

    def __init__(self, connection, aid=None, name=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

        self.name = name
        self.aid = aid

    def get_artists(self):
        self.__cursor.execute("""SELECT id,artistname from artists""")
        return self.__cursor.fetchall()

    def get_artist_by_name(self):
        self.__cursor.execute("""SELECT id from artists WHERE artists.artistname=%s""", [self.name])
        artist = self.__cursor.fetchone()
        if artist:
            return artist
        else:
            return False

    def save(self):
        if not self.get_artist_by_name():
            self.__cursor.execute("""INSERT into artists (artistname) VALUES (%s)""", [self.name])

    def delete(self):
        self.__cursor.execute("""DELETE FROM artists WHERE id=%s""", [self.aid])



