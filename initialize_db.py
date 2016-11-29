def initialize_db_func(cursor):

    #Database for counter
    cursor.execute("""DROP TABLE IF EXISTS COUNTER""")
    cursor.execute("""CREATE TABLE COUNTER (N INTEGER)""")
    cursor.execute("""INSERT INTO COUNTER (N) VALUES (0)""")

    #Table for GENDER
    cursor.execute("""DROP TABLE IF EXISTS GENDER""")
    cursor.execute("""CREATE TABLE GENDER (ID  SERIAL PRIMARY KEY,TYPE character varying(10) NOT NULL )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ('FEMALE' )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ( 'MALE' )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ( 'UNKNOWN' )""")
    #Table for CITY
    cursor.execute("""DROP TABLE IF EXISTS CITY""")
    cursor.execute("""CREATE TABLE CITY (ID  SERIAL PRIMARY KEY,CITYNAME character varying(20) NOT NULL )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ('Istanbul' )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ( 'Ankara' )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ( 'Adana' )""")
     #Table for SCHOOL
    cursor.execute("""DROP TABLE IF EXISTS SCHOOL""")
    cursor.execute("""CREATE TABLE SCHOOL (ID  SERIAL PRIMARY KEY,SCHOOLNAME character varying(50) NOT NULL )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ('ITU' )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ( 'METU' )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ( 'HACETTEPE UNIVERCITY' )""")
    #Table for user login
    cursor.execute("""DROP TABLE IF EXISTS USERLOGIN""")
    cursor.execute("""CREATE TABLE USERLOGIN (USERNAME VARCHAR(50) UNIQUE PRIMARY KEY NOT NULL,
                                              PASSWORD VARCHAR(50) NOT NULL,
                                              LASTLOGIN VARCHAR(50))""")

    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('ali','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('dincer','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('fatih','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('caglar','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('ekrem','password')""")

    #Table for user information
    cursor.execute("""DROP TABLE IF EXISTS USERS""")
    cursor.execute("""CREATE TABLE USERS (USERNAME VARCHAR(50) PRIMARY KEY NOT NULL references USERLOGIN(USERNAME),
                                         NAME VARCHAR(50) NOT NULL,
                                         SURNAME VARCHAR(50) NOT NULL,
                                         MAIL VARCHAR(50) UNIQUE NOT NULL,
                                         GENDER INTEGER  references GENDER(ID),
                                         SCHOOL INTEGER  references SCHOOL(ID),
                                         CITY INTEGER  references CITY(ID))""")

    cursor.execute("""INSERT INTO USERS (USERNAME, NAME, SURNAME, MAIL, GENDER, SCHOOL, CITY) VALUES ('ali',
                                                                                                    'Ali',
                                                                                                    'ERCAN',
                                                                                                    'aliercan@gmail.com',
                                                                                                    2,
                                                                                                    1,
                                                                                                    3)""")


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
