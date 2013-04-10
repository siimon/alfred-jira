import oauth2 as oauth
from signature_method import SignatureMethod_RSA_SHA1
import urlparse
import json

print """
Welcome to Alfred JIRA setup!
You now need to input some values to make Alfred and JIRA work together.
"""

consumer_key = raw_input('JIRA Consumer key: ')
consumer_secret = raw_input('JIRA Consumer key secret: ')
request_token_url = raw_input('JIRA Request token url: ') #'http://jira.company.net/plugins/servlet/oauth/request-token'
access_token_url = raw_input('JIRA Access token url: ') #'http://jira.company.net/plugins/servlet/oauth/access-token'
authorize_url = raw_input('JIRA Authorize url: ') # 'http://jira.company.net/plugins/servlet/oauth/authorize'
key_path = raw_input('Path to private key used in JIRA OAuth setup: ') # args.keyPath
base_url = raw_input('URL to JIRA (http://jira.company.com): ')
data_url = '%s/rest/api/2/issue/' % base_url #'http://jira.company.net/rest/api/2/issue/'

settings = { 'consumer_key' : consumer_key, 'consumer_secret': consumer_secret, 'request_token_url': request_token_url
    ,'base_url': base_url, 'key_path': key_path }

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)
client.set_signature_method(SignatureMethod_RSA_SHA1(key_path))

resp, content = client.request(request_token_url, "POST")
if resp['status'] != '200':
  raise Exception("Invalid respones, %s: %s" % (resp['status'], content))

request_token = dict(urlparse.parse_qsl(content))


print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

accepted = 'n'
while accepted.lower() == 'n':
    accepted = raw_input('Press y to continue after you have copy and pasted the link above ')

token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])

client = oauth.Client(consumer, token)
client.set_signature_method(SignatureMethod_RSA_SHA1(key_path))

resp, content = client.request(access_token_url, "POST")
access_token = dict(urlparse.parse_qsl(content))

print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."
print

accessToken = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
client = oauth.Client(consumer, accessToken)
client.set_signature_method(SignatureMethod_RSA_SHA1(key_path))

resp, content = client.request(data_url, "GET")

settings['access_token'] = access_token['oauth_token']
settings['access_token_secret'] = access_token['oauth_token_secret']
f = open('settings.txt', "w")
try:
  f.write(json.dumps(settings))
finally:
  f.close()
print content
