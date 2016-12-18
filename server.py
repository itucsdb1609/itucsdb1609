import datetime
import json
import os
import psycopg2 as dbapi2
import re
import random
from flask import Flask

from flask import redirect
from flask import render_template
from werkzeug import redirect
from flask import request
from flask.helpers import url_for, flash
from initialize_db import initialize_db_func


from models import *

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

#aliercccan-------------------------------------

#Login page

@app.route('/login')
def login():
    now = datetime.datetime.now()
    return render_template('log_in.html', current_time=now.ctime())


#Sign up page

@app.route('/signUp',methods = ['GET','POST'])
def signUp():

    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query =  """INSERT INTO USER ( USERNAME, PASSWORD) VALUES (%s,%s)"""
            print(query)

            cursor.execute(query,(username, password))
            connection.commit()

        return redirect(url_for('signUp'))
    else:
         now = datetime.datetime.now()
         return render_template('signUp.html')

#--------------- end of aliercccan ---------

#Start of Ahmet Caglar Bayatli's space

@app.route('/', methods = ['GET','POST'])
@app.route('/welcome', methods = ['GET','POST'])
def welcome_page():
    allUsers = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """select id,username from users"""
        cursor.execute(query)
        for currentUser in cursor:
            allUsers.append(currentUser)

        if 'ChooseUser' in request.form:
            userName = request.form['ChooseUser']

            return redirect(url_for('home_page',user=userName))

    return render_template('welcome.html', allUsers=allUsers)

@app.route('/home', methods = ['GET','POST'])
@app.route('/<user>', methods = ['GET','POST'])
@app.route('/<user>/home', methods = ['GET','POST'])
def home_page(user=None):
    user_id=None
    user_data=None
    posts = []
    posts_likes={}
    posts_comments={}
    allUsers = []
    userCheck = False
    with dbapi2.connect(app.config['dsn']) as connection:
        post_like = PostLike(connection=connection)
        post_comment = PostComments(connection=connection)
        cursor = connection.cursor()
        query = """select id,username,name,surname from users"""
        cursor.execute(query)
        for currentUser in cursor:
            allUsers.append(currentUser)

        for uid,username,name,surname in allUsers:
            if user==username:
                user_data=[username,name,surname]
                user_id=uid
                userCheck = True
                break

        if request.method == 'POST':
            if 'delpost' in request.form:
                postid = request.form['postid']
                userid = request.form['userid']
                userName = request.form['username']

                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO HIDDENPOSTS(userid, postid) VALUES (%s,%s) """
                    cursor.execute(query, (userid, postid))
                    connection.commit()
                return redirect(url_for('home_page', user=userName))
            
            elif 'deluser' in request.form:
                userid = request.form['userid']
                userName = request.form['username']

                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO HIDDENUSERS(userid, userhid) VALUES (%s,%s) """
                    cursor.execute(query, (user_id, userid))
                    connection.commit()
                return redirect(url_for('home_page', user=userName))

            elif 'upt' in request.form:
                post = request.form['post']
                desc = request.form['desc']
                userName = request.form['username']

                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """UPDATE posts SET description='""" + desc + """' WHERE id =""" + post + """"""
                    cursor.execute(query)

                    connection.commit()
                return redirect(url_for('home_page', user=userName))

            elif 'like' in request.form:
                post_id = request.form['postId']
                like_type = request.form['like']
                new_like = PostLike(post_id=post_id, user_id=user_id, like_type=like_type, connection=connection)
                if not new_like.search_like_by_user_id_and_post_id():
                    new_like.save()
                else:
                    new_like.update_like_type()

            elif 'saveComment' in request.form:
                post_id = request.form['postId']
                comment =request.form['comment']
                new_comment = PostComments(post_id=post_id, user_id=user_id, comment=comment, connection=connection)
                saved_comment=new_comment.get_comment_by_user_id_and_post_id()
                if saved_comment!=comment:
                    new_comment.save()

            elif 'unlike' in request.form:
                like = PostLike(plid=request.form['unlike'], connection=connection)
                like.delete()

            elif 'uncomment' in request.form:
                comment = PostComments(pcid=request.form['uncomment'], connection=connection)
                comment.delete()
            elif 'newInterest' in request.form:
                new_interest=Interest(interest_name=request.form['interestName'],user_id=user_id,connection=connection)
                new_interest.save()
            elif 'deleteInterest' in request.form:
                new_interest = Interest(iid=request.form['deleteInterest'], connection=connection)
                new_interest.delete()
            elif 'updateInterest' in request.form:
                interest = Interest(iid=request.form['updateInterest'],connection=connection)
                interest.update_interest(request.form['updatedName'])


        if user and userCheck:
            interest = Interest(connection=connection)
            user_interests = interest.get_interest_by_user_id(user_id)
            query = """select distinct r.userid, username, name, surname, r.link as linkpro, r.postid, r.linkpost, date, description from (select * from (select m.mid, uid, m.postid, linkpost, date, description from (select l.mid, userid as uid, id as postid, link as linkpost, date, description from (select k.id as mid, k.following from (select id, following from users join follow on users.id = follow.follower where users.id = """+ str( user_id ) + """) k left join hiddenusers on hiddenusers.userhid = k.following where hiddenusers.userid is null) l join posts on posts.userid = l.following or  posts.userid = l.mid) m left join hiddenposts on hiddenposts.postid = m.postid where hiddenposts.userid is null) n join profilepic on profilepic.userid = n.uid) r join users on r. userid = users.id order by date asc"""
            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                likes = post_like.get_likes_by_post_id(post[5])
                if likes:
                    posts_likes.update({post[5]: likes})
                else:
                    posts_likes.update({post[5]: False})

                comments = post_comment.get_comments_by_post_id(post[5])
                if comments:
                    posts_comments.update({post[5]: comments})
                else:
                    posts_comments.update({post[5]: False})
                posts.append(post)
            
            query = """select * from profilepic"""
            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                if user_id==post[0]:
                    user_data.append(post[1])

        else:
            return render_template('404.html'), 404


        connection.commit()
        if 'ChooseUser' in request.form:
            userName = request.form['ChooseUser']

            return redirect(url_for('home_page',user=userName))



    return render_template('main.html', user=user, user_data=user_data, allUsers=allUsers , posts=posts,postsLikes=posts_likes,postsComments=posts_comments,user_interests=user_interests)

#End of Ahmet Caglar Bayatli's space

@app.route('/initdb')
def initialize_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        initialize_db_func(cursor)
        connection.commit()
    return redirect(url_for('welcome_page'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count


@app.route('/explore')
@app.route('/<user>/explore', methods = ['GET','POST'])
def explore_page(user=None):
    hashs = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT hashTag.HASHID, hashTag.GRUPNAME FROM hashTag"""

        cursor.execute(query)

        for hash in cursor:
            hashs.append(hash)

        connection.commit()

    return render_template('explore.html', hashs=hashs, user=user)

@app.route('/add_hash', methods = ['GET','POST'])
def add_hash():
    hashs = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT hashTag.HASHID, hashTag.GRUPNAME FROM hashTag"""

        cursor.execute(query)

        for hash in cursor:
            hashs.append(hash)

        connection.commit()


    if request.method =='POST':
        hashid = request.form['hashid']
        grupname = request.form['grupname']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO hashTag (HASHID, GRUPNAME ) VALUES (%s, %s )"""
            cursor.execute(query, (hashid, grupname))
            connection.commit()

    return render_template('add_hash.html', hashs=hashs)

@app.route('/delete_hash', methods = ['GET','POST'])
def delete_hash():
    hashs = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT hashTag.HASHID, hashTag.GRUPNAME FROM hashTag"""

        cursor.execute(query)

        for hash in cursor:
            hashs.append(hash)

        connection.commit()
    if request.method =='POST':
        hashid = request.form['hashid']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM hashTag WHERE HASHID = '""" +hashid + """'"""
            cursor.execute(query)
            connection.commit()

    return render_template('add_hash.html', hashs=hashs)

@app.route('/update_hash', methods = ['GET','POST'])
def update_hash():
    hashs = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT hashTag.HASHID, hashTag.GRUPNAME FROM hashTag"""

        cursor.execute(query)

        for hash in cursor:
            hashs.append(hash)

        connection.commit()

    if request.method =='POST':
        hashid = request.form['hashid']
        new_grupname = request.form['new_grupname']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE hashTag SET (HASHID, GRUPNAME ) = (%s,%s ) WHERE HASHID = '""" +hashid + """'"""

            cursor.execute(query, (hashid, new_grupname))
            connection.commit()


    return render_template('add_hash.html', hashs=hashs)

@app.route('/notifications')
@app.route('/<user>/notification', methods = ['GET','POST'])
def notification_page(user=None):
    now = datetime.datetime.utcnow()
    return render_template('notification.html', current_time=now.ctime(), user=user)


#Start of EKREM CIHAD CETIN's space
@app.route('/profile', methods = ['GET','POST'])
@app.route('/<user>/profile', methods = ['GET','POST'])
@app.route('/<user>/<user2>/profile', methods = ['GET','POST'])
def profile_page(user=None, user2=None):
    now = datetime.datetime.now()
    images = []
    kullanici=[]
    userr=[]
    allfollowerpic=[]
    allfollowingpic=[]
    user_id=None
    posts_likes = {}
    posts_comments = {}
    if user==user2:
        user2=None
        return redirect(url_for('profile_page',user=user))

    with dbapi2.connect(app.config['dsn']) as connection:
        post_like = PostLike(connection=connection)
        post_comment = PostComments(connection=connection)
        cursor = connection.cursor()
        query = """select id,username from users"""
        cursor.execute(query)
        for im in cursor:
            if im[1]==user:
                user_id=im[0]
            kullanici.append(im)

        if request.method == 'POST' and user_id:
            if 'like' in request.form:
                post_id = request.form['postId']
                like_type = request.form['like']
                new_like = PostLike(post_id=post_id, user_id=user_id, like_type=like_type, connection=connection)
                if not new_like.search_like_by_user_id_and_post_id():
                    new_like.save()
                else:
                    new_like.update_like_type()

            elif 'saveComment' in request.form:
                post_id = request.form['postId']
                comment = request.form['comment']
                new_comment = PostComments(post_id=post_id, user_id=user_id, comment=comment, connection=connection)
                saved_comment = new_comment.get_comment_by_user_id_and_post_id()
                if saved_comment != comment:
                    new_comment.save()

            elif 'unlike' in request.form:
                like = PostLike(plid=request.form['unlike'], connection=connection)
                like.delete()

            elif 'uncomment' in request.form:
                comment = PostComments(pcid=request.form['uncomment'], connection=connection)
                comment.delete()

        if user and not user2:
            query = """select users.id ,posts.id, link, name, surname,date,description from users,posts where username='"""+user+"""' and users.id=posts.userid order by date desc"""

            cursor.execute(query)

            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                likes = post_like.get_likes_by_post_id(post[1])
                if likes:
                    posts_likes.update({post[1]: likes})
                else:
                    posts_likes.update({post[1]: False})

                comments = post_comment.get_comments_by_post_id(post[1])
                if comments:
                    posts_comments.update({post[1]: comments})
                else:
                    posts_comments.update({post[1]: False})
                images.append(post)

        if user2:
            query = """select users.id ,posts.id, link, name, surname,date,description from users,posts where username='"""+user2+"""' and users.id=posts.userid order by date desc"""

            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                likes = post_like.get_likes_by_post_id(post[1])
                if likes:
                    posts_likes.update({post[1]: likes})
                else:
                    posts_likes.update({post[1]: False})

                comments=post_comment.get_comments_by_post_id(post[1])
                if comments:
                    posts_comments.update({post[1]: comments})
                else:
                    posts_comments.update({post[1]: False})
                images.append(post)


        if user and not user2:
            query ="""select link,users.username from (select following,users.username from users join follow on users.id=follow.follower where username='"""+user+"""') F, profilepic,users where F.following=profilepic.userid and F.following=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowingpic.append(im)

        if user and not user2:
            query ="""select link,users.username from (select follower,users.username from users join follow on users.id=follow.following where username='"""+user+"""') F, profilepic,users where F.follower=profilepic.userid and F.follower=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowerpic.append(im)


        if user and not user2:
            query="""select userid,link, username, name, surname,mail from profilepic,users where username='"""+user+"""' and users.id=profilepic.userid"""
            cursor.execute(query)
            userr = cursor.fetchall()
            if userr:
                interest = Interest(connection=connection)
                user_interests = interest.get_interest_by_user_id(userr[0][0])

        if user2:
            query ="""select link,users.username from (select following,users.username from users join follow on users.id=follow.follower where username='"""+user2+"""') F, profilepic,users where F.following=profilepic.userid and F.following=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowingpic.append(im)

        if user2:
            query ="""select link,users.username from (select follower,users.username from users join follow on users.id=follow.following where username='"""+user2+"""') F, profilepic,users where F.follower=profilepic.userid and F.follower=users.id ORDER BY users.username ASC"""

            cursor.execute(query)
            for im in cursor:
                allfollowerpic.append(im)

        if user2:
            query="""select userid,link, username, name, surname,mail from profilepic,users where username='"""+user2+"""' and users.id=profilepic.userid"""
            cursor.execute(query)
            userr = cursor.fetchall()
            if userr:
                interest = Interest(connection=connection)
                user_interests = interest.get_interest_by_user_id(userr[0][0])



        connection.commit()
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if request.method =='POST':
            if 'EKLE' in request.form:
                Image = request.form['ADD']
                id=request.form['id']
                desc=request.form['DESC']
                username=request.form['username']

                Newpost = posts( user_id=id, description=desc, date=now.strftime("%Y-%m-%d %H:%M:%S"), link=Image, connection=connection)
                Newpost.save()

                return redirect(url_for('profile_page',user=username))
            if 'Change' in request.form:
                username = request.form['Change']

                return redirect(url_for('profile_page',user=username))


            if 'UPDATE' in request.form:
                userid = request.form['PROFILE']
                username=request.form['USERNAME']
                link = request.form['NEWLINK']

                Newprofilepic = ProfilePic( picid=userid, link=link, connection=connection)
                Newprofilepic.update_pic()

                return redirect(url_for('profile_page',user=username))
            if 'POSTDEL' in request.form:
                postid = request.form['POSTDEL']
                username=request.form['USERNAME']

                Newpost = posts( postid=postid , connection=connection)
                Newpost.delete()

                return redirect(url_for('profile_page',user=username))
            if 'POSTUPDATE' in request.form:
                postid = request.form['postid']
                username=request.form['username']
                desc=request.form['DESC']
                link=request.form['ImageUrl']

                Newpost = posts( postid=postid, description=desc, date=now.strftime("%Y-%m-%d %H:%M:%S"), link=link, connection=connection)
                Newpost.update_post()

                return redirect(url_for('profile_page',user=username))
        connection.commit()

    return render_template('profile.html',user=user, user2=user2,allfollowerpic=allfollowerpic,allfollowingpic=allfollowingpic, current_time=now.strftime("%Y-%m-%d %H:%M:%S"),images=images,userr=userr,kullanici=kullanici,postsLikes=posts_likes,postsComments=posts_comments,user_interests=user_interests)

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
if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
