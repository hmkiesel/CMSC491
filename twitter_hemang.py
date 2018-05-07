#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Hemang Bhatt
"""

"""
Implemented assignment using Twitter search API. Twitter search API retrieves most recent last #number of tweets.
In contrast, Twitter Stream API returns #number of tweets happen in future. For our assignments, we used Twitter search api because sometimes if
the tweet, we want to search for, is not active (frequently tweeted) then it would not be feasible to retrieve number of tweets in given time so we used search api 
to get the most recent last #number of tweets. In addition, Vader Sentiment package is used to calculate the sentiment of a tweet. Moreover, lexical diversity is calculated for each tweet. For each tweet, tweet text, number of retweet, sentiment, and Lexical diversity is printed. Also, it prints overall report of lexical diversity, sentiment, and retweet count of all retrieved tweets.
"""

import twitter
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


# SET UP YOUR TWITTER CRED.
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


def removeUnicode(text):
    asciiText = ""
    for char in text:
        if(ord(char) < 128):
            asciiText = asciiText + char
    return asciiText

def get_tweets(q = '#starbucks', count = 25):
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
    tw = twitter.Twitter(auth=auth)
    
    print "==============================" * 2
    print "\n\t" + '\033[95m' +  str(count) + " Tweets with " + q + '\033[0m' + "\n"
    print "==============================" * 2
    
    tweets = tw.search.tweets(q=q, count=count, lang='en')
    
    texts = []
    counter = 0
    neg_tweet = 0
    pos_tweet = 0
    retweet_counter = 0
    total_senti = 0
    for status in tweets["statuses"]:
        counter += 1
        texts.append(status["text"])
        
        words = []
    
        for w in removeUnicode(status['text']).split():
            words.append(w)
        
        vs = vaderSentiment(status["text"].encode('utf-8'))
        if (vs['compound'] > 0): pos_tweet += 1
        if (vs['compound'] < 0): neg_tweet += 1
        print "\n" + "="* 10 + "Tweet # " + str(counter) + "=" * 10 + "\n"    
        print removeUnicode(status['text'])
        retweet_counter += status["retweet_count"]
        print "\nRetweet count: %d\n" % (status["retweet_count"])
        print "Lexical Diversity: ", 1.0 * len(set(words)) / len(words)
        print "\nSentiment: " + str(vs['compound'])
        total_senti += vs['compound']

    print "==============================" * 2
    print "\nReport over %d tweets: \n" % counter
    print "Total number of retweets: %d\n" % retweet_counter

    print "Negative tweets: " + str(neg_tweet)
    print "\nPositive tweets: " + str(pos_tweet)
    print "\nOverall sentiment: " + str(total_senti/counter)

    words = []
    for t in texts:
        words += [ w for w in removeUnicode(t).split() ]

    lexical_diversity = 1.0 * len(set(words)) / len(words)
    print "\nOverall lexical diversity: ", lexical_diversity

