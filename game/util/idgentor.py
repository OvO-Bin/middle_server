# coding:utf-8
'''
Created on 2015年6月27日

@author: Administrator
'''
import os
from random import randint
import time


def genId(serverId, ignore_lst=None):
    '''id构成=42位时间戳+5位服务器ID+5位进程ID+12位随机数'''
    serverBits = 5L
    processBits = 5L
    sequenceBits = 12L
    processShift = sequenceBits
    serverShift = sequenceBits + processBits
    timestampLeftShift = sequenceBits + processBits + serverBits
    twepoch = 1288834974657L
    processId = os.getpid()
    generate_id = ((long(time.time() * 1000) - twepoch) << timestampLeftShift) | (
            serverId & (-1L ^ (-1L << serverBits)) << serverShift) | (
                          processId & (-1L ^ (-1L << processBits)) << processShift) | randint(1, 1000)
    while ignore_lst and generate_id in ignore_lst:
        generate_id = ((long(
            time.time() * 1000) - twepoch) << timestampLeftShift) | (
                              serverId & (
                              -1L ^ (-1L << serverBits)) << serverShift) | (
                              processId & (
                              -1L ^ (-1L << processBits)) << processShift) | randint(1,
                                                                                     1000)
    return generate_id
