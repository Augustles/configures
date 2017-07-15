# coding=utf8

import ipdb
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'127.0.0.1','port':9200}])

ret = es.search(index='web', q='august')
print(ret)
#  ipdb.set_trace()
es.indices.create(index='hello', ignore=400)
#  es.indices.delete(index='hello', ignore=[400, 404])
