Admin Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our server.py class includes admin_page function. These function controls user information. If user is an admin user, system gives the authority to user about add, delete, update operations.

.. code-block:: python

   def admin_page():
    if 'username' in session and 'admin' in session and session['admin']==True:
        user = session['username']
    else:
        return redirect(url_for('login'))
    with dbapi2.connect(app.config['dsn']) as connection:
        admin = Admin(connection=connection)
        if request.method == 'POST':
            if 'save' in request.form:
                collage = Collage(collage_name=request.form['school'], connection=connection)
                collage_id=collage.search_collage_by_name()
                if not collage_id:
                    collage.save()
                    collage_id = collage.search_collage_by_name()
                admin.update_user(email=request.form['email'],school_id=collage_id,user_id=request.form['save'])
            elif 'userdel':
                admin.del_user(request.form['userdel'])

        all_users= admin.get_users()

    return render_template('admin.html',all_users=all_users)
    
    
There is admin.py class under the model directory. Admin can update user information, delete accounts.

.. code-block:: python

   class Admin:

    __connection = None
    __cursor = None

    def __init__(self,connection):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

    def get_users(self):
        self.__cursor.execute(
            """SELECT u.id,name,surname,username,mail,city.cityname,school.schoolname,gender.type FROM users AS u JOIN gender ON u.gender = gender.id JOIN school ON u.school = school.id JOIN city ON u.city = city.id""")
        return self.__cursor.fetchall()

    def get_username_by_id(self,user_id):
        self.__cursor.execute("""SELECT username from users WHERE id=%s""",[user_id])
        return self.__cursor.fetchone()



    def del_user(self,user_id):
        username=self.get_username_by_id(user_id=user_id)
        self.__cursor.execute("""DELETE FROM userlogin WHERE username=%s""",[username])
        self.__cursor.execute("""DELETE FROM profilepic WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM follow WHERE follow.follower=%s or following=%s""", [user_id,user_id])
        self.__cursor.execute("""DELETE FROM posts WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM postlikes WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM postcomments WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM interests WHERE userid=%s""", [user_id])
        self.__cursor.execute("""DELETE FROM hiddenposts WHERE userid=%s""", [user_id])
        self.__cursor.execute(
            """DELETE FROM users WHERE id=%s""",[user_id]
        )
    def update_user(self,email,school_id,user_id):
        self.__cursor.execute("""UPDATE users SET mail=%s,school=%s WHERE id=%s""",[email,school_id,user_id])


