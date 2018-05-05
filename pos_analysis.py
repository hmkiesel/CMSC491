#PART OF SPEECH ANALYSIS - J Do

# WARNING - This may take a while to run because it is unoptimized
# This POS analyzer finds all the tags in the given 'link', counts them
# and then prints all the words associated with each tag separated by spaces,
# counting the number of words for each tag as well. In the end, there is a 
# Chunk analysis using Russell's algorithm.

from bs4 import BeautifulSoup
import requests
import json
import codecs
import nltk

def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText

def get_pos():
	fileObj = codecs.open("POS.rtf","w","UTF")
	link = "https://starbucks.com/about-us/company-information"
	html = requests.get(link)

	soup = BeautifulSoup(html.text,'html5lib')
	all_paras = soup.find_all('p')

	data_2017 = ""
	for para in all_paras:
		fileObj.write(para.text)
		data_2017 = data_2017 + para.text
	asc_2017 = removeUnicode(data_2017)

	lstSent = nltk.tokenize.sent_tokenize(asc_2017)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

	print "Part Of Speech Tags for " + link + " :"

	sentWords = [nltk.tokenize.word_tokenize(s) for s in lstSent]
	posWords = [nltk.pos_tag(w) for w in sentWords]
	posWords = [token for sent in posWords for token in sent]

	#THIS IS THE ORIGINAL PRINTING LOOP - It simply prints the word and the part of speech
	#for (token, pos) in posWords:
	#	print token, pos

	#GET ALL TAGS
	partsofspeech = []
	for (token, pos) in posWords:
		if pos not in partsofspeech:
			partsofspeech.append(pos)
		#print token, pos
	print partsofspeech
	print "Total # of tags: ",
	print len(partsofspeech)

	#PRINT SPECIFIC PARTS OF SPEECH
	for i in partsofspeech:
		count = 0
		print "\n[ Part Of Speech tag: " + i + " ]"
		for (token, pos) in posWords:
			if i == pos:
				print token,
				count += 1
		print "\n=> [ " + i + " ] count is:", 
		print count
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

	chunkCollector = []
	foundChunk = []

	lastPos = None
	for(token, pos) in posWords:
		if pos == lastPos and pos.startswith('NN'):
			foundChunk.append(token)
		elif pos.startswith('NN'):
			if foundChunk != []:
				chunkCollector.append((''.join(foundChunk),pos))
			foundChunk = [token]
		lastPos = pos

	dChunk = {}
	for chunk in chunkCollector:
		dChunk[chunk] = dChunk.get(chunk, 0) + 1

	print "\nCount Frequency for each Chunk using Russell's Algorithm:"
	for (entity, pos) in dChunk:
		if entity.istitle():
			print '\t%s (%s)' % (entity, dChunk[entity, pos])
