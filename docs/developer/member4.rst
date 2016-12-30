Parts Implemented by Fatih Deniz
================================
INTERESTS OPERATIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is a subdirectory "interest.py" under "models" directory and interests operations are implemented here. Below code block shows how interest field is created and controlled via userid. After a user is connected they can save new interests.

.. code-block:: python

   class Interest:

    __connection= None
    __cursor= None
    savable =False
    def __init__(self,iid=None,connection=None,interest_name=None,user_id=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if iid:
            self.iid = iid
            self.get_interest()
        self.user_id= user_id
        self.interest_name = interest_name
        if user_id and len(interest_name)> 0 and not self.interest_control_by_user_id_and_interest_name():
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection

Here, you can see how added interests are fetched:

.. code-block:: python

    def get_interest_by_user_id_and_interest(self):
        self.__cursor.execute("""SELECT id from interests WHERE userid =%s AND interests.interest=%s ORDER BY id desc limit 1""",[self.user_id,self.interest_name])
        interest= self.__cursor.fetchone()
        if interest:
            self.iid= interest[0]
            return True
        else:
            return False


    def get_interest(self):
        self.__cursor.execute("""SELECT userid,interest FROM interests WHERE id =%s""",[self.iid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.interest_name=data[1]

    def get_interest_by_user_id(self,user_id):
        self.__cursor.execute("""SELECT i.id,i.interest from interests as i JOIN users as u ON i.userid = u.id WHERE i.userid= %s ORDER BY i.id ASC """,[user_id])
        return self.__cursor.fetchall()

    def interest_control_by_user_id_and_interest_name(self):
        self.__cursor.execute(
            """SELECT id from interests WHERE userid= %s AND interest=%s """,[self.user_id,self.interest_name])
        interest= self.__cursor.fetchone()
        if interest:
            return True
        else:
            return False
            
            
Update operation for interests is handled in the following code block. Here if you change your interest with another name, it becomes your new updated interest.

.. code-block:: python

    def update_interest(self,new_name):
        if new_name != self.interest_name:
            self.__cursor.execute("""UPDATE interests SET interest=%s WHERE id=%s""",[new_name,self.iid])
            self.__connection.commit()

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT INTO interests (userid,interest) VALUES (%s,%s)""",[self.user_id,self.interest_name])

Delete interest is implemented here, if you use delete button on your interest, it will be deleted via its interest id.

.. code-block:: python

    def delete(self):
        self.__cursor.execute("""DELETE FROM interests WHERE id=%s """,[self.iid])
        self.__connection.commit()

Interest operations on "server.py" is shown below: New interest, delete interest, update interest

.. code-block:: python

      elif 'newInterest' in request.form:
          new_interest=Interest(interest_name=request.form['interestName'],user_id=user_id,connection=connection)
          new_interest.save()
      elif 'deleteInterest' in request.form:
          new_interest = Interest(iid=request.form['deleteInterest'], connection=connection)
          new_interest.delete()
      elif 'updateInterest' in request.form:
          interest = Interest(iid=request.form['updateInterest'],connection=connection)
          interest.update_interest(request.form['updatedName'])
           
End of Interests

LIKE OPERATIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is a subdirectory "postLikes.py" under "models" directory and like operations are implemented here. Below code block shows how like operations are handled.

Here, there are four like types are created to give users different options to like. Two key are kept to control likes: userid and postid, also like type is kept and post like id is primary key here. If a user press one of the other like buttons, that like type is updated with the last one.

.. code-block:: python

   class PostLike:

    __connection= None
    __cursor= None
    savable =False
    accepted_like_types= ['heart', 'thumbs-up', 'thumbs-down', 'frown-o']
    def __init__(self,plid=None,connection=None,post_id=None,user_id=None,like_type=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if plid:
            self.plid = plid
            self.get_post_like()
        self.post_id= post_id
        self.user_id= user_id
        self.like_type = like_type
        if post_id and user_id and self.type_control():
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection

    def type_control(self):
        if self.like_type in self.accepted_like_types:
            return True
        return False

    def search_like_by_user_id_and_post_id(self):
        self.__cursor.execute("""SELECT id from postlikes WHERE userid =%s AND postid=%s""",[self.user_id,self.post_id])
        post= self.__cursor.fetchone()
        if post:
            self.plid= post[0]
            return True
        else:
            return False


    def get_post_like(self):
        self.__cursor.execute("""SELECT userid,postid,liketype FROM postlikes WHERE id =%s""",[self.plid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.post_id=data[1]
            self.like_type=data[2]

    def get_likes_by_post_id(self,post_id):
        self.__cursor.execute("""SELECT pl.id,u.username,pl.liketype from postlikes as pl JOIN users as u ON pl.userid = u.id WHERE pl.postid= %s """,[post_id])
        return self.__cursor.fetchall()

Here, updating of like type is implemented. Like type is updated with the new one.

.. code-block:: python

    def update_like_type(self):
        self.__cursor.execute("""UPDATE postlikes SET liketype =%s WHERE id=%s""",[self.like_type,self.plid])
        self.__connection.commit()

    def save(self):
        if self.savable:
            self.__cursor.execute("""INSERT INTO postlikes (postid,userid,liketype) VALUES (%s,%s,%s)""",[self.post_id,self.user_id,self.like_type])
            self.__connection.commit()

Unlike operation is implemented here, if a user press the delete button, plid is deleted from postlikes table. 

.. code-block:: python

    def delete(self):
        self.__cursor.execute("""DELETE FROM postlikes WHERE id=%s """,[self.plid])
        self.__connection.commit()
        
Like and unlike operations on "server.py" is shown below:

.. code-block:: python

      elif 'like' in request.form:
          post_id = request.form['postId']
          like_type = request.form['like']
          new_like = PostLike(post_id=post_id, user_id=user_id, like_type=like_type, connection=connection)
          if not new_like.search_like_by_user_id_and_post_id():
              new_like.save()
       else:
           new_like.update_like_type()
           
 .. code-block:: python
   
         elif 'unlike' in request.form:
          like = PostLike(plid=request.form['unlike'], connection=connection)
          like.delete()

End of Like Operations

COMMENT OPERATIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is a subdirectory "postComments.py" under "models" directory and comment operations are implemented here. Below code block shows how comment operations are handled.

Here, there are four elements for comments are used: id of the comment, id of the post, id of the user and comment itself.

.. code-block:: python

    class PostComments:

    __connection= None
    __cursor= None
    savable =False
    def __init__(self,pcid=None,connection=None,post_id=None,user_id=None,comment=None):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
        if pcid:
            self.pcid = pcid
            self.get_post_comment()
        self.post_id= post_id
        self.user_id= user_id
        self.comment = comment
        if post_id and user_id and len(comment)> 0:
            self.savable = True

    def connection_getter(self,connection):
        self.__connection = connection

Fetching comments is implemented as followings. Comments, their posts and their users are kept to use later operations like showing these actions on "notifications page" or "show comments". 

.. code-block:: python

    def get_comment_by_user_id_and_post_id(self):
        self.__cursor.execute("""SELECT id,comment from postcomments WHERE userid =%s AND postid=%s ORDER BY id desc limit 1""",[self.user_id,self.post_id])
        post= self.__cursor.fetchone()
        if post:
            self.pcid= post[0]
            return  post[1]
        else:
            return False


    def get_post_comment(self):
        self.__cursor.execute("""SELECT userid,postid,comment FROM postcomments WHERE id =%s""",[self.pcid])
        data= self.__cursor.fetchone()
        if data:
            self.user_id=data[0]
            self.post_id=data[1]
            self.comment=data[2]

    def get_comments_by_post_id(self,post_id):
        self.__cursor.execute("""SELECT pc.id,u.username,pc.comment from postcomments as pc JOIN users as u ON pc.userid = u.id WHERE pc.postid= %s ORDER BY pc.id ASC """,[post_id])
        return self.__cursor.fetchall()


Here delete comment operation is implemented. This can be done by deleting id of that comment from the postcomments table.

.. code-block:: python
 
    def delete(self):
        self.__cursor.execute("""DELETE FROM postcomments WHERE id=%s """,[self.pcid])
        self.__connection.commit()

Comment operations on "server.py" is shown below:

.. code-block:: python

      elif 'saveComment' in request.form:
          post_id = request.form['postId']
          comment =request.form['comment']
          new_comment = PostComments(post_id=post_id, user_id=user_id, comment=comment, connection=connection)
          saved_comment=new_comment.get_comment_by_user_id_and_post_id()
          if saved_comment!=comment:
              new_comment.save()
           
 .. code-block:: python
   
         elif 'uncomment' in request.form:
             comment = PostComments(pcid=request.form['uncomment'], connection=connection)
             comment.delete()

End of Comment Operations

NOTIFICATIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is a subdirectory "notifications.py" under "models" directory and notifications are handled here. Below code block shows the implemetation details.

.. code-block:: python

    class Notifications:

    __connection = None
    __cursor = None
    user_id = None
    search = None
    def __init__(self,username,connection):
        self.__connection = connection
        self.__cursor=connection.cursor()
        if username:
            self.username=username
            self.get_user_id()
        if self.user_id:
            self.search=True

Here, all the likes for a user is getting to be listed on likes column of the notifications page.

.. code-block:: python

    def get_all_likes(self):
        if self.search:
            self.__cursor.execute("""SELECT u.username,p.link from postlikes as pl JOIN users as u on pl.userid=u.id JOIN posts as p on pl.postid=p.id WHERE p.userid=%s ORDER BY pl.id desc""",[self.user_id])
            return self.__cursor.fetchall()

And all comments for a user are getting here to be listed on comments column of the notifications page.

.. code-block:: python

    def get_all_comments(self):
        if self.search:
            self.__cursor.execute(
                """SELECT u.username,p.link from postcomments as pc JOIN users as u on pc.userid=u.id JOIN posts as p on pc.postid=p.id WHERE p.userid=%s ORDER BY pc.id desc""",
                [self.user_id])
            return self.__cursor.fetchall()

User can also go to the profile page of the user who likes or comments and for this, keeping user id operation is implemented.

.. code-block:: python

    def get_user_id(self):
        self.__cursor.execute("""SELECT id from users WHERE username=%s""",[self.username])
        uid=self.__cursor.fetchone()
        if uid:
            self.user_id=uid
            
In "server.py" , notification is defined as follow. Session is used and if a logged-in user can see their notifications on the notification page. First, the list of comments and likes are empty. After getting likes and comments using the functions get_all_comments() and get_all_likes() the list is filled and those likes and comments can be listed.            
 
.. code-block:: python

   @app.route('/notification', methods = ['GET','POST'])
   def notification_page():
    if 'username' in session:
        user = session['username']
    else:
        return redirect(url_for('login'))
    comments=[]
    likes=[]
    if user:
        with dbapi2.connect(app.config['dsn']) as connection:
            notification=Notifications(username=user,connection=connection)
            comments=notification.get_all_comments()
            likes =notification.get_all_likes()

    return render_template('notification.html',user=user, comments=comments,likes=likes)  

End of Notifications




















