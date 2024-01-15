# coding:utf8

from gfirefly.server.globalobject import GlobalObject
import servernames
from game.net.protocol.datapack import MyDataPackProtocol
from game.net import netconst
from game.util import nodeutil


def call_when_conn_lost(conn):
    """
    当与客户端连接断开时的处理
    :param conn:
    :return:
    """
    did = conn.transport.sessionno  # 动态id
    print "call_when_conn_lost %s" % did

    nodeutil.localCallRemote(servernames.GAME_GATE_NAME + "_" + str(netconst.GATE_ID), "net_conn_lost", servernames.get_wrap_did(did, netconst.NET_ID))


def call_when_conn_made(conn):
    """
        连接建立时刻
    """
    did = conn.transport.sessionno  # 动态id
    print "call_when_conn_made %s " % did


def call_when_stop():
    """
    服务器关闭前的处理
    """
    pass


data_protocol = MyDataPackProtocol()  # 协议头
GlobalObject().netfactory.setDataProtocl(data_protocol)

GlobalObject().netfactory.doConnectionLost = call_when_conn_lost
GlobalObject().netfactory.doConnectionMade = call_when_conn_made
GlobalObject().stophandler = call_when_stop


def load_module():
    import netapp
    pass
