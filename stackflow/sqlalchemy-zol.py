# coding=utf-8

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, and_
from sqlalchemy.orm import create_session, sessionmaker
# from sqlalchemy.sql.expression import Cast
# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.dialects.mysql import \
#     BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
#     DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
#     LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
#     NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
#     TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
from pymongo import MongoClient
from fabric.colors import green, red
from time import sleep
from bson.objectid import ObjectId
from chardet import detect
import re
DBINFO = 'mongodb://august:nana@0.0.0.0:27017/'

nbbs = MongoClient(DBINFO).nbbs.nzol
to_mysql_stats = MongoClient(DBINFO).nbbs.tostats
bad = MongoClient(DBINFO).nbbs.bad
import gevent
from gevent import monkey
monkey.patch_all()
from gevent.pool import  Pool, Group

# db_config = {
#     'host': '127.0.0.1:3310',
#     'user': 'root',
#     'passwd': 'wslwsl',
#     'db': 'kmatrix',
#     'charset': 'utf8'
# }
db_config = 'mysql://root:nana@127.0.0.1:3306/kmatrix?charset=utf8'
engine = create_engine(db_config, echo=True)
# , echo=True
# 连接数据表
metadata = MetaData(engine)
tb_data_source = Table('tb_data_source', metadata, autoload=True)
tb_data_source_group = Table('tb_data_source_group', metadata, autoload=True)
tb_document = Table('tb_document', metadata, autoload=True)
# 会话, 查询
session = create_session()
query = session.query(tb_document)
query1 = session.query(tb_data_source_group)
query2 = session.query(tb_data_source)

nzol = nbbs.find({'uri_doc_index': 0}).batch_size(61)
def to_mysql(nzol):
    i = tb_document.insert()
    # global ltd
    # ltd = ObjectId('56fc8b8b47a3436d7bc69c93')
    # ltd = to_mysql_stats.find_one({'ltd': {'$exists': True}}).get('ltd')
    # ltd = ObjectId('56feb60d47a343642f3ed957')
    # ltd =
    # '_id': {'$gt': ltd}
    # {'_id': {'$gt': ltd}
    while True:
        for item in nzol:
            global url
            url = item['download_uri']
            try:
                # 乱码
                ec = detect(item['title'])
#                ec = detect(item['content'])
#                ec = detect(item['author'])
                # tid = item.get('_id')
                # parent_doc_id = unicode(tid).split()[0]
                try:
                    t = nbbs.find({'download_uri': url, 'uri_doc_index': {
                        '$gt': 0}}).sort('uri_doc_index', -1)
                    mdi = t[0]['uri_doc_index']
                    mdc = t.count()
                    del t
                    # t1 = nbbs.nzol.find({'download_uri': url, 'uri_doc_index': {
                    #     '$gt': 0}}).sort('uri_doc_index', 1)
                except Exception as e:
                    t = []
                    mdi = 0
                    mdc = 0
                try:
                    q = query.filter_by(download_uri=url).order_by(
                        'uri_doc_index desc')
                    mli = int(q.first().uri_doc_index)
                    mlc = int(q.count())
                except Exception as e:
                    q = []
                    mli = 0
                    mlc = 0
                # t = nbbs.nzol.find({'download_uri': url, 'parent_doc_id': parent_doc_id, 'dsg_id': item['dsg_id'], 'data_source_id': item['data_source_id']}).sort('uri_doc_index', -1)
                # print t.count(), t[0]['uri_doc_index']

                try:
                    # 判断所有t和第一个的index是否一致, 检查mongo中数据时候正常
                    # 判断mongo中获取到的最大index和mysql的最大index比较
                    # mongo和mysql记录比较
                    if (mdi == mdc) and (mdi > mli):
                        data_source_uri = 'http://bbs.zol.com.cn/' + \
                            item['download_uri'].split('/')[3] + '/'
                        q = query2.filter_by(
                            server=data_source_uri).first()
                        if q:
                            data_source_id = q.data_source_id
                        else:
                            q = query2.filter_by(
                                server='http://bbs.zol.com.cn/otherbbs/').first()
                            data_source_id = q.data_source_id

                        q = query1.filter_by(
                            info='http://bbs.zol.com.cn/').first()
                        data_source_group_id = q.id
                        if mlc != 0:
                            t1 = nbbs.find({'download_uri': url, 'uri_doc_index': {
                                '$gt': mli}}).sort('uri_doc_index', 1)
                            for y in t1:
                                # 判断时候是连续楼层
                                if (y['uri_doc_index'] - 1 == mli):
                                    pass
                                else:
                                    raise Exception
                                ck = [x for x in range(1, 5000, 20)]
                                # 检查title, [1, 21, 41]
                                if y['uri_doc_index'] in ck:
                                    ec = detect(item['title'])
                                y['dsg_id'] = data_source_group_id
                                y['data_source_id'] = data_source_id
                                q1 = query.filter_by(
                                    download_uri=y['download_uri'], uri_doc_index=0).first()
                                if q1:
                                    y['parent_doc_id'] = q1.doc_id
                                    y['master_doc_id'] = q1.doc_id
                                else:
                                    raise Exception
                                y['content'] = re.sub(
                                    r'\s*\n+\s*', '\n', y['content'])
                                y['new_doc'] = 1
                                y['cybermedia_id'] = 3
                                # print(green(y))
                                del y['_id']
                                print(green(y['download_uri']))
                                i.execute(y)
                        else:
                            item['content'] = re.sub(
                                r'\s*\n+\s*', '\n', item['content'])
                            d = {'new_doc': 1, 'cybermedia_id': 3, 'title': item['title'], 'publish_date': item['publish_date'], 'modified_date': item['modified_date'], 'download_uri': item[
                                'download_uri'], 'dsg_id': data_source_group_id, 'data_source_id': data_source_id, 'uri_doc_index': item['uri_doc_index'], 'author': item['author'], 'content': item['content']}
                            print(green(item['download_uri']))
                            i.execute(d)
                            t1 = nbbs.find({'download_uri': url, 'uri_doc_index': {
                                '$gt': mli}}).sort('uri_doc_index', 1)
                            for y in t1:
                                # 判断时候是连续楼层
                                if (y['uri_doc_index'] - 1 == mli) or (mli == 0):
                                    pass
                                else:
                                    raise Exception
                                ck = [x for x in range(1, 5000, 20)]
                                # 检查title, [1, 21, 41]
                                if y['uri_doc_index'] in ck:
                                    ec = detect(item['title'])
                                y['dsg_id'] = data_source_group_id
                                y['data_source_id'] = data_source_id
                                q1 = query.filter_by(
                                    download_uri=y['download_uri'], uri_doc_index=0).first()
                                if q1:
                                    y['parent_doc_id'] = q1.doc_id
                                    y['master_doc_id'] = q1.doc_id
                                else:
                                    raise Exception
                                y['content'] = re.sub(
                                    r'\s*\n+\s*', '\n', y['content'])
                                y['new_doc'] = 1
                                y['cybermedia_id'] = 3
                                # print(green(y))
                                del y['_id']
                                print(green(y['download_uri']))
                                i.execute(y)

                except Exception as e:
                    print(red(e, url))

                # ltd = item['_id']
            except Exception as e:
                if bad.find({'url': url}).count() <= 0:
                    bad.save({'url': url})
                # else:
                #     t = bad.find_one({'url': url})
                #     bad.update({'_id': t.get('_id')}, {'$set': {'url': url}})
                print(red(e, url))

        print(red('==> waiting for update...'))
        sleep(30)
try:
    # to_mysql(nbbs)
    # pool = Pool(4)
    # greenlets = [gevent.spawn(to_mysql, y) for y in nzol]
    # gevent.joinall(greenlets)
    # g = Group()
    # g.map_async(to_mysql, nbbs)
    # g.join()
    for x in xrange(4):
        g = Group()
        g.apply_async(to_mysql, args=(nzol,))
        g.join()
except Exception as e:
    print(11111)
    print(red(e))
