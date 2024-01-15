# coding:utf-8
"""
定时操作
"""

import json
import time

from game.util.timer import add_hour_task, add_day_task, add_minute_task


def day_time_task():
    """
        每日凌晨执行方法
    """
    pass


def hour_time_task():
    """
        小时定时
    """
    pass

# 每天执行一次
# add_day_task(day_time_task)
# # 每小时固定调用
# add_hour_task(hour_time_task)
# 每分钟固定调用
# add_minute_task(minute_time_task)
