"""APP SETUP"""

import env
from flask import Flask, redirect, request, render_template
from flask import session as flasksession
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tweepy


app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
    SQLALCHEMY_DATABASE_URI = env.DATABASE_URL
)
db = SQLAlchemy(app)


"""DB MODEL(S)"""

class AuthToken(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    token = db.Column(db.String(100))
    secret = db.Column(db.String(100))

class Tweet(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True)
    num_likes = db.Column(db.Integer(), default=0)
    num_retweets = db.Column(db.Integer(), default=0)
    def __repr__():
        return "<Tweet by {} at {}>".format(self.username, self.timestamp)


"""SUPPORTING FUNCTIONS"""

def getApiInstance():
    pass


"""FLASK ROUTES"""

@app.route('/', methods=['GET'])
def home():
    pageName = 'HOME'
    data = {'pageName':pageName}
    return render_template('index.html', data=data, pageName=pageName)

@app.route('/top', methods=['POST'])
def top():
    tweets = twitter.getTopTweets()
    mostRts = tweets['mostRts']
    mostLikes = tweets['mostLikes']
    pageName = 'TOP'
    data = {'mostRts':mostRts, 'mostLikes':mostLikes}
    return render_template('index.html', data=data, pageName=pageName)

@app.route('/auth')
def start_auth():
    pass

@app.route('/callback')
def callback():
    pass


"""APP DRIVER"""

if __name__ == "__main__":
    app.run()
