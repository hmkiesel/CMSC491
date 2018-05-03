# File: facebook-james.py
# Author: James Williams

import facebook
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import nltk

# Globals
ACCESS_TOKEN = 'your_key_here'
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

def getSkips():
    return ["and", ",", ".", "to", "the", "for", "in", "of", "that", "a", "on", "is", "get", "you", "has", "as",
         "at", "are", "", "an", "with", "will", "not", "have", "would", "so", "", "but", ":", "be", "like",
         "if", "should", "also", "there", "or", "by", "per", "they", "only", "can", "I", "who", "this",
         "it", "from", "one", "their", "The", "then", "his", "J", "we", "If", "?", "!"]

def tokenizeText(text):
    words = []
    tokenizePosts = nltk.tokenize.sent_tokenize(text)
    
    for sentence in tokenizePosts:
        for word in nltk.tokenize.word_tokenize(sentence):
            words.append(word.lower())
            
    return words

def getFrqDist(text):
    words = tokenizeText(text)
    mostFreqStr = ""
    
    for gmrWord in words:
        if gmrWord not in getSkips():
            mostFreqStr += gmrWord

    return nltk.FreqDist(words)

def getMostFreqWords(text):
    frqDist =  getFrqDist(text)
    mostFreq = []

    for w in frqDist.items():
        if w[0] not in getSkips():
            mostFreq.append(w)
            
    mostFreq.sort(key=lambda c: c[1])
    return mostFreq

def getLexicalDiversity():
    postsString = collectPosts()
    
    frqDist = getFrqDist(postsString)
    wordCnt = len(tokenizeText(postsString))
    hapaxNo = len(frqDist.hapaxes())

    print 'Number of Words:'.ljust(25), wordCnt
    print 'Number of Hapaxes:'.ljust(25), hapaxNo
    print 'Lexical Diversity is %f' % (1.0 * hapaxNo / wordCnt)
    
    print "\nThe most frequent words follow:"
    
    for w in getMostFreqWords(postsString)[:-10:-1]:
        print w[0].encode('utf-8'), "\thas a count of ", w[1]

# just call these two functions
def main():
    print "Analysis of posts from IBM's Facebook"
    printPosts()
    getLexicalDiversity()
    
main()