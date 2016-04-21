# coding=utf-8

from redis import Redis
from rq import Queue
from req import count_words_at_url
from fabric.colors import green, red
from time import sleep
r = Redis(host='192.168.2.193', password='nana')

q = Queue('high', connection=r, default_timeout=600)


job = q.enqueue_call(func=count_words_at_url, args=['http://nvie.com'],
                     result_ttl=86400)  # result过期时间
while True:
    if job.is_finished:
        print(red(job.id))
        print(red(job.result))
        break
