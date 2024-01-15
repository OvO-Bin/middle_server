# -*- coding:utf-8 -*-
import platform
import os
import json
import sys
import somepatch
from extra_master import ExtraMaster
import socket

import struct

CONFIG_NAME = ''
print(os.getcwd())

if 'Windows' in platform.system():
    CONFIG_NAME = 'config/win/config.json'
elif 'Linux' in platform.system():
    CONFIG_NAME = 'config/linux/config.json'
else:
    print("Error: Unknown platform %s " % platform.system())
    # raise StandardError()

if __name__ == "__main__":
    # if 'Linux' in platform.system():
    #     import fcntl
    #     import servernames
    
    #     with open(CONFIG_NAME, 'r') as config_file:
    #         config = json.load(config_file)
    #         sersconf = config.get('servers')
    #         # 修改配置文件到本机ip
    #         ip = servernames.OUTER_IP
    #         for sername in sersconf.keys():
    #             if sername.encode('utf-8').startswith('net'):
    #                 sersconf[sername]['host'] = ip
    #             if sername.encode('utf-8').startswith('chat_net'):
    #                 sersconf[sername]['host'] = ip
    
    #         # 修改数据库位置
    #         db_config = config.get('db')
    #         db_config['db'] = "xxjn" + str(servernames.GAME_SERVER_ID)
    
    #     with open(CONFIG_NAME, 'w') as config_file:
    #         config_file.write(json.dumps(config))

    print ("ConfigPath: %s" % CONFIG_NAME)
    sys_args = sys.argv
    print("args: %s" % sys_args)
    master = ExtraMaster()
    master.config(CONFIG_NAME, 'appmain.py')
    master.start()
