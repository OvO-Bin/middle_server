# coding:utf8
"""
gate进程处理子进程消息
"""
from game.gate.core.usermanager import UserManager
from game.gate.netapp import gatetonethandle
from game.gate.service import gateInMethod
from gfirefly.server.globalobject import rootserviceHandle

from game.proto import NotifyProto_pb2
from game.util.excepts import exceptsInMethod
from gfirefly.dbentrust.memclient import mclient
from game.gate.netapp import gatetonethandle
from game.mem.core import mempush


@rootserviceHandle
def script_to_box(data):
    """
    把脚本发送到盒子
    :param data:
    :return:
    """
    msg_proto = NotifyProto_pb2.NotifyMessagePlay()
    msg_proto.message = data.get("script")
    msg_proto.auto_run = data.get("auto_run")
    msg_proto.cycle_run = data.get("cycle_run")
    gatetonethandle.send_data_to_net(mempush.NOTIFY_PLAY, msg_proto.SerializeToString(), [data.get("did")])


@rootserviceHandle
def speech_string_to_box(data):
    """
    把脚本发送到盒子
    :param data:
    :return:
    """
    msg_proto = NotifyProto_pb2.NotifyMessageSpeechString()
    msg_proto.message = data.get("message")
    gatetonethandle.send_data_to_net(mempush.NOTIFY_SPEECH_STRING, msg_proto.SerializeToString(), [data.get("did")])


@rootserviceHandle
def event_up_to_box(data):
    """
    把脚本发送到盒子
    :param data:
    :return:
    """
    msg_proto = NotifyProto_pb2.NotifyMessageEventUp()
    msg_proto.message = data.get("keycode")
    gatetonethandle.send_data_to_net(mempush.NOTIFY_EVENT_UP, msg_proto.SerializeToString(), [data.get("did")])


@rootserviceHandle
def forwarding(cid, did, data):
    """
    接收net转发过来的信息
    :param cid: int 指令号
    :param did: int 连接id
    :param data: obj proto内容
    :return:
    """
    if cid in gateInMethod._targets.keys():
        return gateInMethod.callTarget(cid, cid, did, data)
    else:
        user = UserManager().get_user_by_did(did)

        if not user:
            gatetonethandle.close_client(did)
            return
        UserManager().opt(did)
        return exceptsInMethod.callTarget(cid, did, data)


@rootserviceHandle
def net_conn_lost(did):
    '''账号掉线时的处理
    @param did: int 动态id
    '''
    print "net_conn_lost handle"
    user = UserManager().get_user_by_did(did)
    if not user:
        print "user = None, did=%s" % did
        return
    # exceptsInMethod.callTarget(998, did)
    UserManager().del_user(user.box_id, did)
    print("gate net_conn_lost account(%s),did(%d)" % (user.box_id, did))
