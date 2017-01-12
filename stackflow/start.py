# coding=utf-8

import os
from tornado import gen, ioloop
from tasks import upload
import shutil
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.pool import Group, Pool

path = '/root/web/configures/stackflow'

def async_upload(cmd):
    print cmd
    r = os.system(cmd)
    gevent.sleep()
    if not r:
        shutil.rmtree(cmd.split()[-1])

os.chdir(path+ '/ck101')
def gen_cmds():
    try:
        cmds = set()
        for x in os.listdir('ck101/卡提諾正妹抱報'):
            cmd = 'bypy upload ck101/卡提諾正妹抱報/%s ck101/卡提諾正妹抱報/%s' %(x, x)
            cmds.add(cmd)
        return cmds
    except:
        pass

cmds = gen_cmds()

pool = Pool(len(cmds))
greenlet = [gevent.spawn(async_upload, x) for x in cmds]
gevent.joinall(greenlet)
