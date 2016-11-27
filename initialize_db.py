def initialize_db_func(cursor):

    #Database for counter
    cursor.execute("""DROP TABLE IF EXISTS COUNTER""")
    cursor.execute("""CREATE TABLE COUNTER (N INTEGER)""")
    cursor.execute("""INSERT INTO COUNTER (N) VALUES (0)""")

 #==============================================================================
 #    #Table for users
 #    cursor.execute("""DROP TABLE IF EXISTS USER""")
 #    cursor.execute("""CREATE TABLE USER (USERNAME CHAR(20) UNIQUE PRIMARY KEY NOT NULL, PASSWORD CHAR(20) )""")
 #
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('user','pass')""")
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('aliercccan','pass')""")
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('dincer','pass')""")
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('fatih','pass')""")
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('caglar','pass')""")
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('ekrem','pass')""")
 #
 #    #Table for admins
 #    cursor.execute("""DROP TABLE IF EXISTS ADMIN""")
 #    cursor.execute("""CREATE TABLE ADMIN (USERNAME CHAR(20) UNIQUE PRIMARY KEY NOT NULL, Password CHAR(20) )""")
 #
 #    cursor.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES ('admin','admin')""")
 #    cursor.execute("""INSERT INTO ADMIN (USERNAME, PASSWORD) VALUES ('aliercccan','admin')""")
 #    cursor.execute("""INSERT INTO ADMIN (USERNAME, PASSWORD) VALUES ('fatih','admin')""")
 #==============================================================================

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