Update Brands and Founders
^^^^^^^^^^^^^^^^^^^^^^^^^^

Update is the most complex part of the application. It is implemented as "edit". The brands and founders edit is again pretty much the same. Whenever the edit button is pressed on the one of the tables,
the field is replaced with an input box, filled with previous information. This is done by javascript. The edit button also contains the id as a value to pass to the edit function via javascript call.

.. code-block:: java

    table = document.getElementById("table_" + id);

    table.cells[0].innerHTML = "<input form='edit_" + id + "' type='text' name='brand-name' placeholder='Name' maxlength='25' value='" + table.cells[0].innerHTML.trim() + "'>";
    table.cells[1].innerHTML = "<input form='edit_" + id + "' type='text' name='industry' placeholder='Industry' maxlength='20' value='" + table.cells[1].innerHTML.trim() + "'>";
    table.cells[2].innerHTML = "<input form='edit_" + id + "' type='number' name='foundation' placeholder='Year' min='1800' max='2015' value='" + parseInt(table.cells[2].innerHTML) + "'>";
    table.cells[3].innerHTML = "<input form='edit_" + id + "' type='text' name='website' placeholder='Website' maxlength='25' value='" + table.cells[3].innerHTML.trim() + "'>";
    table.cells[4].innerHTML = "<input form='edit_" + id + "' type='text' name='imagelink' placeholder='Image Link' maxlength='50' value='" + table.cells[4].innerHTML.trim() + "'>";
    table.cells[5].innerHTML = "<input form='edit_" + id + "' type='text' name='description' placeholder='Description' maxlength='75' value='" + table.cells[5].innerHTML.trim() + "'>";
    table.cells[6].innerHTML = "<input form='edit_" + id + "' type='text' name='country' placeholder='Country' maxlength='15' value='" + table.cells[6].innerHTML.trim() + "'>";

    $(document.getElementsByClassName("edit_delete_forms_" + id)).html("<button form='edit_" + id + "' class='edit_finalize_button green' name='edit' value='" +id+"' type='submit'>" +
       "<span class='icon-checkmark'>Update</span>" +
   "</button>" +
    "</form>");

The table is selected by the table id which is created using the entity id. This id is given as a parameter to this function. After the table selection, each cell of the table is replaced with an input field and the value field is filled with the current values on the cells.
After that, the current buttons on the operation section is replaced with an "Update" button. When this button is pressed, the entered arguments are sent by POST method.
Python handles the remaining job by updating the table values. First, the attributes are taken as variables:

.. code-block:: python

   new_name = request.form['brand-name']
   new_description = request.form['description']
   new_foundation = request.form['foundation']
   new_imagelink = request.form['imagelink']
   new_website = request.form['website']
   new_industry = request.form['industry']
   new_country = request.form['country']
   edit = request.form['edit']


Again, the country should be converted to an ID value. This is done by a simple search as in the add operation. Finally, the update query is executed.

.. code-block:: python

   with dbapi2.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()

       query = """SELECT Id FROM COUNTRIES WHERE COUNTRIES.countries = '""" + new_country + """'"""
       cursor.execute(query)

       countryid = None
       for record in cursor:
           countryid = record

       query = """UPDATE BRANDS SET (Name, Comment, Foundation,  Image, Industry, Website, CountryId) = (%s, %s,%s,%s,%s,%s,%s) WHERE ID = %s;"""
       cursor.execute(query, (new_name, new_description, new_foundation, new_imagelink, new_industry, new_website, countryid[0], edit))
       connection.commit()


