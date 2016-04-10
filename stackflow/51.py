# coding=utf-8

import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from fabric.colors import green, red

dbhost = '127.0.0.1'
dbport = 27017
# nbbs = MongoClient(dbhost, dbport).nbbs.dsl
# try:
#     for x in nbbs.find():
#         url = x['url']
#         tid = x.get('_id')
#         print tid
#         if nbbs.find({'url': url}).count() > 1:
#             nbbs.remove({'_id', tid})
# except Exception as e:
#     print(e)

def login(url):
    headers = {
        'Host': 'www.51yyto.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # Accept-Language: en-US,en;q=0.5
        # Accept-Encoding: gzip, deflate
        'Referer': 'http://www.51yyto.com/index.php/login/aHR0cDovL3d3dy41MXl5dG8uY29tLw==',
        # Cookie: PHPSESSID=d733rskt47r5elo8rgum0mlam2; checkcode=31f57f0b8eed62ee1d28fec7d8bae3aa
        # Connection: keep-alive
    }
    ss = requests.session()
    ss.headers.update(headers=headers)
    # 验证码失败, 主要是下载验证码会产生一个cookies, 和get image的cookie不匹配
    checkcode = 'http://www.51yyto.com/index.php/api/checkcode/image/80_27/1460203188174'
    r = ss.get(checkcode)
    with open('captcha.png', 'wb') as f:
        f.write(r.content)
    def get_code(im):
        from pytesseract import image_to_string
        from PIL import Image
        im = Image.open(im)
        im = im.convert('L')
        code = image_to_string(im)
        im.show()
        # code = raw_input('please enter code: ')
        return code
    code = get_code('captcha.png')
    data = {
        'username': '18665613910',
        'password': '111111',
        'submit': u'登陆',
        'verify': code,
        'hidurl': 'http://www.51yyto.com/',
    }
    print data
    r = ss.post(url, data=data)
    soup = bs(r.content, "html.parser")
    home_url = 'http://www.51yyto.com/'
    r = ss.get(home_url)
    soup = bs(r.content, "html.parser")

    try:
        name = soup.find('span', attrs={'class': 'M-name-txt blue mlr5'}).get_text()
        return name
    except AttributeError:
        pass
while True:
    url = 'http://www.51yyto.com/index.php/login/aHR0cDovL3d3dy41MXl5dG8uY29tLw=='
    name = login(url)
    if not name:
        print(red('==> fail'))
        login(url)
    else:
        print(green(name))
# st = []
# for x in range(1, 15):
#     st.append(
#         'http://test.51yyto.com/?/member/home/orderlist/&p={0}'.format(x))

# def get_item(i):
#     r = requests.get(i, headers=headers)
#     soup = bs(r.text, 'html5lib')
#     title = soup.find('h1').get_text()
#     price = soup.find('span', attrs={'class': 'rmbgray'}).get_text()
#     times = soup.find('div', attrs={'class': 'MaCenter'}).p.em.get_text()
#     lnumber = soup.find('div', attrs={'class': 'formula'}).b.get_text()
#     plist = {'title': title, 'url': i, 'price': price, 'times': times, 'luck_number': lnumber}
#     return plist

# for x in st:
#     r = requests.get(x, headers=headers)
#     soup = bs(r.text, 'html5lib')
#     info = soup.find('div', attrs={'id': 'tbList'}).find_all(
#         'ul', attrs={'class': 'listTitle', 'style': True})
#     for y in info:
#         url = y.find('li', attrs={'class': 'single-xx-has'}).a['href']
#         plist = get_item(url)
#         print plist
#         if nbbs.find({'url': plist['url']}).count() <= 0:
#             nbbs.save(dict(plist))
#         else:
#             t = nbbs.find_one({'url': plist['url']})
#             tid = t.get('_id')
#             nbbs.update({'_id': tid}, {'$set': dict(plist)})


# get_item('http://test.51yyto.com/?/dataserver/2079')
