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

def main():
    os.chdir(path)
    status = os.system('python yua.py')
    print status
    if not status:
        os.chdir('test2')
        print 'starting upload yua ...'
        r = os.system('bypy upload -dv')
        if not r:
            shutil.rmtree('insyua')
            shutil.rmtree('twiyua')

    os.chdir(path)
    status = os.system('python ck101.py')
    if not status:
        os.chdir('ck101')
        print 'starting upload ck101 ...'
        cmds = set()
        for x in os.listdir('ck101/卡提諾正妹抱報'):
            print x
            cmd = 'bypy upload ck101/卡提諾正妹抱報/%s ck101/卡提諾正妹抱報/%s' %(x, x)
            cmds.add(cmd)
        greenlet = [gevent.spawn(async_upload, x) for x in cmds]
        gevent.joinall(greenlet)

main()
