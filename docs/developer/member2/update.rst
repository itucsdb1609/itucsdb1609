Update POST,PROFILEPICTURE
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can Update Profile Picture as Default with registration.

.. code-block:: python

   def update_pic(self):
        self.__cursor.execute("""UPDATE profilepic SET link=%s WHERE userid =%s""",[self.link,self.picid])
        self.__connection.commit()

Server Side profile Picture Update

.. code-block:: python

   if 'UPDATE' in request.form:
                userid = request.form['PROFILE']
                username=request.form['USERNAME']
                link = request.form['NEWLINK']

                Newprofilepic = ProfilePic( picid=userid, link=link, connection=connection)
                Newprofilepic.update_pic()

HTML side of cHange Profile Picture. You can see Routed link for Local image like HizliResim

.. code-block:: python

   <form method="POST" role="form">
		<input type="hidden" name="PROFILE" value={{ id }} >
		<input type="hidden" name="USERNAME" value={{ username }} >
		<input type="text" name="NEWLINK" id="NEWLINK" placeholder="New Picture Url " style="width: 100%; " required oninvalid="setCustomValidity('Please fill out this field')" oninput="setCustomValidity('')"  ><br><hr>
	<div >
		<a href="https://hizliresim.com/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:180px;">
			<span class="glyphicon glyphicon-download"></span>Link from "Hızlı Resim"
		</a>
		<a href="http://resimyukle.xyz/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:180px;">
			<span class="glyphicon glyphicon-download"></span>Link from "Resim Yukle"
		</a>
		<a href="https://postimage.org/" target="_blank" id="code" type="submit" class="btn btn-success" style="width:180px;">
			<span class="glyphicon glyphicon-download"></span>Link from "PostImage"
		</a>
	</div>
	<hr>
		<button type="button" class="btn btn-default" data-dismiss="modal" style="position: relative; top: 10px; left: 390px;">Close</button>
		<button class="btn btn-default" type="submit" name="UPDATE" style="position: relative; top: 10px; left: 400px; background-color: #03C9A9; color: white;">Change</button>
	</form>

Update Post Server side

.. code-block:: python

   if 'POSTUPDATE' in request.form:
        postid = request.form['postid']
        username=request.form['username']
        desc=request.form['DESC']
        link=request.form['ImageUrl']

        Newpost = posts( postid=postid, description=desc, date=now.strftime("%Y-%m-%d %H:%M:%S"), link=link, connection=connection)
        Newpost.update_post()

        return redirect(url_for('profile_page',user=username))

So HTML Side and model update is same profile picture. FOr Follow Table, no need Update Functions.