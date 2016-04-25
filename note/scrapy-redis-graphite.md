##分布式爬虫scrap-redis
####scrapy
* sudo pip install scrapy

#####bloomfilter url去重 http://xiaorui.cc/2014/09/14/%E4%BD%BF%E7%94%A8bloomfilter%E5%AE%9E%E7%8E%B0%E4%BA%BF%E7%BA%A7%E5%88%AB%E7%88%AC%E8%99%ABurl%E9%93%BE%E6%8E%A5%E5%8E%BB%E9%87%8D%E5%AF%B9%E6%AF%94/
* sudo pip install pybloomfiltermmap


####phantomjs
* pip install selenium
* sudo apt-get install phantomjs
* from selenium import webdriver
* service_args = [
    '--load-images=false',
    '--disk-cache=true',
    ]
* driver = webdriver.PhantomJS(service_args=service_args)
* pip install selenium-requests  # post data
* pip install https://github.com/sosign/scrapy-webdriver/archive/master.zip scrapy-webdriver(scrapy&&selenium)

####验证码识别tesseract
####tesseract 训练
1. 读取图片
2. 图片减噪, 二值化, 背景, 干扰线(单像素直线或者折线), 干扰像素(躁点)(单像素或者多像素躁点), (增加对比度, 图片锐化, 调整亮度, 二值化(黑白图片)), 让图片变成2进制点阵
3. 图片切割(横向或者纵向切割)
4. 图像文本输出

## http://blog.csdn.net/shadow67/article/details/50680228

####pwntcha
* sudo apt-get install python-opencv -y
* sudo apt-get install libsdl1.2-dev libsdl1.2debian -y
* sudo apt-get install libsdl1.2-dev -y
* sudo apt-get install libsdl-image1.2-dev -y
* sudo apt-get install libsdl-mixer1.2-dev -y
* sudo apt-get install libsdl-ttf2.0-dev -y
* sudo apt-get install libsdl-gfx1.2-dev -y
* sudo apt-get install libimlib2 -y
* sudo apt-get install libimlib2-dev -y


* sudo apt-get install libsdl2-2.0-0 -y
* sudo apt-get install libsdl2-dev -y
* wget https://www.libsdl.org/release/SDL2-2.0.4.tar.gz
* wget https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.tar.gz

* git clone https://github.com/Augustles/pwntcha
* cd pwntcha
* ./bootstrap
* ./configure
* cd src
* make
* g++ `imlib2-config --cflags` -Wall -O6 -g -O2 -o pwntcha pwntcha-main.o \
pwntcha-filter.o pwntcha-font.o pwntcha-image.o pwntcha-easter-eggs.o \
pwntcha-test.o authimage/libdecoder.a clubic/libdecoder.a java/libdecoder.a \
linuxfr/libdecoder.a livejournal/libdecoder.a lmt/libdecoder.a paypal/libdecoder.a \
phpbb/libdecoder.a scode/libdecoder.a slashdot/libdecoder.a \
ticketmaster/libdecoder.a tickets/libdecoder.a vbulletin/libdecoder.a \
xanga/libdecoder.a `imlib2-config --libs` -lImlib2
* make
* cd ..
* ./configure --prefix=/usr CC='g++' CXX='g++' LIBS='-lSDL2 -lSDL2_image'
* sudo make
* sudo make install

####scrapyjs

######splash
* git clone https://github.com/scrapinghub/splash/
######sip, pyqt5
* wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz
* tar -xzvf sip-4.17.tar.gz
* cd sip-4.17
* python configure.py
* sudo make
* sudo make install
* sip -V
* wget http://120.52.72.57/iweb.dl.sourceforge.net/c3pr90ntcsf0/project/pyqt/PyQt5/PyQt-5.5.1/PyQt-gpl-5.5.1.tar.gz
* tar -xzvf PyQt-gpl-5.5.1.tar.gz
* cd PyQt-gpl-5.5.1
* python configure.py
* sudo make
* sudo make install

######安装docker
* curl -fsSL https://get.docker.com/ | sh

######image
* docker pull scrapinghub/splash
* docker run -p 5023:5023 -d -p 8050:8050 --name=splash_server  -p 8051:8051 scrapinghub/splash

####graphite(画图工具)搭建, whisper数据库, carbon守护进程(缓存数据)
* sudo pip install https://github.com/graphite-project/ceres/tarball/master
* sudo pip install whisper
* sudo pip install carbon
* sudo pip install graphite-web

#####启动一个carbon-cache进程
* cd /opt/graphite/conf
* sudo cp aggregation-rules.conf.example aggregation-rules.conf
* sudo cp blacklist.conf.example blacklist.conf
* sudo cp carbon.conf.example carbon.conf
* sudo cp carbon.amqp.conf.example carbon.amqp.conf
* sudo cp relay-rules.conf.example relay-rules.conf
* sudo cp rewrite-rules.conf.example rewrite-rules.conf
* sudo cp storage-schemas.conf.example storage-schemas.conf
* sudo cp storage-aggregation.conf.example storage-aggregation.conf
* sudo cp whitelist.conf.example whitelist.conf

* python ../bin/carbon-cache.py start
* sudo pip install pytz
* vi /opt/graphite/webapp/graphite/local_settings.py
* TIME_ZONE = 'Asia/Shanghai'

####爬取
* [Amazon](http://www.amazon.com/)
* [zol论坛](http://bbs.zol.com.cn/)(htmlib5)
* [豆瓣](https://www.douban.com/)(403)
* [知乎](http://www.zhihu.com/)(login)
* [watch](http://www.watchforfun.net/)(js, ajax)
