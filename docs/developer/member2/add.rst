Add POSTS,FOLLOW,PROFILEPICTURE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I create a post object and I fill this with HTML tags

.. code-block:: python

   def save(self):
        self.__cursor.execute("""INSERT INTO POSTS (USERID,DATE,LINK,DESCRIPTION ) VALUES (%s,%s,%s,%s)""",[self.user_id, self.date, self.link, self.description])

.. code-block:: python

   if 'EKLE' in request.form:
                Image = request.form['ADD']
                id=request.form['id']
                desc=request.form['DESC']
                username=request.form['username']

                Newpost = posts( user_id=id, description=desc, date=now.strftime("%Y-%m-%d %H:%M:%S"), link=Image, connection=connection)
                Newpost.save()

                return redirect(url_for('profile_page',user=username))

So far, the filled informations are taken as variables. For the Posts, the description variable is a string and it needs to be changed to a text which corresponds to the entered string.



.. code-block:: python

   profilpic=ProfilePic(connection=connection,picid=registeruser.search_id_for_username(),link='http://www.maxibayan.com/wp-content/uploads/2014/10/instagram-avatar-5.png')
   		profilpic.save()

The profilepic is added succesfully with register

