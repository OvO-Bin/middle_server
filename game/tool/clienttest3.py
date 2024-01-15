# # coding:utf8
# '''功能测试'''
# import json
# import threading
# from random import randint
# from socket import AF_INET, SOCK_STREAM, socket
#
# from game.net.protocol.datapack import MyDataPackProtoc
# from game.util import nodeutil, stringutil
# from game.proto import LandProto_pb2, RoleProto_pb2, SoulProto_pb2, \
#     ArenaProto_pb2, EctypeProto_pb2, EventProto_pb2, StoreProto_pb2, \
#     TopnProto_pb2, TowerProto_pb2, ManuProto_pb2, \
#     BagProto_pb2, WealProto_pb2, TaskProto_pb2, ActivityProto_pb2, \
#     WorldbossProto_pb2, NotifyProto_pb2, RelaxProto_pb2
#
# import servernames
# from game.proto import MailProto_pb2
# from game.util.excepts import IllegalStateError
#
# _LOGIN_HOST = "192.168.1.128"
# # _LOGIN_HOST = "120.26.56.18"
# # _LOGIN_HOST = "120.26.245.189"
# # _WORLD_HOST = "120.26.245.189"
# _WORLD_HOST = "192.168.1.128"
# LOGIN_HOST = _LOGIN_HOST + ":2016"
# WORLD_HOST = _WORLD_HOST + ":2017"
# SERVER_IDX = 0
# PORT = 12200
# BUFSIZE = 1024
# client = socket(AF_INET, SOCK_STREAM)
# protoc = MyDataPackProtoc()
# cbs = {}
# RES_CMD_EXTEND = 2000
# def sendData(commandId, request, cb=None):
#     global cbs
#     if cb:
#         cbs[commandId + RES_CMD_EXTEND] = cb
#     dd = request.SerializeToString()
#     if servernames.DATAPACK_MD5_ON:
#         dd = dd + stringutil.getMd5Str([dd, servernames.DATAPACK_MD5_KEY])
#     dd = protoc.pack(dd, commandId, False)
#     client.sendall(dd)
#     print "----->cmd:%d" % commandId
#
#
# buff = ""
# def listenRes():
#     length = protoc.getHeadlength()
#     global buff
#     global cbs
#     while True:
#             data = yield
#             buff += data
#             while buff.__len__() >= length:
#                 unpackdata = protoc.unpack(buff[:length])
#                 if not unpackdata.get('result'):
#                     print('illegal data package --')
#                     break
#                 command = unpackdata.get('command')
#                 rlength = unpackdata.get('length')
#                 request = buff[length:length + rlength]
#                 if request.__len__() < rlength:
#                     print('some data lose')
#                     break
#                 buff = buff[length + rlength:]
#                 errcode = unpackdata.get("errcode")
#                 if errcode != 0:
#                     print "--------->cmd:%d,errcode:%d" % (command, errcode)
#                     break
#                 if cbs.has_key(command):
#                     if servernames.DATAPACK_MD5_ON:
#                         dmd5 = request[-servernames.DATAPACK_MD5_LEN:]
#                         request = request[0:len(request) - servernames.DATAPACK_MD5_LEN]
#                         if not stringutil.equalsIgnoreCase(dmd5, stringutil.getMd5Str([request, servernames.DATAPACK_MD5_KEY])):
#                             raise IllegalStateError(["illegal data pack md5"])
#                     cbs[command](command, request)
# handler = listenRes()
# handler.next()
# def resolveRecvdata():
#     global handler
#     global client
#     while True:
#             data = client.recv(BUFSIZE)
#             handler.send(data)
#
#
# def logRes(cmd, response):
#     print "<---cmd:%d\n%s" % (cmd, response)
# def logHttpRes(response):
#     print "<---\n%s" % response
# class myThread (threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         resolveRecvdata()
# #########deal
# rid = 0
# def res_ptlogin(request):
#     data = nodeutil.http_req(LOGIN_HOST, "/ptlogin", "get", request)
#     logHttpRes(data)
#     data = json.loads(data)
#     assert(data["result"] == 0)
#     data2 = nodeutil.http_req(WORLD_HOST, "/getservers", "get")
#     logHttpRes(data2)
#     data2 = json.loads(data2)
#     global SERVER_IDX
#     ser = data2["server"][SERVER_IDX]
#     ADDR = (ser["ip"] , ser["port"])
#     global client
#     client.connect(ADDR)
#     recTh = myThread()
#     recTh.start()
#
#     request = LandProto_pb2.LoginRequest()
#     request.token = data["token"]
#     sendData(1, request, res_land)
# def res_land(cmd, data):
#     response = LandProto_pb2.LoginResponse()
#     response.ParseFromString(data)
#     assert(response.result == LandProto_pb2.LAND_SUCCESS)
#     logRes(cmd, response)
#     rid = response.player.rolerId
#     if  rid == -1:
#         request = LandProto_pb2.CreateRoleRequest()
#         request.nickname = response.player.user
#         request.avatarId = 1101
#         sendData(2, request, res_createRole)
#     else:
#         request = RoleProto_pb2.RoleRequest()
#         request.rolerId = rid
#         sendData(10, request, res_getRole)
# def res_getRole(cmd, data):
#     response = RoleProto_pb2.RoleResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#     request = RoleProto_pb2.CacheRequest()
#     request.type = 0
#     sendData(15, request)
#     test()
#
# def res_createRole(cmd, data):
#     response = LandProto_pb2.CreateRoleResponse()
#     response.ParseFromString(data)
#     assert(response.result == LandProto_pb2.LAND_SUCCESS)
#     rid = response.rolerId
#     request = RoleProto_pb2.RoleRequest()
#     request.rolerId = rid
#     sendData(10, request, res_getRole)
# def res_Cache(cmd, data):
#     response = RoleProto_pb2.CacheResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getarenastore(cmd, data):
#     response = ArenaProto_pb2.GetArenaStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_arenamain(cmd, data):
#     response = ArenaProto_pb2.GetArenaMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_atkarena(cmd, data):
#     response = ArenaProto_pb2.AtkArenaResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
#     request = EctypeProto_pb2.BattleFinishRequest()
#     request.type = EctypeProto_pb2.BATTLE_ARENA
#     request.leftSeconds = 2
#     sendData(62, request, res_finishbattle)
# def res_finishbattle(cmd, data):
#     response = EctypeProto_pb2.BattleFinishResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_eventmain(cmd, data):
#     response = EventProto_pb2.GetEventMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_usecdkey(cmd, data):
#     response = RoleProto_pb2.UseCdkeyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_readmail(cmd, data):
#     response = MailProto_pb2.ReadMailResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_gettopn(cmd, data):
#     response = TopnProto_pb2.GetTopnResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_gettower(cmd, data):
#     response = TowerProto_pb2.GetTowerMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_useitem(cmd, data):
#     response = BagProto_pb2.UseItemResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_strengsoul(cmd, data):
#     response = SoulProto_pb2.StrengSoulResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_remouldsoul(cmd, data):
#     response = SoulProto_pb2.RemouldSoulResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_gettowerstore(cmd, data):
#     response = TowerProto_pb2.GetTowerStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getblackstore(cmd, data):
#     response = WealProto_pb2.GetBlackStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_buyvipgift(cmd, data):
#     response = StoreProto_pb2.BuyVipGiftResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buyarenastore(cmd, data):
#     response = ArenaProto_pb2.BuyArenaStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buyblackstore(cmd, data):
#     response = WealProto_pb2.BuyBlackStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buytowerstore(cmd, data):
#     response = TowerProto_pb2.BuyTowerStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_createsoul(cmd, data):
#     response = SoulProto_pb2.CreateSoulResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_upsoullv(cmd, data):
#     response = SoulProto_pb2.UpSoulLvResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_upequiplv(cmd, data):
#     response = SoulProto_pb2.UpEquipLvResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getmanu(cmd, data):
#     response = ManuProto_pb2.GetManuResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_manu(cmd, data):
#     response = ManuProto_pb2.ManuResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_atkectype(cmd, data):
#     response = EctypeProto_pb2.AtkEctypeResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getFreeEnergy(cmd, data):
#     response = WealProto_pb2.GetFreeEnergyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_recFreeEnergy(cmd, data):
#     response = WealProto_pb2.RecFreeEnergyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_clearcd(cmd, data):
#     response = ArenaProto_pb2.ClearArenaAtkCdResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buyatknum(cmd, data):
#     response = ArenaProto_pb2.BuyArenaAtkNumResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getheadframes(cmd, data):
#     response = RoleProto_pb2.GetHeadframesResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_sweep(cmd, data):
#     response = EctypeProto_pb2.SweepEctypeResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_gettowermain(cmd, data):
#     response = TowerProto_pb2.GetTowerMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_atktower(cmd, data):
#     response = TowerProto_pb2.AtkTowerResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_rectowerreward(cmd, data):
#     response = TowerProto_pb2.RecTowerRewardResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_rectowerevent(cmd, data):
#     response = TowerProto_pb2.RecTowerEventResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_atkevent(cmd, data):
#     response = EventProto_pb2.AtkEventResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_sweepevent(cmd, data):
#     response = EventProto_pb2.SweepEventResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buyeventatknum(cmd, data):
#     response = EventProto_pb2.BuyEventAtkNumResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_signin(cmd, data):
#     response = WealProto_pb2.SignInResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_buygrow(cmd, data):
#     response = WealProto_pb2.BuyGrowFundResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_recgrow(cmd, data):
#     response = WealProto_pb2.RecGrowFundResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_recchapterreward(cmd, data):
#     response = EctypeProto_pb2.RecChapterStarRewardResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_gettask(cmd, data):
#     response = TaskProto_pb2.GetTaskListResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_rectask(cmd, data):
#     response = TaskProto_pb2.RecTaskResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_fashionSoul(cmd, data):
#     response = SoulProto_pb2.FashionSoulResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_changeAvatar(cmd, data):
#     response = RoleProto_pb2.ChangeAvatarResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getDial(cmd, data):
#     response = ActivityProto_pb2.GetDialResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_dial(cmd, data):
#     response = ActivityProto_pb2.DialResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_reconline(cmd, data):
#     response = ActivityProto_pb2.RecOnlineGiftResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_saveguidestep(cmd, data):
#     response = RoleProto_pb2.SaveGuideStepResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_worldbossunit(cmd, data):
#     response = WorldbossProto_pb2.WorldbossUnit()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_NotifyMessage(cmd, data):
#     response = NotifyProto_pb2.NotifyMessage()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_NotifyActivity(cmd, data):
#     response = NotifyProto_pb2.NotifyActivity()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getBossMain(cmd, data):
#     response = WorldbossProto_pb2.GetBossMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_bossInspire(cmd, data):
#     response = WorldbossProto_pb2.InspireResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_peek(cmd, data):
#     response = WorldbossProto_pb2.PeekResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_buypeek(cmd, data):
#     response = WorldbossProto_pb2.BuyPeekNumResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_clearReviveCd(cmd, data):
#     response = WorldbossProto_pb2.ClearReviveCdResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_autorevive(cmd, data):
#     response = WorldbossProto_pb2.AutoReviveResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_autoai(cmd, data):
#     response = WorldbossProto_pb2.AutoAiResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_exitboss(cmd, data):
#     response = WorldbossProto_pb2.ExitResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_pickprize(cmd, data):
#     response = WorldbossProto_pb2.PickPrizeResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getFistInfo(cmd, data):
#     response = RelaxProto_pb2.GetFistInfoResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_matchFist(cmd, data):
#     response = RelaxProto_pb2.MatchFistResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#     if response.result == RelaxProto_pb2.RELAX_FIST_MATCHED:
#         request = RelaxProto_pb2.FistRequest()
#         sendData(212, request, res_fist)
# def res_fist(cmd, data):
#     response = RelaxProto_pb2.FistResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#     if response.result == RelaxProto_pb2.RELAX_FIST_ROUND:
#         request = RelaxProto_pb2.AtkFistRequest()
#         request.type = randint(0, 1)
#         sendData(213, request, res_atkFist)
#     elif response.result == RelaxProto_pb2.RELAX_FIST_END:
#         print "----fist---end-----"
# def res_atkFist(cmd, data):
#     response = RelaxProto_pb2.AtkFistResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#     if response.result == RelaxProto_pb2.RELAX_FIST_ATKED:
#         request = RelaxProto_pb2.FistRequest()
#         sendData(212, request, res_fist)
# #######push############
# cbs[15 + RES_CMD_EXTEND] = res_Cache
# cbs[200 + RES_CMD_EXTEND] = res_NotifyMessage
# cbs[201 + RES_CMD_EXTEND] = res_NotifyActivity
# cbs[180 + RES_CMD_EXTEND] = res_worldbossunit
# cbs[211 + RES_CMD_EXTEND] = res_matchFist
# cbs[212 + RES_CMD_EXTEND] = res_fist
# cbs[213 + RES_CMD_EXTEND] = res_atkFist
# ###############test###########
# UNAME = "ylc2"
# request = {}
# request["user"] = UNAME
# request["pwd"] = "ylc"
# res_ptlogin(request)
# def test():
# #     request=RelaxProto_pb2.GetFistInfoRequest()
# #     sendData(210, request, res_getFistInfo)
#     request = RelaxProto_pb2.MatchFistRequest()
#     request.type = 0
#     request.matrix = '737897069422842408,738609353824670048,738609353937916802'
#     sendData(211, request, res_matchFist)
#     pass
#
#
#
