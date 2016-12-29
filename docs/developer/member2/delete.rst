Delete Cars,Engines and Creators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At car_delete.html page we take input from user for deleting cars,engines or creator based on their names.And we send this infos into deleting function that inside in server.py
We have 3 deleting functions.All of them we take name of the items.Then in DELETE FROM table_name WHERE Name = input_variable format we execute cursor and delete this items in tables.

.. code-block:: python

   @app.route('/car_delete',methods = ['GET','POST'])
   def car_delete():
       if request.method =='POST':
           car_name = request.form['car_name']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()
               query =  """DELETE FROM CARS WHERE Name=%s"""
               cursor.execute(query,([car_name]))
               connection.commit()
           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_delete.html')


   @app.route('/engine_delete',methods = ['GET','POST'])
   def engine_delete():
       engine_list =[]
       if request.method =='POST':
           engine_name = request.form['engine_name']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """DELETE FROM ENGINES WHERE Engine_Name=%s"""
               cursor.execute(query,([engine_name]))
               connection.commit()
           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_delete.html')

   @app.route('/creator_delete',methods = ['GET','POST'])
   def creator_delete():

       if request.method =='POST':
           creator_name = request.form['creator_name']
           with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()

               query =  """DELETE FROM CREATORS WHERE Name=%s"""
               cursor.execute(query,([creator_name]))
               connection.commit()
           return redirect(url_for('home'))
       else:
            now = datetime.datetime.now()
            return render_template('car_delete.html')