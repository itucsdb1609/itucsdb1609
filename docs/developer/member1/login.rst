User Authentication and Login Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is login.py class under the model directory. There is an authenticator at this block. It compare user information with database information and let session to start. Thus, user can sign in to his/her account. 

.. code-block:: python

   class Login:

    __connection = None
    __cursor = None
    def __init__(self,username,password,connection):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()
            self.username=username
            self.password=password

    def authenticator(self):
        self.__cursor.execute("""SELECT username,admin from userlogin WHERE username=%s AND password=%s """,[self.username,self.password])
        user = self.__cursor.fetchone()
        if user:
            return user
        else:
            return False

Moreover, our server.py class includes login method. This method calls authenticator.

.. code-block:: python

   @app.route('/login',methods = ['GET','POST'])
   def login():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            auth=Login(request.form['username'],request.form['password'],connection)
            user = auth.authenticator()
            if user:
                session['logged_in']='true'
                session['username']=user[0]
                session['admin']=user[1]
        return redirect(url_for('home_page'))

    return render_template('login.html')
