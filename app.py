"""APP SETUP"""

import env
from flask import Flask, redirect, request, render_template
from flask import session as flasksession
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from heapq import nlargest
import tweepy


app = Flask(__name__)
app.config.update(
    SECRET_KEY = env.APP_SECRET_KEY,
    SQLALCHEMY_DATABASE_URI = env.DATABASE_URL
)
db = SQLAlchemy(app)


"""DB MODEL(S)"""

"""
class AuthToken(db.Model):
    screen_name = db.Column(db.String(20), primary_key=True)
    token = db.Column(db.String(100))
    secret = db.Column(db.String(100))
"""

class Tweet(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    screen_name = db.Column(db.String(20), nullable=False)

    def fromTweetObj(tweet):
        id=tweet.id_str
        screen_name=tweet.user.screen_name
        return Tweet(id=id, screen_name=screen_name)

    def __repr__():
        return "<Tweet {} by {}>".format(self.id, self.screen_name)


"""SUPPORTING FUNCTIONS"""

def getApiInstance():
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET)
    auth.access_token, auth.access_token_secret = flasksession['AUTH_TOKEN'], flasksession['AUTH_SECRET']
    api = tweepy.API(auth)
    return api

def getTweets(api):
    #attempt to bypass tweet load
    if not flasksession.get('NEW_AUTH'):
        dbTweets = db.session.query(Tweet).filter_by(screen_name=api.me().screen_name).all()
        tweetIds = [t.id for t in dbTweets]
        tweets = api.statuses_lookup(tweetIds, tweet_mode='extended')
    else:
        #delete any existing tweets
        db.session.query(Tweet).filter_by(screen_name=api.me().screen_name).delete()
        db.session.commit()
        #load tweets
        now = datetime.now()
        startDate = datetime(now.year, 1, 1, 0, 0, 0) #only retrieve tweets from this year
        tweets = []
        tmpTweets = api.user_timeline(count=500, tweet_mode='extended')
        while(tmpTweets[-1].created_at > startDate):
            for tweet in tmpTweets:
                if tweet.full_text[:4] != "RT @": #exclude retweets
                    tweets.append(tweet)
            tmpTweets = api.user_timeline(max_id=tmpTweets[-1].id, count=500, tweet_mode='extended')
        if tmpTweets[0].created_at > startDate:
            for tweet in tmpTweets:
                if tweet.created_at > startDate and tweet.full_text[:4] != "RT @": #exclude retweets
                    tweets.append(tweet)
    return tweets

def getHighlights(tweets):
    top5Rts = nlargest(3, tweets, key=lambda t:t.retweet_count) #bad variable name- top 5 is now top 3
    top5Likes = nlargest(3, tweets, key=lambda t:t.favorite_count)
    mostRts = [{'retweet_count':t.retweet_count, 'favorite_count':t.favorite_count, 'full_text':t.full_text, 'created_at':t.created_at} for t in top5Rts]
    mostLikes = [{'retweet_count':t.retweet_count, 'favorite_count':t.favorite_count, 'full_text':t.full_text, 'created_at':t.created_at} for t in top5Likes]
    payload = {'mostRts':mostRts, 'mostLikes':mostLikes}
    if flasksession['NEW_AUTH']:
        dbTweets = {tweet.id:tweet for tweet in top5Rts}
        for tweet in top5Likes:
            dbTweets[tweet.id] = tweet
        for tweet in list(dbTweets.values()):
            t = Tweet.fromTweetObj(tweet)
            db.session.add(t)
        db.session.commit()
    return payload


"""FLASK ROUTES"""

@app.route('/', methods=['GET'])
def home():
    #check for user authentication
    try:
        api = getApiInstance()
    except Exception:
        return redirect('/auth')
    #load user's top tweets
    tweets = getTweets(api)
    twitterData = getHighlights(tweets)
    flasksession['NEW_AUTH'] = False
    #load page
    data = {'tweetCount':len(tweets), 'mostRts':twitterData['mostRts'], 'mostLikes':twitterData['mostLikes']}
    return render_template('index.html', data=data)

@app.route('/auth')
def start_auth():
    #future addition - bypass repeat auth by caching tokens in database
    auth = tweepy.OAuthHandler(env.TWITTER_API_KEY, env.TWITTER_API_SECRET, env.CALLBACK_URL)
    redirect_url = auth.get_authorization_url()
    flasksession['REQUEST_TOKEN'] = auth.request_token
    flasksession['NEW_AUTH'] = True
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
    #future addition - commit tokens to database for oauth bypass
    flasksession['AUTH_TOKEN'] = token
    flasksession['AUTH_SECRET'] = secret
    return redirect('/')


"""APP DRIVER"""

if __name__ == "__main__":
    app.run()
