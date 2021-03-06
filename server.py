import datetime
import os
import json
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for
from flask import request
from jinja2.runtime import to_string
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


db= SQLAlchemy()
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
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=user.query.get(form.user.data)
        password = user.query.get(form.user.password)
        if user:
            if user == userid and passwordk
    return render_template('login.html', error=error)

@app.route('/initdb')
def initialize_database():
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor=connection.cursor()

            query="""DROP TABLE IF EXISTS COUNTER"""
            cursor.execute(query)

            query="""CREATE TABLE COUNTER (N INTEGER)"""
            cursor.execute(query)

            query="""INSERT INTO COUNTER (N) VALUES (0)"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS USERD"""
            cursor.execute(query)

            query="""CREATE TABLE USERD (
            userid INTEGER PRIMARY KEY,
            password INTEGER NOT NULL,
            TYPE VARCHAR(10) NOT NULL)"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS HASTA"""
            cursor.execute(query)

            query=""" CREATE TABLE HASTA(
            hasta_no INTEGER PRIMARY KEY,
            isim VARCHAR(15),
            YAS INTEGER,
            tc VARCHAR(11) NOT NULL,
            telefon VARCHAR(12),
            FOREIGN KEY (hasta_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS HASTALIK"""
            cursor.execute(query)

            query =""" CREATE  TABLE HASTALIK(
            hasta_no INTEGER,
            hastalik    VARCHAR,
            ilac_ad    VARCHAR,

            PRIMARY KEY ( hasta_no,hastalik,ilac_ad),
            FOREIGN KEY (hasta_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS ODA"""
            cursor.execute(query)

            query = """ CREATE TABLE ODA(
            oda_id INTEGER,
            oda_kap INTEGER,
            kisi_sayi INTEGER,
            hasta_no INTEGER,

            PRIMARY KEY(oda_id,oda_kap,kisi_sayi),
            FOREIGN KEY (hasta_no) REFERENCES USERD (userid)
            )"""
            cursor.execute (query)

            query="""DROP TABLE IF EXISTS DOKTOR"""
            cursor.execute(query)

            query = """ CREATE TABLE DOKTOR(
            doktor_ad VARCHAR,
            doktor_brans VARCHAR,
            doktor_yas INTEGER,
            doktor_tel VARCHAR,
            doktor_oda INTEGER,
            doktor_no INTEGER,

            PRIMARY KEY(doktor_no),
            FOREIGN KEY (doktor_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS RANDEVU"""
            cursor.execute(query)

            query = """ CREATE TABLE RANDEVU(
            hasta_no INTEGER,
            doktor_no INTEGER,
            tarih DATE,
            saat time,
            brans VARCHAR,

            PRIMARY KEY(hasta_no,doktor_no),
            FOREIGN KEY (doktor_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS AMELIYATHANE"""
            cursor.execute(query)

            query = """ CREATE TABLE AMELIYATHANE(
            ameliyathane_id INTEGER,
            hasta_no INTEGER,
            saat time,
            tarih DATE,

            PRIMARY KEY(hasta_no),
            FOREIGN KEY(hasta_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS TAHLIL"""
            cursor.execute(query)

            query = """ CREATE TABLE TAHLIL(
            hasta_no INTEGER,
            sonuc_idrar VARCHAR,
            sonuc_kan VARCHAR,

            PRIMARY KEY(hasta_no),
            FOREIGN KEY(hasta_no) REFERENCES USERD (userid)
            )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS HEMSIRE"""
            cursor.execute(query)

            query = """ CREATE TABLE HEMSIRE(
            hemsire_ad VARCHAR,
            hemsire_brans VARCHAR,
            hemsire_oda INTEGER,
            hemsire_no INTEGER,

            PRIMARY KEY(hemsire_no),
            FOREIGN KEY(hemsire_no) REFERENCES USERD(userid)
            )"""
            cursor.execute(query)

        connection.commit()
        return redirect(url_for('home_page'))

@app.route('/Signedup',methods=['GET','POST'])
def Signedup():
    if request.method == 'POST' :

        name = request.form["name"]
        surname = request.form["surname"]
        userid = request.form["userid"]
        password = request.form["password"]
        tc = request.form["T.C"]
        telno = request.form["telno"]

        with dbapi2.connect(app.config['dsn']) as connection:
            cursor=connection.cursor()


            cursor.execute("""INSERT INTO USERD(userid,password,TYPE) VALUES ("""+userid+""","""+password+""",1)""")

            #cursor.execute("""INSERT INTO HASTA(hasta_no,isim,tc,telefon) VALUES ("""+userid+""","""+name+""","""+tc+""","""+telno+""")""")
            cursor.execute("""INSERT INTO HASTA(hasta_no,isim,tc,telefon) VALUES (%s,%s,%s,%s)""",(userid,name,tc,telno))

            cursor.execute("""INSERT INTO "USER"(userid,password,TYPE) VALUES ("""+userid+""","""+password+""",1)""")

            cursor.execute('INSERT INTO HASTA(hasta_no,isim,tc,telefon) VALUES ('+userid+','+name+','+tc+','+telno+')')


            connection.commit()
        #return "name%s"% name
        return redirect(url_for('home_page'))


    return render_template('Signedup.html')
@app.route('/Signin_as_adminstrator',methods=['GET','POST'])
def Signin_as_adminstrator():
    return render_template('Signin_as_adminstrator.html')
@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query= "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times."% count

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
                               host='itucsdb1719.mybluemix.net' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
#itucsdb1719.mybluemix.net

