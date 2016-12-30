Register Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our server.py class includes register method.

.. code-block:: python

   @app.route('/register',methods=['GET','POST'])
   def register():
    all_cities=[]
    status='Register'
    all_collages=[]
    with dbapi2.connect(app.config['dsn']) as connection:
        if request.method == 'POST':
            registeruser=Register(connection=connection,name=request.form['name'], surname=request.form['surname'], email=request.form['email'],
                                  username=request.form['username'], city=request.form['city'], collage=request.form['collage'],newcity=request.form['newcity'],
                                  newcollage=request.form['newcollage'],gender=request.form['gender'], password=request.form['password'],confirm=request.form['confirm'])
            status=registeruser.save()

            profilpic=ProfilePic(connection=connection,picid=registeruser.search_id_for_username(),link='http://www.maxibayan.com/wp-content/uploads/2014/10/instagram-avatar-5.png')
            profilpic.save()
        city=City(connection=connection)
        all_cities=city.get_all_cities()
        collage= Collage(connection=connection)
        all_collages = collage.get_all_collages()

    return render_template('register.html', all_cities=all_cities,all_collages=all_collages,status=status)
    
    
There is register.py class under the model directory. These methods control the new user information with database. For example; when username is same with another account's username, it does not let to create account, etc.

.. code-block:: python

   class Register:

    __connection= None
    __cursor= None
    savable=True
    error=''
    def __init__(self,connection,name, surname, email, username, city, collage,newcity, newcollage,gender, password,confirm):
        if connection:
            self.__connection = connection
            self.__cursor = connection.cursor()

            self.name=name
            self.surname=surname
            self.email=email
            self.username=username
            self.city=city
            self.collage = collage
            self.newcity = newcity
            self.newcollage = newcollage
            self.password =password
            self.gender=gender
            self.confirm=confirm

            if self.name == '' or self.surname == '' or (self.email == '' or self.search_for_email()) or \
                    (self.username == '' or self.search_for_username()) or (self.city == 0 and len(self.newcity) == 0) or (
                    self.collage == 0 and len(self.newcollage) == 0) or self.password != self.confirm:
                self.savable = False


    def search_for_username(self):
        self.__cursor.execute("""SELECT id from users WHERE username =%s""" ,[self.username])
        user = self.__cursor.fetchone()
        if user:
            return True
        else:
            return False
    def search_id_for_username(self):
        self.__cursor.execute("""SELECT id from users WHERE username =%s""" ,[self.username])
        return self.__cursor.fetchone()

    def search_for_email(self):
        self.__cursor.execute("""SELECT id from users WHERE mail =%s""", [self.email])
        user = self.__cursor.fetchone()
        if user:
            return True
        else:
            return False

    def save(self):
        if self.savable:
            if self.city=='0':
                cityO = City(connection=self.__connection,city_name=self.newcity)
                cityO.save()
                self.city=cityO.search_city_by_name()
            if self.collage == '0':
                collageO = Collage(connection=self.__connection, collage_name=self.newcollage)
                collageO.save()
                self.collage = collageO.search_collage_by_name()
            self.__cursor.execute("""INSERT into users (username, name, surname, mail, gender, school, city) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                                  [self.username,self.name,self.surname,self.email,self.gender,self.collage,self.city])
            self.__cursor.execute("""INSERT into userlogin (username, password) VALUES (%s,%s) """,[self.username,self.password])
            return True
        return False


