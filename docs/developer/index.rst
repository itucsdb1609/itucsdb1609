Developer Guide
===============

**Database Design**
###################

**ER Diagram**

.. figure:: diagram.png
   :scale: 80 %
   :alt: ER Diagram
   :align: center

   The ER diagram of the database, created by SOCIALBUM members.

The database has different dependencies in between as it can be seen from the ER diagram. The application has a default database.
It is defined in "initialize_db.py" file as a seperate file. The other codes are inside a one consistent file. The initialization drops all the current tables accordingly (by that it is referred to using cascade while dropping).
After that tables are created and some default values are inserted. For example:


.. code-block:: python

   cursor.execute("""DROP TABLE IF EXISTS CITY CASCADE""")
   cursor.execute("""CREATE TABLE CITY (ID  SERIAL PRIMARY KEY,CITYNAME character varying(20) NOT NULL )""")
   cursor.execute("""DROP TABLE IF EXISTS SCHOOL CASCADE""")
   cursor.execute("""CREATE TABLE SCHOOL (ID  SERIAL PRIMARY KEY,SCHOOLNAME character varying(50) NOT NULL )""")
   cursor.execute("""DROP TABLE IF EXISTS USERS CASCADE""")
   cursor.execute("""CREATE TABLE USERS (ID SERIAL PRIMARY KEY UNIQUE,
                                          USERNAME VARCHAR(50) UNIQUE NOT NULL ,
                                         NAME VARCHAR(50) NOT NULL,
                                         SURNAME VARCHAR(50) NOT NULL,
                                         MAIL VARCHAR(50) UNIQUE NOT NULL,
                                         GENDER INTEGER  references GENDER(ID),
                                         SCHOOL INTEGER  references SCHOOL(ID),
                                         CITY INTEGER  references CITY(ID))""")

**Code**
########

The code is written in Python 3.5.2. It is used in html documents to create the dynamic tables. Javascript also used for creating a responsive interface along with css. jQuery is used as a framework.

**Group Members**
#################

.. toctree::

   member1
   member2
   member3
   member4
   member5
