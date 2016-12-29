Parts Implemented by EKREM CİHAD CETIN 150110125
================================================

The database is created in the "initialize_db.py" file with default values. The posts and follow tables are implemented while users table which is already created by another member is used. The posts tuples consist of 5 columns: id, userid, date, link, description.
The primary key is "id" and the foreign key is userid in this table. Posts own id is given automatically so it is guaranteed that it is not NULL. Userid can not be NULL because of the definition of it on the HTML and userid can not be NULL because of the reference validation. Date are automatically filled with current time, description can be NULL.But link part is controlled in HTML Validation.

The followers and followings is dependent to follow table. Each follow has to have a followerid and followingid from the users table. In the interface, following a user is made by clicking the FOLLOW button, however if they are already in the table, so UNFOLLOW button is seen in the interface
 And you can change profile picture which adding registered default. In register function, added new profile picture to user. Profile pictures table consist of userid and profilepiclink. So each user has got one profile pic. They can not delete profile picture, they just can delete them.



Profile Picture add

.. code-block:: python

   cursor.execute("""INSERT INTO PROFILEPIC (USERID, LINK) VALUES (1,'http://laelith.fr/Cours/Illus/013-avatar-faceprofil.jpg')""")

Post Add

.. code-block:: python

   cursor.execute("""INSERT INTO POSTS (USERID, DATE,LINK,DESCRIPTION) VALUES (3,'2016-11-27 16:05:25','http://images.freeimages.com/images/previews/fcb/feeling-down-at-the-park-1432442.jpg','PARK' )""")

Follow Add

.. code-block:: python

   cursor.execute("""INSERT INTO FOLLOW (FOLLOWER, FOLLOWING) VALUES (6,1)""")

The database operations are done from the "initialize_db_func" function in the server.py file. It takes the argument as operation variable and makes the requested operation. The operation list is:

=================== ===================
OPERATION      		SUB OPERATION
=================== ===================
users				username,
					name,
					surname,
					mail,
					gender,
               		school,
               		city
listposts      		id,userid,link,
               		date,
               		description
listfollewer   		followerid,
               		followingid
listfollewing  		followerid,
               		followingid
add_post
add_profilepic
add_follower
add_following
delete_post
delete_follower
delete_following
update_post
update_profilepic
=================== ===================

The sub operations are not taken as a different variable, instead they are gatheren in the same "operation" variable. The sub operation string is splitted with a "-" from the main operation. In the pyton code, it there is a try catch mechanism to split the text.

.. code-block:: python

   <form class="form-horizontal" method="post" >

		<div class="form-group" style="margin-top:50px ">
		 	<input type = "hidden" name="id" value={{id}}>
		 	<input type = "hidden" name="username" value={{username}}>
			<label class="control-label col-sm-2 col-xs-2 col-md-2 col-lg-2" for="pwd">Image Url:</label>
			<div class="col-xs-10 col-sm-10 col-md-10 col-lg-10" >
				<input type="text" name="ADD"   class="form-control" id="pwd" placeholder="Enter Image Url" required oninvalid="setCustomValidity('Please fill out this field')" oninput="setCustomValidity('')">

			</div>
			<hr>
			<div class="col-xs-offset-2 col-xs-10 col-sm-offset-2 col-sm-10 col-md-offset-2 col-md-10 col-lg-offset-2 col-lg-10">
				<a href="https://hizliresim.com/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:231px;">
					<span class="glyphicon glyphicon-download"></span> Take link from "Hızlı Resim"
				</a>
				<a href="http://resimyukle.xyz/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:231px;">
					<span class="glyphicon glyphicon-download"></span> Take link from "Resim Yukle"
				</a>
				<a href="https://postimage.org/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:231px;">
					<span class="glyphicon glyphicon-download"></span> Take link from "PostImage"
				</a>
			</div>
			<hr><br>
			<div>
				<label class="control-label col-xs-2 col-sm-2 col-md-2 col-lg-2" for="pwd">Description:</label>
				<div class="col-xs-10 col-sm-10 col-md-10 col-lg-10" >
					<input type="text" name="DESC"   class="form-control" id="pwd" placeholder="Enter Description" >
				</div>
			</div>
			<hr><br>
			<div class="col-xs-offset-2 col-xs-10 col-sm-offset-2 col-sm-10 col-md-offset-2 col-md-10 col-lg-offset-2 col-lg-10">
				<button type="submit" class="btn btn-default" name="EKLE">Add</button>
			</div>
	 	</div>

	</form>

.. toctree::
   member2/list
   member2/add
   member2/delete
   member2/update

