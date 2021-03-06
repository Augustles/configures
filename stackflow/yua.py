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
def worker2(qs, first=True):
    if not first:
        cmd = '''curl 'https://www.instagram.com/query/' -H 'cookie: mid=WHSEXwAEAAFmyVFoJ_n7bZ5eD9VE; ig_pr=2; ig_vw=1276; s_network=""; csrftoken=8Fz2hZOeV0kXQk5tFJkVgUzqcnIAUi7e' -H 'origin: https://www.instagram.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.8' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36' -H 'x-requested-with: XMLHttpRequest' -H 'x-csrftoken: 8Fz2hZOeV0kXQk5tFJkVgUzqcnIAUi7e' -H 'x-instagram-ajax: 1' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: */*' -H 'referer: https://www.instagram.com/mikami_yua/' -H 'authority: www.instagram.com' --data 'q=ig_user(3932298284)+%7B+media.after({0}%2C+12)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++comments_disabled%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow&query_id=17846611669135658' --compressed > test.txt'''.format(qs)
        os.system(cmd)
        with open('test.txt', 'r') as f:
            out = f.readlines()
        soup = json.loads(out[0])
        try:
            next_page = soup['media']['page_info']['end_cursor']
        except:
            return
        info = soup['media']['nodes']
        yield nstart(next_page, first=False)
    else:
        r = webdriver.PhantomJS()
        r.get(qs)
        soup = bs(r.page_source, 'lxml')
        r.quit()
        info = soup.find('div', attrs={'class': '_nljxa'}).find_all('img', attrs={'src': True})
    for x in info:
        try:
            try:
                img = x['display_src'].split('?')[0]
            except:
                img = x.get('src', '').split('?')[0]
            img = img.replace('/s640x640', '')
            r = yield downloader(img)
            fn = img.split('/')[-1].split('_')[-2] + '.jpg'
            print fn
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

@gen.coroutine
def main():
    start = ['https://twitter.com/yua_mikami', 'https://www.instagram.com/mikami_yua/', 'https://www.instagram.com/yua_mikami/']
    for x in start:
        if 'twitter' in x:
            os.chdir(os.getcwd() + 'test2/twiyua')
            yield worker(x)
        elif 'instagram' in x:
            os.chdir(os.getcwd() + 'test2/insyua')
            yield worker2(x)


if __name__ == '__main__':
    st = time()
    ioloop.IOLoop.current().run_sync(main)
    print 'spend %.3f' %(time()-st)
    os.chdir('/root/')
    with open('yyua.txt', 'a') as f:
        f.writelines(npks)

