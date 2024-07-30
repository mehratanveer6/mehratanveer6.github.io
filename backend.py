# app.py
from flask import Flask, render_template, request, jsonify # type: ignore
import tweepy
from collections import Counter
import os

app = Flask(__name__)

# Twitter API credentials
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form['username']
    
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    # Fetch tweets
    tweets = api.user_timeline(screen_name=username, count=200, tweet_mode="extended")
    
    # Process tweets and count keywords
    words = []
    for tweet in tweets:
        words.extend(tweet.full_text.lower().split())
    
    # Remove common words and count
    common_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'is', 'are'])
    word_counts = Counter(word for word in words if word not in common_words and not word.startswith('@'))
    
    # Get top 20 keywords
    top_keywords = dict(word_counts.most_common(20))
    
    return jsonify(top_keywords)

if __name__ == '__main__':
    app.run(debug=True)