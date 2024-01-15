# -*- coding:utf-8 -*-

"""
    工具类
"""
import pprint
import json
import sys
import MySQLdb

PASSWD = ''
DB = ''
PORT = ''
HOST = ''
USER = ''


def get_platform():
    return sys.platform


def get_game_db_connection():
    """
        获取游戏数据库连接
    """
    global DB
    global PASSWD
    global HOST
    global USER
    global PORT
    if get_platform() == "win32":
        config_path = "../config/win/config.json"
    elif get_platform() == "linux2":
        config_path = "../config/linux/config.json"
    else:
        raise Exception("Error Platform!!")

    with open(config_path) as config_file:
        config_str = config_file.read()
        config_json = json.loads(config_str)
        PASSWD = config_json['db']['passwd']
        charset = config_json['db']['charset']
        DB = config_json['db']['db']
        HOST = config_json['db']['host']
        USER = config_json['db']['user']
        PORT = config_json['db']['port']
    conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, charset=charset)
    return conn


def show_columns(conn, table_name):
    """
        获取表格概要
        ((column_name, type, is_None, is_PRI, default, ??), ...)
        exam:
            ('id', 'bigint(20)', 'NO', 'PRI', None, ''),
    """
    # conn.select_db("information_schema")
    conn.select_db(DB)
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM columns WHERE table_name='%s'" % table_name)
    cursor.execute("SHOW COLUMNS FROM %s.%s" % (DB, table_name))
    result = cursor.fetchall()
    return result


def has_column(conn, table_name, column_name):
    """
        是否有这个列
    """
    column_lst = show_columns(conn, table_name)
    column_name_lst = [row[0] for row in column_lst]
    return column_name in column_name_lst


def get_table_ddl(conn, table_name):
    """
        获取表格定义
    """
    conn.select_db(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s" % table_name)
    result = cursor.fetchall()


def add_column(conn, table_name, column_name, column_type, not_null, default, comment):
    """
        添加一列
        exam:
            add_column(_conn, 'biz_role', 'gold2', 'int(4)', True, 0, '金币数量测试测试')
    :param conn: 连接
    :param table_name: 表名
    :param column_name: 列名
    :param column_type: 类型  int(4) string ...
    :param not_null: 是否空 True False
    :param default: 默认值
    :param comment: 说明
    """
    if has_column(conn, table_name, column_name):
        print("add_column column:%s exist" % column_name)
        return
    if isinstance(default, basestring):
        sql = "ALTER TABLE %s ADD %s %s DEFAULT '%s' COMMENT '%s'" % (
            table_name, column_name, column_type, default, comment)
    else:
        sql = "ALTER TABLE %s ADD %s %s DEFAULT %s COMMENT '%s'" % (
            table_name, column_name, column_type, default, comment)
    if not_null:
        sql += " NOT NULL"
    print sql
    conn.select_db(DB)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()


def remove_column(conn, table_name, column_name):
    """
        移除列
    """
    if has_column(conn, table_name, column_name):
        sql = "ALTER TABLE %s DROP COLUMN %s " % (table_name, column_name)
        conn.select_db(DB)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()


def change_column_type(conn, table_name, column_name, new_column_name, column_type, not_null, default, comment):
    """
        修改单元格类型
    """
    if has_column(conn, table_name, column_name):
        if isinstance(default, basestring):
            sql = "ALTER TABLE %s CHANGE COLUMN %s %s %s DEFAULT '%s' COMMENT '%s'" % \
                  (table_name,
                   column_name,
                   new_column_name,
                   column_type,
                   default,
                   comment
                   )
        else:
            sql = "ALTER TABLE %s CHANGE COLUMN %s %s %s DEFAULT %s COMMENT '%s'" % \
                  (table_name,
                   column_name,
                   new_column_name,
                   column_type,
                   default,
                   comment
                   )
        if not_null:
            sql += " NOT NULL"
        print sql
        conn.select_db(DB)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

# _conn = get_game_db_connection()
# add_column(_conn, 'biz_role', 'gold2', 'int(4)', True, 0, '金币数量测试测试')
# change_column_type(_conn, 'biz_role', 'gold2', 'gold2', 'varchar(100)', False)
# remove_column(_conn, 'biz_role', 'gold2')
