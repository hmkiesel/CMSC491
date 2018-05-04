#PART OF SPEECH ANALYSIS

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

for (token, pos) in posWords:
	print token, pos
	
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