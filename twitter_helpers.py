#!/usr/bin/python
#
# Contains code taken from the python-oauth2 README.md here:
#

from oauth_helpers import OauthUrls
import json
from StringIO import StringIO

class Tweet(object):
	def __init__(self, text, screen_name, name, created_at, geo):
		self.text = text
		self.screen_name = screen_name
		self.name = name
		self.created_at = created_at
		self.geo = geo

	def __repr__(self):
		s = StringIO()
		s.write(u"%s\n" % self.created_at)
		s.write(u"%s (%s) wrote: " % (self.screen_name, self.name))
		s.write(u"\"%s\"" % self.text)
		if self.geo:
			self.write(u" at %s" % self.geo)

		return s.getvalue()



def parse_tweets(stream):
	"""
	Turn a json body containing one or more tweets into a list of Tweet objects.
	"""
	tweets = []
	items = json.loads(stream)
	for item in items:
		tweets.append(Tweet(item["text"], item["user"]["screen_name"], item["user"]["name"], item["created_at"], item["geo"]))

	return tweets

def get_twitter_urls():
	"""
	Returns the urls needed to connect to twitter.
	"""
	return OauthUrls("https://api.twitter.com/oauth/request_token",
			"https://api.twitter.com/oauth/authorize",
			"https://api.twitter.com/oauth/access_token")


