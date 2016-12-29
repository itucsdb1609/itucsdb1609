Updates Cars,Engines and Creators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We take inputs for update operations at car_add.html page.Firstly we take name of the existing items and new values and assign to variables. Then we update it's values with new values that came from POST request.
Using UPDATE ENGINES SET query SQL statement.We have again 3 functions each of them for cars,creators and engines.And this functions are like ;

.. code-block:: python

   @app.route('/car_update',methods = ['GET','POST'])
   def car_update():
       if request.method =='POST':
           car_name_up =request.form['car_name_up']
           image_link = request.form['image_link']
           car_name = request.form['car_name']
           engine_id = request.form['engine_id']
           creator_id = request.form['creator_id']
           speed_limit = request.form['speed_limit']
           brand = request.form['brand']
           pilot = request.form['pilot']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """UPDATE CARS SET (Image_Link, Name, Engine_ID,Creator_ID,Speed, BRAND_ID, PILOT_ID) = (%s,%s,%s,%s,%s,%s,%s) WHERE Name=%s"""
               #print(query)

               cursor.execute(query,(image_link,car_name,engine_id,creator_id,speed_limit,brand,pilot,car_name_up))

               connection.commit()

           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_add.html')

   @app.route('/engine_update',methods = ['GET','POST'])
   def engine_update():
       if request.method =='POST':
           engine_name_up =request.form['engine_name_up']
           engine_name =request.form['engine_name']
           horse_power =request.form['horse_power']

           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """UPDATE ENGINES SET (Engine_Name , HorsePower ) = (%s,%s) WHERE Engine_Name=%s"""
               #print(query)

               cursor.execute(query,(engine_name,horse_power,engine_name_up))

               connection.commit()

           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_add.html')

   @app.route('/creator_update',methods = ['GET','POST'])
   def creator_update():
       if request.method =='POST':
           creator_name_up =request.form['creator_name_up']
           creator_name =request.form['creator_name']


           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """UPDATE CREATORS SET Name = %s WHERE Name=%s"""
               #print(query)

               cursor.execute(query,(creator_name,creator_name_up))

               connection.commit()

           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_add.html')