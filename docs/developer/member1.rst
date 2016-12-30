Parts Implemented by Ali ERCAN - 040090506
================================================

Developer Guide

Initialization of database objects which users, userlogin, school, city and gender tables actualize in the initialize_db.py.

Create Table Queries for USERS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
    cursor.execute("""CREATE TABLE USERS (ID SERIAL PRIMARY KEY UNIQUE,
                                          USERNAME VARCHAR(50) UNIQUE NOT NULL ,
                                         NAME VARCHAR(50) NOT NULL,
                                         SURNAME VARCHAR(50) NOT NULL,
                                         MAIL VARCHAR(50) UNIQUE NOT NULL,
                                         GENDER INTEGER  references GENDER(ID),
                                         SCHOOL INTEGER  references SCHOOL(ID),
                                         CITY INTEGER  references CITY(ID))""")
    
Create Table Queries for USERLOGIN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS USERLOGIN CASCADE""")
    cursor.execute("""CREATE TABLE USERLOGIN (USERNAME VARCHAR(50)  PRIMARY KEY  references  users(username) ON DELETE CASCADE ,
                                               PASSWORD VARCHAR(50) NOT NULL,
                                               LASTLOGIN TIMESTAMP DEFAULT NULL,
                                                ADMIN    BOOLEAN       DEFAULT FALSE )""")
    
Create Table Queries for SCHOOL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS SCHOOL CASCADE""")
    cursor.execute("""CREATE TABLE SCHOOL (ID  SERIAL PRIMARY KEY,SCHOOLNAME character varying(50) NOT NULL )""")
    
Create Table Queries for CITY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS CITY CASCADE""")
    cursor.execute("""CREATE TABLE CITY (ID  SERIAL PRIMARY KEY,CITYNAME character varying(20) NOT NULL )""")
    
Create Table Queries for GENDER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    cursor.execute("""DROP TABLE IF EXISTS GENDER CASCADE""")
    cursor.execute("""CREATE TABLE GENDER (ID  SERIAL PRIMARY KEY,TYPE character varying(10) NOT NULL )""")

.. toctree::
   member5/login
   member5/register
   member5/admin
   member5/logout

