List POSTS,FOLLOW
^^^^^^^^^^^^^^^^^

There are 2 listing code. One for listing the posts, one for listing the following and follower.

.. code-block:: python

    def get_post(self):
        self.__cursor.execute("""SELECT userid,date,link,description FROM posts WHERE id =%s""",[self.postid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.date=data[1]
            self.link=data[2]
            self.description=data[3]

And after that part, the sort string is added to the end of the query. The last line is where the assignment is done:

.. code-block:: python

   if user and not user2:
            query = """select users.id ,posts.id, link, name, surname,date,description from users,posts where username='"""+user+"""' and users.id=posts.userid order by date desc"""

            cursor.execute(query)

            cursor.execute(query)
            temp = cursor.fetchall()

For Follower and Following ... you can see all follower with server side below code.

.. code-block:: python

    if user and not user2:
            query ="""select link,users.username from (select following,users.username from users join follow on users.id=follow.follower where username='"""+user+"""') F, profilepic,users where F.following=profilepic.userid and F.following=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowingpic.append(im)

        if user and not user2:
            query ="""select link,users.username from (select follower,users.username from users join follow on users.id=follow.following where username='"""+user+"""') F, profilepic,users where F.follower=profilepic.userid and F.follower=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowerpic.append(im)

ENd Of List