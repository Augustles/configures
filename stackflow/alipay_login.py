# coding=utf-8

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
url = 'https://auth.alipay.com/login/index.htm'
# url = 'http://www.8dwww.com/user/'

# uname = 'cxk517'
# pw = 'e6c02a8c91b5'

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
)
dr = webdriver.PhantomJS(desired_capabilities=dcap)
dr.get(url)
print dr.current_url
soup = bs(dr.page_source, 'lxml')
# print soup
name = dr.find_element_by_id('J-input-user')
pw = dr.find_element_by_id('password_rsainput')
name.clear()
pw.clear()
name.send_keys('')
pw.send_keys('')
# dr.find_element_by_xpath("//input[@name='username']").send_keys('cxk517')
# dr.find_element_by_xpath("//input[@name='password']").send_keys('e6c02a8c91b5')
# uname.clear()
# uname.send_keys("cxk517")
# pw.clear()
# pw.send_keys("e6c02a8c91b5")
dr.find_element_by_id('J-login-btn').click()
dr.implicitly_wait(60)
if dr.find_element_by_id('J-userInfo-account-userEmail'):
    pass

soup = bs(dr.page_source, 'lxml')
# n = soup.find('div', attrs={'class': 'i-assets-balance-amount fn-left'}).get_text()
name = soup.find('a', attrs={'id': 'J-userInfo-account-userEmail'})
print soup.title.get_text()
print name, dr.get_cookies()

print dr.current_url
dr.quit()


# dr = webdriver.PhantomJS()
# url = 'http://www.baidu.com/'
# dr.get(url)

# #-------------------by link--------------------------
# #----------------------------------------------
# login = dr.find_element_by_link_text('登录')
# login.click()
# time.sleep(10)
# print "Current url is:%r" % (dr.current_url)

# #--------------登录-----------------------
# username = dr.find_element_by_name('userName')
# username.send_keys('cxk517')
# time.sleep(3)

# pw = dr.find_element_by_name('password')
# pw.send_keys('zhaoying')
# time.sleep(3)

# login_bt = dr.find_element_by_id('TANGRAM__PSP_8__submit')
# login_bt.click()
# time.sleep(3)
# soup = bs(dr.page_source, 'lxml')
# info = soup.find('span', attrs={'class': 'user-name'}).get_text()
# print info
