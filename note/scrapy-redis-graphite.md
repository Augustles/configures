##分布式爬虫scrap-redis
####scrapy
sudo pip install scrapy
#####bloomfilter url去重 http://xiaorui.cc/2014/09/14/%E4%BD%BF%E7%94%A8bloomfilter%E5%AE%9E%E7%8E%B0%E4%BA%BF%E7%BA%A7%E5%88%AB%E7%88%AC%E8%99%ABurl%E9%93%BE%E6%8E%A5%E5%8E%BB%E9%87%8D%E5%AF%B9%E6%AF%94/
sudo pip install pybloomfiltermmap




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
