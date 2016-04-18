# coding=utf-8

import requests
import re
import time
import random
from bs4 import BeautifulSoup as bs
# cookie = 'pgv_pvi=2606262272; wxuin=1278879662; webwxuvid=61e1261780f36f48f9b47ea65e26bff7013ba77045b3615eee95741ee7eeca49b37f81ac929c26cd4c1c95c3c3b53c96; mm_lang=zh_CN; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; pgv_si=s240206848; wxsid=4tt3aIf8zIsrchXm; wxloadtime=1460617273_expired; webwx_data_ticket=gSd2TQz66dKVW50N0DnkuIfb; wxpluginkey=1460615423'
from fabric.colors import green, red

headers = {
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    # 'Cookie': 'CXID=2231116EBA9024FB6B75FE783493E127; ad=bDxISZllll2gRZ9YlllllVt5lqwllllltV@RFkllllylllllRAoll5@@@@@@@@@@; SUID=4EC35F70526C860A570F0118000B4A09; ABTEST=5|1460618415|v1; IPLOC=CN4403; SUV=004A70CA705FC34E570F44B0CBB64460; weixinIndexVisited=1; PHPSESSID=5b0qmekv0lje4elrs0mvpb13u6; SUIR=1460618425; seccodeErrorCount=1|Thu, 14 Apr 2016 07:25:14 GMT; SNUID=C449D5FA8A8EBAE73008EC188BD605EB; successCount=1|Thu, 14 Apr 2016 07:25:22 GMT; LSTMV=138%2C290; LCLKINT=3950',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}


BASE_URL = 'http://weixin.sogou.com'


def update_cookies():
    s = requests.Session()
    s.headers.update(headers)
    url = 'http://weixin.sogou.com' + '/weixin?query=123'
    r = s.get(url)
    if 'SNUID' not in s.cookies:
        p = re.compile(r'(SNUID=\S+?);')
        m = re.findall(r'(SNUID=\S+?);', cookie.headers['set-cookie'])
        s.cookies['SNUID'] = p.findall(r.text)[0]
        suv = ''.join(
            [str(int(time.time() * 10000) + random.randint(0, 1000))])
        s.cookies['SUV'] = suv
        print s.cookies['SNUID']
    return s.cookies

# Cookie = update_cookies()
# print Cookie


def main():
    preUrl = 'http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(
        int(time.time()))
    ss = requests.session()
    ss.headers.update(headers)
    r = ss.get(preUrl)
    with open('wx-captcha.png', 'wb') as f:
        f.write(r.content)
    t = r'weixin?type=2&query=如果声音会记得&ie=utf8&_sug_=n&_sug_type_='
    from pytesseract import image_to_string
    from PIL import Image
    from urllib import quote
    im = Image.open('captcha_t.png')
    im = im.convert('L')
    code = image_to_string(im)
    code = raw_input('please enter code: ').strip()
    data = {
        'v': 5,
        'r': '%2F' + quote(t),
        'c': code
    }
    url = 'http://weixin.sogou.com/antispider/thank.php'
    print(red(data))
    rr = ss.post(url, data=data)
    import json
    soup = json.loads(rr.content)
    if soup['code'] == 0:
        SNUID = soup['id']
        print(green('Sucess! SNUID ==> {0}'.format(SNUID)))
    url = 'http://weixin.sogou.com/' + t
    # c = update_cookies()
    cc = {'name': 'SNUID', 'value': SNUID,
          'domain': '.sogou.com', 'path': '/'}
    ss.cookies.set(**cc)
    print(red(ss.cookies))
    print url
    from selenium import webdriver
    dr = webdriver.PhantomJS()
    try:
        dr.add_cookie(cc)
    except Exception as e:
        print(red(e))
    dr.get(url)
    print(red(dr.get_cookies()))
    soup = bs(dr.page_source)
    # info = soup.find('div', attrs={'class': 'results'}).find_all('div', attrs={'id': True, 'class': True, 'd': True})
    # print(red(len(info)))
    print(green(soup.title))
main()
