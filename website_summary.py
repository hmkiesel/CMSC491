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
    fileObj = codecs.open("starbucksData.rtf", "w", "UTF")
    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html5lib')
    all_paras = soup.find_all('p')

    # Write test to file and collate it into a str var
    data = ""

    for para in all_paras:
        fileObj.write(para.text)
        data = data + para.text

    parser = HtmlParser.from_url(url, Tokenizer('English'))
    stemmer = Stemmer('English')
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words('English')

    print("\nThree Sentence Summary:\n")
    for sentence in summarizer(parser.document, 3):
        print(sentence)

