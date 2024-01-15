# coding:utf8

from gfirefly.server.globalobject import remoteserviceHandle

from game.gate.core.usermanager import UserManager
from game.gate.netapp import gatetonethandle
import servernames


@remoteserviceHandle(servernames.GAME_DBFRONT_NAME)
def notify(did_list, cid, data):
    if not did_list:
        return
    gatetonethandle.send_data_to_net(cid, data, did_list)


@remoteserviceHandle(servernames.GAME_DBFRONT_NAME)
def kick_user(box_id):
    """
    :param box_id:
    :return:
    """

    UserManager().kick(box_id)
