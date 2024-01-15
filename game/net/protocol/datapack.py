# coding:utf8
'''
Created on 2013-8-1

@author: lan (www.9miao.com)
'''
import struct
import time

from gfirefly.netconnect.datapack import DataPackError
from gfirefly.server.globalobject import GlobalObject
from twisted.python import log

from game.util import dateutil


class DataMock:
    '''数据包监测'''

    def __init__(self, name, nodeName):
        self.lastTm = 0
        self.name = name
        self.reqs = 0
        self.max_reqs = 0
        self.max_reqs_tm = 0
        self.nodeName = nodeName
        self.cmd = 0
        self.length = 0

    def tryresetReqs(self):
        now = time.time()
        if not dateutil.deviationEqual(self.lastTm, now):
            self.lastTm = now
            self.reqs = 0
        self.reqs += 1
        if self.reqs > self.max_reqs:
            self.max_reqs = self.reqs
            self.max_reqs_tm = self.lastTm

    def addb(self, length, cmd):
        self.cmd = cmd
        self.length = length
        self.tryresetReqs()
        self.desc()

    def desc(self):
        print("[%s]----%s>cmd:%d length:%d, 1min:{reqs:%d,max_reqs:%d,max_reqs_tm:%s}=>%dreq/s" % (
            self.nodeName, self.name, self.cmd, self.length, \
            self.reqs, self.max_reqs, \
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.max_reqs_tm)), \
            self.max_reqs / 60 \
            ))


class MyDataPackProtocol:
    """
    数据包协议
    """

    def __init__(self):
        self.__reqid = 0
        self.__cid = 0

        # XXX Test
        self.recvM = DataMock("recv", GlobalObject().json_config.get("name"))
        self.sendM = DataMock("send", GlobalObject().json_config.get("name"))

    def getHeadlength(self):
        """获取数据包的长度
        """
        return 12

    def unpack(self, dpack):
        '''解包
        '''
        try:
            ud = struct.unpack('!IhIh', dpack)
        except DataPackError, de:
            log.err(de)
            return {'result': False, 'command': 0, 'length': 0}
        length = ud[0] - 2 - 2 - 4
        command = ud[1]
        self.__reqid = ud[2]
        self.__cid = command
        errcode = ud[3]
        self.recvM.addb(length, command)  # XXX Test
        return {'result': True, 'command': command, 'length': length, 'errcode': errcode}

    def pack(self, response, command, k2=True):
        '''打包数据包
           @param k2 返回消息ID是否加2000
        '''
        errcode = 0  # 默认成功
        if isinstance(response, int):
            errcode = response
            response = str(response)
        length = response.__len__() + 4 + 2 + 2
        if k2:
            commandID = command + 2000
        else:
            commandID = command
        reqid = 0
        if self.__cid == command:
            reqid = self.__reqid

        data = struct.pack('!IhIh', length, commandID, reqid, errcode)
        data = data + response
        self.sendM.addb(length, command)
        return data
