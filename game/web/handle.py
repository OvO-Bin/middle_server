# coding:utf8
from game.db import userdb
from game.util import nodeutil, stringutil
from flask import request
from gfirefly.server.globalobject import webserviceHandle
from gfirefly.dbentrust.memclient import mclient
import servernames
import json


@webserviceHandle('/get_version_config')
def get_version_config():
    """
    盒子获取apk版本信息的的配置信息
    :return:
    """
    return json.dumps({"version": mclient.get("ApkVersion:version"), "url": mclient.get("ApkVersion:apkurl"),
                       "size": mclient.get("ApkVersion:filesize")})


@webserviceHandle('/reload_version_config')
def reload_version_config():
    """
    重新加载apk版本信息的的配置文件
    :return:
    """
    from game.db import userdb
    version_list = userdb.get_last_version_config()
    if len(version_list) > 0:
        mclient.set("ApkVersion:version", version_list[0].get("version"))
        mclient.set("ApkVersion:apkurl", version_list[0].get("apkurl"))
        mclient.set("ApkVersion:filesize", version_list[0].get("filesize"))
    else:
        print "error----------not find version info in db"
        mclient.set("ApkVersion:version", "")
        mclient.set("ApkVersion:apkurl", "")
        mclient.set("ApkVersion:filesize", "")
    return json.dumps({"version": mclient.get("ApkVersion:version"), "url": mclient.get("ApkVersion:apkurl"),
                           "size": mclient.get("ApkVersion:filesize")})


@webserviceHandle('/online_users')
def online_users():
    """
    服务器在线人数
    :return:
    """
    online = mclient.get("UserManager:online_users")
    if not online:
        online = 0
    result = "online_users: %d" % online
    print result
    return result


@webserviceHandle('/script_to_box', methods=["POST"])
def script_to_box():
    """
    把脚本发送到盒子
    post 方式，并且需要sign验证
    :return:
    """
    args = request.form
    print args

    box_id = args.get("box_id")
    script = args.get("script")
    sign = args.get("sign")
    auto_run = args.get("auto_run")
    cycle_run = args.get("cycle_run")

    if not box_id:
        return json.dumps({"result": "fail", "msg": "box_id is none"})
    if not script:
        return json.dumps({"result": "fail", "msg": "script is none"})
    if not sign:
        return json.dumps({"result": "fail", "msg": "sign is none"})
    if not auto_run:
        auto_run = "false"
    if not cycle_run:
        cycle_run = "false"

    # md5验证
    if sign != stringutil.getMd5Str(box_id+servernames.SEND_SECRET):
        print "error----sign is error"
        return json.dumps({"result": "fail", "msg": "sign is error"})

    data = {
        "box_id": box_id,
        "script": script,
        "auto_run": auto_run,
        "cycle_run": cycle_run
    }

    print script

    user_did = mclient.get("UserManager:did:" + data.get("box_id"))
    gate_name = mclient.get("UserManager:gate:" + data.get("box_id"))
    if not gate_name:
        print "the box is not open (not gate_num)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    if not user_did:
        print "the box is not open (not user_did)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    data["did"] = user_did
    nodeutil.localCallRemote(gate_name, "script_to_box", data)
    return json.dumps({"result": "success", "msg": ""})


@webserviceHandle('/script_to_many_box', methods=["POST"])
def script_to_many_box():
    """
    把脚本发送到一些盒子
    post 方式，并且需要sign验证
    :return:
    """
    args = request.form
    print args

    school = args.get("school")
    room = args.get("room")
    script = args.get("script")
    sign = args.get("sign")
    auto_run = args.get("auto_run")

    if not school:
        return json.dumps({"result": "fail", "msg": "school is none"})
    if not room:
        return json.dumps({"result": "fail", "msg": "room is none"})
    if not script:
        return json.dumps({"result": "fail", "msg": "script is none"})
    if not sign:
        return json.dumps({"result": "fail", "msg": "sign is none"})
    if not auto_run:
        auto_run = "false"

    print script

    # md5验证
    if sign != stringutil.getMd5Str(school + room + servernames.SEND_SECRET):
        print "error----sign is error"
        return json.dumps({"result": "fail", "msg": "sign is error"})

    # ({'box': u'48165465684615'}, {'box': u'48165465684616'})
    box_id_list = userdb.get_box_id_list(school, room)
    open_box_id_list = []
    close_box_id_list = []

    for box in box_id_list:
        box_id = box.get("box")
        user_did = mclient.get("UserManager:did:" + box_id)
        gate_name = mclient.get("UserManager:gate:" + box_id)
        if not gate_name:
            close_box_id_list.append(box_id)
            continue
        if not user_did:
            close_box_id_list.append(box_id)
            continue
        data = {"did": user_did, "box_id": box_id, "script": script, "auto_run": auto_run}
        nodeutil.localCallRemote(gate_name, "script_to_box", data)
        open_box_id_list.append(box_id)

    result = json.dumps({"result": "success", "msg": "", "open_box_id_list": open_box_id_list, "close_box_id_list": close_box_id_list})
    print result
    return result


@webserviceHandle('/speech_string_to_box', methods=["POST"])
def speech_string_to_box():
    """
    把脚本发送到盒子
    post 方式，并且需要sign验证
    :return:
    """
    args = request.form
    print args

    box_id = args.get("box_id")
    message = args.get("message")
    sign = args.get("sign")

    if not box_id:
        return json.dumps({"result": "fail", "msg": "box_id is none"})
    if not message:
        return json.dumps({"result": "fail", "msg": "message is none"})
    if not sign:
        return json.dumps({"result": "fail", "msg": "sign is none"})

    # md5验证
    if sign != stringutil.getMd5Str(box_id+message+servernames.SEND_SECRET):
        print "error----sign is error"
        return json.dumps({"result": "fail", "msg": "sign is error"})

    data = {
        "box_id": box_id,
        "message": message
    }

    user_did = mclient.get("UserManager:did:" + data.get("box_id"))
    gate_name = mclient.get("UserManager:gate:" + data.get("box_id"))
    if not gate_name:
        print "the box is not open (not gate_num)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    if not user_did:
        print "the box is not open (not user_did)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    data["did"] = user_did
    nodeutil.localCallRemote(gate_name, "speech_string_to_box", data)
    return json.dumps({"result": "success", "msg": ""})


@webserviceHandle('/event_up_to_box', methods=["POST"])
def event_up_to_box():
    """
    把脚本发送到盒子
    post 方式，并且需要sign验证
    :return:
    """
    args = request.form
    print args

    box_id = args.get("box_id")
    keycode = args.get("keycode")
    sign = args.get("sign")

    if not box_id:
        return json.dumps({"result": "fail", "msg": "box_id is none"})
    if not keycode:
        return json.dumps({"result": "fail", "msg": "keycode is none"})
    if not sign:
        return json.dumps({"result": "fail", "msg": "sign is none"})

    # md5验证
    if sign != stringutil.getMd5Str(box_id+keycode+servernames.SEND_SECRET):
        print "error----sign is error"
        return json.dumps({"result": "fail", "msg": "sign is error"})

    data = {
        "box_id": box_id,
        "keycode": int(keycode)
    }

    user_did = mclient.get("UserManager:did:" + data.get("box_id"))
    gate_name = mclient.get("UserManager:gate:" + data.get("box_id"))
    if not gate_name:
        print "the box is not open (not gate_num)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    if not user_did:
        print "the box is not open (not user_did)"
        return json.dumps({"result": "fail", "msg": "the box is not open"})
    data["did"] = user_did
    nodeutil.localCallRemote(gate_name, "event_up_to_box", data)
    return json.dumps({"result": "success", "msg": ""})


@webserviceHandle('/test')
def test_net():
    """
    测试
    :return:
    """

    return "success test"
