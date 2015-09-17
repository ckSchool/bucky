import pyodbc
import pymysql

connmy = pymysql.connect(db='ckdb',
                         user='root',
                         passwd='andrew',
                         host='localhost',
                         autocommit=True)
curmy = connmy.cursor()

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

sql =  "TRUNCATE TABLE students"
curmy.execute(sql)

sql = "SELECT * FROM Siswa"
results = cursor.execute(sql)
for siswa in results:
    print siswa['Nama']
"""
for yr in (2005,2006,2007,2008,2009,2010,2011,2012,2013,2014):
    #print yr
    for month in (1,2,3,4,5,6,7,8,9,10,11,12):
        sql = "select * from Absensi where TahunAjaran =%d and Bulan =%d" % (yr,month)
        #print sql
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            
            for row in rows:
                #print row
                id = row[0]
                alldays = row[3:]
                day = 0 
                for c in alldays:
                    day += 1
                    if c and c != "X" and c != "-":
                        date = "%d/%d/%d" % ( day, month, yr)
                        code = str(c)
                        sql = "INSERT INTO absences SET id='%s', date='%s', code='%s'" % (id,date,code)
                        print sql
                        curmy.execute(sql)
                        #curmy.commit()
        except:
            #print ' pass'
            pass
#cursor.execute("select * from Absensi")
#row = cursor.fetchone()
#if row:
#    print row
"""
  