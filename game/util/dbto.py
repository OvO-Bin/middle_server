# coding:utf8
'''
Created on 2013-9-17

@author: jt
'''
from gfirefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor


def exeone(sql):
    '''查找一条记录
    @param sql: str sql查询语句
    @return: {}
    '''
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def exeall(sql):
    '''查找多条记录
    @param sql: str sql查询语句
    @return: {}
    '''
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def exeupdate(sql):
    '''添加 修改 删除记录
    @return: bool
    '''
    conn = dbpool.connection()
    cursor = conn.cursor()

    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count >= 1:
        return True
    else:
        return False


def getAllIds(tbName):
    '''获得ID列表
    '''
    rt = []
    sql = "select id from %s" % tbName
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        rt.append(row[0])
    cursor.close()
    conn.close()
    return rt


def getMaxId(tbName):
    '''获得表中最大ID
    '''
    sql = "select max(id) as maxId from %s" % tbName
    rt = exeone(sql)
    if not rt or not rt["maxId"]:
        return 0
    return rt["maxId"]


def getCount(tbName):
    '''获得表的记录数'''
    sql = "select count(id) as tbCount from %s" % tbName
    rt = exeone(sql)
    return rt["tbCount"]
