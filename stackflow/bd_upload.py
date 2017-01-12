# coding=utf-8

import os
from tornado import gen, ioloop
from tasks import upload
import shutil

path = '/root/web/configures/stackflow'
@gen.coroutine
def upload1(cmd):
    status = os.system(cmd)
    raise gen.Return(status)

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
        for x in os.listdir('ck101/卡提諾正妹抱報'):
            print x
            cmd = 'bypy upload ck101/卡提諾正妹抱報/%s ck101/卡提諾正妹抱報/%s' %(x, x)
            r = os.system(cmd)
            if not r:
                shutil.rmtreee('ck101/卡提諾正妹抱報/%s' %x)

main()
