# coding:utf-8
import time
from game.util import dbto


def get_box_id_list(school, room):
    """
    群发的时候通过用户ID查找对应的盒子ID列表
    :param school:
    :param room:
    :return:
    """
    sql = "select box from tpt_bbox where school=%s and room=%s" % (school, room)
    return dbto.exeall(sql)


def get_last_version_config():
    """
    获取apk版本信息的的配置文件
    :return:
    """
    sql = "select * from tpt_res where islast=1"
    return dbto.exeall(sql)

#
#
# def get_recharge_data(order_id):
#     sql = "select * from biz_recharge_order where order_id='%s'" % \
#           order_id
#     rt = dbto.exeone(sql)
#     return rt
#
# def update_recharge_data(order_id, status, description=''):
#     """
#         更新订单状态
#     """
#     sql = "UPDATE biz_recharge_order SET " \
#           "order_status='%s', " \
#           "update_tm='%s', " \
#           "failed_desc='%s' " \
#           "WHERE order_id=%s" % \
#           (status, time.time(), description, order_id)
#
#     rt = dbto.exeupdate(sql)
#     return rt
