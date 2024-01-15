# coding:utf8

import gc

from gfirefly.server.globalobject import GlobalObject
from gtwisted.core.greactor import GeventReactor
import traceback

reactor = GeventReactor()


def call_when_stop():
    '''服务器关闭前的操作'''
    print("close gate server")


GlobalObject().stophandler = call_when_stop


def gc_collect(delta):
    """
    内存清理
    :param delta:
    :return:
    """
    print("gc_collect")
    gc.collect()
    reactor.callLater(delta, gc_collect, delta)


def load_module():
    gc_collect(1800)
    try:
        import netapp
        import nodeapp
        import schedular  # 不可以移除
    except Exception, e:
        traceback.print_exc()
