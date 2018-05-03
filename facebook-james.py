# File: facebook-james.py
# Author: James Williams

import facebook

# Globals
ACCESS_TOKEN = 'your_key_here'
FB_URL = 'https://graph.facebook.com/'
IBM = '168597536563870'

def removeUnicode(text):
        asciiText = ""
        for char in text:
            if (ord(char) < 128):
                asciiText = asciiText + char
                
        return asciiText

def authenticate():
    return facebook.GraphAPI(ACCESS_TOKEN)

def getPosts():
    fb = authenticate()
    get_fields = ['id', 'message', 'created_time', 'caption', 'shares', 'likes.summary(true)', 'comments']
    get_fields = ','.join(get_fields)
    
    d_posts = fb.get_connections(IBM, 'posts', fields=get_fields)
    return d_posts['data']

def printPosts():
    posts = getPosts();
    asc_2018 = ""
    
    for i in range(0, len(posts)):
        print '\n##############################\n'
        print "Post ", i+1, " is: ", posts[i]['message'].encode('utf-8')
        asc_2018 = asc_2018 + removeUnicode(posts[i]['message'])
        print "Like count is ", posts[i]['likes']['summary']['total_count']
    
printPosts()