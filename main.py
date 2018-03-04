import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from pprint import pprint

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
BASE_URL = 'https://api.instagram.com/v1/'

def owner_info():
    r = requests.get('%susers/self/?access_token=%s' %  (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print "username is %s" %(r['data']['username'])
        print "My no of follower are %s" % (r['data']['counts']['followed_by'])
        print "No of people you are following %s" % (r['data']['counts']['follows'])
        print "no of posts: %s" % (r['data']['counts']['media'])
    else:
        print "status code received does not match"

def owner_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' %  (BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        url = r['data'][1]['images']['standard_resolution']['url']
        name = r['data'][1]['id'] + '.jpg'
        urllib.urlretrieve(url,name)
        print "your image is download"
    else:
        print "status code is wrong"

def get_user_id(uname):
    r = requests.get("%susers/search?q=%s&access_token=%s"%(BASE_URL,uname,APP_ACCESS_TOKEN)).json()
    return r['data'][0]['id']

def user_info(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print "username is %s" % (r['data']['username'])
        print "My no of follower are %s" % (r['data']['counts']['followed_by'])
        print "No of people you are following %s" % (r['data']['counts']['follows'])
        print "no of posts: %s" % (r['data']['counts']['media'])
    else:
        print "status code received does not match"


def user_post(username):
    user_id = get_user_id(username)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print r['data'][0]['videos']['low_resolution']['url']
        url = r['data'][0]['videos']['low_resolution']['url']
        name = r['data'][0]['id'] + '.mp4'
        urllib.urlretrieve(url, name)
        print "your video is download"
    else:
        print "status code is wrong"

def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        return r['data'][0]['id']
    else:
        print "status code is wrong"

def like_post(uname):
    media_id = get_media_id(uname)
    payload ={"access_token": APP_ACCESS_TOKEN}
    url= BASE_URL + 'media/%s/likes' % media_id
    r =requests.post(url,payload).json()
    if r['meta']['code'] == 200:
        print "like successful"
    else:
        print "like unsuccessful"

def comment_post(uname):
    media_id=get_media_id(uname)
    comment =raw_input("what is your comment")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment}
    url = BASE_URL + 'media/%s/comments' % media_id
    r = requests.post(url, payload).json()
    if r['meta']['code'] == 200:
        print "comment successful"
    else:
        print "comment unsuccessful"

def deleat_comment(uname):
    media_id = get_media_id(uname)
    r =requests.get("%smedia/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        if len(r['data']) > 0:
            for index in range(0,len(r['data'])):
                comment_id =r['data'][index]['id']
                comment_text = r['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print 'Negative comment : %s' % comment_text
                    r = requests.delete('%smedia/%s/comments/%s/?access_token=%s' % (
                    BASE_URL, media_id, comment_id, APP_ACCESS_TOKEN)).json()
                    if r['meta']['code'] == 200:
                        print 'Comment successfully deleted!'
                    else:
                        print 'Could not delete the comment'
                else:

                    print comment_text + 'is a positive comment'

        else:
            print "kuch nahi mila"
    else:
        print "kuch to glt hua hai"

def start_bot():
    show_menu = True
    while show_menu:
        query = input("what do u want to do? \n 1. get owner info \n 2.get owner pst \n 3.get user info \n 4.get user post \n 5. like a post \n 6. comment a post \n 7. deleat negative comment \n 0. exit ")
        if query ==1:
            owner_info()
        elif query==2:
            owner_post()
        elif query ==3:
            username = raw_input("what is the name of the user?")
            user_info(username)
        elif query ==4:
            username = raw_input("what is the name of the user?")
            user_post(username)
        elif query == 5:
            username = raw_input("what is the name of the user?")
            like_post(username)
        elif query == 6:
            username = raw_input("what is the name of the user?")
            comment_post(username)
        elif query == 7:
            username = raw_input("what is the name of the user?")
            deleat_comment(username)
        elif query ==0:
            show_menu =False
        else:
            print"error"
start_bot()
