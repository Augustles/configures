# coding=utf-8

from celery import Celery
import time
import os
app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@app.task
def add(x, y):
    return x+y

@app.task
def down_img(url):
    os.chdir('/root/web/configures/stackflow/test2/ck101')
    res = os.system(url)
    return {'result': res}

if __name__ == '__main__':
    app.start()
