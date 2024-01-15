# coding:utf-8

from gfirefly.server.globalobject import GlobalObject
import servernames
from game.util import nodeutil


def notify(dids, cid, data):
    """

    :param dids:
    :param cid: mempush.py 中定义
    :param data:
    :return:
    """
    if not dids:
        return
    for sername in GlobalObject().root.childsmanager._childs.keys():
        if sername.startswith(servernames.GAME_GATE_NAME):
            nodeutil.localCallChildNoResult(sername, "notify", dids, cid, data)
