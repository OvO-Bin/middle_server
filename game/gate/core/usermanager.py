# coding:utf8
import time

import servernames
from game.gate.netapp import gatetonethandle
from gfirefly.dbentrust.memclient import mclient
from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.singleton import Singleton
from twisted.python import log

from game.util import nodeutil

SESSION_VALID_TM = 600  # 玩家N秒不操作断开socket连接
HEARTBEAT_VALID_TM = 180  # N秒收不到心跳断开socket连接 必须大于一分钟心跳包时间


class SessionOverdate(object):
    """
    session有效期验证，用心跳包进行判断，长时间数据，断开连接
    """

    def __init__(self, did):
        self.did = did
        self.last_beat_tm = time.time()  # 最近一次心跳时间
        self.last_opt_tm = self.last_beat_tm  # 玩家最近一次操作时间
        self.__opt_overdate = self.last_opt_tm + SESSION_VALID_TM  # 操作有效时间
        self.__heartbeat_overdate = self.last_beat_tm + HEARTBEAT_VALID_TM  # 心跳有效时间

    def check_valid(self, now):
        if self.last_beat_tm + HEARTBEAT_VALID_TM >= self.__heartbeat_overdate:  # 延长心跳有效时间
            self.__heartbeat_overdate = now + HEARTBEAT_VALID_TM
        # if self.last_opt_tm + SESSION_VALID_TM >= self.__opt_overdate:  # 延长session有效时间
        #     self.__opt_overdate = now + SESSION_VALID_TM
        if now >= self.__heartbeat_overdate:  # 断线 这里不做操作判断 and now >= self.__opt_overdate
            # session_id = servernames.get_session_id(self.did)
            # is_net_has_connection = GlobalObject().netfactory.getConnectionByID(session_id) #这个需要在net中调用，在gate调用会导致下面的代码不执行
            print ">>>>session close handle<<<<"
            self.session_net_conn_lost() # 通知客户端账号掉线  #如果已连接的情况下，会导致gatefromchildhandle.net_conn_lost也执行一次，但是没有关系
            print ">>>>close session did(%s) at now(%s),lastBeatTm(%s)" % (self.did, now, self.last_beat_tm)
            return

    def session_net_conn_lost(self):
        """
        账号掉线时的处理
        :return:
        """
        user = UserManager().get_user_by_did(self.did)
        if not user:
            print "user = None, did=%s" % self.did
            return
        UserManager().kick(user.box_id)


class UserManager(object):
    """
    账号管理类
    """
    __metaclass__ = Singleton

    def __init__(self):
        self._users_dict = {}  # key:账号,value User类
        self._did2box_id = {}  # key:did,value 账号
        self._did2session = {}  # key:did ,value:SessionOverdate

    def get_sessions(self):
        return self._did2session.values()

    def check_online_num(self, n):
        """
        检查在线人数
        :param did:
        :param n:
        :return:
        """
        online = mclient.get("UserManager:online_users")
        if not online:
            online = 0
        online = max(0, online + n)
        mclient.set("UserManager:online_users", online)
        print "UserManager:online_users(%d)" % online

    def add_user(self, user):
        """
        添加账号类
        :param user:
        :return:
        """
        self.kick(user.box_id)
        self._did2box_id[user.did] = user.box_id
        self._users_dict[user.box_id] = user
        self._did2session[user.did] = SessionOverdate(user.did)
        mclient.set("UserManager:did:" + user.box_id, user.did)
        mclient.set("UserManager:gate:" + user.box_id, GlobalObject().json_config.get("name"))
        self.check_online_num(1)

    def opt(self, did):
        """
        记录当前操作时间
        :param did:
        :return:
        """
        so = self._did2session.get(did)
        if so:
            so.last_opt_tm = time.time()

    def heartbeat(self, did):
        """
        记录当前心跳时间
        :param did:
        :return:
        """
        so = self._did2session.get(did)
        if so:
            so.last_beat_tm = time.time()

    def kick(self, box_id):
        """

        :param box_id:
        :return:
        """
        log.err("kick user[%s] start" % box_id)
        old_did = mclient.get("UserManager:did:" + box_id)
        old_gate = mclient.get("UserManager:gate:" + box_id)

        if old_gate:
            if old_gate == GlobalObject().json_config.get("name"):
                # 在同一进程中清理数据
                self.del_user(box_id, old_did)
            else:
                # 其他进程清除数据
                nodeutil.localCallRemote(servernames.GAME_DBFRONT_NAME, "kick_user", box_id, old_gate)
        if old_did:
            gatetonethandle.close_client(old_did)  # 通知客户端账号掉线  did
            log.err("kick user[%s,%d]" % (box_id, old_did))

    def del_user(self, box_id, old_did):
        """
        删除账号
        :param box_id:
        :param old_did:
        :return:
        """
        if self._users_dict.has_key(box_id):
            user = self._users_dict[box_id]
            # print("user.did %s  oldDid %s" % (user.did, oldDid))
            if user.did == old_did:
                print "clear user dict data"
                del self._users_dict[box_id]
                del self._did2box_id[user.did]
                del self._did2session[user.did]
        did = mclient.get("UserManager:did:" + box_id)
        if did == old_did:
            print "clear user memcache data"
            mclient.delete("UserManager:did:" + box_id)
            mclient.delete("UserManager:gate:" + box_id)
            self.check_online_num(-1)

    def get_user_by_did(self, did):
        """
        根据动态id获取账号实例
        :param did:
        :return:
        """
        # print("============getUserBydid: did %s  " % (did, ))
        if self._did2box_id.has_key(did):
            box_id = self._did2box_id[did]
            return self._users_dict.get(box_id)
        return None
