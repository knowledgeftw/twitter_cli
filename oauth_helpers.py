#!/usr/bin/python
#
# Contains code taken from the python-oauth2 README.md here:
#    
#

import urlparse
import oauth2
import os


class OauthToken(object):
	"""
	This is a simple class which we can pickle and restore.
	"""
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret

class OauthUrls(object):
	"""
	Represents the three URLs that you need to perform an oauth
	exchange.
	"""
	def __init__(self, request_token_url, auth_token_url, access_token_url):
		self.request_token_url = request_token_url
		self.auth_token_url = auth_token_url
		self.access_token_url = access_token_url


def authenticate(urls, consumer_key, consumer_secret):
	consumer = oauth2.Consumer(consumer_key, consumer_secret)
	client = oauth2.Client(consumer)

	# Step 1: Get a request token. This is a temporary token that is used for 
	# having the user authorize an access token and to sign the request to obtain 
	# said access token.

	resp, content = client.request(urls.request_token_url, "GET")
	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])

	request_token = dict(urlparse.parse_qsl(content))

	# Step 2: Redirect to the provider. Since this is a CLI script we do not 
	# redirect. In a web application you would redirect the user to the URL
	# below.

	print "Go to the following link in your browser:"
	print "%s?oauth_token=%s" % (urls.auth_token_url, request_token['oauth_token'])
	print 

	# After the user has granted access to you, the consumer, the provider will
	# redirect you to whatever URL you have told them to redirect to. You can 
	# usually define this in the oauth_callback argument as well.
	accepted = 'n'
	while accepted.lower() == 'n':
	    accepted = raw_input('Have you authorized me? (y/n) ')
	oauth_verifier = raw_input('What is the PIN? ')

	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the 
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this 
	# access token somewhere safe, like a database, for future use.
	token = oauth2.Token(request_token['oauth_token'],
	    request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth2.Client(consumer, token)

	resp, content = client.request(urls.access_token_url, "POST")
	access_token = dict(urlparse.parse_qsl(content))

	token = OauthToken(access_token['oauth_token'],
		 access_token['oauth_token_secret'])

	return token


