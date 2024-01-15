# # coding:utf8
# '''压力测试'''
# import json
# import sys
# import time
# from random import randint
# from socket import AF_INET, SOCK_STREAM, socket
#
# import gevent
# from game.net.protocol.datapack import MyDataPackProtoc
# from game.util import nodeutil, stringutil
# from game.proto import LandProto_pb2, RoleProto_pb2, TopnProto_pb2, ArenaProto_pb2, \
#     TaskProto_pb2, TowerProto_pb2, WealProto_pb2, ManuProto_pb2, \
#     EventProto_pb2
#
# import servernames
# from game.proto import MailProto_pb2
# from game.util.excepts import IllegalStateError
#
# protoc = MyDataPackProtoc()
# RES_CMD_EXTEND = 2000
# def logRes(cmd, response):
#
#     print "<---cmd:%d\n%s" % (cmd, response)
# def logHttpRes(response):
#     print "<---\n%s" % response
#
#
# ###############test###########
#
#
# class Roboter(gevent.Greenlet):
#
#     def __init__(self, username, password):
#         """
#         """
#         gevent.Greenlet.__init__(self)
#         self.username = username
#         self.password = password
#         self.rid = 0
#         _LOGIN_HOST = "192.168.1.128"
# #         _LOGIN_HOST = "120.26.56.18"
# #         _LOGIN_HOST = "120.26.245.189"
#         _WORLD_HOST = "192.168.1.128"
# #         _WORLD_HOST = "120.26.245.189"
#         self.LOGIN_HOST = _LOGIN_HOST + ":2016"
#         self.WORLD_HOST = _WORLD_HOST + ":2017"
#         self.endTm = time.time() + 30 * 60
#         self.__serIdx = 0
#         self.PORT = 12200
#         self.BUFSIZE = 1024
#         self.ADDR = None
#         self.cbs = {}
#         self.client = socket(AF_INET, SOCK_STREAM)
#         self.buff = ""
#         self.load()
#
#     def load(self):
#         """
#         """
#         pass
#     def sendData(self, commandId, request, cb=None):
#         if cb:
#             self.cbs[commandId + RES_CMD_EXTEND] = cb
#         dd = request.SerializeToString()
#         if servernames.DATAPACK_MD5_ON:
#             dd = dd + stringutil.getMd5Str([dd, servernames.DATAPACK_MD5_KEY])
#         dd = protoc.pack(dd, commandId, False)
#         self.client.sendall(dd)
#         if cb:
#             self.resolveRecvdata()
#
#     def connect(self):
#         """建立连接
#         """
#         self.client.connect(self.ADDR)
#
#     def res_ptlogin(self, request):
#         data = nodeutil.http_req(self.LOGIN_HOST, "/ptlogin", "get", request)
#         logHttpRes(data)
#         data = json.loads(data)
#         assert(data["result"] == 0)
#         data2 = nodeutil.http_req(self.WORLD_HOST, "/getservers", "get")
#         logHttpRes(data2)
#         data2 = json.loads(data2)
#         ser = data2["server"][self.__serIdx]
#         self.ADDR = (ser["ip"] , ser["port"])
#
#         self.connect()
#         request = LandProto_pb2.LoginRequest()
#         request.token = data["token"]
#         self.sendData(1, request, self.res_land)
#     def res_land(self, cmd, data):
#         response = LandProto_pb2.LoginResponse()
#         response.ParseFromString(data)
#         assert(response.result == LandProto_pb2.LAND_SUCCESS)
#         logRes(cmd, response)
#         self.rid = response.player.rolerId
#         if  self.rid == -1:
#             request = LandProto_pb2.CreateRoleRequest()
#             request.nickname = response.player.user
#             request.avatarId = 1101
#             self.sendData(2, request, self.res_createRole)
#         else:
#             request = RoleProto_pb2.RoleRequest()
#             request.rolerId = self.rid
#             self.sendData(10, request, self.res_getRole)
#     def res_getRole(self, cmd, data):
#         response = RoleProto_pb2.RoleResponse()
#         response.ParseFromString(data)
#         logRes(cmd, response)
#         request = RoleProto_pb2.CacheRequest()
#         request.type = 0
#         self.sendData(15, request)
#
#     def res_createRole(self, cmd, data):
#         response = LandProto_pb2.CreateRoleResponse()
#         response.ParseFromString(data)
#         assert(response.result == LandProto_pb2.LAND_SUCCESS)
#         self.rid = response.rolerId
#         request = RoleProto_pb2.RoleRequest()
#         request.rolerId = self.rid
#         self.sendData(10, request, self.res_getRole)
#     def res_gettopn(self, cmd, data):
#         res = TopnProto_pb2.GetTopnResponse()
#         res.ParseFromString(data)
#         logRes(cmd, res)
#     def res_getarena(self, cmd, data):
#         res = ArenaProto_pb2.GetArenaMainResponse()
#         res.ParseFromString(data)
#         logRes(cmd, res)
#     def res_gettask(self, cmd, data):
#         response = TaskProto_pb2.GetTaskListResponse()
#         response.ParseFromString(data)
#         logRes(cmd, response)
#     def getTopn(self):
#         ts = ['1', '2', '3', '4', '5', '6']
#         req = TopnProto_pb2.GetTopnRequest()
#         req.type = ts[randint(0, len(ts) - 1)]
#         self.sendData(160, req)
#     def getArena(self):
#         req = ArenaProto_pb2.GetArenaMainRequest()
#         self.sendData(70, req)
#     def getMails(self):
#         req = MailProto_pb2.GetMailListRequest()
#         self.sendData(110, req)
#     def getTasks(self):
#         request = TaskProto_pb2.GetTaskListRequest()
#         request.type = 0
#         self.sendData(140, request)
#     def getTowers(self):
#         request = TowerProto_pb2.GetTowerMainRequest()
#         self.sendData(90, request)
#     def getBlackstore(self):
#         request = WealProto_pb2.GetBlackStoreRequest()
#         request.type = 0
#         self.sendData(131, request)
#     def getManuMain(self):
#         request = ManuProto_pb2.GetManuRequest()
#         self.sendData(23, request)
#     def getEventMain(self):
#         request = EventProto_pb2.GetEventMainRequest()
#         self.sendData(80, request)
#     def action(self):
#         """机器人行动
#         """
#         self.tests[randint(0, len(self.tests) - 1)]()
#     def resolveRecvdata(self, m=1):
#         gevent.sleep(m)
#         length = protoc.getHeadlength()
#         data = self.client.recv(self.BUFSIZE)
#         self.buff += data
#         unpackdata = protoc.unpack(self.buff[:length])
#         if not unpackdata.get('result'):
#             print('illegal data package --')
#         command = unpackdata.get('command')
#         rlength = unpackdata.get('length')
#         request = self.buff[length:length + rlength]
#         if request.__len__() < rlength:
#             print('some data lose')
#         self.buff = self.buff[length + rlength:]
#         errcode = unpackdata.get("errcode")
#         if errcode != 0:
#             print "--------->cmd:%d,errcode:%d" % (command, errcode)
#         if self.cbs.has_key(command):
#             if servernames.DATAPACK_MD5_ON:
#                 dmd5 = request[-servernames.DATAPACK_MD5_LEN:]
#                 request = request[0:len(request) - servernames.DATAPACK_MD5_LEN]
#                 if not stringutil.equalsIgnoreCase(dmd5, stringutil.getMd5Str([request, servernames.DATAPACK_MD5_KEY])):
#                     raise IllegalStateError(["illegal data pack md5"])
#             self.cbs[command](command, request)
#     def getArenaStore(self):
#         request = ArenaProto_pb2.GetArenaStoreRequest()
#         request.type = 0
#         self.sendData(75, request)
#     def manu(self):
#         request = ManuProto_pb2.ManuRequest()
#         request.manuId = 2
#         request.num = 10
#         self.sendData(20, request)
#     def _run(self):
#         self.ptlogin()
# #         self.getArena()
# #         self.tests = [self.getArena, self.getTasks, self.getTopn, self.getMails, self.getBlackstore, \
# #                       self.getRpts, self.getManuMain, self.getEventMain, self.getTowers, self.getArenaStore]
#         self.tests = [self.manu]
#         times = sys.maxint
#         curs = 0
#         while curs < times and time.time() <= self.endTm:
#             gevent.sleep(2)
#             self.action()
#             curs += 1
#         gevent.sleep(60)
#         self.client.close()
#     def ptlogin(self):
#         """登陆
#         """
#         request = {}
#         request["user"] = self.username
#         request["pwd"] = self.password
#         self.res_ptlogin(request)
#
#
# if __name__ == "__main__":
#     rotlist = []
#     for i in range(1, 1000):
#         rot = Roboter("test%03d" % i, "test")
#         rot.start()
#         rotlist.append(rot)
#     gevent.joinall(rotlist)
#
#
#
