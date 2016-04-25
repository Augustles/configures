# coding=utf-8


import requests
from bs4 import BeautifulSoup as bs
import random
import string
from fabric.colors import green, red
import os
from time import sleep


def rdstring(length):
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

XCSRF2Cookie = ''.join(rdstring(8))
XCSRF2Token = ''.join(rdstring(24))
XCSRFToken = ''.join(rdstring(24))
headers = {
    'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'X-Requested-With': 'XMLHttpRequest',
    "Referer": "https://www.coursera.org/login",
    'X-CSRF2-Cookie': 'csrf2_token_%s' % XCSRF2Cookie,
    'X-CSRF2-Token': XCSRF2Token,
    'X-CSRFToken': XCSRFToken,
    'Cookie': "csrf2_token_%s=%s; csrftoken=%s" % (XCSRF2Cookie, XCSRF2Token, XCSRFToken)

}
cc = {' Domain': '.coursera.org',
      ' Expires': 'Sat, 11 Jun 2016 03:54:48 GMT',
      ' Max-Age': '4320000',
      ' Path': '/',
      'CAUTH': '-ocNgNuEBdB4yQsQJVPnjx3GhYjZxTc3OssWW0-wlzWtSXC6zAo1vcAHPZON8vxCE8FCYklWz82vc29pSX1Msw.alxbdt_Bo3-RO8tlnI_PSg.64ABb4dxNHt78TsoQ0-KJxkBzG1SFz4Cp3jVSwC6hoF_UoTmUOOhO-qlgvoOstKY8R8RdJIUBt9wxDMl9_GHOpe3GLgSAbYncDBLTqSXj-a_N8VzXDg4ZxshIYDAxCM4qim59mo37sr1ecxD9Pcb4m1QGELkmFf2ZlBLkBS2OcY',
      'CSRF3-Token': '1462167988.sKODb89b1eO7shsL',
      '__204u': '5852517606-1461303988141',
      'csrf_token': 'ZvotAKrUqfpLvVt7IMVv',
      'serve_netease_976159': '1'}
purl = 'https://www.coursera.org/api/login/v3'
turl = 'https://class.coursera.org/ntumlone-003/lecture'
data = {
    'code': '',
    'email': '1927064778@qq.com',
    'password': 'cxk517',
    'webrequest': 'true',
}

# def cheaders():
#     XCSRF2Cookie = 'csrf2_token_%s' % ''.join(rdstring(8))
#     XCSRF2Token = ''.join(rdstring(24))
#     XCSRFToken = ''.join(rdstring(24))
#     c = "csrftoken=%s; %s=%s" % (XCSRFToken, XCSRF2Cookie, XCSRF2Token)
#     headers.update

durl = 'https://class.coursera.org/ntumlone-003/lecture/download.mp4?lecture_id=7'


ss = requests.session()
ss.cookies.update(cc)


def login(url, fn):
    # ss.headers.update(headers)
    # print(green(headers))
    # print(red(data))

    # r = ss.post(url, data=data)
    # print(red(r.headers))
    print(green('downloading {0} ==> {1}'.format(fn, url)))
    r = ss.get(durl, timeout=86400)
    if not os.path.exists('mlvideo'):
        os.mkdir('mlvideo')
    os.chdir(os.getcwd() + '/mlvideo')
    with open(fn, 'wb') as f:
        f.write(r.content)


with open('/home/august/work/mlv.txt') as f:
    c = f.readlines()
for x in c:
    if x.strip():
        fn = x.split(' - ')[0] + '.mp4'
        url = x.split(' - ')[1]
        login(url, fn)
        sleep(60 * 5)
