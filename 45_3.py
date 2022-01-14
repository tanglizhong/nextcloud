import pymysql
import re
import time
import gzip

def data_pack():
    line = file.readline()
    while line:
        log.append(line)
        line = file.readline()



        
name_data = []
log = []
file = open("audit.log.6","r")
data_pack()

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="tang",
                     passwd="1995",
                     db="new_schema",
                     charset="utf8"
                     )
 
cursor = db.cursor()



sql = "SELECT * FROM name"
try:
    cursor.execute(sql)
    ergebnis = cursor.fetchall()
    for item in ergebnis:
            name_data.append(item)
except:
    print("Error")
db.close()
datenbank_list = []
i=1
st=time.time()
for line in log:
    log_list=re.split(r'","', line)
    log_list_vor=log_list[1].split(",")
    log_list[1]=log_list_vor[0]
    log_list.insert(2,log_list_vor[1])
    log_list[7]=log_list[7].replace("'","''")
    log_list[8]=log_list[8].replace("'","''")
    user_name=log_list[4][7:]
    """
    for a in range(len(name_data)):
        if name_data[a][1] == log_list[4][7:]:
            user_name = name_data[a][2]
            break
        else:
            user_name=log_list[4][7:]
    """
    datenbank_list.append((int(i),log_list[0][10:],int(log_list[1][7:]),log_list[2][8:18]+" "+log_list[2][19:27],log_list[3][13:],user_name,log_list[5][6:],log_list[6][9:],log_list[7][6:],log_list[8][10:],log_list[9][12:],log_list[10][10:-3]))
    i += 1
print("Es dauert {} S".format(round((time.time()-st),2)))

