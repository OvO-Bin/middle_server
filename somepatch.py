# coding:utf-8
'''
Created on 2016年6月14日

@author: Administrator
'''
from gevent import monkey;

monkey.patch_all(subprocess=True, socket=False)
import os

if os.name == 'nt':
    from twisted.internet import iocpreactor

    iocpreactor.install()
elif os.name != 'posix':
    from twisted.internet import epollreactor

    epollreactor.install()
