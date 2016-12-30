Posthashtags
^^^^^^^^^^^^

I create a post object and I fill this with HTML tags

.. code-block:: python


class PostHashtag:
    __connection = None
    __cursor = None

    def __init__(self, connection, phid=None, hashtag_id=None,post_id=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.hashtag_id =hashtag_id
        self.post_id =post_id
        self.phid= phid

    def get_hashtags_of_post(self,post_id):
        self.__cursor.execute("""SELECT posthashtags.id,hashtag.hashtagname from posthashtags JOIN hashtag ON posthashtags.hashtagid = hashtag.id JOIN posts ON posthashtags.postid = posts.id WHERE postid=%s""",[post_id])
        return self.__cursor.fetchall()

    def get_posts_of_hashtag(self,hashtag_id,limit=None):
        query=""
        if limit:
            query=" limit 1"
        self.__cursor.execute(
            """SELECT posthashtags.id,posts.link,hashtag.hashtagname from posthashtags JOIN hashtag ON posthashtags.hashtagid = hashtag.id JOIN posts ON posthashtags.postid = posts.id WHERE hashtagid=%s"""+query,
            [hashtag_id])
        if limit:
            return self.__cursor.fetchone()
        return self.__cursor.fetchall()


    def search_post_hashtag(self):
        self.__cursor.execute("""SELECT id from posthashtags WHERE postid=%s AND hashtagid=%s""",[self.post_id,self.hashtag_id])
        posthashtag=self.__cursor.fetchone()
        if posthashtag:
            return True
        else:
            return False

    def save(self):
        if not self.search_post_hashtag():
            self.__cursor.execute("""INSERT into posthashtags (postid,hashtagid) VALUES (%s,%s)""",[self.post_id,self.hashtag_id])

    def delete(self):
        self.__cursor.execute("""DELETE FROM posthashtags WHERE id=%s""",[self.phid])
