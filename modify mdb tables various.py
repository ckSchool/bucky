import pyodbc, gVar

from datetime import datetime, date, time, timedelta

import fetchodbc as fetch

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

def getAllDict(sql):
    try:
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    except:
        print 'getAllDict failed', sql
        return []
        
def getOneDict(sql):
    try:
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = []
        x = cursor.fetchone()
        results.append(dict(zip(columns, x)))
        return results[0]
    except:
        print 'getOneDict failed ', sql
        return []



def giveIdToAll():
    sql = "SELECT COUNT( Nama) FROM Siswa"
    pop = cursor.execute(sql).fetchall()[0][0]
    for sid in range(1, pop):
        string = "UPDATE Siswa SET id =%d " % sid
        cursor.execute(string)
        conn.commit()
        
def getMaxCKID():
    sql = "SELECT MAX (CKID) FROM Siswa "
    CKID = cursor.execute(sql).fetchall()
    print CKID
    CKID =  CKID[0][0]
    return CKID

def clearCKID():
    sql = "UPDATE Siswa SET CKID = 0"
    cursor.execute(sql)
    conn.commit()

def giveCKID_toStudentsWithMultipleEntries():
    CKID = getMaxCKID()
    if not CKID: CKID = 1
    print 'max ckid =', CKID

    sql = "SELECT Nama, TgLahir, id FROM Siswa WHERE CKID < 1 OR CKID IS NULL"
    result1 = cursor.execute(sql).fetchall()

    for row in result1:
        dob  = row[1]
        if dob:
            y, m, d = dob.year, dob.month, dob.day
            dt1 = date(y, m, d)
            dt2 = dt1 + timedelta(days=1)
            nama, TgLahir, sid = row[0], row[1], row[2]
    
            sql = "SELECT Nama, TgLahir, id FROM Siswa WHERE Nama ='%s' AND TgLahir >= %s AND CKID IS NOT NULL" % (nama, dt1)
            result2 = cursor.execute(sql).fetchall()
            
            if len(result2)>1:
                print result2
                for r in result2:
                    Nama, TgLahir, sid = r
                    if TgLahir == dob:
                        sql = "UPDATE Siswa SET CKID=%d WHERE Nama='%s' AND id=%d" % (CKID, Nama, sid)
                        print sql
                        cursor.execute(sql)
                        conn.commit()
    
                   
            CKID += 1
  
   

def giveCKID_toSingles():
    CKID = getMaxCKID()+1
    
    print CKID
    
    sql = "SELECT id, Nama FROM Siswa WHERE CKID IS NULL OR CKID =0"
    result1 = cursor.execute(sql).fetchall()
    
    for row in result1:
        sid, nama  = row[0], row[1]
        
        sql = "SELECT Nama FROM Siswa WHERE Nama ='%s'" % (nama,)
        result2 = cursor.execute(sql).fetchall()
        print result2
        if len(result2)==1:
            sql = "UPDATE Siswa SET CKID=%d WHERE id=%d" % (CKID, sid)
            
            cursor.execute(sql)
            conn.commit()
        CKID += 1
        print CKID

def removeRubbish():
    sql = "SELECT id, NoInduk FROM Siswa"
    result2 = cursor.execute(sql).fetchall()
    
    for row in result2:
        sid = row[0]
        NoInduk = row[1]
        print NoInduk, ' : ', NoInduk[1]
        k = NoInduk[1]
        if k=='B':
            pass
        if k=='I':
            pass
        if k =='3':
            sql ="DELETE FROM Siswa WHERE id=%s" % sid
            cursor.execute(sql)
            #conn.commit()
            
        if k=='6':
            pass
        if k=='7':
            pass
        if k=='8':
            pass
        if k=='9':
            pass
            
        
#clearCKID()
# removeRubbish()
#giveCKID_toStudentsWithMultipleEntries() 
#giveCKID_toSingles()



def getOne_col(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchone()
    except:
        print 'getOne_col failed', sql
        return ''

def getAll_col(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        print 'getAll_col failed', sql
        return ''
    
def getList(sql, colNo=0):
    list =[]
    try:
        res =  getAll_col(sql)
        for row in res:
            list.append(row[colNo])
    except:
        print 'somthing failed with', sql
    return list

def dropTable(table):
    string = "DROP TABLE %s" % table
    try:
        cursor.execute(string)
        conn.commit()
    except:
        pass
    
    
#dropTable('address_items')
#dropTable('address_item_types')
    
def createAddresss():
    dropTable('addresses')
    string = " CREATE TABLE addresses (\
                            id COUNTER PRIMARY KEY, \
                            house VARCHAR(80),  street VARCHAR(30), \
                            estate VARCHAR(80), block VARCHAR(30), \
                            road VARCHAR(80),   kelurahan VARCHAR(80), \
                            postcode integer)"
    cursor.execute(string)
    conn.commit()
    
#createAddresss()
    
#createAddressTables()
def createTableFaiths():
    string = "CREATE TABLE faiths (id COUNTER PRIMARY KEY , faith VARCHAR(30))"
    cursor.execute(string)
    conn.commit()
# createTableFaiths()

def modifyTable_autoIncrement():
    sql = "ALTER TABLE CSiswa MODIFY COLUMN Kode INTEGER AUTOINCREMENT "
    cursor.execute(sql)
    conn.commit()


def createTableFees():
    string = "CREATE TABLE fees (id COUNTER PRIMARY KEY , name VARCHAR(30), schYr INTEGER, course_ids VARCHAR(30), amount INTEGER)"
    cursor.execute(string)
    conn.commit()
# createTableFees()



def createTablenew_users():
    string = "CREATE TABLE new_users (id COUNTER PRIMARY KEY , user_id INTEGER, name VARCHAR(80), password VARCHAR(80), auth_level INTEGER)"
    cursor.execute(string)
    conn.commit()

#createTablenew_users

def modifyColID():
    sql  = "ALTER TABLE Siswa MODIFY COLUMN id INTEGER NOT NULL AUTO_INCREMENT"     
    cursor.execute(sql)
    conn.commit()
    
def altTable_SiswaPerKelas_AddCol():
    sql = "ALTER TABLE SiswaPerKelas ADD COLUMN rereg_next_course_id INTEGER"
    cursor.execute(sql)
    conn.commit()
 
def altTable_resizeAddressCol():
    sql = "ALTER TABLE Wali ALTER COLUMN Alamat TEXT(150)"
    cursor.execute(sql)
    conn.commit()
    
# altTable_resizeAddressCol()

def get_max_sid(result):
    max_sid = {}
    for row in result:
        NoInduk = row['NoInduk']

        sid = row['id']
        prefix,  = NoInduk[0]
        
        if prefix == "I":
            max_sid[1]=sid
            # do nothing
        elif prefix == "A":
            max_sid[2]=sid
            #conn.commit()
        elif prefix == "P":
            max_sid[3]=sid

        elif prefix == "D":
            max_sid[4]=sid

        elif prefix == "K":
            max_sid[5]=sid
            
    import operator
    #max_sid = {1: 2, 3: 4, 4:3, 2:1, 0:0}
    sorted_max_sid = sorted(max_sid.items(), key=operator.itemgetter(1))
    keep_id = sorted_max_sid[0][1]
    
    
    for item in result:
        sid = item['id']
        if keep_id != sid:
            sql = "SELECT id FROM SiswaActive WHERE id = %d AND CKID >0" % sid
            l = getList(sql)
            r = len(l)
            if r>0:
                print 'keep_id:', keep_id
                sql = "DELETE FROM SiswaActive WHERE id = %d" % sid
                cursor.execute(sql)
                conn.commit()
    print '------------------------'
            
def removeOldData_fromSiswaActive():
    sql = "DELETE FROM SiswaActive WHERE TgKeluar > 0"
    #cursor.execute(sql)
    #conn.commit()
    
    sql = "SELECT CKID FROM SiswaActive GROUP BY CKID"
    result = getList(sql)
    #print sql, result
    for CKID in result:
        #print CKID
        sql = "SELECT NoInduk, id FROM SiswaActive WHERE CKID = %d" % int(CKID)
        res = getAllDict(sql)
        if len(res)>1:
            get_max_sid(res)
            
           

# removeOldData_fromSiswaActive()



def copyCSiswaData_toSiswa():
    sql = "SELECT * FROM CSiswa"
    result = fetch.getAllDict(sql)

    for row in result:
        prefexes ={1:'B', 2:'K',3:'D',4:'P',5:'A',6:'I' }
        # s = get school kode fro Kelas row["Kelas"]
        # prefex = prefexes[s].....
        NewTempNoInduk ="????"# = getNetNoInduk(row["Kelas"])
        
        sql = "INSERT INTO Siswa SET NoInduk = '%s'" % NewTempNoInduk
        for key in row:
            print key, row[key]
            
            val = row[key]
            val = ''
            if val.isdigit():
                sql = "UPDATE Siswa SET %s = %d WHERE NoInduk = '%s'" % (key, int(row[key]), NewTempNoInduk)
            else:
                sql = "UPDATE Siswa SET '%s' = %s  WHERE NoInduk = '%s'" % (key, row[key], NewTempNoInduk)
            print sql
            
#copyCSiswaData_toSiswa()
    

def altTableAddCol(table, new_column_name, attribute):
    string = "ALTER TABLE %s ADD %s %s" % (table, new_column_name, attribute)
    cursor.execute(string)
    conn.commit()
    
    
#table, new_column_name, attribute = 'Siswa', 'booking_status', 'VARCHAR(60)'
#table, new_column_name, attribute = 'User', 'password2', 'VARCHAR(32)'
# table, new_column_name, attribute = 'CSiswa', 'notes', 'MEMO'
# altTableAddCol(table, new_column_name, attribute)


def addressItems():
    
    #dropTable('addressItems')
    """
    string = "CREATE TABLE addressItems \
             (id COUNTER PRIMARY KEY, itemType VARCHAR(80), \
              itemName VARCHAR(80), nextItemID INTEGER, postcode INTEGER)"
    try:
        cursor.execute(string)
        conn.commit()
    except:
        pass
    """
    ###sql = "TRUNCATE TABLE addressItems"
    ###cursor.execute(sql)
    ###conn.commit()
    
    """
    sql = "INSERT INTO addressItems (itemType, itemName, nextItemID) VALUES ('country', 'Indonesia', 0)"
    cursor.execute(sql)
    conn.commit()"""
    
    """
    sql = "INSERT INTO addressItems (itemType, itemName, nextItemID) VALUES ('province', 'Sumatera Utara', 1)"
    cursor.execute(sql)
    conn.commit()
    """
    # get province data from postcodes > copy to addressItems
    # itemType:'province', itemName:name_of_province, nextItemID:1
    
    """
    sql = "SELECT province FROM postcodes GROUP BY (province) ORDER BY (province)"
    res = getList(sql)
    #print sql
    #print res
    nextItemID = 1 # = id for Indonesia
    for province in res:"""
    
    
    """
    sql = "INSERT INTO addressItems (itemType, itemName, nextItemID) \
                   VALUES               ('province', '%s',   %d)" % (province, nextItemID)
        cursor.execute(sql)
        conn.commit()
        
    print 'inserted ', len(res), ' provinces'
    
    sql = "SELECT id, itemName FROM addressItems WHERE itemType = 'province'"
    res = getAllDict(sql)
    
    #for row in res:
    #    itemID   = row['id']
    #    province = row['itemName']"""
    """
    sql = "SELECT kabupaten FROM postcodes \
                WHERE province = '%s' \
                GROUP BY (kabupaten)" % 'Sumatera Utara'
    res = getList(sql)
    print sql, res
    
    
    
    # --------------- for each province - add kabupaten-- since this is only for Suatera Utara just id =2---------------------- 
    nextItemID = 2 # code for Sumatera Utara
    for kabupaten in res:
        sql = "INSERT INTO addressItems (itemType, itemName, nextItemID) \
               VALUES ('kabupaten', '%s', %d)" % (kabupaten, nextItemID)
        #print sql
        cursor.execute(sql)
        conn.commit()
    
    print 'inserted ', len(res), ' kabupaten'
    return
    """   
    
    
    # now using the just inserted kabupaten
    # for each kabupaten
    
    """
    sql = "SELECT id, itemName FROM addressItems WHERE itemType = 'kabupaten'"
    res = getAllDict(sql)
    
    print sql
    print len(res), ' records in  addressItems of itemType:kabupaten'
   

    for row in res:
        #print row
        itemID    = row['id']
        kabupaten = row['itemName']
        sql = "SELECT kecamatan FROM postcodes \
                WHERE kabupaten = '%s' \
                GROUP BY (kecamatan)" % kabupaten
        kecamatanList = getList(sql)
        #print sql, '   > ' , len( kecamatanList), ' kecamatan for  kabupaten:', kabupaten
        
        for kecamatan in kecamatanList:
            postcode  = fetch.postcodeForKec(kecamatan)
            sql = "INSERT INTO addressItems (itemType, itemName, nextItemID, postcode) \
                   VALUES ('kecamatan', '%s', %d, %d)" % (kecamatan, itemID, postcode)
            #print sql
            cursor.execute(sql)
            conn.commit()
            #print postcode
        print ' inserted ', len(kecamatanList), ' kecamatan for ', kabupaten 
        # now using each postcode - select kelurahan
    """
 

    sql = "SELECT id, itemName, postcode FROM addressItems WHERE itemType = 'kecamatan'"
    res = getAllDict(sql)
    #print sql, res
        
    for row in res:
        itemID    = row['id']
        postcode  = row['postcode']
        kecamatan = row['itemName']
        
        sql = "SELECT kelurahan FROM postcodes \
                WHERE postcode = %d" % postcode
        res2 = getList(sql)
        print len(res2), ' kelurahan for ', kecamatan
        for kelurahan in res2:
            sql = "INSERT INTO addressItems (itemType, itemName, nextItemID) \
                   VALUES ('kelurahan', '%s', %d)" % (kelurahan, itemID)

            cursor.execute(sql)
            conn.commit()
            #print kelurahan
        
    print 'done'    
    #sql = "INSERT INTO addressItems (itemType, itemName, nextItemID)"
    
# addressItems()

def postcodes():
    string = "CREATE TABLE postcodes (postcode  INTEGER, \
                                      kelurahan VARCHAR(80), \
                                      kecematan VARCHAR(80), \
                                      kabupaten VARCHAR(80), \
                                      province  VARCHAR(80))"
    try:
        cursor.execute(string)
        conn.commit()
    except:
        print ' could not create'
        

    sql = "DELETE * FROM postcodes"
    cursor.execute(sql)
    conn.commit()
    
    res = gVar.postcodeData.split(',')
    for r in res:
        
        a = r.split(':')
        pid = a[0]
        
        try:     spare, postcode, kelurahan, kecematan, kab, kabupaten, province =  (a[1].split("\t"))
        except:  spare, postcode, kelurahan, kecematan, kab, kabupaten, province, spare =  (a[1].split("\t"))
        
        if postcode and kelurahan and  kecematan and kabupaten and province:
            sql = " INSERT INTO postcodes \
                           (postcode,  kelurahan, kecematan,  kabupaten,  province) \
                    VALUES (%d,        '%s',      '%s',       '%s',       '%s')" % (
                        int(postcode), kelurahan,       kecematan,        kabupaten,    province)
        
            #sql = "UPDATE postcodes SET province = '%s' WHERE postcode = %d " % (province, int(postcode))
            try:
                fetch.updateDB(sql)
            except:
                pass
            
        else:
            print "failed on ", postcode, ' - ', Kel, ' - ', Kec, ' - ', KabKota, ' - ', Prov

# postcodes()

def cleanUpAddresses():
    sql = "SELECT Kode, AlamatA FROM OrangTua"
    ref = fetch.getAllDict(sql)
    for address in res:
        adddress = adddress.replace(our_str, 'Jl.', 'Jln.', 1)
        adddress = adddress.replace(our_str, 'Perumahan Cemara Asri Deliserdang', 'Perumahan Cemara Asri, Deliserdang', 1)
        #adddress = adddress.replace(our_str, 'Deliserdang.', 'Deliserdang,', 1)
        adddress = adddress.replace(our_str, 'Medan - Sumut.', 'Medan, Sumut', 1)
        adddress = adddress.replace(our_str, 'Perumahan Cemara Hijau Deliserdang', 'Perumahan Cemara Hijau, Deliserdang', 1)
        adddress = adddress.replace(our_str, 'Deliserdang.', 'Deliserdang,', 1)
        adddress = adddress.replace(our_str, 'Deliserdang.', 'Deliserdang,', 1)
        adddress = adddress.replace(our_str, 'Deliserdang.', 'Deliserdang,', 1)
        
        
        
        
  