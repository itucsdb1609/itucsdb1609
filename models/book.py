
class Book:
    __connection = None
    __cursor = None

    def __init__(self, connection, bid=None, name=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

        self.name = name
        self.bid = bid

    def get_books(self):
        self.__cursor.execute("""SELECT id,bookname from books""")
        return self.__cursor.fetchall()

    def get_book_by_name(self):
        self.__cursor.execute("""SELECT id from books WHERE books.bookname=%s""", [self.name])
        book = self.__cursor.fetchone()
        if book:
            return book
        else:
            return False

    def save(self):
        if not self.get_book_by_name():
            self.__cursor.execute("""INSERT into books (bookname) VALUES (%s)""", [self.name])

    def delete(self):
        self.__cursor.execute("""DELETE FROM books WHERE id=%s""", [self.bid])
