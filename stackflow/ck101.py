# coding=utf-8

from tornado import gen, ioloop
import requests
from selenium import webdriver
from time import time
import os
from bs4 import BeautifulSoup as bs
from hashlib import md5 as _md5
import ipdb
import json
from subprocess import check_output, Popen, PIPE

def md5(msg):
    return _md5(msg).hexdigest()

with open('yua.txt', 'r') as f:
    pks = set(f.readlines())

npks = set()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
}
@gen.coroutine
def gen_md5(qs):
    pk = md5(qs) + '\n'
    raise gen.Return(pk)

@gen.coroutine
def downloader(qs):
    r = requests.get(qs, headers=headers, verify=True)
    raise gen.Return(r)

@gen.coroutine
def worker(qs, first=True):
    print 'starting %s ...' %qs
    if not first:
        url = 'https://twitter.com/i/profiles/show/yua_mikami/timeline/tweets?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' %qs
        r = requests.get(url, headers=headers)
        soup = r.json()
        if soup['has_more_items']:
            soup = bs(soup['items_html'], 'lxml')
            info = soup.find_all('li', attrs={'data-item-type': 'tweet'})
            next_page = info[-1].get('data-item-id', '')
            yield worker(next_page, first=False)
        else:
            return
    else:
        r = requests.get(qs, headers=headers, verify=True)
        soup = bs(r.content, 'lxml')
        info = soup.find('div', attrs={'class': 'stream'}).find_all('li', attrs={'data-item-type': 'tweet'})
        # next_page = info[-1].get('data-item-id', '')
        # yield worker(next_page, first=False)

    for x in info:
        try:
            imgs = x.find_all('img', attrs={'data-aria-label-part': True})
            videos = x.find('div', attrs={'class': 'AdaptiveMedia-video'})
            if imgs:
                for y in imgs:
                    try:
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
                    except Exception as e:
                        with open('yua.log', 'a') as f:
                            f.writelines(e)

            if videos:
               for z in videos.find_all('div', attrs={'class': 'PlayableMedia-player'}):
                   try:
                       video = 'https://savedeo.com/download?url=' +  'https://twitter.com/yua_mikami/status/' + x.get('data-item-id', '')
                       r = yield downloader(video)
                       soup = bs(r.content, 'lxml')
                       gen_file = soup.find('span', attrs={'data-hash': True}).get('data-checksize', '')
                       r = yield downloader(gen_file)
                       fn = gen_file.split('/')[-1]
                       content = r.content
                       res = gen_md5(content)
                       pk = res.result()
                       if pk in pks:
                           continue
                       else:
                           npks.add(pk)
                       print 'downloading %s' %(gen_file)
                       with open(fn, 'wb') as f:
                           f.writelines(content)
                   except Exception as e:
                       with open('yua.log', 'a') as f:
                           f.writelines(e)

        except Exception as e:
            with open('yua.log', 'a') as f:
                f.writelines(e)




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
        info = soup.find('td', attrs={'class': 't_f', 'id': True}).find_all('a', attrs={'target': '_blank'})
        for y in info:
            if 'http://ck101.com/thread' in y.get('href', ''):
                print y

@gen.coroutine
def main():
    for x in xrange(3):
        url = 'http://ck101.com/forum-1345-%s.html' %x
        yield parse_url(url)


if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)

