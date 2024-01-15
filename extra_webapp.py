# coding:utf-8

from flask import request
from gfirefly.server.globalobject import webserviceHandle, GlobalObject
from gtwisted.core import reactor


@webserviceHandle('/sstop')
def sstop():
    '''sstop service
    '''
    n = request.args["node"]
    s = request.args["site"]
    print "-----x-----sstop the node:%s,site:%s " % (n, s)
    for child in GlobalObject().root.childsmanager._childs.values():
        if (s == "0" and child.getName() == n) or (s == "-1" and child.getName().startswith(n)) or (
                s == "1" and child.getName().endswith(n)):
            child.callbackChildNotForResult('serverStop')
    return "sstop"


@webserviceHandle('/report_and_stop')
def report_and_stop():
    '''stop service
    '''

    for child in GlobalObject().root.childsmanager._childs.values():
        child.callbackChildNotForResult('serverStop')
    reactor.callLater(0.5, reactor.stop)

    return "report_and_stop"
