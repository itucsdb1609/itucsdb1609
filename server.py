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
from flask import request,session
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

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        with dbapi2.connect(app.config['dsn']) as connection:
            auth=Login(request.form['username'],request.form['password'],connection)
            user = auth.authenticator()
            if user:
                session['logged_in']='true'
                session['username']=user[0]
                session['admin']=user[1]
        return redirect(url_for('home_page'))

    return render_template('login.html')

@app.route('/logout',methods = ['GET','POST'])
def logout():
    session.pop('username',None)
    session.pop('admin',None)
    return redirect(url_for('login'))

#Sign up page

@app.route('/register',methods=['GET','POST'])
def register():
    all_cities=[]
    status='Register'
    all_collages=[]
    with dbapi2.connect(app.config['dsn']) as connection:
        if request.method == 'POST':
            registeruser=Register(connection=connection,name=request.form['name'], surname=request.form['surname'], email=request.form['email'],
                                  username=request.form['username'], city=request.form['city'], collage=request.form['collage'],newcity=request.form['newcity'],
                                  newcollage=request.form['newcollage'],gender=request.form['gender'], password=request.form['password'],confirm=request.form['confirm'])
            status=registeruser.save()
        city=City(connection=connection)
        all_cities=city.get_all_cities()
        collage= Collage(connection=connection)
        all_collages = collage.get_all_collages()

    return render_template('register.html', all_cities=all_cities,all_collages=all_collages,status=status)


#--------------- end of aliercccan ---------

#Start of Ahmet Caglar Bayatli's space

@app.route('/admin', methods = ['GET','POST'])
def admin_page():
    if 'username' in session and 'admin' in session and session['admin']==True:
        user = session['username']
    else:
        return redirect(url_for('login'))
    with dbapi2.connect(app.config['dsn']) as connection:
        admin = Admin(connection=connection)
        if request.method == 'POST':
            if 'save' in request.form:
                collage = Collage(collage_name=request.form['school'], connection=connection)
                collage_id=collage.search_collage_by_name()
                if not collage_id:
                    collage.save()
                    collage_id = collage.search_collage_by_name()
                admin.update_user(email=request.form['email'],school_id=collage_id,user_id=request.form['save'])
            elif 'userdel':
                admin.del_user(request.form['userdel'])

        all_users= admin.get_users()

    return render_template('admin.html',all_users=all_users)



@app.route('/home', methods = ['GET','POST'])
@app.route('/', methods = ['GET','POST'])
def home_page():
    if 'username' in session:
        user=session['username']
    else:
        return redirect(url_for('login'))
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
            if 'del' in request.form:
                postid = request.form['postid']
                userid = request.form['userid']
                userName = request.form['username']

                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = """INSERT INTO HIDDENPOSTS(userid, postid) VALUES (%s,%s) """
                    cursor.execute(query, (userid, postid))
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
            query = """select m.userid, m.username, m.name, m.surname, m.linkpro, m.pid, m.linkpost, m.date, m.desc from (select users.id as userid, users.username as username, users.name as name, users.surname as surname, k.link1 as linkpro, k.id as pid, k.link2 as linkpost, k.date as date, k.description as desc from (select profilepic.link as link1,id,posts.userid as userid1,date,posts.link as link2,description from profilepic join posts on posts.userid=profilepic.userid) k join users on users.id=k.userid1) m left join hiddenposts on hiddenposts.postid=m.pid where hiddenposts.userid is null order by m.date desc"""
            cursor.execute(query)
            temp = cursor.fetchall()
            for post in temp:
                if post[0]==user_id:
                    user_data.append(post[4])
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

        else:
            return render_template('404.html'), 404


        connection.commit()
        if 'ChooseUser' in request.form:
            userName = request.form['ChooseUser']

            return redirect(url_for('home_page',user=userName))



    return render_template('main.html', user=user, user_data=user_data, allUsers=allUsers , posts=posts,postsLikes=posts_likes,postsComments=posts_comments,user_interests=user_interests)

@app.route('/add_post', methods = ['GET','POST'])
def add_post():
    posts = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT PostForView.ID, PostForView.FID, PostForView.POSTID FROM PostForView"""

        cursor.execute(query)

        for post in cursor:
            posts.append(post)

        connection.commit()


    if request.method =='POST':
        id = request.form['id']
        fid = request.form['fid']
        postid = request.form['postid']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PostForView (ID, FID, POSTID ) VALUES (%s, %s, %s )"""
            cursor.execute(query, (id, fid, postid))
            connection.commit()

    return render_template('add_post.html', posts=posts)

@app.route('/delete_post', methods = ['GET','POST'])
def delete_post():
    posts = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT PostForView.ID, PostForView.FID, PostForView.POSTID FROM PostForView"""

        cursor.execute(query)

        for post in cursor:
            posts.append(post)

        connection.commit()
    if request.method =='POST':
        fid = request.form['fid']
        postid = request.form['postid']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PostForView WHERE FID = '""" +fid + """' AND POSTID = '""" +postid + """'"""
            cursor.execute(query)
            connection.commit()

    return render_template('add_post.html', posts=posts)

@app.route('/update_post', methods = ['GET','POST'])
def update_post():
    posts = []
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT PostForView.ID, PostForView.FID, PostForView.POSTID FROM PostForView"""

        cursor.execute(query)

        for post in cursor:
            posts.append(post)

        connection.commit()

    if request.method =='POST':
        id = request.form['id']
        fid = request.form['fid']
        new_post = request.form['new_postid']

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE PostForView SET (ID, FID, POSTID) = (%s,%s, %s) WHERE ID = '""" +id + """' AND FID = '""" +fid + """'"""

            cursor.execute(query, (id, fid, new_post))
            connection.commit()


    return render_template('add_post.html', posts=posts)
#End of Ahmet Caglar Bayatli's space

@app.route('/initdb')
def initialize_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        initialize_db_func(cursor)
        connection.commit()
    return redirect(url_for('home_page'))

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

@app.route('/notification', methods = ['GET','POST'])
def notification_page():
    if 'username' in session:
        user = session['username']
    else:
        return redirect(url_for('login'))
    comments=[]
    likes=[]
    if user:
        with dbapi2.connect(app.config['dsn']) as connection:
            notification=Notifications(username=user,connection=connection)
            comments=notification.get_all_comments()
            likes =notification.get_all_likes()

    return render_template('notification.html',user=user, comments=comments,likes=likes)


#Start of EKREM CIHAD CETIN's space
@app.route('/profile', methods = ['GET','POST'])
@app.route('/<user2>/profile', methods = ['GET','POST'])
def profile_page(user2=None):
    if 'username' in session:
        user = session['username']
    else:
        return redirect(url_for('login'))
    now = datetime.datetime.now()
    images = []
    kullanici=[]
    userr=[]
    allfollowerpic=[]
    allfollowingpic=[]
    user_id=None
    posts_likes = {}
    posts_comments = {}
    user_interests=[]
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
            query="""select userid,link, username, name, surname,mail from users left join profilepic on  users.id=profilepic.userid where username='"""+user+"""' """
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
    app.secret_key = 'itucsdb1609'
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
