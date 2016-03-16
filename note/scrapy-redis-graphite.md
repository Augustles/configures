##分布式爬虫scrap-redis
####scrapy
sudo pip install scrapy



####graphite(画图工具)搭建, whisper数据库, carbon守护进程(缓存数据)
sudo pip install https://github.com/graphite-project/ceres/tarball/master
sudo pip install whisper
pip install carbon
sudo pip install graphite-web
#####启动一个carbon-cache进程
cd /opt/graphite/conf
sudo cp aggregation-rules.conf.example aggregation-rules.conf
sudo cp blacklist.conf.example blacklist.conf
sudo cp carbon.conf.example carbon.conf
sudo cp carbon.amqp.conf.example carbon.amqp.conf
sudo cp relay-rules.conf.example relay-rules.conf
sudo cp rewrite-rules.conf.example rewrite-rules.conf
sudo cp storage-schemas.conf.example storage-schemas.conf
sudo cp storage-aggregation.conf.example storage-aggregation.conf
sudo cp whitelist.conf.example whitelist.conf

python ../bin/carbon-cache.py start
sudo pip install pytz
vi /opt/graphite/webapp/graphite/local_settings.py
TIME_ZONE = 'Asia/Shanghai'
