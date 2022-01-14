import gzip
 
def un_gz(file_name):
    f_name = file_name.replace(".gz", "")
    g_file = gzip.GzipFile(file_name)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()
for i in range(29):
    un_gz("audit.log."+str(i+2)+".gz")
