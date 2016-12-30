Logout Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Our server.py class includes logout function. These function ended the session and user logout from account. This operations direct the user to login page.

.. code-block:: python

   @app.route('/logout',methods = ['GET','POST'])
   def logout():
    session.pop('username',None)
    session.pop('admin',None)
    return redirect(url_for('login'))
