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
import pymysql
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
from gevent.pool import Pool, Group


conn = pymysql.connect(host='127.0.0.1', port=3309,
                       user='root', passwd='wslwsl', db='kmatrix', charset='utf8')

nzol = nbbs.find({'uri_doc_index': 0}).batch_size(61)


def to_mysql(nzol):
    # i = tb_document.insert()
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
                detect(item['title'])
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
                    cmd = 'select uri_doc_index,download_uri from tb_document where download_uri="{0}" order by uri_doc_index desc'.format(
                        url)
                    with conn.cursor() as cur:
                        mlc = cur.execute(cmd)
                        mli = cur.fetchall()[0][0]
                except Exception as e:
                    mli = 0
                    mlc = 0
                print(2333, mli, mlc)
                # t = nbbs.nzol.find({'download_uri': url, 'parent_doc_id': parent_doc_id, 'dsg_id': item['dsg_id'], 'data_source_id': item['data_source_id']}).sort('uri_doc_index', -1)
                # print t.count(), t[0]['uri_doc_index']

                try:
                    # 判断所有t和第一个的index是否一致, 检查mongo中数据时候正常
                    # 判断mongo中获取到的最大index和mysql的最大index比较
                    # mongo和mysql记录比较
                    if (mdi == mdc) and (mdi > mli):
                        data_source_uri = 'http://bbs.zol.com.cn/' + \
                            item['download_uri'].split('/')[3] + '/'
                        cmd = 'select data_source_id,server from tb_data_source where server="{0}";'.format(
                            data_source_uri)
                        cur = conn.cursor()
                        if cur.execute(cmd):
                            data_source_id = cur.fetchone()[0]
                            # print(red(data_source_id))
                        else:
                            cmd = 'select data_source_id,server from tb_data_source where server="http://bbs.zol.com.cn/otherbbs/";'
                            # q = query2.filter_by(
                            #     server='http://bbs.zol.com.cn/otherbbs/').first()
                            data_source_id = cur.fetchone()[0]
                        cmd = 'select id,info from tb_data_source_group where info="http://bbs.zol.com.cn/";'
                        cur.execute(cmd)
                        data_source_group_id = cur.fetchone()[0]
                        # print(red(data_source_group_id))
                        if mlc != 0:
                            cmd = 'select doc_id,download_uri,uri_doc_index from tb_document where download_uri="{0}" and uri_doc_index=0'.format(
                                url)
                            cur.execute(cmd)
                            doc_id = cur.fetchone()[0]
                            # print(red(mlc))
                            # print(red(doc_id))
                            t1 = nbbs.find({'download_uri': url, 'uri_doc_index': {
                                '$gt': mli}}).sort('uri_doc_index', 1)
                            if t1[0]['uri_doc_index'] - 1 == mli:
                                pass
                            else:
                                raise Exception('Not compare')

                            for y in t1:
                                # 判断时候是连续楼层
                                ck = [x for x in range(1, 5000, 20)]
                                # 检查title, [1, 21, 41]
                                if y['uri_doc_index'] in ck:
                                    detect(item['title'])
                                y['dsg_id'] = data_source_group_id
                                y['data_source_id'] = data_source_id
                                if doc_id:
                                    y['parent_doc_id'] = doc_id
                                    y['master_doc_id'] = doc_id
                                else:
                                    raise Exception
                                y['content'] = re.sub(
                                    r'\s*\n+\s*', '\n', y['content'])
                                print(green(y['download_uri']))
                                cmd = 'INSERT INTO tb_document (data_source_id, cybermedia_id, title, publish_date, modified_date, download_uri, uri_doc_index, author, new_doc, master_doc_id, parent_doc_id, content, dsg_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                p = (data_source_id, 3, y['title'], y['publish_date'], y['modified_date'], y[
                                     'download_uri'], y['uri_doc_index'], y['author'], 1, doc_id, doc_id, y['content'], data_source_group_id)
                                with conn.cursor() as cur:
                                    cur.execute(cmd, p)
                                conn.commit()
                        else:
                            item['content'] = re.sub(
                                r'\s*\n+\s*', '\n', item['content'])
                            print(green(item['download_uri']))
                            cmd = 'INSERT INTO tb_document (data_source_id, cybermedia_id, title, publish_date, modified_date, download_uri, uri_doc_index, author, new_doc, content, dsg_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                            p = (data_source_id, 3, item['title'], item['publish_date'], item['modified_date'], item[
                                'download_uri'], item['uri_doc_index'], item['author'], 1, item['content'], data_source_group_id)
                            with conn.cursor() as cur:
                                cur.execute(cmd, p)
                                doc_id = cur.lastrowid
                            conn.commit()
                            # print(red(doc_id))
                            t1 = nbbs.find({'download_uri': url, 'uri_doc_index': {
                                '$gt': mli}}).sort('uri_doc_index', 1)
                            if t1[0]['uri_doc_index'] - 1 == mli:
                                pass
                            else:
                                raise Exception('Not compare')

                            for y in t1:
                                # 判断时候是连续楼层
                                ck = [x for x in range(1, 5000, 20)]
                                # 检查title, [1, 21, 41]
                                if y['uri_doc_index'] in ck:
                                    detect(item['title'])
                                y['dsg_id'] = data_source_group_id
                                y['data_source_id'] = data_source_id
                                if doc_id:
                                    y['parent_doc_id'] = doc_id
                                    y['master_doc_id'] = doc_id
                                else:
                                    raise Exception
                                y['content'] = re.sub(
                                    r'\s*\n+\s*', '\n', y['content'])
                                print(green(y['download_uri']))
                                cmd = 'INSERT INTO tb_document (data_source_id, cybermedia_id, title, publish_date, modified_date, download_uri, uri_doc_index, author, new_doc, master_doc_id, parent_doc_id, content, dsg_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                p = (data_source_id, 3, y['title'], y['publish_date'], y['modified_date'], y[
                                     'download_uri'], y['uri_doc_index'], y['author'], 1, doc_id, doc_id, y['content'], data_source_group_id)
                                with conn.cursor() as cur:
                                    cur.execute(cmd, p)
                                conn.commit()

                except Exception as e:
                    print(red(e, url))

                # ltd = item['_id']
            except Exception as e:
                if bad.find({'url': url}).count() <= 0:
                    bad.save({'url': url})
                print(red(e, url))

        print(red('==> waiting for update...'))
        sleep(30)
try:
    # to_mysql(nzol)
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
