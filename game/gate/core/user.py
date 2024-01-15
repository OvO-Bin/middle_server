# coding:utf8
"""
在线用户
"""


class User(object):
    """
    在线用户登录信息DAO
    """

    def __init__(self, did, box_id, token=None):
        """

        :param did:
        :param box_id: 盒子的唯一ID
        :param token: 登录验证的token
        """
        self.box_id = box_id  # 账号登陆账号
        self.did = did  # 账号动态id
        self.tid = 0  # 账号现在正在哪个场景服务器中
        self.token = token
