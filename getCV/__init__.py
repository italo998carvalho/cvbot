from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from time import sleep
import requests, os
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://italo:1234@localhost/webbot'
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

from getCV.models.user import User

curriculos = [
    '1268591658881312', 
    '5948825528321491', 
    '6788650231964768'
    ]

cvs_json = []

def index():
    while True:
        sleep(5)
        count, qtd = 0, len(curriculos)
        if count == qtd:
            count = 0
        r = requests.get("http://18.188.15.38/cnpq/cv/{}".format(curriculos[count]), auth=('inova', '!nov@123'))
        user = User(r.json())
        db.session.add(user)
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=index,
    trigger=IntervalTrigger(seconds=5),
    replace_existing=True)
atexit.register(lambda: scheduler.shutdown())
