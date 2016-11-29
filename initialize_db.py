def initialize_db_func(cursor):

    #Database for counter
    cursor.execute("""DROP TABLE IF EXISTS COUNTER""")
    cursor.execute("""CREATE TABLE COUNTER (N INTEGER)""")
    cursor.execute("""INSERT INTO COUNTER (N) VALUES (0)""")

    #Table for GENDER
    cursor.execute("""DROP TABLE IF EXISTS GENDER CASCADE""")
    cursor.execute("""CREATE TABLE GENDER (ID  SERIAL PRIMARY KEY,TYPE character varying(10) NOT NULL )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ('FEMALE' )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ( 'MALE' )""")
    cursor.execute("""INSERT INTO GENDER ( TYPE) VALUES ( 'UNKNOWN' )""")
    #Table for CITY
    cursor.execute("""DROP TABLE IF EXISTS CITY CASCADE""")
    cursor.execute("""CREATE TABLE CITY (ID  SERIAL PRIMARY KEY,CITYNAME character varying(20) NOT NULL )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ('Istanbul' )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ( 'Ankara' )""")
    cursor.execute("""INSERT INTO CITY ( CITYNAME) VALUES ( 'Adana' )""")
     #Table for SCHOOL
    cursor.execute("""DROP TABLE IF EXISTS SCHOOL CASCADE""")
    cursor.execute("""CREATE TABLE SCHOOL (ID  SERIAL PRIMARY KEY,SCHOOLNAME character varying(50) NOT NULL )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ('ITU' )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ( 'METU' )""")
    cursor.execute("""INSERT INTO SCHOOL ( SCHOOLNAME) VALUES ( 'HACETTEPE UNIVERCITY' )""")
    #Table for user information
    cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
    cursor.execute("""CREATE TABLE USERS (ID SERIAL PRIMARY KEY UNIQUE,
                                          USERNAME VARCHAR(50) UNIQUE NOT NULL ,
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
    cursor.execute("""INSERT INTO USERS (USERNAME, NAME, SURNAME, MAIL, GENDER, SCHOOL, CITY) VALUES ('dincer',
                                                                                                    'DINCER',
                                                                                                    'ADANALI',
                                                                                                    'dincertarbil@gmail.com',
                                                                                                    2,
                                                                                                    1,
                                                                                                    2)""")
    cursor.execute("""INSERT INTO USERS (USERNAME, NAME, SURNAME, MAIL, GENDER, SCHOOL, CITY) VALUES ('seda',
                                                                                                    'SEDA',
                                                                                                    'TIPCI',
                                                                                                    'sedamedipol@gmail.com',
                                                                                                    1,
                                                                                                    3,
                                                                                                    1)""")


    #Table for user login
    cursor.execute("""DROP TABLE IF EXISTS USERLOGIN CASCADE""")
    cursor.execute("""CREATE TABLE USERLOGIN (USERNAME VARCHAR(50)  PRIMARY KEY  references users(username),
                                               PASSWORD VARCHAR(50) NOT NULL,
                                               LASTLOGIN VARCHAR(50))""")

    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('ali','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('dincer','password')""")
    cursor.execute("""INSERT INTO USERLOGIN (USERNAME, PASSWORD) VALUES ('seda','password')""")



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

    #Table for picture-post//not active just trying
    cursor.execute("""DROP TABLE IF EXISTS picPost""")
    cursor.execute("""CREATE TABLE picPost (PicId  SERIAL PRIMARY KEY,Description CHAR(20) )""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('School')""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('With My Friends')""")
    cursor.execute("""INSERT INTO picPost ( Description) VALUES ('Enjoy')""")
    #Table for Profil PICTURE
    cursor.execute("""DROP TABLE IF EXISTS PROFILEPIC CASCADE""")
    cursor.execute("""CREATE TABLE PROFILEPIC (USERID INTEGER PRIMARY KEY references USERS(ID),LINK character varying(255) NOT NULL )""")
    cursor.execute("""INSERT INTO PROFILEPIC (USERID, LINK) VALUES (1,'http://laelith.fr/Cours/Illus/013-avatar-faceprofil.jpg')""")
    cursor.execute("""INSERT INTO PROFILEPIC (USERID, LINK) VALUES (2,'http://laelith.fr/Cours/Illus/013-Me.jpg' )""")
    cursor.execute("""INSERT INTO PROFILEPIC (USERID, LINK) VALUES (3,'http://laelith.fr/Cours/Illus/013-Exercice2.png' )""")
     #Table for POST table
    cursor.execute("""DROP TABLE IF EXISTS POSTS CASCADE""")
    cursor.execute("""CREATE TABLE POSTS (ID SERIAL PRIMARY KEY UNIQUE,
                                            USERID INTEGER  references USERS(ID),
                                            DATE character varying(50) ,
                                            LINK character varying(255) NOT NULL,
                                            DESCRIPTION character varying(255))""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (3,'28.11.2016','https://cdn.pixabay.com/photo/2015/12/01/20/28/green-1072828__340.jpg','GREEN' )""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (1,'26.11.2016','https://cdn.pixabay.com/photo/2016/11/25/15/14/baffin-island-1858603__340.jpg','BAFFIN ISLAND' )""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (3,'28.11.2016','https://cdn.pixabay.com/photo/2016/11/23/14/51/clouds-1853340__340.jpg','ANGRY CLOUDS' )""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (2,'29.11.2016','https://cdn.pixabay.com/photo/2016/11/18/15/26/gull-1835351__340.jpg','GULL' )""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (3,'25.11.2016','https://cdn.pixabay.com/photo/2015/09/22/23/42/tibet-952688__340.jpg','TIBET' )""")
    cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (2,'28.11.2016','https://cdn.pixabay.com/photo/2015/08/29/18/53/sunset-913350__340.jpg','SUNSET' )""")
