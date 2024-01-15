# coding:utf8

import servernames
from game.util import nodeutil
from gfirefly.server.globalobject import GlobalObject


def send_data_to_net(cid, data, did_list):
    """

    :param cid: int 指令号
    :param data: obj proto内容
    :param did_list: [int] did列表
    :return:
    """
    if GlobalObject().json_config.get("name") == servernames.GAME_DBFRONT_NAME:
        print "send_data_to_net need gate"
        return

    if did_list:
        did_dic = {}
        for did in did_list:
            net_id = servernames.get_net_id(did)
            if net_id > 0:
                if not did_dic.has_key(net_id):
                    did_dic[net_id] = []
                did_dic[net_id].append(servernames.get_session_id(did))
            else:
                print("net_id(%s) error : did %s" % (net_id, did))
        for _net_id, _session_id_list in did_dic.items():
            nodeutil.localCallChildNoResult(servernames.GAME_NET_NAME + "_" + str(_net_id), 'push_data', cid, data,
                                            _session_id_list)


def close_client(did):
    """
        关闭客户端连接
    """
    nodeutil.localCallChildNoResult(servernames.GAME_NET_NAME + "_" + str(servernames.get_net_id(did)), 'close_client',
                                    servernames.get_session_id(did))
