from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from bs4 import BeautifulSoup
import requests
import codecs


def get_summary(url):
    parser = HtmlParser.from_url(url, Tokenizer('English'))
    stemmer = Stemmer('English')
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words('English')

    print("\nThree Sentence Summary:\n")
    for sentence in summarizer(parser.document, 3):
        print(sentence)


def scrape_profile():
    fileObj = codecs.open("starbucksData.rtf", "w", "UTF")
    html = requests.get("https://www.starbucks.com/about-us/company-information/starbucks-company-profile")

    soup = BeautifulSoup(html.text, 'html5lib')
    all_paras = soup.find_all(['p','li'])

    # Write test to file and collate it into a str var
    data = ""
    year = ""
    stores = ""
    coffees = ""
    publicdate = ""
    price = ""
    for para in all_paras:
        if 'began in' in para.text:
            line = para.text.split('began in ')
            year = line[1][0:3]
        if 'Total stores' in para.text:
            line = para.text.split('Total stores: ')
            stores = line[1].split('*')[0]
        if 'blends' in para.text:
            line = para.text.split(' blends')
            coffees = line[0].split('More than ')[-1]
        if 'public on' in para.text:
            line = para.text.split('public on ')
            publicdate = line[1].split(' at')[0]
            line2 = para.text.split('price of ')
            price = line2[1].split(' per share')[0]

        #fileObj.write(para.text)
        #data = data + para.text
    print("\nScreen Scrape of Starbucks Company Profile:\n")
    print("opening date: %s"%year)
    print("date starbucks went public: %s"%publicdate)
    print("shares starting price: %s"%price)
    print("current number of coffee blends: %s"%coffees)
    print("current total # stores: %s"%stores)