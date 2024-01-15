# -*- coding:utf-8 -*-
import base64

import servernames
from game.util import stringutil, nodeutil, http_util
import json
from urllib import quote_plus
import time


# def test_local_box_send():
#     data = {
#         "box_id": "e84e0643ae9e3228",#"123456789",
#         "script": "testscript"
#     }
#     #data = "box_id=123456789&script=testscript"
#
#     result = nodeutil.http_req_form("127.0.0.1:2015", "script_to_box", "post", data)
#     print result
#
#
# test_local_box_send()

if "f42b6f10ca8ddea3cd1025799e8bd6fa" != stringutil.getMd5Str("13a73b23600aa8cb" + servernames.SEND_SECRET):
    print "----------"
