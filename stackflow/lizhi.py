# coding=utf-8

import requests
from bs4 import BeautifulSoup as bs
# from fabric.colors import green, red
import math
import re
from chardet import detect
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getLink(url):
    r = requests.get(url)
    soup = bs(r.text, 'html5lib')
    pages = soup.find(
        'div', attrs={'class': 'box-title box-title-with-radio-controller'}).get_text()
    pages = re.search(r'\d+', pages).group(0)
    pages = math.ceil(int(pages) / 20.0)
    info = soup.find(
        'ul', attrs={'class': 'audioList fontYaHei js-audio-list'}).find_all('li')
    # print(len(info))
    for x in info:
        mp3 = x.find('a', attrs={'href': True,
                                 'data-url': True}).get('data-url')
        title = x.find(
            'a', attrs={'href': True, 'data-url': True}).get('title')
        name = title.encode('utf-8').strip() + '===' + mp3.strip() + '\n'
        with open('fm80.txt', 'a+') as f:
            f.write(name)


def getList(url):
    sturl = []
    for x in xrange(20):
        x = 'http://www.lizhi.fm/12006/p/{0}.html'.format(x)
        try:
            getLink(x)
        except Exception as e:
            print(e)

url = 'http://www.lizhi.fm/12006/'
# getLink(url)
getList(url)
