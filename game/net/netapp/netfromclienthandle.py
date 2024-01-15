# coding:utf8

from game.util import nodeutil, stringutil
from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.services import CommandService
from twisted.python import log
import servernames
from game.net import netconst


class NetCommandService(CommandService):

    def callTarget(self, targetKey, *args, **kw):
        '''call Target
        @param conn: client connection
        @param targetKey: target ID
        @param data: client data
        '''
        target = self.getTarget(0)
        if not target:
            print("target: %s " % self._targets)
            log.err('game NetCommandService: the command ' + str(targetKey) + ' not Found on service %s ' % self._name)
            return None
        if targetKey not in self.unDisplay:
            print("call method %s on service[single]" % target.__name__)
        args = (targetKey,) + args
        response = target(*args, **kw)
        return response


net_service = NetCommandService("gameService")


def net_service_handle(target):
    net_service.mapTarget(target)


GlobalObject().netfactory.addServiceChannel(net_service)


@net_service_handle
def forwarding_0(cid, _conn, data):
    """
    消息转发，将客户端发送的消息请求转发给gateserver分配处理
    :param cid:
    :param _conn:
    :param data:
    :return:
    """
    if not nodeutil.is_can_handle(servernames.GAME_GATE_NAME + "_" + str(netconst.GATE_ID)):
        # 还没有和父进程建立链接
        print "-- not connect gate server --"
        GlobalObject().netfactory.loseConnection(_conn.transport.sessionno)
        return
    dd = nodeutil.localCallRemote(servernames.GAME_GATE_NAME + "_" + str(netconst.GATE_ID), "forwarding", cid,
                                  servernames.get_wrap_did(_conn.transport.sessionno, netconst.NET_ID), data)
    return dd
