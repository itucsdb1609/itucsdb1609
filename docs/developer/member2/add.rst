Add Brands and Founders
^^^^^^^^^^^^^^^^^^^^^^^

The adding operation is done according to the main operation. There are two adding functions: one for brandsa and one for founders.
On the html page, when the fields are filled and add button is pressed, the server receives a POST method and the filled fields are taken as arguments.
With this information, the adding operation is done easily.

.. code-block:: python

   if request.method =='POST':
      brand_name = request.form['brand-name']
      description = request.form['description']
      foundation = request.form['foundation']
      imagelink = request.form['imagelink']
      website = request.form['website']
      industry = request.form['industry']
      country = request.form['country']

So far, the filled informations are taken as variables. For the brands, the country variable is a string and it needs to be changed to a integer which correspnds to the entered string.

.. code-block:: python

   with dbapi2.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()

       query = """SELECT Id FROM COUNTRIES WHERE COUNTRIES.countries = '""" + country + """'"""
       cursor.execute(query)

       countryid = None
       for record in cursor:
           countryid = record

Now the id for the requested country is taken and it is ready to be add.

.. code-block:: python

    query = """INSERT INTO BRANDS (Name, Comment, Foundation, Image, Industry, Website, CountryId) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(query, (brand_name,description,foundation,imagelink,industry,website, countryid[0]))
    connection.commit()

The brand is added succesfully. Adding the founder is pretty much the same.

