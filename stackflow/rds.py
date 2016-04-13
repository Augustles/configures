# coding=utf-8

from fabric.colors import green, red
import redis
from pymongo import MongoClient
# , decode_responses=True
dbhost = '127.0.0.1'
dbport = 27017
toSum = MongoClient(dbhost, dbport).r.to_sum
dsl = MongoClient(dbhost, dbport).r.sums


r = redis.StrictRedis(host='192.168.2.16', port=3369, db=0)
info = r.keys()
# print info
# for x in info:
#     all = r.hgetall(x)

sp = u'192.168.2.188:like:save:count'
sp1 = u'192.168.13.13:sinatweet:pop:count'
sp2 = '120.24.37.104:forward:pop:count'
total = 'total:daily:'


def get_item(sp):
    try:
        info = r.hgetall(sp)
        d = {}
        l = []
        n = 0
        for x, y in info.iteritems():
            # print x, y
            if len(x) == 8:
                d[x] = y
        # l.append({'name': sp, 'key': x, 'value': y})
        if toSum.find({'name': sp, 'key': x, 'value': y}).count() <= 0:
            toSum.save({'name': sp, 'key': x, 'value': y})
            # r.hset(nsp,  x, y)
            # return l
    except Exception as e:
        print(red(e))


def to_sum(info):
    l = []
    for x in info:
        if x.split(':')[1] not in l:
            # l.append(x.split(':')[1])
            print(green(x.split(':')[1]))
            if dsl.find({'name': x.split(':')[1]}).count() <= 0:
                dsl.save({'name': x.split(':')[1]})
    # return l
try:
    try:
        # to_sum(info)
        # for x in info:
        #     get_item(x)
        pass


    except Exception:
        pass
except Exception as e:
    print(red(e))


l = []
d = {}
n = 0
for x in toSum.find():
    for y in dsl.find():
        # 需要判断的字段
        # print y['name'], x['key']
        if y['name'] in x['name'] and ':day' not in x['name']:
            # 判断day
            if x['key'] not in d:
                d['key'] = x['key']
                d['value'] = x['value']
                d['name'] = y['name']
            else:
                d['value'] = x['value'] + d['value']
            d['name'] = total + d['name']
            print d['name'],  d['key'], d['value']
            # r.hset(d['name'],  d['key'], d['value'])
