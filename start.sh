#!/bin/sh

# 判断servernames中的DEBUG_MODE参数是否是True
# 如果是True就不再输出svr.log

LINE=$(cat servernames.py | grep DEBUG_MODE| sed s/[[:space:]]//g)
DEBUG_MODE=${LINE#*=}
echo $DEBUG_MODE
if [ $DEBUG_MODE == 'True' ]
then
    nohup python start_game_server.py > svr.log 2>&1 &
else
    nohup python start_game_server.py > /dev/null 2>&1 &
fi