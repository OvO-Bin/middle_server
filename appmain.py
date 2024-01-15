# coding:utf8


import json, sys, os
from gfirefly.server.server import FFServer
import somepatch
import servernames

if __name__ == "__main__":

    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')

    args = sys.argv
    servername = None
    config = None
    if len(args) > 2:
        servername = args[1]
        config = json.load(open(args[2], 'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers', {})
    masterconf = config.get('master', {})
    serconfig = sersconf.get(servername)
    ser = FFServer()
    ser.config(serconfig, servername=servername, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
