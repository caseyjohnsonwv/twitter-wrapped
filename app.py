import env
from flask import Flask, redirect, request, render_template
from flask import session as flasksession
from flask_sqlalchemy import SQLAlchemy
import tweepy

app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
    SQLALCHEMY_DATABASE_URI = env.DATABASE_URL
)
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def home():
    data = {'pageName':'HOME'}
    return render_template('index.html', data=data)
