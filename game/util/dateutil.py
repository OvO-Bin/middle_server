# coding:utf-8
'''
Created on 2015年6月26日

@author: Administrator
'''
import calendar
import datetime
from math import ceil
import time


def truncateTm(tm, h):
    '''将时间tm的时分秒设置成h'''
    tm = time.localtime(tm)
    return time.mktime((tm.tm_year, tm.tm_mon, tm.tm_mday, h[0], h[1], h[2], 0, 0, 0))


def getHMS(tm):
    '''获得时间tm的时分秒'''
    tm = time.localtime(tm)
    return (tm.tm_hour, tm.tm_min, tm.tm_sec)


def strToSec(s, fmt):
    '''将fmt格式的日期字符串转成时间戳(秒)'''
    sm = time.strptime(s, fmt)
    return time.mktime((sm.tm_year, sm.tm_mon, sm.tm_mday, sm.tm_hour, sm.tm_min, sm.tm_sec, 0, 0, 0))


def isSameDayOfReset(a, now, h):
    '''a,b是否属于同一天
        @param h 以每天的h点为当天的起始时间
    '''
    nowTp = time.localtime(now)
    hTm = time.mktime((nowTp.tm_year, nowTp.tm_mon, nowTp.tm_mday, h[0], h[1], h[2], 0, 0, 0))
    if now < hTm:
        return time.mktime((nowTp.tm_year, nowTp.tm_mon, nowTp.tm_mday - 1, h[0], h[1], h[2], 0, 0, 0)) <= a < hTm
    else:
        return hTm <= a < time.mktime((nowTp.tm_year, nowTp.tm_mon, nowTp.tm_mday + 1, h[0], h[1], h[2], 0, 0, 0))


def deviationEqual(a, b, sec=60):
    '''
    在误差范围内也认为相等
    @param sec 误差秒数
    '''
    return abs(a - b) <= sec


def differDays(a, b):
    '''两个时间之间相差的天数'''
    return int(ceil(abs(a - b) / (24 * 60 * 60)))


def differTime(h, m, s, interval, now=None):
    '''到达预设时间执行函数  return与指定时间戳相差的秒数
    @param h,m,s: int 预设 时,分,秒 
    @param interval 间隔秒数
    return int 秒数
    '''
    if not now:
        now = time.time()
    al = time.localtime(now)
    hour = al.tm_hour
    minute = al.tm_min
    second = al.tm_sec
    old = h * 3600 + m * 60 + s  # 预设时间 据0点得秒数
    young = hour * 3600 + minute * 60 + second  # 当前时间据0点得秒数

    if old >= young:
        return old - young
    else:
        n = 1
        while old + interval * n < young:
            n += 1
        return n * interval - (young - old)


def get_pre_task_time(h, m, s):
    """
    获取上次任务的时间，按照天计算的
    :param h:
    :param m:
    :param s:
    :param interval: 间隔秒数
    :return:
    """
    now = time.time()
    local_now = time.localtime()
    pre_time = time.mktime((local_now.tm_year, local_now.tm_mon, local_now.tm_mday, h, m, s, 0, 0, 0))
    if now >= pre_time:
        return pre_time
    else:
        return pre_time - 86400


def beforeNow(h, m, s):
    '''比较时间是否早于现在
    @param h,m,s: int 预设 时,分,秒 
    return int 秒数
    '''
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    old = h * 3600 + m * 60 + s  # 预设时间 据0点得秒数
    young = hour * 3600 + minute * 60 + second  # 当前时间据0点得秒数    
    return old < young


def monthdays(tyear=None, tmon=None):
    '''该月天数'''
    al = time.localtime()
    if not tyear:
        tyear = al.tm_year
    if not tmon:
        tmon = al.tm_mon
    return calendar.monthrange(tyear, tmon)[1]


def is_same_week(time_1, time_2):
    """
        判断是同一周
    """
    time_1_tp = time.localtime(time_1)
    time_2_tp = time.localtime(time_2)

    if abs(time_1 - time_2) > 604800:  # 3600*24*7 防止跨年的情况出现
        return False
    if abs(time_1_tp.tm_yday - time_2_tp.tm_yday) > 6:
        return False
    if time_1_tp.tm_yday >= time_2_tp.tm_yday and time_1_tp.tm_wday >= time_2_tp.tm_wday:
        return True
    if time_2_tp.tm_yday >= time_1_tp.tm_yday and time_2_tp.tm_wday >= time_1_tp.tm_wday:
        return True
    return False


def is_same_month(time_1, time_2):
    """
        同一月
    """
    time_1_tp = time.localtime(time_1)
    time_2_tp = time.localtime(time_2)
    return time_1_tp.tm_mon == time_2_tp.tm_mon and time_1_tp.tm_year == time_2_tp.tm_year


def is_same_day(time_1, time_2):
    """
        同一日
    """
    time_1_tp = time.localtime(time_1)
    time_2_tp = time.localtime(time_2)
    return time_1_tp.tm_mday == time_2_tp.tm_mday and time_1_tp.tm_mon == time_2_tp.tm_mon and time_1_tp.tm_year == time_2_tp.tm_year


def is_same_hour(time_1, time_2):
    """
        同小时
    """
    time_1_tp = time.localtime(time_1)
    time_2_tp = time.localtime(time_2)
    return time_1_tp.tm_hour == time_2_tp.tm_hour and time_1_tp.tm_mday == time_2_tp.tm_mday and time_1_tp.tm_mon == time_2_tp.tm_mon and time_1_tp.tm_year == time_2_tp.tm_year


def day_range(time_1, time_2):
    """
    计算两个时间点之间经过了多少天
    time_2 需要 大于 time_1
    :param time_1:
    :param time_2:
    :return:
    """
    # 判断是否是同一天
    time_1_tp = time.localtime(time_1)
    time_2_tp = time.localtime(time_2)
    if time_1_tp.tm_mday == time_2_tp.tm_mday and time_1_tp.tm_mon == time_2_tp.tm_mon and time_1_tp.tm_year == time_2_tp.tm_year:
        # 同一日
        return 1
    else:
        time_1_zero = time.mktime((time_1_tp.tm_year, time_1_tp.tm_mon, time_1_tp.tm_mday, 0, 0, 0, 0, 0, 0))
        time_2_zero = time.mktime((time_2_tp.tm_year, time_2_tp.tm_mon, time_2_tp.tm_mday, 0, 0, 0, 0, 0, 0))
        return (time_2_zero - time_1_zero) / 86400 + 1
