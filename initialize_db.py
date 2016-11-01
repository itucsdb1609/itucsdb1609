def initialize_db_func(cursor):
    
    #Database for counter
    cursor.execute("""DROP TABLE IF EXISTS COUNTER""")
    cursor.execute("""CREATE TABLE COUNTER (N INTEGER)""")
    cursor.execute("""INSERT INTO COUNTER (N) VALUES (0)""")
    
    #Table for main
    cursor.execute("""DROP TABLE IF EXISTS POSTLIST""")
    cursor.execute("""CREATE TABLE POSTLIST (ID CHAR(10) NOT NULL, POSTID INTEGER, POST BYTEA)""")
    cursor.execute("""INSERT INTO POSTLIST (ID,POSTID,POST) VALUES ('12',1,'./Users/ahmetcaglarbayatli/downloads/like.png')""")