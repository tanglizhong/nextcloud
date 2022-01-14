from time import *
import pymysql
import re
import gzip

def aktualisierung():
    def data_packen():
        global file,log
        line = file.readline()
        while line:
            log.append(line)
            line = file.readline()
            
    def insert(datenbank,i):
        global file,log
        log = []
        file = open("audit.log."+str(i+1),"r")
        data_packen()
        i=1
        for line in log:
            log_list=re.split(r'","', line)
            log_list_vor=log_list[1].split(",")
            log_list[1]=log_list_vor[0]
            log_list.insert(2,log_list_vor[1])
            log_list[7]=log_list[7].replace("'","''")
            log_list[8]=log_list[8].replace("'","''")
            for a in range(len(name_data)):
                if name_data[a][1] == log_list[4][7:]:
                    user_name = name_data[a][2]
                    break
                else:
                    user_name=log_list[4][7:]
            datenbank.append((int(i),log_list[0][10:],int(log_list[1][7:]),log_list[2][8:18]+" "+log_list[2][19:27],
                                    log_list[3][13:],user_name,log_list[5][6:],log_list[6][9:],log_list[7][6:],log_list[8][10:],
                                    log_list[9][12:],log_list[10][10:-3]))
            i += 1
        print(i-1," werden hochgeladen")
    
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="new_schema",charset="utf8")
    cursor = db.cursor()
    name_data = []
    try:
        cursor.execute("SELECT * FROM name ")
        ergebnis = cursor.fetchall()
        for item in ergebnis:
            name_data.append(item)
    except:
        print("Error")
    sql = "INSERT INTO nextcloud(id,\
        reqid,level,time,remoteaddr,user,app,method,url,message,useragent,version) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    i=0
    for i in range(30):
        datenbank_list = []
        table_create()
        insert(datenbank_list,i)
        if i == 0:
            cursor.execute("truncate table nextcloud")
            db.commit()
        cursor.executemany(sql,datenbank_list)
        cursor.execute("SET SQL_SAFE_UPDATES = 0")
        cursor.execute("INSERT INTO new_table SELECT * FROM nextcloud WHERE time > date_sub(now(), interval 60 day)")
        #cursor.execute("delete FROM new_schema.nextcloud where time < date_sub(now(), interval 30 day)")
        cursor.execute("drop table nextcloud")
        cursor.execute("create index main on new_table(time,user,method)")
        cursor.execute("RENAME TABLE new_table TO nextcloud")
        db.commit()
        print("Sie können nun die Datenbank aktualisieren")
    db.close()
    sleep(60)
        
    
    
############################################################### Hauptfunktion  #################################################    
def table_create():
    db = pymysql.connect(host="localhost",port=3306,user="root",passwd="123456",db="new_schema",charset="utf8")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS new_table")
    cursor.execute("""CREATE TABLE new_table(
    id          int            not null,
    reqid       varchar(1000)  not null,
    level       int            not null,
    time        varchar(200)   not null,
    remoteaddr  varchar(200)   not null,
    user        varchar(200)   not null,
    app         varchar(45)    not null,
    method      varchar(45)    not null,
    url         varchar(9000) not null,
    message     varchar(1000)  not null,
    useragent   varchar(3000)  not null,
    version     varchar(1000)  not null
    )""")
    #index time(time),index user(user),index method(method)
    db.commit()
    db.close()


while True:
    if __name__ == "__main__":
        def un_gz(file_name):
            f_name = file_name.replace(".gz", "")
            g_file = gzip.GzipFile(file_name)
            open(f_name, "wb+").write(g_file.read())
            g_file.close()
        print("Start...")
        for i in range(29):
            un_gz("audit.log."+str(i+2)+".gz")
        aktualisierung()
        
