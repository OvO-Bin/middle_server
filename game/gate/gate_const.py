# coding:utf-8
from gfirefly.server.globalobject import GlobalObject

GATE_ID = 0

def gate_id():
    global GATE_ID
    if GATE_ID == 0:
        GATE_ID = int(GlobalObject().json_config.get("name").split("_")[-1])
    return GATE_ID
