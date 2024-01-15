# -*- coding:utf-8 -*-
import sys
import urllib, sys

if __name__ == "__main__":
    hostname = "localhost"
    masterport = int(sys.argv[1])

    url = "http://%s:%s/report_and_stop" % (hostname, masterport)
    try:
        response = urllib.urlopen(url)
    except:
        response = None
    if response:
        sys.stdout.write("stop service success \n")
    else:
        sys.stdout.write("stop service failed \n")
