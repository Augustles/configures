##elasticsearch
####安装
curl -L -O  https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.4.3.zip
unzip elasticsearch-5.4.3.zip
####启动
./bin/elasticsearch
####测试
curl 'http://localhost:9200/?pretty'
####配置mongo,需要一个replSet
####初始化replset
rs.initiate()
####python mongo
pip install 'mongo-connector[elastic5]'
####插入数据测试
use web
db.user.save({username='august', password='nana'})

curl -XGET -H 'charset=UTF-8' 127.0.0.1:9200/web/user/_search?pretty -d '{ "query" : { "match" : { "username" : "august" } } }'
####计算集群中文件的数量
 curl -XGET 'http://localhost:9200/_count?pretty' -d '{"query": {"match_all": {}}}'
####注意点
字段值中不能有空字符串
