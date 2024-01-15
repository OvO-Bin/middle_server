# coding:utf8
"""
DB进程中处理数据，gate进程数据共享
"""

from gfirefly.server.globalobject import rootserviceHandle, GlobalObject

from game.util import nodeutil


@rootserviceHandle
def kick_user(box_id, gate_name):
    """
    :param box_id:
    :param gate_name:
    :return:
    """

    nodeutil.localCallChild(gate_name, "kick_user", box_id)
