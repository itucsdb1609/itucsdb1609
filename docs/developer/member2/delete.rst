Delete Brands and Founders
^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete operation is done by entity IDs. The entities have their IDs integrated on the table id. The table ids are in the "table_<entity_id>" format.
The id value is also placed inside the delete button in the value field.

.. code-block:: python

   <form action="{{ url_for('brands_db', operation='delete_founder') }}" method="post">
                   <button class="delete_button red" name="delete" value="{{id}}" type="submit">
                     <span class="icon-minus "></span>
                   </button>
                 </form>

As it can be seen in the snippet, pressing the delete button will sent the id value as an argument via POST method. This case applies for brands and founders tables. Both deletions are done in the same way.

.. code-block:: python

   if request.method == 'POST':
      brand_id = request.form['delete']

      with dbapi2.connect(app.config['dsn']) as connection:
          cursor = connection.cursor()
          cursor.execute("DELETE FROM BRANDS WHERE Id = %s ", ([brand_id]))
          connection.commit()

Deleting a brand will cause the deletion of the founder but deleting the founder will not cause the deletion of the brand.


