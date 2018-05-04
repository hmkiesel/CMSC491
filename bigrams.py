"""
Bigrams are collocated words taken 2 at a time;
they're useful and effective for finding words
that should be considered as a unit. Since the
company we chose is Starbucks, using bigrams lets
us know that phrases like "Starbucks Rewards" and
"Bonus Stars" should be considered collectively.
"""

from bs4 import BeautifulSoup
import codecs
import json
import nltk
from nltk import BigramAssocMeasures
import requests

# routine to remove unicode characters
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if (ord(char) < 128):
			asciiText = asciiText + char
	return asciiText

def findBigrams():
	fileObj = codecs.open("starbucksData.rtf", "w", "UTF")

	# accesses a specified webpage
	html = requests.get("https://www.starbucks.com/")
	
	# creates a parse tree
	soup = BeautifulSoup(html.text, 'html5lib')

	# specifies the paragraph tag to get meaningful words
	all_paras = soup.find_all('p')

	# writes text to file and collates it into a str var
	full_string = ""
	for para in all_paras:
		fileObj.write(para.text)
		full_string = full_string + para.text
	
	asc_2017 = removeUnicode(full_string)

	# retrieves a list of words by sentence to feed into our searcher
	bigWords = nltk.tokenize.word_tokenize(asc_2017)

	# number of collocations to find
	collocations = 25

	# analyzes bigWords for collocations with a searcher
	search = nltk.BigramCollocationFinder.from_words(bigWords)

	# filter out collocations that don't occur at least 2 times
	search.apply_freq_filter(2)

	# filter out collocations that have stopwords
	search.apply_word_filter(lambda skips: skips in nltk.corpus.stopwords.words('English'))

	# uses Jaccard index to find our biagrams
	idxJaccard = BigramAssocMeasures.jaccard
	bigrams = search.nbest(idxJaccard, collocations)

	print "Set of bigrams (for homepage)"
	for bigram in bigrams:
		print str(bigram[0]).encode('utf-8'), " ", str(bigram[1].encode('utf-8'))