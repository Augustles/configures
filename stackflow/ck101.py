# coding=utf-8

from tornado import gen, ioloop
import requests
from time import time
import os
import re
from bs4 import BeautifulSoup as bs
import ipdb
from tasks import down_img
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
    os.chdir(ur'/root/web/configures/stackflow/ck101/ck101/卡提諾正妹抱報/')
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
def parse_url(qs):
    urls = set()
    r = requests.get(qs, headers=headers)
    soup = bs(r.content, 'lxml')
    info = soup.find('ul', attrs={'class': 'waterfall'}).find_all('li')
    for x in info:
        url = x.find('a').get('href', '')
        urls.add(url)
    print(len(urls))
    for x in urls:
        r = requests.get(x, headers=headers)
        soup = bs(r.content, 'lxml')
        title = soup.find('h1').text
        print title
        title = re.search(ur'第\d+期', title).group(0)    
        info = soup.find('td', attrs={'class': 't_f', 'id': True}).find_all('a', attrs={'target': '_blank'})
        for y in info:
            if 'http://ck101.com/thread' in y.get('href', ''):
                url = y.get('href', '')
                yield parse_img(url, title)

@gen.coroutine
def main():
    t = db.find_one()
    n = int(t.get('n') + 1)
    db.save({'_id': t['_id'], 'n': n})
    print n
    for x in xrange(n, n+1):
        url = 'http://ck101.com/forum-1345-%s.html' %x
        yield parse_url(url)
    


if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

