Search Cars,Engines and Creators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At seacrh part if user select Cars and search a text we go to search function and at elif area=1 is for cars pages.In this area we search our text in
4 different area.Firstly all of the Query have do join operations like in list funcitions and it is enough since all of the information for cars have in this query.
And we search based their name because searching a value like 300 is nonsense and user generally search names so we search names in our Joined table.We use %like% SQL statement for
searching.Again we use cursor for executing this operation.

.. code-block:: python

   elif area == '1':
                   #search cars
                   search = "%" +search + "%"
                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (CARS.Name ILIKE %s)"""
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (ENGINES.Engine_Name ILIKE %s) """
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (CREATORS.Name ILIKE %s)"""
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (PILOTS.Name ILIKE %s)"""
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (PILOTS.Surname ILIKE %s)"""
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query = """SELECT CARS.Image_Link,CARS.Name,ENGINES.Engine_Name,CREATORS.Name,ENGINES.HorsePower,CARS.Speed,TEAMS.Teams,PILOTS.Name,PILOTS.Surname FROM CARS,ENGINES,CREATORS,PILOTS,TEAMS WHERE (CARS.Engine_ID = ENGINES.Id ) AND (CARS.Creator_ID = CREATORS.Id) AND (CARS.BRAND_ID = TEAMS.Id) AND (CARS.PILOT_ID = PILOTS.Id) AND (TEAMS.Teams ILIKE %s)"""
                   cursor.execute(query, ([search]))
                   for record in cursor:
                       query_list.append(record)

                   query_list = list(set(query_list))

                   connection.commit()
                   return render_template('search.html', current_time= now.ctime(), query_list = query_list, table = 1)