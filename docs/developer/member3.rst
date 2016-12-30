Parts Implemented by Ahmet Çağlar BAYATLI - 040100031
================================

Developer Guide

Initialization of database objects hiddenposts, hiddenusers and lastvisits in the initialize_db.py.

Drop and Create Table Queries for hiddenposts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS HIDDENPOSTS CASCADE""")
    cursor.execute("""CREATE TABLE HIDDENPOSTS 
    				(USERID INTEGER  references USERS(ID),
                     POSTID INTEGER PRIMARY KEY UNIQUE references POSTS(ID))""")
    
Drop and Create Table Queries for hiddenusers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS HIDDENUSERS CASCADE""")
    cursor.execute("""CREATE TABLE HIDDENUSERS 
    					(USERID INTEGER  references USERS(ID),
                        USERHID INTEGER references USERS(ID),
                        PRIMARY KEY (USERID, USERHID),
                        CHECK (USERID !=USERHID))""")
    
Drop and Create Table Queries for lastvisits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS LASTVISITS CASCADE""")
    cursor.execute("""CREATE TABLE LASTVISITS 
    					(USERID INTEGER PRIMARY KEY references USERS(ID),
                         DATE character varying(50))""")
                         
All Post Methods of Home Page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All post methods of home page are listed below.

Adding to hiddenposts;

.. code-block:: python
	
	if 'hidepost' in request.form:
        postid = request.form['postid']
        userid = request.form['userid']
        userName = request.form['username']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HIDDENPOSTS(userid, postid) VALUES (%s,%s) """
            cursor.execute(query, (userid, postid))
            connection.commit()
        return redirect(url_for('home_page', user=userName))
                
Adding to hiddenusers;

.. code-block:: python

    elif 'hideuser' in request.form:
        userid = request.form['userid']
        userName = request.form['username']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HIDDENUSERS(userid, userhid) VALUES (%s,%s) """
            cursor.execute(query, (user_id, userid))
            connection.commit()
        return redirect(url_for('home_page', user=userName))
                
Updating the posts;

.. code-block:: python

    elif 'upt' in request.form:
        post = request.form['post']
        desc = request.form['desc']
        userName = request.form['username']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE posts SET description='""" + desc + """' 
            				WHERE id =""" + post + """"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('home_page', user=userName))
                
Deleting from posts;

.. code-block:: python

    elif 'del' in request.form:
        post = request.form['post']
        userName = request.form['username']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM posts where id = """+post+""" and userid= """+str(user_id)+""""""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('home_page', user=userName))
                
Adding to follow;

.. code-block:: python
            
    elif 'follow' in request.form:
        userid = request.form['userid']
        userName = request.form['username']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO FOLLOW (follower, following) VALUES (%s,%s) """
            cursor.execute(query, (user_id, userid))
            connection.commit()
        return redirect(url_for('home_page', user=userName))
    
Operations Without Post Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Operations without post method, which means without needing and form etc. this operations will keep doing their functionalities.

Updating the lastvisits;

.. code-block:: python

	for uid,username,name,surname in allUsers:
        if user==username:
            user_data=[username,name,surname]
            user_id=uid
            userCheck = True
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """select date from lastvisits where userid="""+str(user_id)+""""""
                cursor.execute(query)
                temp = cursor.fetchall()
                for date in temp:
                    lastseen=date[0]
                query = """UPDATE LASTVISITS SET date='"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""' 
                				WHERE userid="""+str(user_id)+""" """
                cursor.execute(query)
                connection.commit()
            break

Selection of Data For Display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To show necessary elements in the home page, some selection operations are used.

Here are selection for posts, profile pictures, suggests etc.

.. code-block:: python

	if user and userCheck:
            interest = Interest(connection=connection)
            user_interests = interest.get_interest_by_user_id(user_id)
            query = """select distinct r.userid, username, name, surname, r.link as linkpro, 
            					r.postid, r.linkpost, date, description 
            			from (select * 
    					 from (select m.mid, uid, m.postid, linkpost, date, description 
    					  from (select l.mid, userid as uid, id as postid, link as linkpost, date, description 
    					   from (select k.id as mid, k.following 
    					    from (select id, following 
    						 from users 
    						 join follow on users.id = follow.follower where users.id = """+ str( user_id ) + """) k 
    						left join hiddenusers on hiddenusers.userhid = k.following where hiddenusers.userid is null 
    																					or hiddenusers.userid!=k.id) l 
    					   join posts on posts.userid = l.following or  posts.userid = l.mid) m 
    				  	  left join hiddenposts on hiddenposts.postid = m.postid where hiddenposts.userid is null) n 
    					 join profilepic on profilepic.userid = n.uid) r 
        				join users on r. userid = users.id order by date desc"""
            cursor.execute(query)
            temp = cursor.fetchall()
            
            if not temp:
                query = """select distinct k.id, k.username, k.name, k.surname, l.link as linkpro, k.postid, 
                								k.link as linkpost, k.date, k.description 
                				from (select m.id, username, name, surname, n.id as postid, link, date, description 
                					from users m 
                					join posts n on m.id=n.userid where m.id = """+str(user_id)+""") k 
                				join profilepic l on l.userid=k.id"""
                cursor.execute(query)
                temp = cursor.fetchall()
            
            for post in temp:
                likes = post_like.get_likes_by_post_id(post[5])
                if likes:
                    posts_likes.update({post[5]: likes})
                else:
                    posts_likes.update({post[5]: False})

                comments = post_comment.get_comments_by_post_id(post[5])
                if comments:
                    posts_comments.update({post[5]: comments})
                else:
                    posts_comments.update({post[5]: False})
                posts.append(post)

            query = """select * from profilepic"""
            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                if user_id==post[0]:
                    user_data.append(post[1])
            
            query = """select userid, username, name, surname, link as linkpro 
            			from(select userid, link 
            			 from (select distinct k.following 
            			  from (select distinct n.following 
            			   from follow m 
            			   join follow n on m.following=n.follower where m.follower="""+str(user_id)+""")k 
            			  left join follow l on l.following=k.following and l.follower="""+str(user_id)+""" 
            			   				where l.follower is null and k.following!="""+str(user_id)+""")p 
            			 join profilepic on p.following=userid) r 
            			join users on users.id=r.userid"""
            cursor.execute(query)
            temp = cursor.fetchall()
            if not temp:
                query = """select * from follow where follower="""+str(user_id)+""""""
                cursor.execute(query)
                temp = cursor.fetchall()
                if not temp:
                    query = """select userid, m.username, m.name, m.surname, link as linkpro 
                    			from (select * from users) m 
                    			join profilepic on m.id=profilepic.userid where m.id!="""+str(user_id)+""" 
                    						ORDER BY RANDOM() LIMIT 5"""
                    cursor.execute(query)
                    temp = cursor.fetchall()
                    for suggest in temp:
                        suggests.append(suggest)
                
            else:
                for suggest in temp:
                    suggests.append(suggest)
                    
        else:
            return render_template('404.html'), 404

As can be seen above lots of control have been done to obtain display elements.

End of Home Page.
