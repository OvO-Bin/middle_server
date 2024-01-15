# -*- coding:utf-8 -*-
"""
    起服务器的时候查看是否有异常
"""

file_name_list = ("dbfront.log", "dbsync.log", "guild_res_war.log", "mail.log",
                  "gate_1.log", "gate_2.log", "gate_3.log", "gate_4.log", "gate_5.log",
                  "net_1.log", "net_2.log", "net_3.log", "net_4.log", "net_5.log")


def print_traceback(file_name):
    file_name = "logs/" + file_name
    print "file(%s)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" % file_name
    taceback_list = []
    with open(file_name) as log_f:
        while True:
            line = log_f.readline()
            if line:
                try:
                    # 有可能是错误的日志
                    if line.count("[-]") > 1:
                        continue

                    if "[-] Traceback" in line:
                        track_back_str = line
                        for line_idx in xrange(20):
                            track_back_str += log_f.readline()
                        taceback_list.append(track_back_str)
                except Exception, e:
                    continue
            else:
                break
        for track_dat in taceback_list:
            print track_dat
    print "file(%s)<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" % file_name


if __name__ == "__main__":
    for file_name in file_name_list:
        print_traceback(file_name)
