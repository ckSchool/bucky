import pyodbc
import pymysql

conn_new = pymysql.connect(db='ckdb',
                         user='root',
                         passwd='andrew',
                         host='localhost',
                         autocommit=True)
cur_new = conn_new.cursor()
dict_cur_new = conn_new.cursor(pymysql.cursors.DictCursor)

conn_master = pymysql.connect(db='masternew',
                         user='root',
                         passwd='andrew',
                         host='localhost',
                         autocommit=True)
cur_master = conn_master.cursor()
dict_cur_master = conn_master.cursor(pymysql.cursors.DictCursor)

#sql = "SELECT id, code FROM absences LIMIT 200"
#cur_new.execute(sql)
#result = cur_new.fetchall()

def getallnew(sql,):
    cur_new.execute(sql)
    return cur_new.fetchall()

def getallmaster(sql,):
    cur_master.execute(sql)
    return cur_master.fetchall()
    
def getalldict_master(sql):
    cursor = conn_master.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

#DBfile = 'D:/master.mdb'
#conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
#cursor = conn.cursor()

#sql =  "TRUNCATE TABLE students"
#cur_new.execute(sql)

sql = "UPDATE siswa SET CKID=0"
cur_master.execute(sql)


ckid = 1

# step 1: get a list of all student names
sql = "SELECT Nama, TgLahir FROM masternew.siswa LIMIT 4000"
res = getallmaster(sql)
cur_master.execute("SET SQL_SAFE_UPDATES = 0")
#results = sorted(res,key=lambda x: x[0])

# step 2: 
for row in res:
    name, dob = row
    
    sql = 'UPDATE siswa SET CKID=%d WHERE Nama="%s" AND TgLahir="%s" AND CKID=0' % (ckid, name, dob)
    #rintsql
    ckid += 1
    cur_master.execute(sql)



#results = sorted(results,key=lambda x: x[1])
##rintnames
#for name in names:
    ##rintname
    
    #sql = "SELECT CKID, NoInduk  FROM Siswa WHERE Nama ='%s'" % name
    ##rintsql
    #try:
    #    ids = cursor.execute(sql)
    #    #rintname, ids
    #except:
    #]    pass    
    #for row in ids:
    #    #rintname, row
"""
for yr in (2005,2006,2007,2008,2009,2010,2011,2012,2013,2014):
    ##rintyr
    for month in (1,2,3,4,5,6,7,8,9,10,11,12):
        sql = "select * from Absensi where TahunAjaran =%d and Bulan =%d" % (yr,month)
        ##rintsql
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            
            for row in rows:
                ##rintrow
                id = row[0]
                alldays = row[3:]
                day = 0 
                for c in alldays:
                    day += 1
                    if c and c != "X" and c != "-":
                        date = "%d/%d/%d" % ( day, month, yr)
                        code = str(c)
                        sql = "INSERT INTO absences SET id='%s', date='%s', code='%s'" % (id,date,code)
                        #rintsql
                        curmy.execute(sql)
                        #curmy.commit()
        except:
            ##rint' pass'
            pass
#cursor.execute("select * from Absensi")
#row = cursor.fetchone()
#if row:
#    #rintrow
"""
  