# root ubuntu14.04 scrapy
sudo apt-get update
sudo apt-get -y install zsh git python wget curl
sudo apt-get -y install python-dev python-setuptools
sudo apt-get install -y libevent-dev libxml2-dev libxslt1-dev libffi-dev
sudo apt-get install -y libssl-dev libcurl4-openssl-dev python-devs libffi-dev
sudo apt-get install -y build-essential autoconf libtool cmake pkg-config python-opengl libjpeg8-dev
sudo apt-get install -y aptitude
sudo easy_install pip
sudo pip install virtualenv virtualenvwrapper
sudo pip install fabric
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sudo apt-get install ctags build-essential cmake python-dev silversearcher-ag
sudo pip install pyflakes pylint pep8
cd ~
git clone https://github.com/wklken/k-vim.git
cd k-vim
sh install.sh
#sudo pip install scrapy
#sudo pip install pyOpenSSL==0.13
#sudo pip install beautisoupful4
#sudo pip install fabric
# pip
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv env
workon env
pip install scrapy
pip install cchardet
pip install bs4
pip install requests
pip install html5lib
pip install pymongo
pip install pymysql
pip install redis
pip install scrapyjs
# pip install scrapy-splash
# 安装docker

# check scrapy
#scrapy -h
# mongo
sudo aptitude install mongodb
#check mongo 进程
#ps -aux | grep mongo
# 检查mongo端口
# netstat -nlt | grep 27017
# redis-server
#sudo aptitude install -y redis-server
# 修改密码 修改redis.conf文件配置
# vi /etc/redis/redis.conf
# supervisor, web, dir设定
#sudo aptitude install -y supervisor
#sudo aptitude install mysql
# Graphite http://www.vpsee.com/2012/05/install-graphite-on-ubuntu-12-04/
#sudo apt-get install apache2 libapache2-mod-wsgi python-django \
#python-twisted python-cairo python-pip python-django-tagging
