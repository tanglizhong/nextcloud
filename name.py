import pymysql
import re
log = []
def data_pack():
    line = file.readline()
    while line:
        log.append(line)
        line = file.readline()

file = open("userlist.txt","r")
data_pack()

# 打开数据库连接
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     passwd="123456",
                     db="new_schema",
                     charset="utf8"
                     )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


i=1
for line in log:
    list = line.replace("'","''")
    log_list=list.split(':')
    
    log_list[1]=log_list[1].split("(")

    sql = ("insert into name(id,\
           code,name) \
           VALUES (%s,'%s','%s')" % \
           (int(i),log_list[0][4:],log_list[1][0][1:-1]))

    try:
           # 执行sql语句
        cursor.execute(sql)
        db.commit()
           # 提交到数据库执行
        
    except:
           # 如果发生错误则回滚
        db.rollback()
    i += 1
""" 
query = "truncate table name"
cursor.execute(query)
db.commit()
"""

db.close()
