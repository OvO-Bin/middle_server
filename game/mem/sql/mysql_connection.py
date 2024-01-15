# -*- coding:utf-8 -*-
"""
    mysql
"""
import servernames
import patches.mysql
import sys
import json


def get_platform():
    return sys.platform


def get_config_mysql_connection():
    """
        获取游戏配置表的库
    """
    databases_name = servernames.CONFIG_SQL_DB
    mysql_connect = patches.mysql.Connection(servernames.CONFIG_SQL_HOST, databases_name,
                                             servernames.CONFIG_SQL_ACC, servernames.CONFIG_SQL_PAS)
    return mysql_connect


def get_server_data_connection():
    """
        获取游戏数据库连接
    """
    global DB
    global PASSWORD
    global HOST
    global USER
    global PORT
    if get_platform() == "win32":
        config_path = "middle_server/config/win/config.json"
    elif get_platform() == "linux2":
        config_path = "middle_server/config/linux/config.json"
    else:
        raise Exception("Error Platform!!")

    with open(config_path) as config_file:
        config_str = config_file.read()
        config_json = json.loads(config_str)
        HOST = config_json['db']['host']
        DB = config_json['db']['db']
        USER = config_json['db']['user']
        PASSWORD = config_json['db']['passwd']
    mysql_connect = patches.mysql.Connection(HOST, DB, USER, PASSWORD)
    return mysql_connect
