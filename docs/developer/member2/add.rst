Add Cars,Engines and Creators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At car_add html page we have a html for that get informations from users and send to this input our servers.At backend page,
server.py, we handle add opertions in 3 main functions.
At car_add function we take inputs from html page using POST request.Then we declera our variables such as image_link,car_name etc. then
we create cursor for doing database operations.Firtly we selected from ENGINES because we referenced from ENGINES and if there no engines with that id
we don't do this operations for concistency of databases.Then we check is there same name for cars name since it is primary key.Then lastly
we define our inserting query for cars tables and do adding operations.And if we haven't POST request we directed to again car_add.html page.

.. code-block:: python

   @app.route('/car_add',methods = ['GET','POST'])
   def car_add():
   engine_list = []
   name_list = []
   if request.method =='POST':
        image_link = request.form['image_link']
        car_name = request.form['car_name']
        engine_id = request.form['engine_id']
        creator_id = request.form['creator_id']
        speed_limit = request.form['speed_limit']
        brand = request.form['brand']
        pilot = request.form['pilot']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()


            query = """SELECT Id FROM ENGINES WHERE Id=%s"""
            cursor.execute(query,(engine_id))

            for record in cursor:
                engine_list.append(record)


            if len(engine_list) == 0 or engine_id =='':
                return redirect(url_for('home'))

            query = """SELECT Name FROM CARS WHERE Name=%s"""
            cursor.execute(query,([car_name]))

            for record in cursor:
                name_list.append(record)

            if len(name_list) != 0:
                return redirect(url_for('home'))

            query =  """INSERT INTO CARS (Image_Link, Name, Engine_ID,Creator_ID,Speed, BRAND_ID, PILOT_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            print(query)

            cursor.execute(query,(image_link,car_name,engine_id,creator_id,speed_limit,brand,pilot))
            connection.commit()

        return redirect(url_for('home'))
    else:
         now = datetime.datetime.now()
         return render_template('car_add.html')


In same way we add Creators and Engines.But we don't do any check since they are not referenced from any tables.Codes of this two functions is like ;

.. code-block:: python

   @app.route('/engine_add',methods = ['GET','POST'])
   def engine_add():
       if request.method =='POST':
           engine_name = request.form['engine_name']
           horsepower = request.form['horsepower']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """INSERT INTO ENGINES (Engine_Name, HorsePower) VALUES (%s,%s)"""
               print(query)

               cursor.execute(query,(engine_name,horsepower))
               connection.commit()

           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_add.html')

   @app.route('/creator_add',methods = ['GET','POST'])
   def creator_add():
       if request.method =='POST':
           name = request.form['creator_name']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """INSERT INTO CREATORS (Name) VALUES ('"""+name+"""')"""
               print(query)

               cursor.execute(query)
               connection.commit()

           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_add.html')



