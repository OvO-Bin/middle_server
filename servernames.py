# -*- coding:utf-8 -*-

# 是否是调试模式
DEBUG_MODE = True
# 本机IP
OUTER_IP = ""  # "154.8.173.52"没有用
# 世界服务器 数据库地址
SERVER_WORLD_HOST = "127.0.0.1:3306"
# 游戏配置表: 用户名
CONFIG_SQL_ACC = "root"
# 游戏配置表: 密码
CONFIG_SQL_PAS = "wokejiaoyu668"
# 游戏配置表: URL
CONFIG_SQL_HOST = "127.0.0.1"
CONFIG_SQL_DB = "woke"

LOGIN_SECRET = "wokejiaoyu" # 登录时用的
SEND_SECRET = "wokejiaoyuboxsecret" # 发送消息时用

# 包加密
# DATAPACK_MD5_LEN = 32  # md5长度
# DATAPACK_MD5_KEY = "wokejiaoyu"  # 通讯协议的md5密钥
# DATAPACK_MD5_ON = False  # 是否开启通讯协议的MD5加密

GAME_GATE_NUMS = 5  # 游戏服的GATE数量
GAME_GATE_NAME = "gate"
GAME_DBFRONT_NAME = "dbfront"
GAME_NET_NAME = "net"
GAME_WEB_NAME = "web"

# 拆分玩家到对应的 net 原则
WRAP_DID_BASE = 100000000


def get_net_id(wrap_did):
    return wrap_did / WRAP_DID_BASE


def get_session_id(wrap_did):
    return wrap_did % WRAP_DID_BASE


def get_wrap_did(sesson_id, net_id):
    return WRAP_DID_BASE * net_id + sesson_id
