# -*- coding:utf-8 -*-
"""
    用来做异步HTTP调用
"""
import json
import urllib
import urllib2
import httplib
from gevent.greenlet import Greenlet
from gevent import monkey

monkey.patch_all()


class HttpRequest(Greenlet):

    def __init__(self, url, callback, errback, body_data, *args, **kwargs):
        Greenlet.__init__(self)
        self.callback = callback
        self.errback = errback
        self.url = url
        self._args = args
        self._kwargs = kwargs
        self.body = body_data
        self.cookie = []
        pass

    def add_cookie(self, key, val):
        """
            加入一个cookie
        """
        self.cookie.append("%s=%s" % (key, val))

    def _run(self):
        try:
            if self.body:
                headers = {
                    "content-type": "text/json",
                }
                if self.cookie:
                    headers["Cookie"] = ";".join(self.cookie)

                _body_json = json.dumps(self.body)
                _request = urllib2.Request(self.url, _body_json, headers=headers)
                response = urllib2.urlopen(_request).read()
            else:
                response = urllib2.urlopen(self.url).read()
            self.callback(response, self.body, *self._args, **self._kwargs)
        except urllib2.URLError, e:
            if self.errback:
                self.errback(e, self.body, *self._args, **self._kwargs)
            else:
                raise e


def request(url, callback, errback, data, *args, **kwargs):
    _g = HttpRequest(url, callback, errback, data, *args, **kwargs)
    _g.start()


# ---------------------------------------------------------------------------


class HttpRequest2(Greenlet):

    def __init__(self, host, url, method, headers, req_data, is_need_urlencode, callback, errback, *args, **kwargs):
        """

        :param host: 这里不包含http:/
        :param url: 请求的方法
        :param method: GET 或 POST
        :param headers: 例如{"Content-Type": "application/json", 'Cookie': 'session_id=openid;session_type=kp_actoken;org_loc=/mpay/get_balance_m'}
        :param req_data: 请求数据字典类型
        :param is_need_urlencode: GET时是否需要进行urlencode编码
        :param callback: 返回方法
        :param errback: 错误方法
        :param args:
        :param kwargs:
        """
        Greenlet.__init__(self)
        self.host = host
        self.url = url
        self.method = method.upper()
        self.headers = headers
        self.req_data = req_data
        self.is_need_urlencode = is_need_urlencode
        self.callback = callback
        self.errback = errback
        self._args = args
        self._kwargs = kwargs
        pass

    def _run(self):
        conn = httplib.HTTPConnection(self.host)
        try:
            if self.method == "GET":
                params = None
                if self.req_data:
                    if self.is_need_urlencode:
                        params = urllib.urlencode(self.req_data)
                    else:
                        l = []
                        for k, v in self.req_data.items():
                            l.append(str(k) + '=' + str(v))
                        params = '&'.join(l)
                conn.request(self.method, self.url + (params and "?" + params or ""), None, self.headers)
            else:
                conn.request(self.method, self.url, self.req_data, self.headers)
            r1 = conn.getresponse()
            if r1 and r1.status == 200:
                response = r1.read()
                response = response.decode('utf-8', 'ignore')
                self.callback(response, self.req_data, *self._args, **self._kwargs)
            else:
                self.errback(r1, self.req_data, *self._args, **self._kwargs)
        except Exception, e:
            if self.errback:
                self.errback(e, self.req_data, *self._args, **self._kwargs)
            else:
                raise e


def request2(host, url, method, headers, req_data, is_need_urlencode, callback, errback, *args, **kwargs):
    _g = HttpRequest2(host, url, method, headers, req_data, is_need_urlencode, callback, errback, *args, **kwargs)
    _g.start()
