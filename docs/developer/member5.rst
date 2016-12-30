Parts Implemented by Mehmet Dinçer Bozdoğan 040080222
================================================

The database is created in the "initialize_db.py" file with default values. The posts and follow tables are implemented while users table which is already created by another member is used. The posts tuples consist of 5 columns: id, userid, date, link, description.
The primary key is "id" and the foreign key is userid in this table. Posts own id is given automatically so it is guaranteed that it is not NULL. Userid can not be NULL because of the definition of it on the HTML and userid can not be NULL because of the reference validation. Date are automatically filled with current time, description can be NULL.But link part is controlled in HTML Validation.

The followers and followings is dependent to follow table. Each follow has to have a followerid and followingid from the users table. In the interface, following a user is made by clicking the FOLLOW button, however if they are already in the table, so UNFOLLOW button is seen in the interface
 And you can change profile picture which adding registered default. In register function, added new profile picture to user. Profile pictures table consist of userid and profilepiclink. So each user has got one profile pic. They can not delete profile picture, they just can delete them.



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



.. toctree::
   member5/hashtag
   member5/posthashtag
   member5/book
   member5/userbooks
   member5/artists
   member6/userartists

