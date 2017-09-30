# coding=utf-8

from tornado import gen, ioloop
import requests
from time import time
import os
import re
from bs4 import BeautifulSoup as bs
import ipdb
from pymongo import MongoClient

db = MongoClient().web.ck101

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
}

@gen.coroutine
def curl_down(cmd, title):
    status = down_img.delay(cmd, title)
    raise gen.Return(status)

@gen.coroutine
def parse_img(qs, title):
    r = requests.get(qs, headers=headers)
    soup = bs(r.content, 'lxml')
    info = soup.find_all('img', attrs={'class': 'zoom'})
    imgs = [x.get('file', '') + '\n' for x in info]
    if not os.path.exists(title):
        os.mkdir(title)
    else:
        return
    os.chdir(title)
    with open('download.txt', 'a') as f:
        f.writelines(imgs)
    cmd = 'wget -t 5 -c -i %s' %('download.txt')
    status = yield curl_down(cmd, title)
    print status



@gen.coroutine
def parse_url(url):
    try:
        res = requests.get(url, headers=headers)
    except:
        yield parse_url(url)
    soup = bs(res.content, 'lxml')
    if soup.find('ul', attrs={'class': 'waterfall'}):
        infos = {x.find('a').get('href', ''):x.find('a').get('title', '').strip()  for x in soup.find('ul', attrs={'class': 'waterfall'}).find_all('li')}
    else:
        infos = {}
    for url, name in infos.items():
        updater = {'url': url, 'name': name}
        db.update({'url': url}, {'$set': updater}, upsert=True)
    ipdb.set_trace()

@gen.coroutine
def main():
    uri = 'http://ck101.com/forum-1345-%s.html'
    for x in xrange(1, 100):
        url = uri%x
        yield parse_url(url)

if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

