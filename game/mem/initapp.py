# coding:utf-8
import traceback
from gfirefly.server.globalobject import GlobalObject
from gfirefly.dbentrust.memclient import mclient


def call_when_stop():
    """
    服务器关闭前的处理
    """
    print("Stop Server DB....")


GlobalObject().stophandler = call_when_stop


def clean_memcache():
    """
    清理memCache缓存中的数据
    """
    print "clean_memcache"
    mclient.flush_all()


def load_last_version_config():
    """

    :return:
    """
    from game.db import userdb
    version_list = userdb.get_last_version_config()
    if len(version_list) > 0:
        version_list[0].get("version")
        version_list[0].get("apkurl")
        mclient.set("ApkVersion:version", version_list[0].get("version"))
        mclient.set("ApkVersion:apkurl", version_list[0].get("apkurl"))
        mclient.set("ApkVersion:filesize", version_list[0].get("filesize"))
    else:
        mclient.set("ApkVersion:version", "")
        mclient.set("ApkVersion:apkurl", "")
        mclient.set("ApkVersion:filesize", "")
        print "error----------not find version info in db"


def load_module():
    clean_memcache()
    try:
        import netapp
        import schedular  # 不可以移除
        load_last_version_config()
    except Exception, e:
        traceback.print_exc()

    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "DB server inited"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
