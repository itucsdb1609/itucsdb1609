Add POSTS,FOLLOW,PROFILEPICTURE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I create a post object and I fill this with HTML tags

.. code-block:: python

class UserArtist:
    __connection = None
    __cursor = None

    def __init__(self, connection, uaid=None, user_id=None,artist_id=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.user_id =user_id
        self.artist_id =artist_id
        self.uaid= uaid

    def get_artists_of_user(self,user_id):
        self.__cursor.execute(
            """SELECT userartists.id,artistname from userartists JOIN artists ON userartists.artistid = artists.id WHERE userid =%s""",
            [user_id])
        return self.__cursor.fetchall()


    def search_user_artist(self):
        self.__cursor.execute("""SELECT id from userartists WHERE userid=%s AND artistid=%s""",[self.user_id,self.artist_id])
        artist_id=self.__cursor.fetchone()
        if artist_id:
            return True
        else:
            return False

    def save(self):
        if not self.search_user_artist():
            self.__cursor.execute("""INSERT into userartists (userid,artistid) VALUES (%s,%s)""",[self.user_id,self.artist_id])

    def delete(self):
        self.__cursor.execute("""DELETE FROM userartists WHERE id=%s""",[self.uaid])
