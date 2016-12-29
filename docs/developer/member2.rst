Parts Implemented by EKREM CİHAD CETIN 150110125
================================================

The database is created in the "initialize_db.py" file with default values. The posts and follow tables are implemented while users table which is already created by another member is used. The posts tuples consist of 5 columns: id, userid, date, link, description.
The primary key is "id" and the foreign key is userid in this table. Posts own id is given automatically so it is guaranteed that it is not NULL. Userid can not be NULL because of the definition of it on the HTML and userid can not be NULL because of the reference validation. Date are automatically filled with current time, description can be NULL.But link part is controlled in HTML Validation.

The followers and followings is dependent to follow table. Each follow has to have a followerid and followingid from the users table. In the interface, following a user is made by clicking the FOLLOW button, however if they are already in the table, so UNFOLLOW button is seen in the interface
 And you can change profile picture which adding registered default. In register function, added new profile picture to user. Profile pictures table consist of userid and profilepiclink. So each user has got one profile pic. They can not delete profile picture, they just can delete them.

Profile Picture add

..  code-block:: python
	cursor.execute("""INSERT INTO PROFILEPIC (USERID, LINK) VALUES (1,'http://laelith.fr/Cours/Illus/013-avatar-faceprofil.jpg')""")

Post Add

..  code-block:: python
	cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (3,'2016-11-27 16:05:25','http://images.freeimages.com/images/previews/fcb/feeling-down-at-the-park-1432442.jpg','PARK' )""")

Follow Add
..  code-block:: python
	cursor.execute("""INSERT INTO FOLLOW (FOLLOWER, FOLLOWING) VALUES (6,1)""")

The database operations are done from the "initialize_db_func" function in the server.py file. It takes the argument as operation variable and makes the requested operation. The operation list is:

============== =============
OPERATION      SUB OPERATION
============== =============
listbrands     name,
               industry,
               year,
               website,
               image,
               comment,
               country
listfounders   name,
               surname
listjoint      fname,
               surname,
               bname,
               year,
               industry,
               website,
               description
add_brand
add_founder
delete_brand
delete_founder
edit_brand
edit_founder
============== =============

The sub operations are not taken as a different variable, instead they are gatheren in the same "operation" variable. The sub operation string is splitted with a "-" from the main operation. In the pyton code, it there is a try catch mechanism to split the text.

.. code-block:: python
   splitted = operation.split('-', 1)
   operation = splitted[0]
   #print(splitted)
   try:
      sub_operation = splitted[1]
      make_sub_operation = True
   except:
      #print("Single String, not splitted")
      make_sub_operation = False

The main and sub operation is gathered by this piece of code and the flag is set whether if there will be a sub operation or not. The only sub operations are on the listing phase. After this part, the corresponding operation is done by if-elif-else statements.

.. toctree::
   member2/list
   member2/add
   member2/delete
   member2/update

