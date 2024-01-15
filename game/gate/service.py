# coding:utf8
"""
处理gate里面的端口号逻辑不对外开放
"""

from gfirefly.utils.services import CommandService

gateInMethod = CommandService("gate_in")  # gate拦截并处理的指令号方法


def gate_in(target):
    gateInMethod.mapTarget(target)
