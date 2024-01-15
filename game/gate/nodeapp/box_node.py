# coding:utf8
"""
逻辑处理
"""

import json
import time
from game.util import nodeutil, stringutil, jsonutil
from game.util.excepts import IllegalStateError, exceptsInMethod
from game.util.excepts import MyExceptsHandle
from game.util import dateutil

from game.gate.netapp import gatetonethandle
from game.gate.core.user import User
from game.gate.core.usermanager import UserManager
import servernames
from game.proto import BoxProto_pb2
from game.gate.service import gate_in


def __add_user(did, box_id, token):
    """
    进入场景
    :param did:
    :param box_id:
    :param token:
    :return:
    """
    user = User(did, box_id)
    user.token = token
    UserManager().add_user(user)
    return user


@gate_in
def land_1(cid, did, data):
    """
    盒子登录验证
    :param cid:
    :param did: int 账号动态id
    :param data: string proto数据
    :return:
    """
    request = BoxProto_pb2.BoxLoginRequest()
    request.ParseFromString(data)
    response = BoxProto_pb2.BoxLoginResponse()
    box_id = request.box_id
    token = request.token

    #  之后用md5处理
    if stringutil.getMd5Str(box_id + servernames.LOGIN_SECRET) != token:
        print "非法登录校验失败:" + "box_id=" + box_id + ",token=" + token
        gatetonethandle.close_client(did)
        assert ("fei fa deng lu jiao yan shi bai" == "")
    __add_user(did, box_id, token)

    response.result = BoxProto_pb2.BOX_SUCCESS
    return response.SerializeToString()


@gate_in
def heartbeat_999(cid, did, data):
    """
    心跳
    :param cid:
    :param did:
    :param data:
    :return:
    """
    UserManager().heartbeat(did)
