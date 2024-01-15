# coding:utf-8

import time

from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.services import CommandService
from twisted.python import log

exceptsInMethod = CommandService("excepts")  # excepts拦截并处理的指令号方法


class IllegalStateError(RuntimeError):
    '''业务逻辑异常'''

    def __init__(self, args):
        self.args = args


class IllegalStateErrorIntercept:
    '''业务方法异常拦截'''

    def __init__(self, method):
        self.method = method

    def invoke(self, *args, **kw):
        try:
            now = time.time()
            log.msg("=====>>>>>%s:%s" % (GlobalObject().json_config.get("name"), self.method.__name__))
            rt = self.method(*args, **kw)
            log.msg("<<<<<=====%s:%s:%s" % (
                GlobalObject().json_config.get("name"), self.method.__name__, time.time() - now))
        except IllegalStateError, e:
            log.err("error:{0},cmd:{1},data:{2}".format(e, self.method.__name__, args))
            return isinstance(e[0], int) and e[0] or 999
        return rt


class myRemoteserviceHandle:
    """
        支持业务方法异常拦截的remoteserviceHandle
    """

    def __init__(self, remotename):
        """
        """
        self.remotename = remotename

    def __call__(self, target):
        """
        """
        key = int((target.__name__).split('_')[-1])
        sc = GlobalObject().remote[self.remotename]._reference._service
        if sc._targets.has_key(key):
            exist_target = sc._targets.get(key)
            raise "target [%d] Already exists,\
                Conflict between the %s and %s" % (key, exist_target.__name__, target.__name__)
        c = IllegalStateErrorIntercept(target)
        sc._targets[key] = c.invoke


class MyExceptsHandle:
    """
                支持业务方法异常拦截的method
    """

    def __init__(self):
        """
        """
        pass

    def __call__(self, target):
        """
        """
        key = int(target.__name__.split('_')[-1])
        sc = exceptsInMethod
        if sc._targets.has_key(key):
            exist_target = sc._targets.get(key)
            raise "target [%d] Already exists,\
                Conflict between the %s and %s" % (key, exist_target.__name__, target.__name__)
        c = IllegalStateErrorIntercept(target)
        sc._targets[key] = c.invoke


class RemoteServiceMultiHandle:
    """作为remote节点，供多个节点调用的接口描述符
    """

    def __init__(self, remotename, gatenumes):
        """
        """
        self.remotename = remotename
        self.gatenumes = gatenumes

    def __call__(self, target):
        """
        """
        for i in range(1, self.gatenumes + 1):
            GlobalObject().remote[self.remotename + "_" + str(i)]._reference._service.mapTarget(target)
