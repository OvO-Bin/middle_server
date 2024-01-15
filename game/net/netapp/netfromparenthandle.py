# coding:utf8
from game.util import stringutil
from gfirefly.server.globalobject import GlobalObject

import servernames
from game.util.excepts import RemoteServiceMultiHandle


@RemoteServiceMultiHandle(servernames.GAME_GATE_NAME, servernames.GAME_GATE_NUMS)
def push_data(cid, data, session_id_list):
    """
    向客户端推送信息
    :param cid:
    :param data:
    :param session_id_list:
    :return:
    """
    GlobalObject().netfactory.pushObject(cid, data, session_id_list)


@RemoteServiceMultiHandle(servernames.GAME_GATE_NAME, servernames.GAME_GATE_NUMS)
def close_client(session_id):
    """
    关闭与游戏客户端的连接
    :param session_id: int 与游戏客户端连接的动态id
    :return:
    """
    GlobalObject().netfactory.loseConnection(session_id)
    print("net close_client session_id(%d)" % session_id)
