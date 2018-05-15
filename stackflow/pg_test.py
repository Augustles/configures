# coding=utf8

import psycopg2
import psycopg2.extras
import ipdb

config = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'postgres',
    #  'password': '',
    'database': 'test'
}

conn = psycopg2.connect(
    host=config['host'],
    port=config['port'],
    user=config['user'],
    #  password=config['password'],
    database=config['database']
)
# connect()也可以使用一个大的字符串参数, 比如”host=localhost port=5432 user=postgres password=postgres dbname=test”
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#这里创建的是一个字典Cursor, 这样返回的数据, 都是字典的形式, 方便使用
