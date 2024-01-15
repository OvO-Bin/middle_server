# coding:utf-8
'''
Created on 2015年6月29日

@author: Administrator
'''
import hashlib
from random import randint, random, shuffle, choice

import hmac
from hashlib import sha1


def get_random_str(str_len=8):
    """
    获取随机字符串
    :param str_len:
    :return:
    """
    # seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    seed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(str_len):
        sa.append(choice(seed))
    salt = ''.join(sa)
    return salt


def hmacSHA1EncryptForMI(encryptKey, encryptText):
    '''
    使用 HMAC-SHA1 签名方法对对encryptText进行签名
    不能通用
    :param encryptText 被签名的字符串
	:param encryptKey 密钥
	:return 返回被加密后的字符串
    例子：调用的时候在try中
    from hashlib import sha1
    hmacSHA1Encrypt('08F5B4886112BC6F1E04FE42DACDB2E8', 'xinxin')
    '''
    hmac_code = hmac.new(encryptKey.encode(), encryptText.encode(), sha1)
    return hmac_code.hexdigest()


def hmacSHA1Encrypt(encryptKey, encryptText):
    '''
    使用 HMAC-SHA1 签名方法对对encryptText进行签名
    不能通用
    :param encryptText 被签名的字符串
	:param encryptKey 密钥
	:return 返回被加密后的字符串
    例子：调用的时候在try中
    from hashlib import sha1
    hmacSHA1Encrypt('08F5B4886112BC6F1E04FE42DACDB2E8', 'xinxin')
    '''
    hmac_code = hmac.new(encryptKey, encryptText, sha1)
    return hmac_code.digest()


def equalsIgnoreCase(s1, s2):
    '''判断字符串是否相等，忽略大小写'''
    return s1.lower() == s2.lower()


def getMd5Str(ll):
    '''获得字符串列表的MD5值'''
    string_val_md5 = hashlib.md5(ll).hexdigest()
    return string_val_md5


def multi_sort(L, cons):
    '''
    @param L 待排序的列表
    @param cons 排序条件：为[["key",isAsc]]是map值排序；为bool时为基础值排序
    '''
    if not L or len(L) < 2:
        return

    def multi_cmp1(a, b):
        idx = not isinstance(cons, list) and -1 or 0

        def multi_cmp2(a, b, idx):
            multi_v = isinstance(a, dict)
            if multi_v:
                a_v = a.get(cons[idx][0])
                b_v = b.get(cons[idx][0])
            else:
                a_v = a
                b_v = b
            if a_v == b_v:
                if not multi_v or idx == len(cons) - 1:
                    return 0
                else:
                    idx += 1
                    return multi_cmp2(a, b, idx)
            else:
                if idx == -1:
                    return (cons and 1 or -1) * (a_v > b_v and 1 or -1)
                else:
                    return (cons[idx][1] and 1 or -1) * (a_v > b_v and 1 or -1)

        return multi_cmp2(a, b, idx)

    L.sort(multi_cmp1)


def distinctStr(sss, ss):
    '''去除str中重复的字符串ss'''
    if not (sss and ss):
        return sss
    ss2 = ss + ss
    if sss.find(ss2) == -1:
        return sss
    tmp = sss.replace(ss2, ss)
    return distinctStr(tmp, ss)


def weightRandom(items, n=1):
    '''权重掉落
         @param items point.x 主键，point.y 权重
        @param  n N次
        @return  返回掉落列表
     '''
    assert (len(items) > 0)
    wsum = 0.0
    for p in items:
        wsum += p.get("y")
    rt = []
    shuffle(items)
    for i in range(0, n):
        ssum = 0.0
        r = random()
        for p in items:
            ssum += p.get("y")
            if ssum == wsum or r <= ssum / wsum:
                rt.append(p.get("x"))
                break
    return rt


def weight_drop(items, drop_num=1, is_repeat=False, id_key="x", weight_key="y"):
    """
    权重掉落 可处理是否重复掉落
    :param items: [{id_key:主键, weight_key:权重}]
    :param drop_num: 掉落id列表的长度，掉落id数目
    :param is_repeat: 是否可重复掉落
    :param id_key:
    :param weight_key:
    :return: 返回掉落id列表
    """
    # 不能重复的情况下，数据必须>=掉落数
    if not is_repeat:
        assert (len(items) >= drop_num)
    rt = []
    for i in range(0, drop_num):
        wsum = 0.0  # 权重和
        for p in items:
            wsum += p.get(weight_key)

        shuffle(items)  # 方法将序列的所有元素随机排序。
        ssum = 0.0
        r = random()  # [0,1)
        for p in items:
            ssum += p.get(weight_key)
            if ssum == wsum or r <= ssum / wsum:
                rt.append(p.get(id_key))
                if not is_repeat:
                    # 不能重复
                    items.remove(p)
                break
    return rt


def isDrop(base, thresh):
    '''是否掉落'''
    return randint(1, base) <= thresh


def stringToFloat(rmb):
    '''
        字符串类型转换成float类型
        主要用于金钱的转换
        return 保留两位小数的float类型
    '''
    return round(float(rmb), 2)


def equipRmb(rmb1, rmb2):
    '''
        比较金钱是否相等
    @param rmb1:
    @param rmb2:
    @return: True or False
    '''
    # 比较方法是：去精度两位小数，然后乘以100，在做比较
    return int(stringToFloat(rmb1) * 100) == int(stringToFloat(rmb2) * 100)
