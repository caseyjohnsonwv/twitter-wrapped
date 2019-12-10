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
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    auth.access_token, auth.access_token_secret = flasksession['AUTH_TOKEN'], flasksession['AUTH_SECRET']

def getTopTweets():
    api = getApiInstance()


"""FLASK ROUTES"""

@app.route('/', methods=['GET'])
def home():
    #load user's top tweets
    try:
        tweets = getTopTweets()
    except Exception as ex:
        print(ex)
        return redirect('/auth')
    #load page
    data = {}
    return render_template('index.html', data=data)


@app.route('/auth')
def start_auth():
    #future addition - bypass repeat auth by caching tokens in database
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET, env.CALLBACK_URL)
    redirect_url = auth.get_authorization_url()
    flasksession['REQUEST_TOKEN'] = auth.request_token
    return redirect(redirect_url)


@app.route('/callback')
def callback():
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    auth.request_token = flasksession['REQUEST_TOKEN']
    del flasksession['REQUEST_TOKEN']
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    #test auth
    token, secret = auth.access_token, auth.access_token_secret
    api = tweepy.API(auth)
    username = api.me().screen_name
    #future addition - commit tokens to database for oauth bypass
    flasksession['AUTH_TOKEN'] = token
    flasksession['AUTH_SECRET'] = secret
    return redirect('/')


"""APP DRIVER"""

if __name__ == "__main__":
    app.run()
