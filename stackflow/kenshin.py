# coding=utf-8

from tornado import gen, ioloop
import requests
from time import time, sleep
import os
import re
from bs4 import BeautifulSoup as bs
import ipdb
from pymongo import MongoClient
import urllib

db = MongoClient('104.225.144.193:27019').web.kenshin

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
}

@gen.coroutine
def parse_page(url):
    try:
        res = requests.get(url, headers=headers)
    except:
        gen.Sleep(3)
        yield parse_url(url)
    if res.status_code == 200:
        info = {}
        soup = bs(res.content, 'lxml')
        article = soup.find('article')
        if article.find('span', attrs={'class': 'postDateLine'}):
            info['create_time_str'] = article.find('span', attrs={'class': 'postDateLine'}).text.strip()
        if article.find('a', attrs={'class': 'authorName'}):
            info['username'] = article.find('a', attrs={'class': 'authorName'}).get('title', '').strip()
            info['user_space'] = 'https://ck101.com' + article.find('a', attrs={'class': 'authorName'}).get('href', '')
        if article.find('tbody'):
            info['html3'] = str(article.find('tbody'))
        raise gen.Return(info)
    else:
        gen.Sleep(3)
        yield parse_page(url)

@gen.coroutine
def parse_url(url):
    print(url)
    try:
        res = requests.get(url, headers=headers)
    except:
        sleep(3)
        yield parse_url(url)
    soup = bs(res.content, 'lxml')
    items = soup.find('div', attrs={'id': 'content'}).find_all('div', attrs={'id': re.compile(r'post-\S*')})
    for y in items:
        url = urllib.unquote(y.find('h2', attrs={'class': 'entry-title'}).a.get('href', '').strip())
        #  print('%s upsert to db'%url)
        attrs = dict(
            url=url,
            status=0,
            update_time=int(time()),
        )
        t = db.find_one({'url': url})
        if not t:
            db.update({'url': url}, {'$set': attrs}, upsert=True)
        else:
            attrs['create_time'] = int(time())
            db.update({'url': url}, {'$set': attrs})

@gen.coroutine
def main():
    uri = 'http://kenshin.hk/page/%d/'
    for x in range(1, 1700):
        try:
            url = uri%x
            yield parse_url(url)
        except:
            pass

if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

