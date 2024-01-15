# coding:utf-8
'''
Created on 2015年6月28日

@author: Administrator
'''

import time
import datetime
from gtwisted.core.greactor import GeventReactor
from twisted.python import log

from game.util import dateutil

reactor = GeventReactor()


def addTask(func, delay, at=None, errLog=1, new=True):
    '''
            添加1个间隔型定时器
            @param new 是否是创建定时器
            @param errLog 0无LOG 1控制台LOG 2error LOG
    '''
    if new and at:
        firstDelay = dateutil.differTime(at[0], at[1], at[2], delay)
    else:
        firstDelay = delay
    now = time.time()
    preAt = now + (new and firstDelay or 0) - delay
    at = new and preAt or now
    if errLog:
        lc = "run %s at[%s],pre at[%s],next at[%s]" % (
            func.__name__, time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(at)), \
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(preAt)), \
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(firstDelay + time.time())))
        log.err(lc)
    func(at)
    reactor.callLater(firstDelay, addTask, func, delay, None, errLog, False)


def addTaskAt(func, ats, idx=None, errLog=1, new=True):
    '''
            添加1个定点型定时器
            @param ats 时间点列表(由小到大)
            @param idx 当前时间列表索引
    '''
    now = time.time()
    nowTp = time.localtime(time.time())
    secs = []
    preIdx = -1
    preAt = None
    for n in range(0, len(ats)):
        tm = time.mktime((nowTp.tm_year, nowTp.tm_mon, nowTp.tm_mday, ats[n][0], ats[n][1], ats[n][2], 0, 0, 0))
        secs.append(tm)
        # 60秒误差
        if tm + 60 < now:
            preIdx = n
            preAt = tm

    ONEDAY = 86400
    if preIdx == -1:
        preIdx = len(ats) - 1
        preAt = secs[preIdx] - ONEDAY  # 昨天
    at = now
    if new:
        idx = preIdx
        at = preAt
    nextIdx = -1
    nextAt = None
    if idx == len(ats) - 1:
        nextIdx = 0
        nextAt = secs[0] + (not new and ONEDAY or 0)
    else:
        nextIdx = idx + 1
        nextAt = secs[nextIdx]
    nextAt = max(nextAt, now)
    if errLog:
        lc = "run %s at[%s],pre at[%s],next at[%s]" % (
            func.__name__, time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(at)), \
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(preAt)), \
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(nextAt)))
        log.err(lc)
    func(at)
    reactor.callLater(nextAt - now, addTaskAt, func, ats, nextIdx, errLog, False)


def getNextAtHour(ats):
    '''获得下一次整点刷新时间
                @param ats 时间点列表(由小到大)
    '''
    nowTp = time.localtime(time.time())
    h = ats[0][0]
    for t in ats:
        if t[0] > nowTp.tm_hour:
            return t[0]
    return h


def add_hour_task(func):
    """
        加入一个整点执行的方法
    """
    dis_next_hour_secs = int(3600 - time.time() % 3600) + 1
    reactor.callLater(dis_next_hour_secs, __repeat_task, 3600, func)


def add_minute_task(func):
    """
        增加分钟任务
    """
    dis_next_minute_secs = int(60 - time.time() % 60) + 1
    reactor.callLater(dis_next_minute_secs, __repeat_task, 60, func)


def add_5_minute_task(func):
    """
        15分钟迭代一次
    """
    dis_next_minute_secs = int(60 * 5 - time.time() % (60 * 5)) + 1
    reactor.callLater(dis_next_minute_secs, __repeat_task, 60 * 5, func)


# def add_time_task(func, delay):
#     """
#         增加delay时间间隔任务
#     """
#     dis_next_minute_secs = int(delay - time.time() % delay) + 1
#     reactor.callLater(dis_next_minute_secs, __repeat_task, delay, func)

def get_timer_second():
    """
        计算出到1970,01,01 0:0:0经过的秒数
    """
    return time.time() + time.mktime(time.localtime()) - time.mktime(time.gmtime())


def add_day_task(func):
    """
        每日任务
    """
    day_sec = 3600 * 24
    dis_next_day_secs = int(day_sec - get_timer_second() % day_sec) + 1
    reactor.callLater(dis_next_day_secs, __repeat_task, day_sec, func)


def add_sec_task(func, dis=0.1):
    """
        秒任务
    """
    reactor.callLater(dis, __repeat_task2, dis, func)


def __repeat_task(seconds, func, offset=1):
    """
        重复任务
    """
    # dis_next_minute_secs = int(seconds - get_timer_second() % seconds) + offset
    reactor.callLater(seconds, __repeat_task, seconds, func)
    # print("Call Function %s  Timer: %s" % (func.__name__, seconds))
    func()


def __repeat_task2(seconds, func):
    """
        高频率定时器
    """
    reactor.callLater(seconds, __repeat_task2, seconds, func)
    func()


def time_method(func):
    def time_func(*args):
        cur_time = time.time()
        result = func(*args)
        log.msg("%s: %s" % (func.__name__, time.time() - cur_time))
        return result

    return time_func


class TimerBlock:

    def __init__(self, info=''):
        self.info = info

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print self.info + ":" + str(time.time() - self.start_time)
