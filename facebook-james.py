# File: facebook-james.py
# Author: James Williams

import facebook
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

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
    
    totalSentiment = 0;
    positivePosts = 0;
    negativePosts = 0;
    
    for i in range(0, len(posts)):
        
        # general information
        print "Post ", i+1, " is: ", posts[i]['message'].encode('utf-8'), "\n"
        print "Like count is ", posts[i]['likes']['summary']['total_count']
        
        # sentiment
        vs = getSentiment(posts[i]['message'])
        print "Post Sentiment is ", vs
        totalSentiment += vs
        
        if vs < 0:
            negativePosts += 1
        
        else:
            positivePosts += 1
            
        print '\n##############################\n'
            
    print "End of posts"
    print "Overall Sentiment is ", str((totalSentiment / len(posts)))
    print "Number of positive posts is ", str(positivePosts)
    print "Number of negative posts is ", str(negativePosts)
        
def getSentiment(text):
    vs = vaderSentiment(text.encode('utf-8'))
    return vs['compound']

def collectPosts():
    posts = getPosts();
    postsString = ""
    
    for i in range(0, len(posts)):
        postsString += removeUnicode(posts[i]['message'])
        
    return postsString
    
printPosts()