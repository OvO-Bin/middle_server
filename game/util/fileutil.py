# coding:utf-8
'''
Created on 2016年1月14日

@author: Administrator
'''
import sys, os

from twisted.python import log


def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def read(rptId):
    '''读文件'''
    if isExist(rptId):
        rpt = None
        try:
            rpt = open(rptId, 'r')
            content = []
            while True:
                chs = rpt.read(1024)
                if not chs:
                    break
                else:
                    content.append(chs)
            return "".join(content)
        finally:
            if rpt:
                rpt.close()
    return None


def write(rptId, content):
    '''写文件'''
    rpt = None
    try:
        rpt = open(rptId, 'w+')
        rpt.write(content)
    finally:
        if rpt:
            rpt.close()


def append(f, content):
    '''追写文件
        @param ln 在行尾添加换行符
    '''
    try:
        f.write(content)
        f.flush()
        return len(content)
    except:
        log.err("write file %s fail" % f.name)
    return 0


def isExist(rptId):
    '''文件是否存在'''
    return os.path.exists(rptId)


def delete(rptId):
    '''删除文件'''
    try:
        if os.path.exists(rptId):
            os.remove(rptId)
    except:
        log.err("delete file %s fail" % rptId)
