# coding=utf-8

import ipdb
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
# from fabric.colors import green, red
import math
import re
from chardet import detect
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

basedir = os.getcwd() + '/fm80/'
print basedir
if not os.path.exists(basedir):
    os.mkdir(basedir)

def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()

regexs = [
    re.compile(p)
    for p in [u'主播', 'NJ', 'nj']
]

def down(url):
    r = requests.get(url)
    return r

def getLink(url):
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    # pages = soup.find(
        # 'div', attrs={'class': 'box-title-with-radio-controller'}).get_text()
    # pages = re.search(r'\d+', pages).group(0)
    # pages = math.ceil(int(pages) / 20.0)
    info = soup.find(
        'ul', attrs={'class': 'js-audio-list'}).find_all('li')
    # print(len(info))
    for x in info:
        mp3 = x.find('a', attrs={'href': True,
                                 'data-url': True}).get('data-url').strip()
        title = x.find(
            'a', attrs={'href': True, 'data-url': True}).get('title')
        # for regex in regexs:
            # if regex.search(title):
                # flag = regex.search(title).group(0)
                # author = title.split(flag)[-1]
        # if 'author' not in locals():
            # author = title.split()[-1]

        # print mp3, title, author, nt
        title = '-'.join(title.split())
        title = uniform(title)
        print title, mp3
        res = down(mp3)
        os.chdir(basedir)
        if os.path.exists(title):
            continue
        if res.content < 10*1024:
            sleep(15)
            res = requests.get(mp3)
        print 'downloading %s %s' %(mp3, title)
        with open('%s-hd.mp3' %(title), 'wb') as f:
            f.writelines(res.content)
        name = title.strip() + ' => ' + mp3 + '\n'
        with open('fm80.txt', 'a+') as f:
            f.write(name)
        sleep(6)


def getList(url):
    sturl = []
    for x in xrange(1, 23):
        x = 'http://www.lizhi.fm/12006/p/{0}.html'.format(x)
        try:
            getLink(x)
        except Exception as e:
            print(e)

url = 'http://www.lizhi.fm/12006/'
# getLink(url)
getList(url)
