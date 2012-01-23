#!/usr/bin/python
#
#
import os
import cPickle as pickle
import oauth2
from oauth_helpers import authenticate,OauthToken
from twitter_helpers import get_twitter_urls, parse_tweets
from twitter_app_key import consumer_key, consumer_secret

# This is where we put the user's authenticated key.
STORED_FILE = "twit_auth.key"

if not os.path.exists(STORED_FILE):
	print "No token stored - Need to authenticate"
	
	token_details = authenticate(get_twitter_urls(), consumer_key, consumer_secret)
	f = open(STORED_FILE, "w")
	pickle.dump(token_details, f)
	f.close()
else:
	f = open(STORED_FILE, "r")
	token_details = pickle.load(f)
	f.close()

token = oauth2.Token(token_details.key, token_details.secret)

consumer = oauth2.Consumer(consumer_key, consumer_secret)
client = oauth2.Client(consumer, token)

resp, content = client.request("http://api.twitter.com/1/statuses/home_timeline.json?count=20", "GET")

tweets = parse_tweets(content)

for tweet in tweets:
	print unicode(tweet).encode("utf-8")

