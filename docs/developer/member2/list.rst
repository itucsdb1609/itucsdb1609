List Cars,Engines and Creators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cars.html page we list all cars and their attributes.For this showing we use JOIN operations for retrieving some attributes from other tables that CARS table referenced like Pilots,Teams,Engines and Creators.
Also we list all of the Creators and Engines at bottom of the page.We list this operation at cars functions.

.. code-block:: python

   @app.route('/cars')
   def cars():
       now = datetime.datetime.now()
       cars_list = []
       engine_list = []
       creator_list = []
       with dbapi2.connect(app.config['dsn']) as connection:
               cursor = connection.cursor()
               query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id)"""


               cursor.execute(query)

               for record in cursor:
                   cars_list.append(record)
               connection.commit()

               query = """SELECT Engine_Name,HorsePower FROM ENGINES"""
               cursor.execute(query)
               for record in cursor:
                   engine_list.append(record)

               query = """SELECT Name FROM CREATORS"""
               cursor.execute(query)
               for record in cursor:
                   creator_list.append(record)
       return render_template('cars.html', creator_list = creator_list , engine_list = engine_list, cars_list=cars_list, current_time=now.ctime())
