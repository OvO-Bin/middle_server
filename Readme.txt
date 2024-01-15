断线：1踢，2无心跳，3客户端断开

sesson_id = _conn.transport.sessionno = 10
gateid = netid = 1
wrap_did = 100000000 * netid + sesson_id = 100000010






socket端口：			web端口：
game 12000			2015     
world 12100			2017     2025
login 12200			2016     2018-2021
chat 12300          2014     2035

+++++++++特殊消息(其它消息见app\scenes\nodeapp\__init__.py)++++
心跳 999
退出 998
JOB监视 997


# 版本号规则
v1.v2.v3
v1 大版本号 非重大改动不增加
v2 每次提交审核 +1
v3 bug修改的累加...
服务器判断 v1 v2 必须相同才可以进入



++++++++++++++++++++++++++++++++++++++++++
# 因为IOS的充值返回值过长，底层代码需要做一定修改
# 否则会因为IOS返回值过长而导致断线
# 内容：
 /usr/local/lib/python2.7/site-packages/firefly-1.3.3dev_r0-py2.7.egg/gfirefly/netconnect/protoc.py

# 增加条件判断
59行 if request.__len__()< rlength and rlength > 302400:  #300k
         self.factory.connmanager.loseConnection(self.transport.sessionno)
         log.msg('Error: packet length error disconnect!! len: %s total_len: %s' % (request.__len__(), rlength))
         break

# 解决日志问题    debug模式不要修改，会出现 lose
# gfirefly里面是固定输出日志到STDOUT，需要修改成每日的
# 测试代码的时候可以修改回来
# 内容
 /usr/local/lib/python2.7/site-packages/firefly-1.3.3dev_r0-py2.7.egg/gfirefly/server/server.py
97行 # 注销并添加
# if logpath:
#     log.addObserver(loogoo(logpath))#日志处理
# log.startLogging(sys.stdout)

if logpath:
    from twisted.python.logfile import DailyLogFile
    daily_file = DailyLogFile.fromFullPath(logpath)
    log.startLogging(daily_file)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
R2Games任务计划（在线、角色信息日志）
将servernames.py copy 一份到patches一份

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
港澳台服务器因为空间问题，故移动日志至  /kx_data/logs
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
