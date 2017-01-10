# coding=utf-8

from tornado import gen, ioloop
import requests
from selenium import webdriver
from time import time
import os
from bs4 import BeautifulSoup as bs
from hashlib import md5 as _md5
import ipdb


def md5(msg):
    return _md5(msg).hexdigest()

with open('yua.txt', 'r') as f:
    pks = set(f.readlines())

npks = set()

os.chdir(os.getcwd() + '/yua/')
headers = {
    'UserAgent': 'Googlespider',
}
@gen.coroutine
def gen_md5(qs):
    pk = md5(qs) + '\n'
    raise gen.Return(pk)

@gen.coroutine
def downloader(qs):
    r = requests.get(qs, verify=False)
    raise gen.Return(r)

@gen.coroutine
def worker(qs):
    r = requests.get(qs, headers=headers, verify=False)
    soup = bs(r.content, 'lxml')
    info = soup.find('div', attrs={'class': 'stream'}).find_all('li', attrs={'data-item-type': 'tweet'})
    for x in info:
        # text = x.find('div', attrs={'class': 'js-tweet-text-container'}).text
        imgs = x.find_all('img', attrs={'data-aria-label-part': True})
        videos = x.find('div', attrs={'class': 'AdaptiveMedia-video'})
        # if len(text) > 10:
            # text = text[:11]
        if imgs:
            for y in imgs:
                img = y.get('src', '')
                r = yield downloader(img)
                fn = img.split('/')[-1]
                content = r.content
                res = gen_md5(content)
                pk = res.result()
                if pk in pks:
                    continue
                else:
                    npks.add(pk)
                print 'downloading %s' %(img)
                with open(fn, 'wb') as f:
                    f.writelines(content)
        if videos:
           for z in videos.find_all('div', attrs={'class': 'PlayableMedia-player'}):
               video = 'https://savedeo.com/download?url=' +  'https://twitter.com/yua_mikami/status/' + x.get('data-item-id', '')
               print video
               r = yield downloader(video)
               soup = bs(r.content, 'lxml')
               gen_file = soup.find('span', attrs={'data-hash': True}).get('data-checksize', '')
               r = yield downloader(gen_file)
               fn = video.split('/')[-1]
               content = r.content
               res = gen_md5(content)
               pk = res.result()
               if pk in pks:
                   continue
               else:
                   npks.add(pk)
               print 'downloading %s' %(video)
               with open(fn, 'wb') as f:
                   f.writelines(content)

    raise gen.Return(npks)

@gen.coroutine
def main():
    start = 'https://twitter.com/yua_mikami'
    npks = yield worker(start)
    os.chdir('/root/')
    with open('yua.txt', 'a') as f:
        f.writelines(npks)

if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

