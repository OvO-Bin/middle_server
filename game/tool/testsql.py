# coding:utf8
"""

@Time    : 2018/1/16 12:58
@Author  : CHQ
"""

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "kx123456", "xxjn")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()

print "Database version : %s " % data

# 关闭数据库连接
db.close()
