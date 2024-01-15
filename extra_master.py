# coding:utf-8
'''
Created on 2016年3月29日

@author: Administrator
'''
from gfirefly.master.master import Master


class ExtraMaster(Master):

    def masterapp(self):
        """
        """
        Master.masterapp(self)
        import extra_webapp
