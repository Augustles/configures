# coding=utf-8

from tornado import gen, ioloop
import requests
from time import time
import os
import re
from bs4 import BeautifulSoup as bs
import ipdb
from pymongo import MongoClient

db = MongoClient('127.0.0.1:27019').web.ck101

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
def parse_page(url):
    try:
        res = requests.get(url, headers=headers)
    except:
        gen.Sleep(3)
        yield parse_url(url)
    if res.status_code == 200:
        raise gen.Return(res)
    else:
        gen.Sleep(3)
        yield parse_page(url)

@gen.coroutine
def parse_url(url, idx):
    try:
        res = requests.get(url, headers=headers)
    except:
        gen.Sleep(3)
        yield parse_url(url)
    soup = bs(res.content, 'lxml')
    if soup.find('table', attrs={'id': 'threadlisttableid'}):
        infos = {x.find('a').get('href', ''):x.find('a').get('title', '').strip()  for x in soup.find('table', attrs={'id': 'threadlisttableid'}).find_all('tbody', attrs={'tid': True})}
    else:
        infos = {}
    for url, name in infos.items():
        updater = {'url': url, 'name': name, 'category': idx}
        db.update({'url': url, 'category': idx}, {'$set': updater}, upsert=True)

@gen.coroutine
def main():
    # uri = 'http://ck101.com/forum-1345-%s.html'
    #  uri = 'https://ck101.com/forum-%s-%s.html'
    #  source_types = [3581, 3583, 3584, 3582]
    #  for x in xrange(1, 999):
        #  for y in source_types:
            #  url = uri%(y, x)
            #  yield parse_url(url, y)

    for x in db.find({'category': {'$exists': True}}, no_cursor_timeout=True):
        url = x.get('url', '')
        if url:
            res = yield parse_page(url)
            db.update({'url': url, 'category': x['category']}, {'$set': {'html': res.content}})

if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

