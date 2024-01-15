# coding:utf-8
'''
Created on 2015年7月3日

@author: Administrator
'''
import httplib
import socket
import urllib
import struct

from gfirefly.server.globalobject import GlobalObject


def is_can_handle(remote_name):
    ro = GlobalObject().remote[remote_name]
    if ro and ro._factory._protocol:
        return True
    else:
        return False


def localCallRemote(remotename, targetname, *args):
    return GlobalObject().remote[remotename].callRemote(targetname, *args)


def localCallChild(childname, targetname, *args):
    return GlobalObject().root.callChild(childname, targetname, *args)


def localCallRemoteNoResult(remotename, targetname, *args):
    GlobalObject().remote[remotename].callRemoteNotForResult(targetname, *args)


def localCallChildNoResult(childname, targetname, *args):
    GlobalObject().root.callChildNotForResult(childname, targetname, *args)


def get_inner_ip():
    """
        获取内网IP
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def get_ip():
    import platform
    if 'Windows' in platform.system():
        # 内网
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        return myaddr
    else:
        import servernames
        return servernames.OUTER_IP


def http_req(host, url, method, params=None, headers={}):
    '''HTTP请求
    @param GET请求时params的类型为dict
    '''
    conn = httplib.HTTPConnection(host)
    try:
        method = method.upper()
        if method == "GET":
            if params:
                params = urllib.urlencode(params)
            print("params %s" % (url + (params and "?" + params or "")))
            conn.request(method, url + (params and "?" + params or ""), None, headers)
        else:
            conn.request(method, url, params, headers)
        r1 = conn.getresponse()
        return r1.read()

    finally:
        if conn:
            conn.close()


def https_req(host, url, method, params=None, headers={}):
    '''HTTPS请求
    result = nodeutil.http_req_test("127.0.0.1:3017",
                           "/test",
                           "post",
                           "a=1&b=1")
    @param GET请求时params的类型为dict
    '''
    conn = httplib.HTTPSConnection(host)
    try:
        method = method.upper()
        if method == "GET":
            if params:
                params = urllib.urlencode(params)
            print("params %s" % (url + (params and "?" + params or "")))
            conn.request(method, url + (params and "?" + params or ""), None, headers)
        else:
            conn.request(method, url, params, headers)
        r1 = conn.getresponse()
        return r1.read()

    finally:
        if conn:
            conn.close()


def http_req_form(host, url, method, params=None, headers={}):
    '''HTTP请求 form获取

    @param 请求时params的类型为dict
    '''
    conn = httplib.HTTPConnection(host)
    try:
        method = method.upper()

        if method == "GET":
            if params:
                params = urllib.urlencode(params)
            uurl = url + (params and "?" + params or "")
            print uurl
            conn.request(method, uurl, None, headers)
        else:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            if params:
                params = urllib.urlencode(params)
                print params
            conn.request(method, url, params, headers)

        r1 = conn.getresponse()
        if r1.status == 200:
            return r1.read()
        return None
    finally:
        if conn:
            conn.close()
