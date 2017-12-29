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

def parse_content(raw_url, url, htmls=[], imgs=[]):
    print(url)
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            sleep(3)
            return parse_content(url)
    except:
        sleep(3)
        return parse_content(url)
    soup = bs(res.content, 'lxml')
    html = soup.find('div', attrs={'class': 'entry-content'})
    htmls.append(str(html))
    if html:
        next_url = html.find('p', attrs={'align': 'center'})
        img = [x.get('data-lazy-src', '') for x in html.find_all('img', attrs={'src': True, 'data-lazy-src': True, 'data-lazy-type': 'image'})]
        imgs.extend(img)
        if next_url:
            next_url = next_url.find('button', attrs={'class': 'border222'})
            if next_url:
                next_url = next_url.findNext().get('href', '')
                if next_url and next_url.startswith('http'):
                    print next_url, 111
                    return parse_content(raw_url, next_url, htmls, imgs)
    category, tag, read_count = [], [], 0
    if soup.find('div', attrs={'class': 'entry-utility'}):
        category = [y.text for y in  soup.find('div', attrs={'class': 'entry-utility'}).find_all('a', attrs={'rel': 'category'})]
        tag = [y.text for y in soup.find('div', attrs={'class': 'entry-utility'}).find_all('a', attrs={'rel': 'tag'}) if y.text not in category]
        read_count_str = soup.find('div', attrs={'class': 'entry-utility'}).text
        read_count_str = read_count_str[:read_count_str.find('|')]
        read_count = ''.join(re.findall(r'\d+', read_count_str))
    now = int(time())
    attrs = dict(
        category=category,
        tag=tag,
        imgs=imgs,
        htmls=htmls,
        read_count=read_count,
        update_time=now,
        status=2,
    )
    print('update url: %s'%raw_url)
    db.update({'url': raw_url}, {'$set': attrs})

def get_items():
    return db.find({'status': 0}).limit(10)

#  @gen.coroutine
def main():
    #  uri = 'http://kenshin.hk/page/%d/'
    #  url = 'http://kenshin.hk/2017/11/21/【cm】北川景子穿黑色吊帶長裙和超漂亮電視機成絕/'
    #  parse_content(url)
    #  ipdb.set_trace()
    items = get_items()
    while items:
        for x in items:
            url = x['url']
            parse_content(url, url)
        items = get_items()

if __name__ == '__main__':
    main()
    #  st = time()
    #  ioloop.IOLoop.current().run_sync(main)
    #  print 'spend %.3f' %(time()-st)

