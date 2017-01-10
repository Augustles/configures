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
        next_page = info[-1].get('data-item-id', '')
        yield worker(next_page, first=False)

    for x in info:
        try:
            # text = x.find('div', attrs={'class': 'js-tweet-text-container'}).text
            imgs = x.find_all('img', attrs={'data-aria-label-part': True})
            videos = x.find('div', attrs={'class': 'AdaptiveMedia-video'})
            # if len(text) > 10:
                # text = text[:11]
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

    raise gen.Return(npks)

@gen.coroutine
def master(qs):
    url = 'https://twitter.com/i/profiles/show/yua_mikami/timeline/tweets?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false' %qs
    r = requests.get(url, headers=headers)
    soup = r.json()
    if soup['has_more_items']:
        info = bs(soup['items_html'], 'lxml')

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

