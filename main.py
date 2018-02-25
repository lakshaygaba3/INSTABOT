import requests
from pprint import pprint

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
BASE_URL = 'http://api.instagram.com/v1/'

def owner_info():
    r = requests.get('%susers/self/?access_token=%s' %  (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print "username is %s" %(r['data']['username'])
        print "My no of follower are %s" % (r['data']['counts']['followed_by'])
    else:
        print "status code received does not match"

owner_info()