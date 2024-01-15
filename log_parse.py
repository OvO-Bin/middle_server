# -*- coding:utf-8 -*-
"""
    日志分析
    单消息时间
    秒请求处理数据
    错误统计 和 筛选

"""
import time
import sys

REQUEST_NUM = {}
REQUEST_COST_TIME = {}
REQUEST_SECOND_REQUEST_NUM = {}  # 记录每秒请求的数量
TOTAL_REQUEST_NUM = 0  # 总请求次数
TOTAL_REQUEST_TIME = 0  # 总请求时间
TOP_SECOND_REQUEST_NUM = 0  # 最高每秒处理请求次数
AVG_SECOND_REQUEST_NUM = 0  # 平均每秒处理请求次数
TRACK_BACK_LST = []


def add_request_num(_request_name):
    if _request_name in REQUEST_NUM:
        REQUEST_NUM[_request_name] += 1
    else:
        REQUEST_NUM[_request_name] = 1


def add_request_cost(_request_name, _cost_time):
    if _request_name in REQUEST_COST_TIME:
        REQUEST_COST_TIME[_request_name] = (REQUEST_COST_TIME[_request_name] + _cost_time) / 2
    else:
        REQUEST_COST_TIME[_request_name] = _cost_time


if __name__ == "__main__":
    file_name = "svr.log"
    parse_request_name = ''
    if len(sys.argv) > 1:
        parse_request_name = sys.argv[1]

    with open(file_name) as log_f:
        last_request_time = 0
        request_start_time = 0
        second_request_num = 0
        while True:
            line = log_f.readline()
            if line:
                try:
                    # 有可能是错误的日志
                    if line.count("[-]") > 1:
                        continue
                    # 是结束标记
                    if "[-] <<<<<=====" in line:
                        request_time = time.mktime(time.strptime(line[0:19], "%Y-%m-%d %H:%M:%S"))
                        request_name = line[46: line.find("Time:")]

                        # 是否是需求统计的方法
                        if parse_request_name and not request_name.startswith(parse_request_name):
                            continue
                        time_str = line.split(':')[-1]
                        request_cost_time = float(time_str)

                        add_request_num(request_name)
                        add_request_cost(request_name, request_cost_time)
                        TOTAL_REQUEST_NUM += 1
                        last_time = request_time
                        if request_start_time == 0:
                            request_start_time = request_time
                        # 计算秒请求数
                        if last_request_time == 0:
                            last_request_time = request_time
                        if last_request_time != request_time:
                            # 过去了1秒
                            cur_second = request_time - request_start_time
                            REQUEST_SECOND_REQUEST_NUM[int(cur_second)] = second_request_num
                            TOP_SECOND_REQUEST_NUM = max(TOP_SECOND_REQUEST_NUM, second_request_num)
                            second_request_num = 1
                            last_request_time = request_time
                        else:
                            second_request_num += 1

                    if "[-] Traceback" in line:
                        track_back_str = line
                        for line_idx in xrange(20):
                            track_back_str += log_f.readline()
                        TRACK_BACK_LST.append(track_back_str)
                except Exception, e:
                    continue
            else:
                TOTAL_REQUEST_TIME = last_request_time - request_start_time
                AVG_SECOND_REQUEST_NUM = float(TOTAL_REQUEST_NUM) / float(TOTAL_REQUEST_TIME)
                break

        print "总请求次数: %s" % TOTAL_REQUEST_NUM
        print "总时间: %s" % TOTAL_REQUEST_TIME
        print "---------------------------"
        print "平均每秒处理请求数: %s" % round(AVG_SECOND_REQUEST_NUM, 4)
        print "最高每秒请求数量: %s" % TOP_SECOND_REQUEST_NUM

        # print "每秒请求处理次数:"
        # for _second_num in xrange(1, int(TOTAL_REQUEST_TIME)):
        #     if REQUEST_SECOND_REQUEST_NUM.has_key(_second_num) and  REQUEST_SECOND_REQUEST_NUM.get(_second_num, 0):
        #         print "秒数: %s   处理次数次数: %s" % (_second_num, REQUEST_SECOND_REQUEST_NUM.get(_second_num, 0))
        #
        print "---------------------------"
        print "处理速度慢的协议:"
        for request_name, cost_time in REQUEST_COST_TIME.items():
            if cost_time > 0.02:
                print "协议: %s   平均花费时间: %s  总次数: %s" % (request_name, cost_time, REQUEST_NUM[request_name])
        print "---------------------------"
        print "发现代码抛错:"
        for track_dat in TRACK_BACK_LST:
            print track_dat
