# coding=utf-8

from fabric.colors import green, red
import redis
from pymongo import MongoClient
import datetime
# , decode_responses=True
dbhost = '127.0.0.1'
dbport = 27017
toSum = MongoClient(dbhost, dbport).r.to_sum
dsl = MongoClient(dbhost, dbport).r.sums
good = MongoClient(dbhost, dbport).r.day

now = datetime.datetime.now() + datetime.timedelta(days=-1)
now = now.strftime('%Y%m%d')
r = redis.StrictRedis(host='192.168.2.16', port=3369, db=0)
info = r.keys()
total = 'total:daily:'

def get_item(sp):
    try:
        info = r.hgetall(sp)
        d = {}
        l = []
        n = 0
        for x, y in info.iteritems():
            if len(x) == 8:
                d[x] = y
                if toSum.find({'name': sp, 'key': x, 'value': y}).count() <= 0:
                    toSum.save({'name': sp, 'key': x, 'value': y})
    except Exception as e:
        print(red(e))


def to_sum(info):
    l = []
    for x in info:
        if x.split(':')[1] not in l:
            # print(green(x.split(':')[1]))
            if dsl.find({'name': x.split(':')[1]}).count() <= 0:
                dsl.save({'name': x.split(':')[1]})
try:
    try:
        pass
        to_sum(info)
        for x in info:
            get_item(x)

    except Exception:
        pass
except Exception as e:
    print(red(e))


def t():
    try:
        d = {}
        for x in toSum.find():
            for y in dsl.find():
                # 需要判断的字段
                # print y['name'], x['key']
                if (y['name'] in x['name']) and (':day' not in x['name']) and ('total:daily' not in x['name']):
                    # 判断day
                    if x['key'] not in d:
                        d['key'] = x['key']
                        d['value'] = x['value']
                        d['name'] = y['name']
                    else:
                        d['value'] = x['value'] + d['value']
                    d['name'] = total + d['name']
                    if now == x['key']:
                        good.save(dict(d))
                        # r.hset(d['name'],  d['key'], d['value'])
    except Exception as e:
        print(red(e))

try:
    t()
    l = []
    for x in good.find().sort('value', -1):
        if x['name'] not in l:
            l.append(x['name'])
            print x['name'], x['key'], x['value']
            r.hset(x['name'], x['key'], x['value'])
    good.remove({})
except Exception as e:
    print(red(e))
