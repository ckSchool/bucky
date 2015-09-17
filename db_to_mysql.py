
import fetch

import pyodbc

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
        return []
    
def getAllCol(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    except:
        return []    

def moveSiswaPerKelas():
    sql = "TRUNCATE students_by_form"
    fetch.updateDB(sql)
    
    sql = "SELECT KKelas, NoInduk FROM SiswaPerKelas WHERE TahunAjaran > 2013"
    res = getAllDict(sql)
    print sql, res
    for row in res:
       
        form_id = row['KKelas']
        NoInduk = row['NoInduk']
        
        sql = "SELECT id FROM students WHERE NoInduk = '%s'" % NoInduk                  
        student_id = fetch.getDig(sql)
        
        sql = "INSERT INTO students_by_form (form_id, student_id) VALUES (%d, %d)" % (form_id, student_id)
        print sql
        fetch.updateDB(sql)
# moveSiswaPerKelas()
    
def moveStaff():
    sql = "TRUNCATE staff"
    fetch.updateDB(sql)
    
    sql = "SELECT   ID, Nama,  Agama, TgMulai, \
                    NoInduk, Alamat, Telepon, HP, Gaji, \
                    TempatLahir, FullTime, TipeGaji, Deposito, KDivisi, \
                    KJabatan, Pria \
                    FROM Staf " 
    res = getAllDict(sql)
    print sql
    for row in res:
        
        ID = row['ID']
        if not ID: ID = 0
        
        name = row['Nama']
        if not name: name = ''
        
        if name == "Ahmad Rafi'i (EC. Design HG)":
            name = "Ahmad Rafi`i (EC. Design HG)"
        
        faith_id = row['Agama']
        if not faith_id: faith_id = 0
        
        join_date = row['TgMulai']
        if not join_date: join_date = '0000-00-00'
        
        NoInduk = row['NoInduk']
        if not NoInduk:NoInduk = ''
        
        address = row['Alamat']
        if not address : address = ''
        
        telp = row['Telepon']
        if not telp: telp = ''
        
        hp = row['HP']
        if not hp: hp = ''
        
        salary = row['Gaji']
        if not salary :salary = 0
        
        pob = row['TempatLahir']
        if not pob:pob = ''
        
        fulltime = row['FullTime']
        if not fulltime:fulltime = 0
        
        salary_type_id = row['TipeGaji']
        if not salary_type_id:salary_type_id = 0
        
        deposit = row['Deposito']
        if not deposit: deposit= 0
        
        division_id = row['KDivisi']
        if not division_id:division_id = 0
        
        position_id = row['KJabatan']
        if not position_id: position_id = 0
        
        gender = row['Pria']
        if gender == 'N': gender = 0
        else:             gender = 1

        sql = "INSERT INTO staff \
                            (name, faith_id, join_date, NoInduk, \
                             address, telp, hp, salary, pob, fulltime, \
                             salary_type_id, deposit, division_id, position_id, gender ) \
                    VALUES ('%s', %d, '%s', '%s', \
                            '%s', '%s', '%s', %d, '%s', %d, \
                            %d, %d, %d, %d, %d)" % (
                            name, int(faith_id), join_date, NoInduk,
                            address, telp, hp, int(salary), pob, int(fulltime),
                            int(salary_type_id), int(deposit), int(division_id), int(position_id), gender )
        print sql
        
        fetch.updateDB(sql)
        
# moveStaff()


def upadateForms_setStaff_id():
    sql = "SELECT id, NoInduk FROM staff"
    
    res = fetch.getAllDict(sql)
    for row in res:
        id = row['id']
        NoInduk = row['NoInduk']
        sql = "UPDATE forms SET staff_id = %d WHERE "

def getStaff_id(NoIndukStaf):
    sql = "SELECT id FROM staff WHERE NoInduk = '%s'" % NoIndukStaf
    res = fetch.getDig(sql)
    return res
    
def moveForms():
    sql = "TRUNCATE forms"
    fetch.updateDB(sql)
    
    sql = "SELECT Kode, TahunAjaran, Nama, Sekolah, NoIndukStaf, course_level \
             FROM Kelas WHERE Kode >  0"
    res = getAllDict(sql)
     
    print len(res) 
    for row in res:
        name      = row['Nama']
        level     = row['course_level']
        school_id = row['Sekolah']
        NoIndukStaf  = row['NoIndukStaf']
        staff_id = getStaff_id(NoIndukStaf)
        schYr     = row['TahunAjaran']
        KKelas = row['Kode']
        sql = "INSERT INTO forms (name, level, school_id, staff_id, schYr, KKelas) \
               VALUES ('%s', %d, %d, %d, %d, %d)" % (name, level, school_id, staff_id, schYr, KKelas)
        print sql
        fetch.updateDB(sql)
# moveForms()


 
def moveStudents():
    sql = "TRUNCATE students "
    fetch.updateDB(sql)
    
    sql = "SELECT * FROM siswa"
    res = fetch.getAllDict(sql)
    for row in res:
        
        NISN        = row['NISN']
        Nama        = row['Nama']
        Panggilan   = row['Panggilan']
        CKID        = row['CKID']
        Pria        = row['Pria']
        Agama       = row['Agama']
        Kapal       = row['Kapal']
        AnakKe      = row['AnakKe']
        TgLahir     = row['TgLahir']
        TempatLahir = row['TempatLahir']
        NoInduk     = row['NoInduk']
        HP          = row['HP']
        GolDarah    = row['GolDarah']
        KOrangTua      = row['KOrangTua']
        KWali          = row['KWali']
        HubunganWali   = row['HubunganWali']
        TinggalDengan  = row['TinggalDengan']
        PergiDengan    = row['PergiDengan']
        TgKeluar       = row['TgKeluar']
        NoSKHUN        = row['NoSKHUN']
        TahunSKHUN     = row['TahunSKHUN']
        NoSTLTamat     = row['NoSTLTamat']
        NoSTLAsal      = row['NoSTLAsal']
        TahunSTLAsal   = row['TahunSTLAsal']
        TahunTamat     = row['TahunTamat']
        TgDiterima     = row['TgDiterima']
        KKelasDiterima = row['KKelasDiterima']
        SaudaraTiri    = row['SaudaraTiri']
        SaudaraAngkat  = row['SaudaraAngkat']
        SaudaraKandung = row['SaudaraKandung']
        AlasanPindah   = row['AlasanPindah']
        NoSuratPindah  = row['NoSuratPindah']
        AlasanKeluar   = row['AlasanKeluar']
        KSekolahPindah = row['KSekolahPindah']
        KSekolahAsal   = row['KSekolahAsal']
        Deposito       = row['Deposito']
        MedicalRecord  = row['MedicalRecord']
        BookForYear    = row['BookForYear']
        
        if not CKID: CKID=0
        
        a = "%s, %d, %s," % ( NISN, int(CKID), NoInduk,)
        
        TgLahir = fetch.convertDate_fromAccess_toMYSQL(TgLahir)
        print 'TgLahir', TgLahir
        b = "%s, %s, %s, %s," %  (Nama, Panggilan,  TgLahir, TempatLahir,)
        
        if   Pria =='N': Pria = 0
        elif Pria =='Y': Pria = 1
        else:            Pria = 1
        if not GolDarah: GolDarah=0
        if not Agama:    Agama = 0
        if not Kapal :   Kapal= 0
        c = "%d, %s, %d, %d, %d," % (int(Pria), HP, int(Kapal),  int(GolDarah), int(Agama),)
        
        if not KOrangTua: KOrangTua =0
        if not KWali: KWali = 0
        if not TinggalDengan: TinggalDengan = 0
        if not PergiDengan: PergiDengan = 0
        d = "%d, %d, %s, %d, %d, " %  (int(KOrangTua), int(KWali), HubunganWali,   int(TinggalDengan), int(PergiDengan),)
        
        
        if not SaudaraKandung:SaudaraKandung=0
        if not SaudaraTiri:SaudaraTiri=0
        if not SaudaraAngkat:SaudaraAngkat=0
        if not AnakKe:AnakKe=0
        e = "%d, %d, %d, %d," % (int(SaudaraKandung),   int(SaudaraTiri),    int(SaudaraAngkat),  int(AnakKe),)
        
        if not KSekolahAsal:  KSekolahAsal   = 0
        if not KKelasDiterima:KKelasDiterima = 0
        
        TgDiterima = fetch.convertDate_fromAccess_toMYSQL(TgDiterima)
        f = "%d, %s, %d, " %  (int(KSekolahAsal),     TgDiterima,     int(KKelasDiterima),)
        
        if not KSekolahPindah:KSekolahPindah = 0
        g = "%s, %d, %s," % (NoSuratPindah,    int(KSekolahPindah), AlasanPindah,)
        
        if not TahunSTLAsal: TahunSTLAsal = 0
        if not TahunTamat  : TahunTamat   = 0
        h = "%d, %s, %s, %d," % (int(TahunSTLAsal),     NoSTLAsal,      NoSTLTamat,   int(TahunTamat),)
        
        if not TahunSKHUN: TahunSKHUN = 0
        if not Deposito:   Deposito   = 0
        
        TgKeluar = fetch.convertDate_fromAccess_toMYSQL(TgKeluar)
        i = "%s, %d, %s, %s, %d, " % (NoSKHUN,        int(TahunSKHUN),  AlasanKeluar, TgKeluar, int(Deposito),)
        
        if not BookForYear: BookForYear = 0
        j = "%s, %s" % (MedicalRecord,    int(BookForYear))
                          
        sql = "INSERT INTO students ( \
                        NISN,  CKID, NoInduk, \
                        name,   callname, dob, pob, \
                        gender, hp,   ship_id, blood_type_id, faith_id, \
                        KOrangTua,      KWali, guardian_relationship,   lives_with, travels_with, \
                        siblings_by_birth,     siblings_step,    siblings_adopted,  child_no, \
                        previous_school_id,    join_date,     join_class_id, \
                        transfer_out_ref,      next_school_id, join_reason, \
                        YrSTL,     NoSTL,      NoGraduateSTL,   YrGraduate, \
                        NoSKHUN,   YrSKHUN,    exit_reason, exit_date, Deposito, \
                        medicalRecord,         book_for_yer) \
                VALUES ('%s', %d, '%s', \
                        '%s', '%s', '%s', '%s', \
                        %d, '%s', %d, %d, %d, \
                        %d, %d, '%s', %d, %d, \
                        %d, %d, %d, %d, \
                        %d, '%s', %d, \
                        '%s', %d, '%s', \
                        %d, '%s', '%s', %d, \
                        '%s', %d, '%s', '%s', %d, \
                        '%s', '%s')" % (
                                NISN, int(CKID), NoInduk,
                                Nama, Panggilan,  TgLahir, TempatLahir,
                                int(Pria), HP, int(Kapal),  int(GolDarah), int(Agama), 
                                int(KOrangTua), int(KWali), HubunganWali,   int(TinggalDengan), int(PergiDengan),
                                int(SaudaraKandung),   int(SaudaraTiri),    int(SaudaraAngkat),  int(AnakKe),
                                int(KSekolahAsal),     TgDiterima,     int(KKelasDiterima),
                                NoSuratPindah,    int(KSekolahPindah), AlasanPindah,
                                int(TahunSTLAsal),     NoSTLAsal,      NoSTLTamat,   int(TahunTamat),
                                NoSKHUN,          int(TahunSKHUN),     AlasanKeluar, TgKeluar, int(Deposito),
                                MedicalRecord,    BookForYear)
        
        
        
   
        
        print sql
        fetch.updateDB(sql)
        
# moveStudents()

def addColumns_toGuardians():
    sql = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE table_name =  'OrangTua'"
    res = fetch.getAllDict(sql)
    for row in res:
        COLUMN_NAME = row['COLUMN_NAME']
        print COLUMN_NAME
        sql = "ALTER TABLE guardians ADD %s INT(4)" % COLUMN_NAME
        print sql
        #fetch.c.execute(sql)
        #fetch.mySQLconn.commit()
        
def move_fromWali_toGuardians():
    #sql = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE table_name =  'wali'"
    #res = fetch.getAllDict(sql)
    #print res
    sql = "TRUNCATE guardians"
    fetch.updateDB(sql)
    
    
    sql = "SELECT Kode, Nama, TempatLahir,TgLahir,Agama,Kewarganegaraan,\
                  Pekerjaan,PekerjaanLain,Alamat,Wilayah,Telepon,HP FROM wali "
    res = fetch.getAllDict(sql)
    for row in res:
        # print 'row', row
        Kode        = row['Kode']
        Nama        = row['Nama']
        TempatLahir = row['TempatLahir']
        TgLahir     = row['TgLahir']
        Agama       = row['Agama']
        Kewarganegaraan = row['Kewarganegaraan']
        Pekerjaan       = row['Pekerjaan']
        PekerjaanLain   = row['PekerjaanLain']
        Alamat      = row['Alamat']
        Wilayah     = row['Wilayah']
        Telepon     = row['Telepon']
        HP          = row['HP']
        
        if not Kode        : Kode = 0
        if not Nama        : Nama = ''
        if not TempatLahir : TempatLahir = ''
        
        if TgLahir:
            print 'TgLahir'
            #TgLahir = fetch.convertDate_fromAccess_toMYSQL(TgLahir)
        else:
            TgLahir = '0000-00-00'
        if not Kewarganegaraan : Kewarganegaraan=''
        if not PekerjaanLain   : PekerjaanLain=''
        if not Alamat    : Alamat  = ''
        if not Wilayah   : Wilayah = ''
        if not Telepon   : Telepon = ''
        if not HP        : HP      = ''   
        
        if not Agama     : Agama=0
        if not Pekerjaan : Pekerjaan=0
        
        sql = "INSERT INTO guardians (\
                           Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,\
                           Pekerjaan, PekerjaanLain, Alamat, \
                           Wilayah, Telepon, HP ) \
                    VALUES (%d, '%s', '%s', '%s', %d, '%s', \
                            %d, '%s', '%s', \
                            '%s', '%s', '%s')" % (
                            Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,
                            Pekerjaan, PekerjaanLain, Alamat,
                            Wilayah, Telepon, HP)
        print sql
        inserted_id = fetch.updateDB(sql)
        print inserted_id
        
        sql = "UPDATE Wali SET new_id = %d WHERE Kode=%d" % (inserted_id, Kode)
        print sql
        fetch.updateDB(sql)

 
def move_fromOrangTua_toGuardians():
    #sql = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE table_name =  'wali'"
    #res = fetch.getAllDict(sql)
    #print res
    #sql = "TRUNCATE guardians"
    #fetch.updateDB(sql)
    
    # fathers
    
    sql = "SELECT Kode, NamaA, TempatLahirA,TgLahirA,AgamaA,KewarganegaraanA,\
                  PekerjaanA,PekerjaanLainA,AlamatA,WilayahA,TeleponA,HPA FROM OrangTua "
    res = fetch.getAllDict(sql)
    for row in res:
        # print 'row', row
        Kode        = row['Kode']
        Nama        = row['NamaA']
        TempatLahir = row['TempatLahirA']
        TgLahir     = row['TgLahirA']
        Agama       = row['AgamaA']
        Kewarganegaraan = row['KewarganegaraanA']
        Pekerjaan       = row['PekerjaanA']
        PekerjaanLain   = row['PekerjaanLainA']
        Alamat      = row['AlamatA']
        Wilayah     = row['WilayahA']
        Telepon     = row['TeleponA']
        HP          = row['HPA']
        
        if not Kode        : Kode = 0
        if not Nama        : Nama = ''
        if not TempatLahir : TempatLahir = ''
        
        if TgLahir:
            print 'TgLahir'
            #TgLahir = fetch.convertDate_fromAccess_toMYSQL(TgLahir)
        else:
            TgLahir = '0000-00-00'
        if not Kewarganegaraan : Kewarganegaraan=''
        if not PekerjaanLain   : PekerjaanLain=''
        if not Alamat    : Alamat  = ''
        if not Wilayah   : Wilayah = ''
        if not Telepon   : Telepon = ''
        if not HP        : HP      = ''   
        
        if not Agama     : Agama=0
        if not Pekerjaan : Pekerjaan=0
        
        sql = "INSERT INTO guardians (\
                           Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,\
                           Pekerjaan, PekerjaanLain, Alamat, \
                           Wilayah, Telepon, HP ) \
                    VALUES (%d, '%s', '%s', '%s', %d, '%s', \
                            %d, '%s', '%s', \
                            '%s', '%s', '%s')" % (
                            Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,
                            Pekerjaan, PekerjaanLain, Alamat,
                            Wilayah, Telepon, HP)
        print sql
        inserted_id = fetch.updateDB(sql)
        print inserted_id
        
        sql = "UPDATE OrangTua SET father_id = %d WHERE Kode=%d" % (inserted_id, Kode)
        print sql
        fetch.updateDB(sql)
        
        
        # mothers
    
    sql = "SELECT Kode, NamaI, TempatLahirI,TgLahirI,AgamaI,KewarganegaraanI,\
                  PekerjaanI, PekerjaanLainI, AlamatA, SamaDenganAyah, AlamatI, WilayahI, TeleponI, HPI FROM OrangTua "
    res = fetch.getAllDict(sql)
    for row in res:
        # print 'row', row
        Kode        = row['Kode']
        Nama        = row['NamaI']
        TempatLahir = row['TempatLahirI']
        TgLahir     = row['TgLahirI']
        Agama       = row['AgamaI']
        Kewarganegaraan = row['KewarganegaraanI']
        Pekerjaan       = row['PekerjaanI']
        PekerjaanLain   = row['PekerjaanLainI']
        
        AlamatA     = row['AlamatA']
        SamaAyah    = row['SamaDenganAyah']
        
        if SamaAyah:
            Alamat  = row['AlamatA']
        else:
            Alamat  = row['AlamatI']
        Wilayah     = row['WilayahI']
        Telepon     = row['TeleponI']
        HP          = row['HPI']
        
        if not Kode        : Kode = 0
        if not Nama        : Nama = ''
        if not TempatLahir : TempatLahir = ''
        
        if TgLahir:
            print 'TgLahir'
            #TgLahir = fetch.convertDate_fromAccess_toMYSQL(TgLahir)
        else:
            TgLahir = '0000-00-00'
        if not Kewarganegaraan : Kewarganegaraan=''
        if not PekerjaanLain   : PekerjaanLain=''
        if not Alamat    : Alamat  = ''
        if not Wilayah   : Wilayah = ''
        if not Telepon   : Telepon = ''
        if not HP        : HP      = ''   
        
        if not Agama     : Agama=0
        if not Pekerjaan : Pekerjaan=0
        
        sql = "INSERT INTO guardians (\
                           Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,\
                           Pekerjaan, PekerjaanLain, Alamat, \
                           Wilayah, Telepon, HP ) \
                    VALUES (%d, '%s', '%s', '%s', %d, '%s', \
                            %d, '%s', '%s', \
                            '%s', '%s', '%s')" % (
                            Kode, Nama, TempatLahir, TgLahir, Agama, Kewarganegaraan,
                            Pekerjaan, PekerjaanLain, Alamat,
                            Wilayah, Telepon, HP)
        print sql
        inserted_id = fetch.updateDB(sql)
        print inserted_id
        
        sql = "UPDATE OrangTua \
                  SET mother_id = %d \
                WHERE Kode=%d" % (inserted_id, Kode)
        print sql
        fetch.updateDB(sql)
        
#move_fromWali_toGuardians()
#move_fromOrangTua_toGuardians()


def update_father_mother_guardian_id_into_students():
    sql = " SELECT id, KOrangTua, KWali FROM students"
    res = fetch.getAllDict(sql)
    for row in res:
        sid = row['id']
        KOrangTua = row['KOrangTua']
        KWali     = row['KWali']
        print 'Student:', sid, 'KOrangTua:', KOrangTua, ' KWali:', KWali
        if KWali:
            sql = "SELECT new_id FROM Wali WHERE Kode = %d" % KWali
            print sql
            new_id = fetch.getDig(sql)
            sql = "UPDATE students SET guardian_id = %d WHERE id =%d" % (new_id, sid)
            fetch.updateDB(sql)
            
        if KOrangTua:
            sql = "SELECT father_id, mother_id FROM OrangTua WHERE Kode = %d" % KOrangTua
            print sql
            res = fetch.getOneDict(sql)
            father_id = res['father_id']
            mother_id = res['mother_id']
            sql = "UPDATE students \
                      SET father_id = %d, mother_id =%d \
                    WHERE id = %d" % (father_id, mother_id, sid)
            fetch.updateDB(sql)
            

# update_father_mother_guardian_id_into_students()

def prepDateForMysql(date):
    print date
    if date:
        yr,m,d = date.split('-')
        print yr, m, d
        
        
    else:
        return '0000-00-00'
def fixDobStudent():
    sql = "SELECT id, dob FROM students "
    res = fetch.getAllDict(sql)
    
    for row in res:
        sid = row['id']
        dob = row['dob']
        #print 'sid', sid, '   dob:',dob
        if not dob : dob ='0000-00-00'
        sql = "UPDATE students SET dob2 = '%s' WHERE id =%d"  % (dob, int(sid))
        #print sql
        try:
            print fetch.updateDB(sql)
        except:
            print 'failed', sql
    
# fixDobStudent()
def addColumnsToStudents():
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name =  'siswa'"
    res = fetch.getAllDict(sql)
    print res[0]
    
    for row in res:
        COLUMN_NAME = row['COLUMN_NAME']
        sql = "ALTER TABLE students ADD %s INT(1)" % COLUMN_NAME
        print sql
        fetch.c.execute(sql)
        fetch.mySQLconn.commit()
        
        
        
def moveAddressItems():
    sql = "TRUNCATE address_items "
    print sql
    fetch.c.execute(sql)
    fetch.mySQLconn.commit()
    

    sql = "SELECT id, itemName, itemType, nextItemID, postcode \
             FROM addressItems"
    print sql
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    for row in res:
        iid, itemName, itemType, nextItemID, postcode = row
        sql = "INSERT INTO address_items \
                           (aiID, name, type, next_item_id, postcode) \
                    VALUES (%d, '%s','%s',%d,'%s')"  % (
                            iid, itemName, itemType, nextItemID, str(postcode))
        print sql
        fetch.updateDB(sql)
        #i += 1
        #if i == 10: return
        
# moveAddressItems()



def updateAddressIDs():
    sql = "SELECT id, aiID, nextItemID FROM address_items"
    res = fetch.getAllCol(sql)
    i = 0
    for row  in res:
        iid, aiID, nextItemID = row
        
        sql = "SELECT id FROM address_items WHERE aiID = %d" % nextItemID
        #print sql
        next_item_id = fetch.getDig(sql)
        
        sql = "UPDATE address_items \
                  SET next_item_id = %d \
                WHERE id = %d" % (next_item_id, iid)
        #print sql
        fetch.updateDB(sql)
        #i+=1
        #if i >8 :return
    
# updateAddressIDs()


def moveAccounts():
    sql = "TRUNCATE acc_accounts"
    fetch.updateDB(sql)
    print 'moveAccounts'
    sql = "SELECT Kode, Nama, Saldo, Kunci FROM Perkiraan"
    res = getAllCol(sql)
    print sql, res
    for row in res:
        print 'row', row
        Kode, Nama, Saldo, Kunci = row
        sql = "INSERT INTO acc_accounts (code, name, balance, locked) \
              VALUES ('%s', '%s', %d, %d)" % (Kode, Nama, Saldo, Kunci)
        print sql
        fetch.updateDB(sql)
# moveAccounts()
        