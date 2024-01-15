# coding:utf-8
"""
gate定时操作
"""

import time
from game.gate.core.usermanager import UserManager
from game.util.timer import addTask, addTaskAt, add_hour_task, add_minute_task, add_day_task, time_method


def frequent_timer_task(at):
    """
    每10秒运行一次
    :param at:
    :return:
    """
    now = time.time()
    try:
        for session in UserManager().get_sessions():
            session.check_valid(now)
    except:
        pass


# 高频率定时器
addTask(frequent_timer_task, 10, None, 0)
