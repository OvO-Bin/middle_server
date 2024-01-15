# coding:utf-8
'''
Created on 2013-11-1

@author: jiangtao
'''
import base64
import json


def loadzlibstr(data):
    '''加载经ZLIB压缩的STR'''
    return json.loads(base64.decodestring(data).decode("zlib"))


def dumpzlibstr(obj):
    '''ZLIB压缩经dump的STR'''
    return base64.encodestring(json.dumps(obj).encode("zlib"))


def loads(data):
    '''str转换成obj'''
    return json.loads(data)


def dumps(rtn):
    '''字典列表转换成str'''
    return json.dumps(rtn, separators=(',', ':'))


def objstr(obj):
    '''对象转换成字符串'''
    return json.dumps(ots(obj))


# complex obj to json
# 复杂对象转换json对象 (dict、list)
def ots(obj):
    '''对象转换成字符串'''
    if isinstance(obj, list):
        return list2json(obj)
    elif isinstance(obj, dict):
        return dict2json(obj)
    elif isinstance(obj, unicode):  # unicode   *****notice******* unicode is changed to str 
        return obj.encode('utf-8')
    elif obj == None or isinstance(obj, int) or isinstance(obj, long) or isinstance(obj, str) or isinstance(obj,
                                                                                                            float):  # int or str or long
        return obj
    elif isinstance(obj, object):  # other class
        return obj2dict(obj)
    else:
        return obj


# 用于生成json 对象     
def obj2dict(obj):
    dd = {}
    for m in dir(obj):
        # print m
        if m[0] != "_" and not callable(m):
            value = getattr(obj, m)
            if isinstance(value, unicode):  # unicode   *****notice******* unicode is changed to str 
                value = value.encode('utf-8')
            elif isinstance(value, list) or isinstance(value, set):  # list  
                value = list2json(value)
            elif value == None or isinstance(value, int) or isinstance(value, long) or isinstance(value,
                                                                                                  str) or isinstance(
                value, float):  # int or str or long
                pass
            elif isinstance(value, dict):  # dict
                value = dict2json(value)
            elif isinstance(value, object):  # other class
                try:
                    value = obj2dict(value)
                except:
                    pass
            else:
                pass
            dd[m] = value
    return dd


def list2json(ll):
    res_list = []
    for item in ll:
        res_list.append(ots(item))

    return res_list


def dict2json(dd):
    res = {}
    for item in dd:
        res[item] = ots(dd[item])
    return res


class Obj(object):
    def __init__(self):
        pass
