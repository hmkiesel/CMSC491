'''
Author: Hannah Kiesel
In this file, we extract a 3 sentence summary of a webpage. This will be used to create summaries of Starbucks' economic
platform, as well as blog posts. The function provides a short TLDR summary of the webpage passed in (url).
I also included a screen scraper function that scrapes the Starbucks 'Company Profile' page, which includes numerical
information about dates, stock values, and number of stores. Screen scraping is useful for extracting text from a webpage,
and in our case, it allows us to form a better, concise description of Starbucks from its early beginnings to now. In this
screen scraper function, I used BeautifulSoup to parse the text and extract several of these important data values (year the
comany began, total number of stores, etc) from the page, and print out a concise profile description for the company. 
'''

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

    print("\nScreen Scrape of Starbucks Company Profile:\n")
    print("opening date: %s"%year)
    print("date starbucks went public: %s"%publicdate)
    print("shares starting price: %s"%price)
    print("current number of coffee blends: %s"%coffees)
    print("current total # stores: %s"%stores)
