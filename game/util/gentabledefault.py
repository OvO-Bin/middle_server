# coding:utf-8
'''
Created on 2015年7月14日
生成表中字段的默认值
@author: Administrator
'''
import json

from gfirefly.dbentrust import dbpool
from twisted.python import log


def ReadDDL(tablename):
    '''

    :param tablename:
    :return: ((u'id', u'bigint(20)', u'NO', u'PRI', u'0', u''), (u'actcode', u'varchar(10)', u'NO', u'', None, u''), (u'create_tm', u'bigint(20)', u'NO', u'', u'0', u''), (u'used_tm', u'bigint(20)', u'NO', u'', u'0', u''), (u'uname', u'varchar(64)', u'NO', u'', u'', u''))
    '''
    sql = "desc %s" % tablename
    conn = dbpool.dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def writeTable(tbName):
    '''

    :param tbName:
    :return:
    '''
    rows = ReadDDL(tbName)
    kv = {}
    for row in rows:
        if row[1].find("char") != -1:
            kv[row[0]] = row[4]
        elif row[1].find("int") != -1:
            kv[row[0]] = row[4] and int(row[4]) or 0
        else:
            kv[row[0]] = row[4] and float(row[4]) or 0
    return kv


def writeTables(tbNames):
    kv = {}
    for tbName in tbNames:
        kv[tbName] = writeTable(tbName)
    return kv


def getAllTbNames(dbName):
    '''
    result = ((u'biz_actcode',), (u'biz_player',), (u'biz_recharge_order',))
    :param dbName:
    :return: [u'biz_actcode', u'biz_player', u'biz_recharge_order']
    '''
    sql = "select table_name from information_schema.tables where table_schema='%s' and table_type='base table'" % dbName
    conn = dbpool.dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    rt = []
    for row in result:
        rt.append(row[0])
    return rt


def genTableDefault(dbName):
    return writeTables(getAllTbNames(dbName))
