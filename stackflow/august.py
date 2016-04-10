# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from fabric.colors import green, red
from bs4 import BeautifulSoup as bs
from scrapy.spider import BaseSpider
from scrapy.http.cookies import CookieJar

# from scrapy_webdriver.http import WebdriverRequest

# scrapy 验证码&&登陆 爬取 Request


class AugustSpider(scrapy.spiders.Spider):
    name = "august"
    allowed_domains = ["www.51yyto.com"]
    start_urls = (
        'http://www.51yyto.com/',
    )
    # 通过状态码结束抓取
    handle_httpstatus_list = [403]
    HTTPERROR_ALLOWED_CODES = [200]
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

    def start_requests(self):
        # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
        # COOKIES_ENABLED=True
        # COOKIES_DEBUG=True
        # 在setting中启用cookie, 不用在添加cookiejar来标示
        return [Request(
            "http://www.51yyto.com/index.php/api/checkcode/image/80_27/1460203188174",
            # meta={'cookiejar': 1},
            callback=self.post_login)]

    def post_login(self, response):
        print(green('Prepare login ...'))
        with open('captcha_t.png', 'wb') as f:
            f.write(response.body)
        from pytesseract import image_to_string
        from PIL import Image
        im = Image.open('captcha_t.png')
        im = im.convert('L')
        code = image_to_string(im)
        # im.show()
        # code = raw_input('please enter code: ')
        data = {
            'username': '18665613910',
            'password': '111111',
            'submit': u'登陆',
            'verify': code,
            'hidurl': 'http://www.51yyto.com/',
        }
        url = 'http://www.51yyto.com/index.php/login/aHR0cDovL3d3dy41MXl5dG8uY29tLw=='

        print(green(data))
        return [FormRequest(url,
                            # meta={'cookiejar': CookieJar()]},
                            headers=self.headers,
                            formdata=data,
                            callback=self.after_login,
                            dont_filter=True
                            )]

    def after_login(self, response):
        cookie = response.headers.items()[1][1:][0]  # 字符串
        print(red(cookie))
        print(red(response.headers))
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        # print(red(CookieJar.extract_cookies()))
        cookies = {}
        for x in cookie.split(';'):
            x = x.split('=')
            cookies[x[0].strip()] = x[1].strip()

        print type(cookies), red(cookies)
        # del cookies['path']
        # print red(1111), response.headers
        if u'成功' in bs(response.body_as_unicode()).title.get_text():
            print(green('Success!'))
            print(green(response.meta))
            from selenium import webdriver
            dr = webdriver.PhantomJS()

            for url in self.start_urls:
                # 这里需要带cookie爬取
                print(red(url))
                dr.get(url)
                # dr.clearcookies()
                print(red(dr.get_cookies()))
                dr.add_cookie(cookies)
                print(red(1111))
                soup = bs(dr.page_source)
                name = soup.find(
                    'span', attrs={'class': 'M-name-txt blue mlr5'}).get_text()
                print(green(name))
                # yield Request(url,
                #               # meta={'cookiejar': response.meta['cookiejar']},
                #               callback=self.parse)
                # yield WebdriverRequest(url, meta={'cookiejar':
                # response.meta['cookiejar']}, callback=self.parse)
        else:
            print bs(response.body_as_unicode()).title.get_text()

    def parse(self, response):
        soup = bs(response.body_as_unicode())
        name = soup.find(
            'span', attrs={'class': 'M-name-txt blue mlr5'}).get_text()
        print(green(name))
