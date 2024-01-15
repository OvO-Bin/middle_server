# # coding:utf8
# '''功能测试'''
# import json
# import threading
# import time
# from random import randint
# from socket import AF_INET, SOCK_STREAM, socket
#
# from game.net.protocol.datapack import MyDataPackProtoc
# from game.util import nodeutil, stringutil
# from game.proto import LandProto_pb2, RoleProto_pb2, SoulProto_pb2, \
#     ArenaProto_pb2, EctypeProto_pb2, EventProto_pb2, StoreProto_pb2, \
#     TopnProto_pb2, TowerProto_pb2, ManuProto_pb2, \
#     BagProto_pb2, WealProto_pb2, TaskProto_pb2, ActivityProto_pb2, \
#     WorldbossProto_pb2, NotifyProto_pb2, RelaxProto_pb2, ChatProto_pb2,MilitaryProto_pb2
#
# import servernames
# from game.proto import MailProto_pb2
# from game.util.excepts import IllegalStateError
#
# # 洪全
# # _LOGIN_HOST = "192.168.1.104"
# # _WORLD_HOST = "192.168.1.104"
#
# # 内部测试用
# # _LOGIN_HOST = "192.168.1.117"
# # _WORLD_HOST = "192.168.1.117"
#
# # 外网测试 153
# # _LOGIN_HOST = "121.41.58.161"
# # _WORLD_HOST = "182.92.201.153"
#
# # 外网测试 189
# _LOGIN_HOST = "121.41.58.161"
# _WORLD_HOST = "121.41.58.161"
#
#
# LOGIN_HOST = _LOGIN_HOST + ":2016"
# WORLD_HOST = _WORLD_HOST + ":2017"
# SERVER_IDX = 3
# IS_CHAT = False  # 是否是聊天
# PORT = 12200
# BUFSIZE = 1024
# client = socket(AF_INET, SOCK_STREAM)
# chat_socket = socket(AF_INET, SOCK_STREAM)
# protoc = MyDataPackProtoc()
# cbs = {}
# RES_CMD_EXTEND = 2000
# TOKEN = 0
# SERVER_LST = []
#
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
# def sendChatData(commandId, request, cb=None):
#     global cbs
#     if cb:
#         cbs[commandId + RES_CMD_EXTEND] = cb
#     dd = request.SerializeToString()
#     if servernames.DATAPACK_MD5_ON:
#         dd = dd + stringutil.getMd5Str([dd, servernames.DATAPACK_MD5_KEY])
#     dd = protoc.pack(dd, commandId, False)
#     chat_socket.sendall(dd)
#     print "----->cmd:%d" % commandId
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
#
#
# def resolveRecvdata():
#     global handler
#     global client
#     while True:
#         data = client.recv(BUFSIZE)
#         handler.send(data)
#
# def logRes(cmd, response):
#     print "<---cmd:%d\n%s" % (cmd, response)
#
# def logHttpRes(response):
#     print "<---\n%s" % response
#
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
#     if(data["result"] == 1): # 未注册
#         data = nodeutil.http_req(LOGIN_HOST, "/ptregist", "get", request)
#         print data
#         assert (data["result"] == 0)
#         #data = nodeutil.http_req(LOGIN_HOST, "/ptlogin", "get", request)
#
#     assert(data["result"] == 0)
#     global SERVER_LST
#     SERVER_LST = nodeutil.http_req(WORLD_HOST, "/getservers2", "get")
#     logHttpRes(SERVER_LST)
#     SERVER_LST = json.loads(SERVER_LST)
#     global SERVER_IDX
#     # ser = SERVER_LST["server"][SERVER_IDX]
#     # ADDR = (ser["ip"] , ser["port"])
#     # print "Connect %s %s" % (ser["ip"] , ser["port"])
#     # 120.26.245.189
#     ADDR = ('127.0.0.1', 12015)
#     global client
#     client.connect(ADDR)
#     recTh = myThread()
#     recTh.start()
#     # 发送登录消息
#     global TOKEN
#     TOKEN = data["token"]
#     request = LandProto_pb2.LoginRequest()
#     request.token = TOKEN
#     request.platform = 0
#     request.version = "0.1.0"
#     sendData(1, request, res_land)
#
#
#
# def res_chat_land(cmd, data):
#     """
#         聊天服务器登录
#     @param cmd:
#     @param data:
#     @return:
#     """
#     print("res_chat_land -------- ")
#     response = ChatProto_pb2.LoginChatResponse()
#     response.ParseFromString(data)
#     assert (response.result == ChatProto_pb2.CHAT_SUCCESS)
#     logRes(cmd, response)
#     test_chat()
#
#
# def res_chat(cmd, data):
#     """
#         聊天数据
#     @param cmd:
#     @param data:
#     @return:
#     """
#     response = ChatProto_pb2.ChatResponse()
#     response.ParseFromString(data)
#     assert (response.result == ChatProto_pb2.CHAT_SUCCESS)
#     logRes(cmd, response)
#
#
#
# def res_land(cmd, data):
#     response = LandProto_pb2.LoginResponse()
#     response.ParseFromString(data)
#     assert(response.result == LandProto_pb2.LAND_SUCCESS)
#     # logRes(cmd, response)
#     rid = response.player.rolerId
#     if rid == -1:
#         request = LandProto_pb2.CreateRoleRequest()
#         request.nickname = response.player.user
#         request.avatarId = 1101
#         request.actcode = ""
#         request.platform = 0
#         sendData(2, request, res_createRole)
#     else:
#         request = RoleProto_pb2.RoleRequest()
#         request.rolerId = rid
#         sendData(10, request, res_getRole)
#
# def res_getRole(cmd, data):
#     response = RoleProto_pb2.RoleResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#     request = RoleProto_pb2.CacheRequest()
#     request.type = 0
#     sendData(15, request)
#     test()
#
#
# def res_createRole(cmd, data):
#     response = LandProto_pb2.CreateRoleResponse()
#     response.ParseFromString(data)
#     assert(response.result == LandProto_pb2.LAND_SUCCESS)
#     rid = response.rolerId
#     request = RoleProto_pb2.RoleRequest()
#     request.rolerId = rid
#     sendData(10, request, res_getRole)
#
# def res_Cache(cmd, data):
#     response = RoleProto_pb2.CacheResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_getarenastore(cmd, data):
#     response = ArenaProto_pb2.GetArenaStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_arenamain(cmd, data):
#     response = ArenaProto_pb2.GetArenaMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
#
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
#         time.sleep(2)
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
#         time.sleep(3)
#         request = RelaxProto_pb2.FistRequest()
#         sendData(212, request, res_fist)
# def res_getAllActState(cmd, data):
#     response = ActivityProto_pb2.GetAllActStateResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
# def res_getActBuy(cmd, data):
#     response = ActivityProto_pb2.GetActBuyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_getActTask(cmd, data):
#     response = ActivityProto_pb2.GetActTaskResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_getGroupBy(cmd, data):
#     response = ActivityProto_pb2.GetGroupBuyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_actBuy(cmd, data):
#     response = ActivityProto_pb2.ActBuyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_actAllState(cmd, data):
#     response = ActivityProto_pb2.GetAllActStateResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_act_time_exchange(cmd, data):
#     response = ActivityProto_pb2.GetTimeExchangeResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_act_time_buy(cmd, data):
#     response = ActivityProto_pb2.GetTimeBuyResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_time_buy(cmd, data):
#     response = ActivityProto_pb2.TimeBuyItemResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_act_recharge_gift(cmd, data):
#     response = ActivityProto_pb2.GetRechargeGiftResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_act_cost_gift(cmd, data):
#     response = ActivityProto_pb2.GetCostGiftResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_payment_act_state(cmd, data):
#     response = ActivityProto_pb2.GetPaymentActStateResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
#
# def res_get_daily_recharge_gift_response(cmd, data):
#     response = ActivityProto_pb2.GetDailyRechargeGiftResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_get_forces_war_main_response(cmd, data):
#     response = ActivityProto_pb2.GetForcesWarMainResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_time_exchange(cmd, data):
#     response = ActivityProto_pb2.TimeExchangeItemResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
#
# # 获取火星商店
# def res_marsStore(cmd, data):
#     response = StoreProto_pb2.GetMarsStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# #购买火星商店物品
# def res_buymarsStore(cmd, data):
#     response = StoreProto_pb2.BuyMarsStoreResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# # 修改名字
# def res_change_name(cmd, data):
#     response = RoleProto_pb2.ChangeNameResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_soul_skill_up(cmd, data):
#     response = SoulProto_pb2.SoulSkillUpResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# def res_forces_war_attack(cmd, data):
#     response = MilitaryProto_pb2.ForcesWarAttackResponse()
#     response.ParseFromString(data)
#     logRes(cmd, response)
#
# #######push############
# cbs[15 + RES_CMD_EXTEND] = res_Cache
# cbs[200 + RES_CMD_EXTEND] = res_NotifyMessage
# cbs[201 + RES_CMD_EXTEND] = res_NotifyActivity
# cbs[180 + RES_CMD_EXTEND] = res_worldbossunit
# cbs[211 + RES_CMD_EXTEND] = res_matchFist
# cbs[212 + RES_CMD_EXTEND] = res_fist
# cbs[213 + RES_CMD_EXTEND] = res_atkFist
# ###############test###########
# UNAME = "zt1019080"
# request = {}
# request["user"] = UNAME
# request["pwd"] = "111111"
# res_ptlogin(request)
#
# def test_chat():
#     # 发送聊天信息
#     request = ChatProto_pb2.ChatRequest()
#     request.type = 0
#     request.message = "1111111111111"
#     # request.toRole =
#     sendChatData(41, request, res_chat)
#     print "test_chat--------------------"
#     pass
#
# def test():
#     # request = RoleProto_pb2.UseCdkeyRequest()
#     # request.cdkey = '090102GRF51J30=q'
#     # sendData(14, request, res_usecdkey)
#     # request = ActivityProto_pb2.GetActBuyRequest()
#     # request.type= 4
#     # sendData(173, request, res_actBuy)
#
#     # request = ActivityProto_pb2.GetActTaskRequest()
#     # request.type = 8
#     # sendData(175, request, res_actBuy)
#
#     # request = ActivityProto_pb2.GetAllActStateRequest()
#     # sendData(173, request, res_actAllState)
#
#     # 获取限时兑换条目
#     # request = ActivityProto_pb2.GetTimeExchangeRequest()
#     # sendData(174, request, res_act_time_exchange)
#     # 限时兑换
#     # request = ActivityProto_pb2.TimeExchangeItemRequest()
#     # request.entry_id = 11
#     # sendData(175, request, res_time_exchange)
#     # 获取限时秒杀条目
#     # request = ActivityProto_pb2.GetTimeBuyRequest()
#     # sendData(176, request, res_act_time_buy)
#     # 限时秒杀
#     # request = ActivityProto_pb2.TimeBuyItemRequest()
#     # request.entry_id = 3
#     # sendData(177, request, res_time_buy)
#     # 充值送好礼
#     # request = ActivityProto_pb2.GetRechargeGiftRequest()
#     # sendData(178, request, res_act_recharge_gift)
#     # 消费送好礼
#     # request = ActivityProto_pb2.GetCostGiftRequest()
#     # sendData(300, request, res_act_cost_gift)
#
#     # 获取支付类活动的状态
#     # request = ActivityProto_pb2.GetPaymentActStateRequest()
#     # sendData(302, request, res_payment_act_state)
#     # 获取每日充值礼包活动条目
#     # request = ActivityProto_pb2.GetDailyRechargeGiftResponse()
#     # sendData(303, request, res_get_daily_recharge_gift_response)
#     # 军事 获取主页面
#     # request = MilitaryProto_pb2.GetForcesWarMainRequest()
#     # sendData(501, request, res_get_daily_recharge_gift_response)
#
#     request = MilitaryProto_pb2.ForcesWarAttackRequest()
#     request.id = 788639059399414721
#     request.ship_id = 1
#     request.team_id = 2
#     sendData(502, request, res_forces_war_attack)
#
#
#     """
# 2016-10-19 17:09:46+0800 [-] -----key = 788639059395219718_1
# 2016-10-19 17:09:46+0800 [-] -----ship_id_dict = {1: 788639059395219569L, 2: 788
# 639059395219669L, 3: 788639059399414565L, 4: 788639059399413904L, 5: 78863905939
# 9414033L}
# 2016-10-19 17:09:46+0800 [-] -----key = 788639059395219718_2
# 2016-10-19 17:09:46+0800 [-] -----ship_id_dict = {1: 788639059399414721L, 2: 788
# 639059403608169L, 3: 788639059403608563L, 4: 788639059403608643L, 5: 78863905940
# 7802450L}
#
#     """
#
#     """
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 5, 'team_id': 1, 'id': 788639059399414033L, 'last_hit_time': 0L}
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 1, 'team_id': 2, 'id': 788639059399414721L, 'last_hit_time': 0L}
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 2, 'team_id': 2, 'id': 788639059403608169L, 'last_hit_time': 0L}
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 3, 'team_id': 2, 'id': 788639059403608563L, 'last_hit_time': 0L}
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 4, 'team_id': 2, 'id': 788639059403608643L, 'last_hit_time': 0L}
#     2016-10-19 15:21:20+0800 [-] {'count': 5L, 'ship_id': 5, 'team_id': 2, 'id': 788639059407802450L, 'last_hit_time': 0L}
#     """
#
#     """
#     2016-10-19 15:24:26+0800 [-] ship_dat {'count': 5L, 'team_double_rate': 0L, 'bel
#     ong': 3L, 'last_hit_time': 0L, 'ship_id': 1, 'team_id': 1L, 'group_id': 78863905
#     9395219718L, 'kill_team_score': 10L, 'id': 788639059395219569L, 'self_double_rat
#     e': 0L}
#     """
#
#     # 改名
#     # request = RoleProto_pb2.ChangeNameRequest()
#     # request.nickname = u"新名字中文的2".encode("utf-8")
#     # print request.nickname
#     # sendData(17, request, res_change_name)
#
#     # 提升机娘等级
#     # request = SoulProto_pb2.SoulSkillUpRequest()
#     # request.soulId = 780593518878917187
#     # request.skillIdx = 1
#     # sendData(58, request, res_soul_skill_up)
#
#
#     # 获取竞技场界面
#     # request = ArenaProto_pb2.GetArenaMainRequest()
#     # sendData(70, request, res_marsStore)
#
#     # 发送获取火星商店 122
#     # request = StoreProto_pb2.GetMarsStoreRequest()
#     # request.type = 0
#     # sendData(122, request, res_marsStore)
#
#
#     # 发送获取火星商店 123
#     # request = StoreProto_pb2.BuyMarsStoreRequest()
#     # request.pos = 1
#     # sendData(123, request, res_buymarsStore)
#
#     pass
#
#
#
