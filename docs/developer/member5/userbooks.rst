userbooks
^^^^^^^^^

I create a post object and I fill this with HTML tags

.. code-block:: python


class UserBooks:
    __connection = None
    __cursor = None

    def __init__(self, connection, ubid=None, user_id=None,book_id=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        self.user_id =user_id
        self.book_id =book_id
        self.ubid= ubid

    def get_books_of_user(self,user_id):
        self.__cursor.execute(
            """SELECT userbooks.id,bookname from userbooks JOIN books ON userbooks.bookid = books.id WHERE userid =%s""",
            [user_id])
        return self.__cursor.fetchall()


    def search_user_book(self):
        self.__cursor.execute("""SELECT id from userbooks WHERE userid=%s AND bookid=%s""",[self.user_id,self.book_id])
        book=self.__cursor.fetchone()
        if book:
            return True
        else:
            return False

    def save(self):
        if not self.search_user_book():
            self.__cursor.execute("""INSERT into userbooks (userid,bookid) VALUES (%s,%s)""",[self.user_id,self.book_id])

    def delete(self):
        self.__cursor.execute("""DELETE FROM userartists WHERE id=%s""",[self.ubid])

