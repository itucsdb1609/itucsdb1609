def initialize_db_func(cursor):

    #Database for counter
    cursor.execute("""DROP TABLE IF EXISTS COUNTER""")
    cursor.execute("""CREATE TABLE COUNTER (N INTEGER)""")
    cursor.execute("""INSERT INTO COUNTER (N) VALUES (0)""")

    #Table for user login
    cursor.execute("""DROP TABLE IF EXISTS USERLOGIN""")
    cursor.execute("""CREATE TABLE USERLOGIN (USERNAME VARCHAR(50) UNIQUE PRIMARY KEY NOT NULL,
                                              PASSWORD VARCHAR(50) NOT NULL, 
                                              LASTLOGIN VARCHAR(50))""")

    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('ali','ali')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('dincer','dincer')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('fatih','fatih')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('caglar','caglar')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('ekrem','ekrem')""")

    #Table for user information
    cursor.execute("""DROP TABLE IF EXISTS USERS""")
    cursor.execute("""CREATE TABLE USERS (USERNAME VARCHAR(50) UNIQUE PRIMARY KEY NOT NULL,
                                         NAME VARCHAR(50) NOT NULL,
                                         SURNAME VARCHAR(50) NOT NULL,
                                         MAIL VARCHAR(50) UNIQUE NOT NULL,
                                         SEX INTEGER NOT NULL,
                                         SCHOOL INTEGER NOT NULL,
                                         CITY INTEGER NOT NULL)""")

    #Table for main
    cursor.execute("""DROP TABLE IF EXISTS PostForView""")
    cursor.execute("""CREATE TABLE PostForView(ID CHAR(20) NOT NULL, FID CHAR(20), POSTID Char(10) )""")
    cursor.execute("""INSERT INTO PostForView (ID, FID, POSTID) VALUES ('2', '5', '1' )""")
    cursor.execute("""INSERT INTO PostForView (ID, FID, POSTID) VALUES ('2', '3', '4' )""")

    #Table for explore
    cursor.execute("""DROP TABLE IF EXISTS hashTag""")
    cursor.execute("""CREATE TABLE hashTag (HASHID CHAR(20) NOT NULL, GRUPNAME CHAR(20) )""")
    cursor.execute("""INSERT INTO hashTag (HASHID, GRUPNAME) VALUES ('2', 'NATURE' )""")
    cursor.execute("""INSERT INTO hashTag (HASHID, GRUPNAME) VALUES ('5', 'FUTBOL')""")
    cursor.execute("""INSERT INTO hashTag (HASHID, GRUPNAME) VALUES ('6', 'NATURE' )""")
    cursor.execute("""INSERT INTO hashTag (HASHID, GRUPNAME) VALUES ('9', 'ART')""")

    #Table for Profile-picture-post
    cursor.execute("""DROP TABLE IF EXISTS picPost""")
    cursor.execute("""CREATE TABLE picPost (PicId  SERIAL PRIMARY KEY,Description CHAR(20) )""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('School')""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('With My Friends')""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('Enjoy')""")
    #Table for IMAGES
    cursor.execute("""DROP TABLE IF EXISTS IMAGES""")
    cursor.execute("""CREATE TABLE IMAGES (ID  SERIAL PRIMARY KEY,IMAGE character varying(255) NOT NULL )""")
