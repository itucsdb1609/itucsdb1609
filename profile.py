import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from werkzeug import redirect
from flask import request
from flask.helpers import url_for, flash
from initialize_db import initialize_db_func

from config import app

#Start of EKREM CIHAD CETIN's space
@app.route('/profile', methods = ['GET','POST'])
@app.route('/profile/<user>', methods = ['GET','POST'])
def profile_page(user=None):
    now = datetime.datetime.now()
    images = []
    kullanici=[]
    userr=[]
    allfollowerpic=[]
    allfollowingpic=[]
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """select id,username from users"""
        cursor.execute(query)
        for im in cursor:
            kullanici.append(im)
        if user:
            query = """select users.id,posts.link from users,posts where username='"""+user+"""' and users.id=posts.userid"""
            cursor.execute(query)
            for im in cursor:
                images.append(im)

        if user:
            query ="""select link,users.username from (select following,users.username from users join follow on users.id=follow.follower where username='"""+user+"""') F, profilepic,users where F.following=profilepic.userid and F.following=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowingpic.append(im)

        if user:
            query ="""select link,users.username from (select follower,users.username from users join follow on users.id=follow.following where username='"""+user+"""') F, profilepic,users where F.follower=profilepic.userid and F.follower=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowerpic.append(im)


        if user:
            query="""select userid,link, username, name, surname,mail from profilepic,users where username='"""+user+"""' and users.id=profilepic.userid"""
            cursor.execute(query)
            for us in cursor:
                userr.append(us)
        connection.commit()
    if request.method =='POST':
        if 'EKLE' in request.form:
            Image = request.form['ADD']
            id=request.form['id']
            desc=request.form['DESC']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO POSTS (USERID,DATE,LINK,DESCRIPTION ) VALUES ("""+id+""",'"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""','%s','%s' )"""%(Image,desc)
                cursor.execute(query)
                connection.commit()
            return redirect(url_for('profile_page'))
        if 'Change' in request.form:
            username = request.form['Change']

            return redirect(url_for('profile_page',user=username))
        if 'FOLLOWING' in request.form:
            prof = request.form['FOLLOWING']

            return redirect(url_for('profile_page',user=prof))
        if 'FOLLOWER' in request.form:
            prof = request.form['FOLLOWER']

            return redirect(url_for('profile_page',user=prof))

        if 'UPDATE' in request.form:
                userid = request.form['PROFILE']
                username=request.form['USERNAME']
                link = request.form['NEWLINK']
                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """UPDATE profilepic SET link='"""+link+"""' WHERE userid ="""+userid+""""""
                    cursor.execute(query)

                    connection.commit()
                return redirect(url_for('profile_page',user=username))



    return render_template('profile.html',user=user,allfollowerpic=allfollowerpic,allfollowingpic=allfollowingpic, current_time=now.strftime("%Y-%m-%d %H:%M:%S"),images=images,userr=userr,kullanici=kullanici)

@app.route('/add_pic', methods = ['GET','POST'])
def add_pic():
    pics = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT picPost.PicId, picPost.Description FROM picPost"""

        cursor.execute(query)

        for pic in cursor:
            pics.append(pic)

        connection.commit()
    if request.method =='POST':
        if 'ADD' in request.form:
            picDesc = request.form['ADD']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO picPost (Description ) VALUES ('%s' )"""%picDesc
                cursor.execute(query)
                connection.commit()
            return redirect(url_for('add_pic'))

        if 'Delete' in request.form:
            picId=request.form['id']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM picPost WHERE PicId = '""" +picId + """'"""
                cursor.execute(query)
                connection.commit()
            return redirect(url_for('add_pic'))

        if 'Update' in request.form:
            picId=request.form['id']
            Desc = request.form['newname']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """UPDATE picPost SET (Description ) = ('"""+Desc+"""') WHERE PicId = '""" +picId + """'"""
                cursor.execute(query)

                connection.commit()
            return redirect(url_for('add_pic'))

    return render_template('add_pic.html', pics=pics)

@app.route('/deneme', methods = ['GET','POST'])
@app.route('/deneme/<user>', methods = ['GET','POST'])
def deneme_page(user=None):
    images = []
    kullanici=[]
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID,LINK FROM POSTS"""

        cursor.execute(query)

        for im in cursor:
            images.append(im)

        query = """select id,username from users"""
        cursor.execute(query)
        for im in cursor:
            kullanici.append(im)
        connection.commit()

    if request.method =='POST':
        if 'ADD' in request.form:
            Image = request.form['ADD']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """INSERT INTO POSTS (link ) VALUES ('%s' )"""%Image
                cursor.execute(query)
                connection.commit()
            return redirect(url_for('deneme_page'))
        if 'Change' in request.form:
            username = request.form['Change']

            return redirect(url_for('deneme_page',user=username))

    return render_template('deneme.html',user=user,images=images,kullanici=kullanici)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
#
# #END of EKREM CIHAD CETIN's space