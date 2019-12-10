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

class Tweet(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True)
    num_likes = db.Column(db.Integer(), default=0)
    num_retweets = db.Column(db.Integer(), default=0)
    def __repr__():
        return "<Tweet by {} at {}>".format(self.username, self.timestamp)


"""SUPPORTING FUNCTIONS"""

def getApiInstance():
    """
    returns: tweepy api object authenticated with oauth2
    """
    auth = tweepy.AppAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    api = tweepy.API(auth)
    return api

def getTopTweets(username):
    """
    username: str -> screen name of a twitter user
    returns: dictionary containing 'mostRts' and 'mostLikes' with lists of 5 tweet objects each, sorted from most to fewest
    """
    api = getApiInstance()


"""FLASK ROUTES"""

@app.route('/', methods=['GET'])
def home():
    pageName = 'HOME'
    data = {'pageName':pageName}
    return render_template('index.html', data=data)

@app.route('/top', methods=['POST'])
def top():
    tweets = twitter.getTopTweets()
    mostRts = tweets['mostRts']
    mostLikes = tweets['mostLikes']
    pageName = 'TOP'
    data = {'mostRts':mostRts, 'mostLikes':mostLikes, 'pageName':pageName}
    return render_template('index.html', data=data)
