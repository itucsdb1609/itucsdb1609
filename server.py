import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
# from werkzeug import redirect
from flask.helpers import url_for


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


@app.route('/')
def home_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
          
        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)
          
        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)
          
        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)
          
        connection.commit()
    return render_template('main.html')

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
def explore_page():
    now = datetime.datetime.now()
    return render_template('explore.html', current_time=now.ctime())

@app.route('/notifications')
def notification_page():
    now = datetime.datetime.now()
    return render_template('notification.html', current_time=now.ctime())

@app.route('/profile')
def profile_page():
    now = datetime.datetime.now()
    return render_template('profile.html', current_time=now.ctime())


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
