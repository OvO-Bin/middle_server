# -*- coding:utf-8 -*-

"""
    对服务器表的操作
"""
from gfirefly.dbentrust import util


def get_data(tb_name):
    """
        获取对应表数据
    """
    return util.ReadDataFromDB(tb_name)


def update_data(tb_name, props, prere):
    """
        更新数据到数据库
    """
    util.UpdateWithDict(tb_name, props, prere)


def del_data(tb_name, props):
    """
        移除数据
    """
    util.DeleteFromDB(tb_name, props)


def insert_data(tb_name, props):
    """
        插入数据库
    """
    util.InsertIntoDB(tb_name, props)
