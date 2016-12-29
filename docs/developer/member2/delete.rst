Delete POSTS,FOLLOW
^^^^^^^^^^^^^^^^^^^

Delete operation is done by entity IDs. The entities have their IDs integrated on the table id. The table ids are in the "table_<entity_id>" format.
The id value is also placed inside the delete button in the value field.

.. code-block:: python

   if 'POSTDEL' in request.form:
                postid = request.form['POSTDEL']
                username=request.form['USERNAME']

                Newpost = posts( postid=postid , connection=connection)
                Newpost.delete()

     			return redirect(url_for('profile_page',user=username))

As it can be seen in the snippet, pressing the delete button will sent the id value as an argument via POST method. This case applies for  posts tables. Both deletions are done in the same way.

.. code-block:: python

   def delete(self):
        self.__cursor.execute("""DELETE FROM POSTS WHERE id =%s""",[self.postid])
        self.__connection.commit()


Deleting a post will cause the deletion of the tags but deleting the tags will not cause the deletion of the post.

You can delete follow with unFollow button as follower and following

.. code-block:: html

   <form method="POST" role="form">
      	{% if status %}
         	<button href="#" class="btn  btn-danger btn-xs" type="submit"  name="UNFOLLOW" style="display: inline;">UNFOLLOW
         		<span class="glyphicon glyphicon-remove"></span>
         	</button>
        {% else %}
         	<button href="#" class="btn  label-success btn-xs" type="submit"  name="FOLLOW" style="display: inline;">FOLLOW
         		<span class="glyphicon glyphicon-plus"></span>
         	</button>
        {% endif %}
   </form>


 And server.py operations is here (query)

.. code-block:: python

   if 'UNFOLLOW' in request.form:
                query="""delete from follow where follower=%s and following=%s """
                cursor.execute(query,(user_id,user2_id))
				return redirect(url_for('profile_page',user=user))


End Of deletion