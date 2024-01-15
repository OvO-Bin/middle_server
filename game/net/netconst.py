# coding:utf-8

from gfirefly.server.globalobject import GlobalObject
import servernames

NET_ID = int(GlobalObject().json_config.get("name").split("_")[-1])
GATE_ID = NET_ID
