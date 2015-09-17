# FIND_IN_SET(student_id, %s) % '1,3,56,89,987,8'
import wx, gVar
import re
import pyodbc as MySQLdb
import MySQLdb

import warnings, datetime, time, pyodbc, types, images, hashlib, random
import DlgDatePicker

from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
        
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
Printon = False
# Printon = True #

Dell   = ('192.168.0.251', 'andrew', 'andrew123', 'chandrakusuma', 3306)
Vostro = ('localhost',     'root',   'passwordroot','ckdb', 3306)

useConnection =   Vostro # Dell #

c=''
cc=''
try:
    import deft
    '''# connect to dell
    ckhost, ckuser, ckpassword, mydb, myport = useConnection
    mySQLconn  = MySQLdb.Connect(
          host = ckhost, user=ckuser,
        passwd = ckpassword, db=mydb, port = myport, compress=1)
    c  = mySQLconn.cursor(cursorclass=MySQLdb.cursor.DictCursor)
    cc = mySQLconn.cursor()'''
except:
    try:
        ckhost, ckuser, ckpassword, mydb, myport =  useConnection
        mySQLconn  = MySQLdb.Connect(
          host = ckhost, user=ckuser,
        passwd = ckpassword, db=mydb, port = myport, compress=1)
        c  = mySQLconn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cc = mySQLconn.cursor()
    except:
        print "can't connect ckdb"
    
class DB:
    #rint 'Connect to Vostro'
    #Vostro = ('localhost', 'root', '', 'chandrakusuma', 3306)
    ckhost, ckuser, ckpassword, mydb, myport = useConnection
    def connect(self):
        try:
            conn = MySQLdb.connect(host   = ckhost,     user=ckuser,
                                        passwd = ckpassword, db=mydb,
                                        port   = myport,     compress=1)
            #rint 'connected'
            
        except (AttributeError, MySQLdb.OperationalError), e:
            #rint ' can not connect'
            raise e

    def query( sql, params = (), resultType='byColumn'):
        if  resultType=='byColumn':
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params)
            except (AttributeError, MySQLdb.OperationalError) as e:
                #rint 'exception generated during sql connection: ', e
                connect()
                cursor = conn.cursor()
                cursor.execute(sql, params)
        
        else: #mySQLconn.cursor
            try:
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                cursor.execute(sql, params)
            except (AttributeError, MySQLdb.OperationalError) as e:
                msg( 'exception generated during sql connection: ', e)
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                cursor.execute(sql, params)    
                
        return cursor
    
    def close(self):
        try:
            if conn:
                conn.close()
                msg( '...Closed Database Connection: ' + str(conn))
            else:
                msg('...No Database Connection to Close.')
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

db = DB()
db.connect()

def rc():
    global c,cc
    try:
        ckhost, ckuser, ckpassword, mydb, myport = useConnection
        mySQLconn  = MySQLdb.Connect(
          host = ckhost, user=ckuser,
        passwd = ckpassword, db=mydb, port = myport, compress=1)
        c  = mySQLconn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cc = mySQLconn.cursor()
    except:
        msg( "can't connect ckdb"    )
    
def rollback():
    mySQLconn.rollback()
    
def c_execute(sql):
    c.execute(sql)
    return  mySQLconn.insert_id()
    
def updateDB(sql):
    inserted_id = 0
    try:
        c.execute(sql)
        inserted_id = mySQLconn.insert_id()
        mySQLconn.commit()
    except:
        #rint 'Update failed' , sql
        msg( 'Update failed')
        
    return inserted_id

def updateDBcommit():
    mySQLconn.commit() 

def updateDBtransaction(sql):
    c.execute(sql)
    return 


#-------------------------------------------------------------------------------
'''
if gVar.Offline:
    mysqlLocal = 1
else:
    mysqlLocal = 0

if mysqlLocal:
    ckhost, ckuser, ckpassword = 'localhost', 'root', 'andrew'
    $rint 'should have passed'
else:
    #ckhost, ckuser, ckpassword =  '192.168.0.12', 'andrew', 'andrew'
    ckhost, ckuser, ckpassword =  '220.247.171.76', 'root', 'CNS6616666'
    $rint '220.247.171.76', 'root', 'CNS6616666'

    mySQLconn=MySQLdb.Connect(
        host=ckhost, user=ckuser,
        passwd=ckpassword, db='fedena_ultimate',compress=1)
    c = mySQLconn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cc = mySQLconn.cursor()
'''
#-------------------------------------------------------------------------------
mdb = 0 # 1: mdb.on  0: mdb.off
mdblocal = 0
if mdb:
    import pyodbc
    if mdblocal:
        # connect to MDB localy        
        #DBPATH = "C:\Users\andrewVostro\Documents\master.mdb"
        
        if dir(DBPATH) == "" :
           msg( "File database tidak ditemukan.")
           
        else:
            connString = (" DRIVER={Microsoft Access Driver (*.mdb)}; \
                            DBQ=C:\\Users\\andrewVostro\\Documents\\master.mdb ")
    else:
        # connect to MDB over network
        #DBPATH = "\\192.168.0.3\database\master.mdb"
        DBPATH = "\\192.168.0.3\absensi\\master.mdb"
        if dir(DBPATH) == "" :
           msg( "File database tidak ditemukan.")
           
        else:
            connString = (" DRIVER={Microsoft Access Driver (*.mdb)}; \
                            DBQ=\\\\192.168.0.3\\absensi\\master.mdb;UID=office;PWD='ckinno633423';QUIETMODE=YES;")

    mdbConn = pyodbc.connect(connString)
    d = mdbConn.cursor() 
            
def mdbAllDict(sql):
    d.execute(sql)
    res = d.fetchall()
    return res
    
def updateMdb(sql):
    #inserted_id = 0
    d.execute(sql)
    #inserted_id = mdbConn.insert_id()
    mdbConn.commit() 
    return 0 # inserted_id

#-------------------------------------------------------------------------------
def echo(s):
    if Printon:
        print 'echo:', s

def getAllDict(sql):
    try:
        #mySQLconn.commit()
        c.execute(sql)
        return c.fetchall()
        mySQLconn.commit()
    except: return ''

def getOneDict(sql):
    #echo(sql)
    try:
        c.execute(sql)
        return c.fetchone()
    except:
        return ''
    
def getAllCol(sql):
    #echo(sql)
    try:
        mySQLconn.commit()
        cc.execute(sql)
        res= cc.fetchall()
        return res
    except:
        return ''    
    
def getOneCol(sql):
    echo(sql)
    try:
        cc.execute(sql)
        res = cc.fetchone()
        return res
    except:
        return ''
    
def getCount(sql):
    echo(sql)
    try:
        mylist = getAllDict(sql)
        if mylist:
            return mylen(list)
        return 0
    except:
        return 0
    
def getStr(sql):
    echo(sql)
    try:
        cc.execute(sql)
        res = cc.fetchone()
        if res:
            return str(res[0])
    except:
        pass
    return ''

def getSum(sql):
    #rint 'getSum ', sql
    try:
        cc.execute(sql)
        res = cc.fetchone()
        #rint ' res = ' , int(res[0])
        return int(res[0])
    except:
        #rint 'no res : 0'
        return 0
    
def getDig(sql):
    #rint  sql
    cc.execute(sql)
    res = cc.fetchone()
    try:    return int(res[0])
    except: return 0

def getRes(sql, want = 'dict'):
    if   want=='dict': return getAllDict(sql)
    elif want=='list': return getList(sql)
    else:              return getCount(sql)
    
def getList(sql, colNo=0):
    echo(sql)
    list =[]
    try:
        res =  getAllCol(sql)
        if res:
            for row in res: list.append(row[colNo])
    except:
        pass
    return list

def getListString(sql, colNo=0):
    alist  = getList(sql, colNo)
    blist  = [str(x) for x in alist]
    string = ','.join(blist)
    return string

def getListTuples(sql):
    list =[]
    try:
        cc.execute(sql)
        res = cc.fetchall()
        for eachitem in res:
            list.append(eachitem)
    except:
        pass
    return list

def build_dictionary(mylist):
    index  = 0
    myDict = {}
    
    for row in mylist:
        newrow=[]
        for x in row:
            if x: x = str(x)
            else: x = ''
            newrow.append(x)

        newrow[0]     = int(newrow[0])
        newrow        = tuple(newrow)
        myDict[index] = newrow
        index +=1
    return myDict
    
#-------------------------------------------------------------------------------
 

#-   A     ---------------------------------------------------------------------

def ask(txt):
    return wx.MessageBox(txt, 'Info', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)

def account_name(account_id):
    sql = "SELECT FROM acc_accounts WHERE id = %d" % account_id
    return getStr(sql)

def addNewStudent(user_name, name):
    return addNewCustomer(user_name, name, 'student')
    
def addNewEmployee(user_name, name):
    return addNewCustomer(user_name, name, 'employee')
    
def addNewAdmin(user_name, name):
    return addNewCustomer(user_name, name, 'admin')
    
def addNewGuardian(user_name, name):
    return addNewCustomer(user_name, name, 'guardian')

def addNewCustomer(user_name, name, user_type): # every person entered is in some form a cusomer or 'Customer' 
    if not user_name: return ''
    full_name = "%s %s %s" % (name)
    
    temp_password = user_name + '123'
    salt = ''.join(random.choice(ALPHABET) for i in range(8))

    h= hashlib.new('sha1')
    h.update(salt + temp_password)
    hashed_password = h.hexdigest()
    
    guid = hashed_password[:32]

    datetime_now = dtNow()
    sql = "INSERT INTO customers \
              SET guid ='%s', username ='%s', name ='%s', \
                  salt ='%s', hashed_password ='%s', created_at ='%s',  updated_at ='%s', \
                  id='', notes=''" % (
                  guid, user_name, name,
                  salt, hashed_password, datetime_now, datetime_now)
    if user_type == 'student':
        sql += ", user_type ='student', student =1"
        
    elif user_type == 'guardian':
        sql += ", user_type ='guardian', guardian =1"
        
    elif user_type == 'admin':
        sql += ", user_type ='admin', admin =1"
            
    elif user_type == 'employee':
        sql += ", user_type ='employee', employee =1"
        
    updateDB(sql)
    return guid

def affectiveIDs_forBatch(form_id):
    id_list = []
    sql = " SELECT c.affectiveIDs \
              FROM curriculum c \
              JOIN forms f ON f.curriculum_id = c.id \
             WHERE f.id = %d" % form_id
    ids = getStr(sql)
    if ids: id_list = ids.split(',')
    return id_list

def affectiveTitle(affective_id):
    sql = " SELECT a.affectiveTitle \
              FROM standards a \
             WHERE a.affective_id=%d" % int(affective_id)
    return getStr(sql)

def allTableNames():
    sql = " SHOW  TABLES \
            FROM `ckdb`"
    return getAllCol(sql)

def assignmentNo_forAssignment(assignment_id):
    sql = " SELECT assignment_no \
              FROM assignments \
             WHERE assignment_id=%d" % int(assignment_id)
    return getStr(sql)

def assignmentInfo(assignment_id):
    sql = " SELECT a.number, a.title, a.date, \
                   a.value, a.catagory_id, a.standards_ids, a.notes \
              FROM assignments a \
              JOIN assignment_catagories ac ON a.catagory_id = ac.id \
             WHERE a.id = %d"  % int(assignment_id)
    return getOneDict(sql)

def assignmentIDs_forStudygroup(studygroup_id, semester_no):
    #rint 'studygroup_id, semester_no', studygroup_id, ' | ', semester_no
    sql = " SELECT a.id \
              FROM assignments a \
             WHERE a.studygroup_id = %d \
               AND a.semester = %d " % (studygroup_id,  semester_no)
    #rint sql
    return getList(sql)
        
def avoidList(form_id, group):
    sql = "SELECT divisions \
             FROM forms \
            WHERE id = %d" % form_id
    res = getStr(sql)
    list = res.replace('/',',')
    list = list.split(',')
    i=0
    avoidList=[]
    for item in list:
        if item != group:
            avoidList.append(item)
            i +=1
    return avoidList

def acc_code_exists(acc_code):
    sql = "SELECT * \
             FROM acc_accounts \
            WHERE code =%s" % acc_code
    return getCount(sql)
        
def acc_name_exists(acc_name):
    sql = "SELECT * \
             FROM acc_accounts \
            WHERE name ='%s'" % account_name
    return getCount(sql)

def acc_catagory_id(acc_code):
    sql = "SELECT acc_catagory_id FROM acc_accounts WHERE code=%d" % int(acc_code)
    return getDig(sql)
    
    
def acc_name(acc_code):
    sql = "SELECT name FROM acc_accounts WHERE code=%d" % acc_code
    return getStr(sql)

def acc_balance(acc_code):
    sql  = "SELECT balance FROM acc_accounts WHERE code = %d" % int(acc_code)
    return getDig(sql)
        
#- B     ---------------------------------------------------------------------
def blood_type(blood_type_id):
    sql = " SELECT name \
              FROM blood_types \
             WHERE id =  %s" % blood_type_id
    return getStr(sql)

def buttondate(olddate):
    gVar.gDate = olddate
    #rint 'olddate',olddate
    newDate = olddate
    dlg = DlgDatePicker.create(None, olddate)
    try:
        if dlg.ShowModal() == wx.ID_OK: 
            newDate = dlg.calendardate
            
    finally:   
        dlg.Destroy()
        
    #rint 'newDate',newDate
    return newDate

def bus_fee_monthly(student_id, schYr):
    return 111111



#-   C     ---------------------------------------------------------------------
def childStatus(childStatus_id):
    sql = " SELECT childStatus \
              FROM childstatus \
             WHERE id = %s" % childStatus_id
    return getStr(sql)

'''def nis(student_id):
    sql = " SELECT nis \
              FROM students \
             WHERE id = %d " % int(student_id)
    return getStr(sql)'''

def ckid(student_id):
    sql = " SELECT ckid \
              FROM students \
             WHERE id = %d " % int(student_id)
    return getStr(sql)

def choiceID(choiceCtrl):
    index = choiceCtrl.GetSelection()
    if index > 0: selected_id = choiceCtrl.GetClientData(index)
    else:         selected_id = 0
    return selected_id
    
def cmbID(cmb):
    index = cmb.GetSelection()
    print 'cmb name:',cmb.GetName(), ', index=', index, ' value = ', cmbValue(cmb)
    if index > -1:
        cid = int(cmb.GetClientData(index))
        print 'returning ', cid
        return cid
    else:
        print 'return 0'
        return 0

def cmbValue(cmb):
    index= cmb.GetSelection()
    #rint index
    if index > -1:
        return str(cmb.GetStringSelection())
    return ''

def colNames(tablename):
    sql = " SHOW COLUMNS \
            FROM %s \
            FROM fedena_ultimate" % tablename
    return getAllCol(sql)

def convertDate_fromAccess_toMYSQL(date):
    inverted_dict = dict([[v,k] for k,v in gVar.numborBulan.items()]) 
    #rint 'convertDate_fromAccess_toMYSQL', date
    if date:
        if date:
            try: 
                dateArray = str(date).split(" ")
            
                month = dateArray[1]
                if type(month) is str:
                    
                    #rint 'month_name', month
                    d2 = inverted_dict[month]
                else:
                    d2 = month
                date = "%s-%s-%s" % (dateArray[2], d2, dateArray[0])
            except:
                #rint ' except '
                dateArray = str(date).split("/")
                #rint dateArray
                month = dateArray[1]
                date  = "%s-%s-%s" % (dateArray[2], month, dateArray[0])
        #rint 'converted date:', date
        return str(date)
    return ''

def convert_fromDBdate(date):
    if date:
        if date:
            dateArray = str(date).split()[0].split("-")
            date = "%s-%s-%s" % (dateArray[2],dateArray[1],dateArray[0])
        #rint date
        return str(date)
    return ''

def comment_forStudygroup(student_id, studygroup_id, semester_no):
    sql = " SELECT g.comment \
              FROM grades_comments g \
             WHERE g.student_id=%d \
               AND g.studygroup_id=%d \
               AND g.semester_no=%d" % (
            student_id, studygroup_id, semester_no)
    return getStr(sql) 
      
def comment_forForm(student_id, form_id, semester_no):
    sql = " SELECT g.comment \
              FROM grades_comments g \
             WHERE g.student_id = %d \
               AND g.form_id = %d \
               AND g.semester_no = %d" % (
            student_id, form_id, semester_no)
    return getStr(sql)

#  count ------------------------------
def countStudents_newForCourse(rereg_course_id):
    sql = " SELECT COUNT(s.id) \
              FROM students s \
             WHERE s.enter_course_id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr" % (rereg_course_id, gVar.schYr)
    return getDig(sql)
    
def countStudents_retakingCourse(rereg_course_id): 
    sql = " SELECT COUNT(s.id) \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms f ON f.id = sbf.form_id \
             WHERE f.course_id = %d \
               AND f.schYr = %d  \
               AND '%s'  BETWEEN s.register_schYr AND s.exit_schYr \
               AND sbf.rereg_status = 'retake' " % (rereg_course_id, gVar.schYr, gVar.schYr)
    return getDig(sql)
    
def countStudents_reregFeePaid_forCourse(rereg_course_id):
    sql = " SELECT COUNT(s.id) \
              FROM students_by_form sbf \
              JOIN students s ON sbf.student_id = s.id \
             WHERE sbf.rereg_course_id = %d \
               AND s.exit_schYr <='%s' \
               AND '%s'  BETWEEN s.register_schYr AND s.exit_schYr \
               AND sbf.rereg_status = 'paid' "  % (rereg_course_id, gVar.schYr, gVar.schYr)
    return getDig(sql)

def countStudents_inCourse(course_id):
    sql ="SELECT COUNT(s.id) \
            FROM students s \
            JOIN students_by_form sbf ON s.id = sbf.student_id \
            JOIN forms              f ON f.id = sbf.form_id \
            JOIN courses            c ON c.id = f.course_id \
           WHERE c.id = %d \
             AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (course_id, gVar.schYr)
    #rint sql
    return getDig(sql)


def classCount_forCourse(course_id): # returns 'number_of_classes_next_schYr'
    sql = " SELECT COUNT(f.id) \
              FROM forms f \
             WHERE f.course_id = %d AND f.schYr =%d" % (course_id, gVar.schYr)
    return getDig(sql)

def countStudents_inCourseTitle(course_id):
    sql ="SELECT COUNT(s.id) \
            FROM students s \
            JOIN students_by_form sbf ON s.id = sbf.student_id \
            JOIN forms              f ON f.id = sbf.form_id \
	    JOIN courses            c ON c.id = f.course_id \
           WHERE c.id = %d \
             AND '%s' BETWEEN s.register_year AND s.exit_schYr " % (course_id, gVar.schYr)
    return getDig(sql)


# courses_for/by


def courses_byLevel_tupleList():
    sql = " SELECT c.id, cl.name, cl.level \
              FROM courses c \
	      JOIN course_levels cl ON cl.level = c.level \
             WHERE cl.level > -5 \
               AND c.terminated  = False \
             ORDER BY cl.level"
    return getListTuples(sql)
    
def courses_byLevel(result_type = 'dict' ):
    #rint ' fetch > courses_byLevel'
    sql = " SELECT c.id, c.name, LPAD(c.level, 2, 0) AS level \
              FROM courses c \
	      JOIN course_levels cl ON cl.level = c.level \
             WHERE NOT c.ceased  \
             ORDER BY cl.level"
    #rint 'fetch.courses_byLevel:',  sql, getAllDict(sql)
    if result_type=='dict':   
          return getAllDict(sql)
    else: return getAllCol(sql)
                                
    
def courses_for_year(yr):
    sql = "SELECT c.id, c.name, LPAD(level, 2, 0) AS level \
             FROM courses c \
             JOIN courses_by_year cby ON c.id = cby.course_id \
            WHERE cby.schYr =%d" % yr
    #rint "fetch courses_for_year > ", sql
    return getAllDict(sql)

def courses_for_year_DATA(yr):
    sql = "SELECT c.id, c.name, LPAD(c.level, 2, 0) \
             FROM courses c \
             JOIN courses_by_year cby ON c.id = cby.course_id \
            WHERE cby.schYr =%d" % yr
    
    DATA = build_dictionary(getAllCol(sql))
    #rint sql, DATA
    return DATA


def courses_forSchool_forYear(school_id, yr):
    sql = " SELECT c.id, c.course_title \
              FROM courses c \
	      JOIN course_levels cl ON cl.level = c.level \
             WHERE cl.level > -5 \
               AND cl.school_id =%d \
               AND c.schYr = %d  \
             ORDER BY cl.level" %(school_id, yr)
    #rint sql
    return getAllDict(sql)

def courses_forSchool(school_id):
    sql ="SELECT c.id, c.name \
            FROM courses c \
            JOIN course_levels cl ON cl.level = c.level \
           WHERE cl.school_id = %d \
           GROUP BY c.name \
           ORDER BY cl.level " % (school_id) #  GROUP BY cl.level \
    #rint sql
    return getAllDict(sql)

def courses_forLevel_forYr(level, yr):
    sql ="SELECT c.id, c.name \
            FROM courses c \
            JOIN course_levels cl ON c.level = cl.level \
           WHERE cl.level > -5 \
             AND c.schYr = %d \
             AND cl.level = %d \
        ORDER BY cl.level " % (yr, level) #  GROUP BY cl.level \
    #rint sql
    return getAllDict(sql)

def courses_forLevel(level):
    sql ="SELECT name \
            FROM courses \
           WHERE level = %d " % level

    return getList(sql)

def courses_DATA():
    sql = "SELECT id, name, LPAD(level, 2, 0) \
             FROM courses "
    DATA = build_dictionary(getAllCol(sql))
    return DATA
def course_level(level_id=0):
    sql = " SELECT level \
              FROM course_levels \
             WHERE id = %d" % level_id
    return getDig(sql)

# -courseLevels----------------

def courseLevels_forSchool(school_id):
    res = schoolInfo(school_id)
    min_level = res['min_level']
    max_level = res['max_level']
    return (min_level, max_level)

def regCourseLevels():
    this_year = gVar.schYr
    next_year = gVar.schYr +1
    sql = "SELECT id, LPAD(level, 2, 0) \
             FROM courses  \
            WHERE schYr = %d OR schYr = %d \
            GROUP BY level \
            ORDER BY level " % (this_year, next_year)
    #rint sql
    return getAllDict(sql)

def courseLevels():
    sql = "SELECT id, LPAD(level, 2, 0) \
             FROM course_levels \
            GROUP BY level \
            ORDER BY level"
    return getAllDict(sql) 
             
def courseLevel_forCourse(course_id):
    sql = "SELECT cl.level \
             FROM course_levels cl \
             JOIN courses c ON cl.level = level \
            WHERE c.id = %d" % int(course_id)
    return getDig(sql)

def courseLevel_forCourseTitle(courseLevel_forCourseTitle):  
    sql = "SELECT cl.level \
             FROM course_levels cl \
             JOIN courses c ON c.level = cl.level \
            WHERE c.course_title = '%s'" % courseLevel_forCourseTitle
    return getDig(sql)

def courseLevel_id_forStudent(student_id):
    sql = " SELECT cl.level \
              FROM students s \
              JOIN students_by_form sbf ON sbf.student_id = s.id \
              JOIN forms              f ON sbf.form_id = f.id \
	      JOIN courses            c ON c.id = f.course_id \
              JOIN course_levels     cl ON cl.level = c.level \
             WHERE s.id = %d " % student_id
    return getDig(sql)


def course_level_forForm(form_id):
    sql = "SELECT c.course_level \
             FROM forms   f \
	     JOIN courses c ON c.id = f.course_id \
            WHERE f.id = %d" % int(form_id)
    return getDig(sql)


def courses_levels_all_DATA():
    sql = " SELECT id, LPAD(level, 2, 0) , name \
              FROM course_levels \
             ORDER BY level"
    return build_dictionary(getAllCol(sql))

def course_level_info(course_level):
    if not course_level: return {}
    sql = " SELECT name, level, school_id, \
              FROM course_levels cl \
             WHERE id = %d " % (course_level, )
    #rint sql
    return getAllDict(sql)

# oursesIDs ---------------------------    
def coursesIDs_all():        # returns:course_level
    sql = " SELECT id \
              FROM courses \
             GROUP BY name \
             ORDER BY name"
    return getList(sql)
    
def courseID_forStudent(student_id):
    sql = " SELECT f.level \
              FROM students s \
              JOIN students_by_form sbf ON sbf.student_id = s.id \
              JOIN forms              f ON sbf.form_id = f.id \
             WHERE s.id = %d " % student_id
    return getDig(sql)

def courseId_forForm(form_id):
    sql = "SELECT c.id \
             FROM courses c \
             JOIN forms f ON c.id = f.course_id \
            WHERE f.id = %d \
              AND c.schYr =%d" % (int(form_id), gVar.schYr)
    #rint sql
    return getDig(sql)

def course_id_forTitleYear(course_title, schYr):
    sql ="SELECT id \
            FROM courses \
           WHERE name = '%s' \
             AND schYr =%d" % (course_title, schYr,)
    #rint sql
    return getDig(sql)

def courseTitles_details():
    sql = " SELECT id, name, section_name, level \
              FROM courses \
             GROUP BY level \
             ORDER BY level"
    return getAllDict(sql)
    
def course_details(course_id): 
    if not course_id: return {}
    sql = " SELECT c.name, c.schYr,  cl.level, cl.name AS level_name, cl.section, \
                  cl.school_id, cl.code \
              FROM courses c \
              JOIN course_levels cl ON cl.level = c.level \
             WHERE c.id = %d " % (course_id,)
    #rint sql
    return getOneDict(sql)


def courseTitle_forCourse(course_id):
    sql = "SELECT name  \
             FROM courses  \
            WHERE id = %d " % course_id
    return getStr(sql)
               
def courseTitles_forLevel(course_level):
    #rint 'courseTitles_forLevel', course_level, yr
    sql = " SELECT cl.level, cl.name \
              FROM course_levels cl \
             WHERE cl.level = %d \
          ORDER BY name" % (int(course_level),)
    return getAllDict(sql)


def courseTitles():
    sql = "SELECT cl.level, cl.name \
             FROM course_levels cl \
            ORDER BY cl.level"
    return getAllDict(sql)

def currentCourse(student_id):
    sql = " SELECT cl.name \
              FROM course_levels cl \
	      JOIN courses c ON cl.level = c.course_level \
              JOIN forms   f ON c.id = f.course_id \
              JOIN students_by_form sbf ON f.id = sbf.form_id \
             WHERE sbf.student_id = %d \
               AND f.schYr =%d" % (int(student_id), gVar.schYr)
    return getStr(sql)




#-   D     --------------------------------------------------------------------

def DATA(sql):
    return build_dictionary(getAllCol(sql))

def displayDate(date):
    # this takes a DATE object and converts it to text for display
    txt = date.strftime("%d") + ' ' + date.strftime("%B") + ' ' + date.strftime("%Y")
    return txt

def dateConvert_YMDtoMDY(ymd):
    # this takes a DATE object and converts it to text 
    m = date.strftime("%d") 
    d = date.strftime("%B") 
    y = date.strftime("%Y")
    #rint "month / day / year", m, d, y
    return mdy
    
def dtNow(indate=''):
    if indate: n = indate.split('-')
    
    t  = datetime.time(1, 2, 3)                    
    d  = datetime.date.today()
    dt = datetime.datetime.combine(d, t)
    return dt

#-  E     ----------------------------------------------------------------------
def employeeDetails(id): # # returns:* , working May 2012
    sql = " SELECT * \
              FROM staff \
             WHERE id = %d" % id
    return getOneDict(sql)

def employeeName(staff_id):
    if not staff_id:return ''
    sql = "SELECT name \
             FROM staff \
            WHERE id = %s" % staff_id
    return getStr(sql)
    
def eduLevel(id=0):
    if not id:return''
    sql = "SELECT name \
             FROM qualifications \
            WHERE id = %s" % id
    return getStr(sql)

def exculRemainingStudents(sch_id, existingStudents):
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON sbf.student_id = s.id\
              JOIN forms              f ON sbf.form_id    = f.id \
             WHERE f.school_id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (gVar.schYr, sch_id, gVar.schYr )
    # $rint sql
    remainingstudentIDs = getList(sql)
    # $rint remainingstudentIDs
    remainingstudents=[]
    if remainingstudentIDs:
        # compare ids : if id not match add to list
        for remainingstudent_id in remainingstudentIDs:
            add = True
            for existingstudent_id in existingStudents:
                
                if int(existingstudent_id) == int(remainingstudent_id):
                    add = False
        
            if add:
                remainingstudents.append(str(remainingstudent_id))

    return remainingstudents   

def excuric_activityIDs():
    sql = " SELECT id, name \
              FROM excuric_activities"
    return getAllDict(sql)

def excuric_info(excuric_id):
    sql = " SELECT staff_id, subject_id \
              FROM excuric \
             WHERE id=%d" % int(excuric_id)
    return getOneDict(sql)
                                
def excuric_groups_forSchSemYr(dayNo, semester, sch_id):
    sql = " SELECT ex.id, ea.id AS subject_id, ea.name AS subject_name, e.id, st.name AS teacher_name \
              FROM excuric ex \
              JOIN excuric_schedule es ON es.id = ex.exculset_id \
         LEFT JOIN excuric_subjects ea ON ea.id = ex.subject_id \
         LEFT JOIN staff            st ON st.id = ex.staff_id \
             WHERE es.day = %d AND es.semester = %d AND es.schYr = %d AND es.school_id = %d " % (
                   dayNo, semester, gVar.schYr, sch_id)
    #if getAllCol(sql): rint sql
    return getAllCol(sql)

def exculsetinfo(set_id):
    sql = " SELECT s.name, d.day, es.semester, es.schYr \
              FROM excuric_schedule es \
              JOIN schools s ON s.id = es.school_id \
              JOIN days d    ON d.id = es.day \
             WHERE es.id = %d" % set_id
    return getOne_col(sql)
    
def excuric_groups_forExculSet(schedule_id):
    sql = " SELECT ex.id, \
                  sub.id AS subject_id, sub.name AS subject_name, \
                    s.id AS staff_id,     s.name AS staff_name\
              FROM excuric ex \
              JOIN excuric_schedule  es ON  es.id = ex.excuric_schedule_id \
         LEFT JOIN excuric_subjects sub ON sub.id = ex.subject_id \
         LEFT JOIN staff s              ON   s.id = ex.staff_id \
             WHERE es.id = %d " % (schedule_id, )
    #rint sql
    return getAllCol(sql)

def exculDays_forSchSemYr(school_id, semester_no, yr):
    sql = " SELECT day \
              FROM excuric_schedule \
             WHERE semester = %d \
               AND school_id = %d \
               AND schYr = %d" % (semester_no, school_id, yr)
    #rint sql
    return getList(sql)

def subject_by_excuric(excuric_id):
    sql = "SELECT s.name \
             FROM excuric_subjects s \
             JOIN excuric ex ON s.id = ex.subject_id \
            WHERE ex.id = %d" % int(excuric_id)
    #rint sql
    return getStr(sql)


def excuric_subject_name(subject_id):
    sql = "SELECT name \
             FROM excuric_subjects \
            WHERE id = %d" % int(subject_id)
    return getStr(sql)  

def excuric_activityPool(listOfActivityIDs):
    listOfActivityIDs = [str(x[0]) for x in listOfActivityIDs]
    #rint 'listOfActivityIDs', listOfActivityIDs
    listStr = "'%s'" % ','.join(listOfActivityIDs)
    sql = " SELECT id, name \
              FROM excuric_subjects \
             WHERE NOT FIND_IN_SET(id, %s)" % listStr
    #rint sql
    return getAllCol(sql)

def excuric_teacherPool(teacherIDs):
    teacherIDs = [str(x[0]) for x in teacherIDs]
    listStr = "'%s'" % ','.join(teacherIDs)
    sql = " SELECT id, name \
              FROM staff \
             WHERE staff_type_id = 2 \
               AND %d BETWEEN join_schYr AND exit_schYr \
               AND NOT FIND_IN_SET(id, %s)" % (gVar.schYr, listStr)
    #rint sql
    return getAllCol(sql)

def exculset_id():
    sql = " SELECT id \
              FROM excuric_schedule \
             WHERE day = %d \
               AND semester = %d \
               AND school_id = %d \
               AND schYr = %d" % (gVar.dayNo, gVar.semester, gVar.school_id, gVar.schYr)
    return getDig(sql)
  
#-   F     ---------------------------------------------------------------------
def faith(id):
    sql = " SELECT name \
              FROM faiths \
             WHERE id = %s" % id
    return getStr(sql)

def feeType(id):
    sql = " SELECT feeTitle \
              FROM feetypes \
             WHERE feeType_id = %s" % id
    return getStr(sql)

def fee_monthly(course_id, yr):
    sql = "SELECT course_fee_monthly \
             FROM courses_by_year \
            WHERE course_id = %d \
              AND schYr = %d" % (course_id, yr)
    return getDig(sql)

def fee_yearly(course_id, yr):
    print 'fee_yearly'
    sql = "SELECT course_fee_yearly \
             FROM courses_by_year \
            WHERE course_id = %d \
              AND schYr = %d" % (course_id, yr)
    print sql
    return getDig(sql)

def fees(yr):
    sql = "SELECT id, type, amount, description \
             FROM school_fees \
            WHERE schYr" % yr
    return getAllDict(sql)

def filter_list(full_list, excludes):
    s = set(excludes)
    return (x for x in full_list if x not in s)

def formatDateForDB(date): 
    dbDate = "0000-00-00"
    if date: 
        #rint 'date =',  date
        d = str(date).split("-")
        if len(d) == 3:
            if len(d[0]) < 3:
                dbDate = "%s-%s-%s" % (d[2],d[1],d[0]) # yyyy/mm/dd
    return dbDate

def formatDateForDisplay(date):
    # date yyyy/mm/dd
    dispDate=''
    if date:
        # rint 'str(date)', str(date)
        d = str(date).split("-")
        dispDate = "%s-%s-%s" % (d[2],d[1],d[0]) # dd/mm/yyyy
    return dispDate

def formsAndGroups_inStudygroup(studygroup_id): # used x 2
    #???????????????
    sql = " SELECT form_ids, groups \
              FROM studygroups \
             WHERE id = %d" % studygroup_id
    #rint sql
    row = getOneDict(sql)
    returnStrings, forms, groups = [],[],[]
    if row:
        form_ids  = row['form_ids']
        #form_Name = formName(form_id)
        groups  = row['groups']
        #forms.append(form_Name)
        groups.append(groupName)
    form_str = ','.join(forms)
    group_str = ','.join(groups)
    #
    returnStrings.append(form_str)
    returnStrings.append(group_str)
    return returnStrings

def forms_inStudygroup(studygroup):# not used
    sql = " SELECT form_ids \
              FROM studygroups \
             WHERE id = %d" % studygroup
    return getStr(sql).split(',')
    
def forms_forSchool(school_id):
    sql = "SELECT f.id, f.name \
             FROM forms f \
	     JOIN courses        c ON c.id = f.course_id \
             JOIN course_levels cl ON cl.level = c.course_level \
            WHERE cl.level > -5 \
              AND cl.school_id = %d" % school_id
    return getAllDict(sql)

def forms_forSchool_forYear(school_id, schYr=0):
    sql = "SELECT f.id, f.name \
             FROM forms f  \
	     JOIN courses        c ON c.id = f.course_id \
             JOIN course_levels cl ON cl.level = c.level \
            WHERE cl.level > -5 \
              AND cl.school_id = %d" % school_id
    if schYr:  sql += " AND f.schYr =%d" % schYr
    #rint sql
    return getAllDict(sql)

def forms_forMentor(staff_id):
    formsList = []
    sql = " SELECT id \
              FROM forms \
             WHERE schYr = %d \
               AND staff_id = %d" % (gVar.schYr, staff_id,)
    #rint sql
    return getList(sql)

def formName(form_id):
    sql = " SELECT name \
              FROM forms \
             WHERE id = %d" % int(form_id)
    return getStr(sql)
    
def formInfo(form_id):
    sql = " SELECT name, short, course_id \
              FROM forms \
             WHERE id = %d" % int(form_id)
    return getOneDict(sql)

def formInfo2(form_id):
    sql = " SELECT f.name, f.course_id, cl.name, cl.level, f.course_id \
              FROM forms f \
	      JOIN courses        c ON c.id = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE f.id = %d" % int(form_id)
    return getOneDict(sql)
    
def formName_forMentor(staff_id):
    names_string = ''
    form_ids_list = forms_forMentor(staff_id).strip()
    #rint "form_ids_list ; ", form_ids_list
    if form_ids_list:
        names_list = []
        for form_id in form_ids_list:
            #rint "form_id in form_ids_list ;", form_id
            name = formName(int(form_id))
            names_list.append(name)
        names_string = ', '.join(names_list)
    return names_string
    
def formName_forStudent(student_id):
    sql = " SELECT f.name \
              FROM students s \
              JOIN forms f ON f.id = s.form_id \
             WHERE schYr = %d \
               AND s.id= %d" % (gVar.schYr, int(student_id))
    return getStr(sql)
    
def formID_forStudent(student_id, schYr = None):
    
    sql = " SELECT form_id \
              FROM students_by_form  \
             WHERE student_id = %d" % student_id
    if schYr:
        sql += " AND schYr = %d" % schyr
    return getDig(sql)  
    
def formIds_forYear(schYr):
    sql = " SELECT f.id \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels cl ON c.level = cl.level \
             WHERE f.schYr = %d \
             ORDER BY cl.level" % int(schYr)
    return getList(sql)

def formNames_all():
    sql = " SELECT DISTINCT f.name \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels cl ON c.level = cl.level \
             WHERE cl.level > -10 \
             ORDER BY cl.level"
    return getList(sql)
    
def forms_byYear(year):
    sql = " SELECT f.id, f.name, cl.level \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE f.schYr = %d \
             ORDER BY cl.level" % year
    return getListTuples(sql)

def forms_forLevel_forYear(level, schYr):
    #rint 'forms_forLevel_forYear', level, schYr
    sql ="SELECT f.id, f.name \
            FROM forms f \
	    JOIN courses c ON c.id = f.course_id \
            JOIN course_levels cl ON cl.level = c.level \
           WHERE cl.level  = %d \
             AND f.schYr = %d" % (int(level), int(schYr))
    #rint  '    forms_forLevel_forYear  ', sql
    return getAllDict(sql)

def forms_pool():
    sql = " SELECT f.id, f.name, c.course_level \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels cl ON cl.level = c.level \
             WHERE cl.level > -10 \
               AND f.schYr = %s \
             GROUP BY f.name \
             ORDER BY c.level" % gVar.schYr
    return getListTuples(sql)
    
    
def forms_forCourse(course_id):
    sql = " SELECT f.id, f.name, cl.level \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels ct ON cl.level = c.course_level \
             WHERE c.id = %d \
               AND f.schYr = %d \
          ORDER BY cl.level " % (course_id, gVar.schYr)

    return getAllDict(sql)    
'''    
def forms_forCourse(course_id, result_type = 'dict'):
    sql = " SELECT f.id, f.name, cl.level \
              FROM forms f \
	      JOIN courses c ON c.id = f.course_id \
              JOIN course_levels cl ON cl.level = c.level \
             WHERE f.course_id = %d \
               AND f.schYr = %d \
          ORDER BY cl.level " % (course_id, gVar.schYr)

    if   result_type =='dict':      return getAllDict(sql)
    elif result_type =='by column': return getAllCol(sql)
    else:                           return getListTuples(sql)
'''      
def formCount_forCourse(course_id, result_type = 'dict'):
    sql = " SELECT COUNT( f.id) \
              FROM forms f \
             WHERE f.course_id =%d " % (int(course_id),)
    #rint sql
    return getDig(sql) 
    


def formGrades_forStudent(student_id):
    return 'temp','temp','temp'
    



#-  G     ----------------------------------------------------------------------
def gender(g):# converts db.res to str or str to db ready entry
    gender =""
    if g =="m":     gender = "Male"
    if g =="Male":  gender = "m"
    if g =="f":     gender = "Female"
    if g =="Female":gender = "m"
    return gender

def gradingStandard(standard_id):
    sql = "SELECT standard \
             FROM grading_standards \
            WHERE id = %d" % int(standard_id)
    return getStr(sql)

def gradeAverage_forStudygroup(student_id, studygroup_id, semester_no):
    assignmentIDs = assignmentIDs_forStudygroup(studygroup_id, semester_no)
    if not assignmentIDs: return 999

    total = 0
    assignmentCount = 1
    for assignment_id in assignmentIDs:
        grades = gradesForAssignment(student_id, assignment_id)
        if grades: 
            gradeT = grades['gradeT']
            gradeP = grades['gradeP']
            gTot = gradeT + gradeP
            if gradeT and gradeP:  gTot = gTot/2
            total += gTot
            if gradeT or gradeP:   assignmentCount += 1
            
    return total/assignmentCount

def gradeAverage_forBatch(student_id, form_id, semester_no):
    total = 0
    count = 0
    studygroups = studygroups_forForm(form_id)
    for studygroup in studygroups:
        studygroup_id = studygroup['id']
        gradeAve = gradeAverage_forStudygroup(student_id, studygroup_id, semester_no)
        if gradeAve < 101:
            total += gradeAve
            count += 1
    ave = 0
    if count: ave = str(total/count)
    if ave == 0: ave = 0
    return ave

    
def gradesForAssignment(student_id, assignment_id):    
    # rint student_id, assignment_id
    sql = "SELECT g.gradeT, g.gradeP \
             FROM grades_academic g \
            WHERE g.assignment_id=%d \
              AND g.student_id = %d" % (int(assignment_id), int(student_id))
    return getOneDict(sql)



# h -------------------------------

def hasPermission(feature):
    sql = "SELECT p.id \
             FROM staff s \
             JOIN permisions p ON p.id IN s.permisions \
            WHERE s.staff_id =  %d \
              AND p.name = '%s'" % (gVar.user_id, feature)
    #rint sql , fetch.getAllDict(sql)
    if getAllDict(sql):
          return True
    else: return False

#- I ---------------------------------------------------------------------------
def image_scale(image, maxWidth, maxHeight):
    width  = image.GetWidth()
    height = image.GetHeight()
    
    #rint "maxWidth  width maxHeight height", maxWidth , width, maxHeight, height
    ratio  = min( maxWidth / width, maxHeight/ height )
    #rint "ratio*width, ratio*height", ratio*width, ratio*height
    image  = image.Scale(ratio*width, ratio*height, wx.IMAGE_QUALITY_HIGH)
    return wx.BitmapFromImage(image)

def image_loadCtrl(ctrl, image, padding = 0):
    bmp = wx.BitmapFromImage(image)
    w, h = ctrl.GetSize()
    w = w - padding*2
    h = h - padding*2
    bmp = image_scale(bmp, w, h)        
    ctrl.SetBitmap(bmp)

def image_getIndex( path, imagePaths):
    """Retrieve index of image from imagePaths"""
    i = 0
    for image in imagePaths:
        if image == path:
            return i
        i += 1
    return -1

def image_resize( ctrl, image, size, padding):
    ctrl.SetSize(size)
    if total:
        w = size[0] - padding*2
        h = size[1] - padding*2
        bmp = image_scale(image, w, h)
        ctrl.SetBitmap(bmp)
        
def is_recurring_monthly(product_id):
    sql = "SELECT recurring_monthly \
             FROM acc_products \
            WHERE id =%d" % product_id
    return getDig(sql)
    
def is_recurring(product_id):
    sql = "SELECT is_recurring \
             FROM acc_products \
            WHERE id =%d" % product_id
    return getDig(sql)

def is_unique_product(description):
    sql = "SELECT * \
             FROM products \
            WHERE description = '%s'" % description
    res = getCount(sql)
    print 'is_unique_product > getCount', res
    if res == 0: return True
    else: return False
    


# J------------------------------

def journal_entries_by_schYr(yr):
    sql = "SELECT * \
             FROM acc_journal \
             JOIN acc_journal_items ON acc_journal_items.journal_id = acc_journal.id \
              AND schYr = %d" % yr
    return getAllDict(sql)

#-   L     ---------------------------------------------------------------------

def levels_forSchool(school_id):
    sql ="SELECT cl.level, cl.name \
            FROM courses c \
            JOIN course_levels cl ON cl.level = c.level \
       LEFT JOIN schools sch ON sch.id = cl.school_id \
           WHERE c.schYr = %d \
             AND cl.school_id =%d \
        GROUP BY cl.level \
        ORDER BY cl.level " % (gVar.schYr, school_id) #  GROUP BY cl.level \
    #rint ' levels_forSchool :',sql, getAllDict(sql)
    return getAllDict(sql)


def levelName(level):
    sql = " SELECT name \
              FROM course_levels \
             WHERE id = %d" % level
    return getStr(sql)

def levelTitle_level(course_level):  # returms:course_title
    sql = " SELECT cl.name \
              FROM course_levels cl  \
             WHERE cl.level = %d" % course_level
    return getStr(sql)

def livesWith(guardian_id):
    #rint '  guardian_id   '  , guardian_id
    if guardian_id :
        sql = " SELECT name \
                  FROM guardians \
                 WHERE id = %d" % int(guardian_id)
        return getStr(sql)
    else: return ''
    
def levelTitle(course_level):
    sql = "SELECT name \
             FROM course_levels \
            WHERE id = %d " % course_level
    return getStr(sql)

def level_level_id(level_id):
    sql = " SELECT level\
              FROM course_levels \
             WHERE id = %d" % level_id
    return getDig(sql)

def level_unused(level):
    sql = "SELECT id FROM courses WHERE level =%d" % level
    if getCount(sql):
           return True
    else : return False
# M ---------------------------------

def msg(txt):
    return wx.MessageBox(txt, 'Info', wx.OK | wx.ICON_INFORMATION)



def monthName(month_number):
    sql = "SELECT month_name \
             FROM school_year \
            WHERE month_number = %d" % month_number
    print sql
    return getStr(sql)

def ck_ref_last():
    sql = "SELECT MAX(ck_ref) FROM acc_invoices"
    res = getList(sql)
    schYr = str(gVar.schYr)
    schYr = schYr[-2:]
    if any(res):
        ck_ref = res[0].split('-')
        ck_ref_new = int(ck_ref[1]) + 1
       
        if ck_ref_new > 999:
            ck_ref_new = str(ck_ref_new).zfill(5)
        elif ck_ref_new > 99:
            ck_ref_new = str(ck_ref_new).zfill(5)
        elif ck_ref_new > 9:
            ck_ref_new = str(ck_ref_new).zfill(5)
        else:
            ck_ref_new = str(ck_ref_new).zfill(5)
        
        ck_ref = 'CK'+schYr+'-'+str(ck_ref_new)
    else:
        ck_ref = 'CK'+schYr+'-00001'
    return ck_ref

def month_last_paid(student_id, yr, type_id):
    sql = "SELECT MAX(ii.month_to) \
             FROM acc_invoices       i \
             JOIN acc_invoice_items ii ON i.id = ii.invoice_id \
             JOIN acc_products       p ON p.id = ii.product_id \
            WHERE student_id = %d \
              AND i.schYr    = %d \
              AND p.type_id  = %d " % (student_id, yr, type_id)
    return getDig(sql)

# r -----------------------------------
def NoInduk(student_id, schYr):
    sql = "SELECT s.NoInduk \
             FROM students s \
             JOIN students_by_form sbf ON s.id = sbf.student_id \
             JOIN forms f ON f.id = sbf.form_id \
            WHERE s.id = %d AND f.schYr = %d" % (student_id, schYr)
    print sql
    return getStr(sql)
    
    
def nextCourse(student_id):
    if not student_id: return ''
    sql = " SELECT cl.name \
              FROM course_levels cl \
	      JOIN courses c ON cl.level = c.course_level \
              JOIN students_by_form sbf ON c.id = sbf.rereg_course_id \
             WHERE sbf.student_id = %d \
               AND c.schYr = %d" % (int(student_id), (gVar.schYr+1))
    return getStr(sql)

def nis(student_id):
    sql = "SELECT nis \
             FROM nis \
            WHERE student_id = %d \
              AND %d BETWEEN schYr_from AND schYr_to" % (student_id, gVar.schYr)
    return getStr(sql)

def nextID(table_name):
    sql = "SELECT Auto_increment \
            FROM information_schema.tables \
           WHERE table_name='%s'" % table_name
    #rint sql
    return getDig(sql)

#-   O     ---------------------------------------------------------------------
def occ(id):
    sql = " SELECT name \
              FROM occupations \
             WHERE id = %d " % id
    return getStr(sql)
                
def overallGrade_forAssignment(student_id, assignment_id):
    overallGrade = 10
    grades = gradesForAssignment(student_id, assignment_id)
    if grades:
        gList = grades.split(',')
        for item in gList:
            overallGrade = 5
            
            ## much more to be done - weighting etc
    return overallGrade

def openDialog(dlg, item_id=0):
    dlg = dlg.create(None)
    try:
        dlg.displayData(int(item_id))
        if dlg.ShowModal() == wx.ID_OK:
            item_id = dlg.getItemId()
    finally:    
        dlg.Destroy()
    return item_id

#-   P     ---------------------------------------------------------------------
def parentName(id):
    sql = " SELECT name \
              FROM guardians \
             WHERE id = %d" % id
    return getStr(sql)

def parentDetails(id):
    sql = " SELECT * \
              FROM guardians \
             WHERE id = %s" % id
    return getOneDict(sql)

def phoneNos(id):# for appending to a list (almost duplicate of telpNoList
    sql = " SELECT phone_number \
              FROM phone_numbers \
             WHERE guid = %s"

def population_ofBatch(form_id, do_filter = '', want = 'dict'):
    #rint form_id, do_filter , want
    sql = "SELECT COUNT(s.id) \
             FROM students s \
             JOIN students_by_form sbf ON sbf.student_id = s.id \
            WHERE sbf.form_id = %d \
              AND %d BETWEEN s.register_schYr AND s.exit_schYr " % (int(form_id), gVar.schYr)
    
    if do_filter:  sql +=  " AND sbf.rereg_status = '%s' " % do_filter
    #rint sql
    return getDig(sql)

def previous_school_id(nis):
    sql = "SELECT previous_school_id \
             FROM nis WHERE nis = '%s'" % nsi


def product_details(product_id):
    sql = "SELECT description, price \
             FROM acc_products WHERE id =%d" % int(product_id)
    res = getOneDict(sql)
    if res:
        return (res['description'], int(res['price']))
    else:
        return ('', 0)
    
def product_price(product_id):
    sql = "SELECT price \
             FROM acc_products \
            WHERE id = %d" % product_id
    return getDig(sql)

def get_product_type_id(product_id):
    sql = "SELECT type_id FROM acc_products WHERE id = %d" % int(product_id)
    return getDig(sql)


#-   R     ---------------------------------------------------------------------
def registeredStudents(bool, yr): # returns list (students_id)
    # looks for students that are registering
    # for the school but are not yet active
    sql = "SELECT id \
             FROM students \
            WHERE admision_status = 'paid' \
              AND register_schYr = %d \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (yr, gVar.schYr) 
    return getAllDict(sql)

def re_registrationDetails_forBatch(form_id):
    form_id = int(form_id)
    formDetails = []
    #  form_id, 'form', formName, population, leaving, retake, may_stay, reregistered, paid
    formDetails.append(form_id)
    formDetails.append('form')
    
    formDetails.append(formName(form_id))
    
    population = population_ofBatch(form_id, '', 'count')
    formDetails.append(population)
   
    leaving = population_ofBatch(form_id, 'leave', 'count')
    formDetails.append(leaving)
    
    retake = population_ofBatch(form_id, 'retake', 'count')
    formDetails.append(retake)
    
    may_stay = population - leaving - retake
    formDetails.append(may_stay)
    
    reregistered = population_ofBatch(form_id, 'stay', 'count')
    formDetails.append(reregistered) 
     
    paid = population_ofBatch(form_id, 'paid', 'count')
    formDetails.append(paid)
    return formDetails

def reregList_forBatch(form_id, sqlfilter = False):  
    # returns tuple list (students_id, first_name, rereg_status, rereg_course_id)
    # of existing students in form
    sql = " SELECT s.id, s.name, sbf.rereg_status, sbf.rereg_course_id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
             WHERE sbf.form_id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (form_id, gVar.schYr)
    if sqlfilter:
        sql += " AND sbf.rereg_status = %d" % sqlfilter
    return getAllDict(sql)

def registrationTotals_forCourse(course_level): # returns [course_level, type, name, rereg, retake, new_reg, total, classes, size, spaces]
    if not course_level: return
    
    title = courseTitle(course_level)

    rereg   = countStudents_reregFeePaid_forCourse(course_level)
    retake  = countStudents_retakingCourse(course_level)
    new_reg = countStudents_newForCourse(course_level) #, 'count')  # new_reg | studentIDs_newreg_forCourse
    
    total   = rereg + retake + new_reg
    classes = classCount_forCourse(course_level)
    size    = recomended_classSize(course_level)
    spaces  = classes * size - total
    
    return list((int(course_level), 'course_level', title, rereg,
                         retake, new_reg, total, classes, size, spaces))
    
def re_regDetails_forStudent(student_id, yr): 
    sql = "SELECT s.id, s.first_name, cl.level, cl.name, \
                 cs.id, sbf.rereg_status, sbf.rereg_course_id, f.id \
             FROM students s \
             JOIN students_by_form sbf ON sbf.student_id = s.id \
             JOIN forms   f ON f.id = sbf.form_id  \
	     JOIN courses c ON c.id = f.course_id \
             JOIN course_levels cl ON cl.level = c.course_level \
            WHERE s.id = %d \
              AND c.schYr = %d" % (int(student_id), yr)
    return getOneDict(sql)

def reregDetails_forStudent(student_id):
        sql ="SELECT s.first_name, sbf.id as bs_id, sbf.rereg_status, sbf.rereg_course_id, \
                     f.id as form_id \
                FROM students s \
                JOIN students_by_form sbf ON sbf.student_id = s.id \
                JOIN forms f ON f.id = sbf.form_id  \
               WHERE s.id = %d AND f.schYr = %d " % (student_id, gVar.schYr)
        return getOneDict(sql)
        
def regStatus(re_reg_id):
    data = studentRegDetails(re_reg_id)
    return data['isEnrolled']   
  
def removeWithdrawnStudents(listOfIDs): 
    x = ','.join(listOfIDs)
    listOfIDs = "'%s'" % x
    sql = "SELECT * \
             FROM students \
            WHERE FIND_IN_SET(id, %s) \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (listOfIDs, gVar.schYr)
    return getList(sql)
  

def reverseList(list):
    newList=[]
    i = len(list) 
    for idx in range(i):  
        x = i-idx-1
        newList.append(list[x])
    return newList


def roamingStudents_forBatchLevel(form_id):
    level = formInfo2(form_id)['course_level']
    
    sql = "SELECT s.id \
             FROM students s \
             JOIN students_by_form sbf ON s.id = sbf.student_id \
             JOIN forms   f ON f.id = sbf.form_id \
	     JOIN courses c ON c.id = f.course_id \
             JOIN course_levels cl ON cl.level = c.course_level \
            WHERE '%s' BETWEEN s.register_schYr AND s.exit_schYr \
              AND course_level = %d " % (gVar.schYr, level,)

def roamingStudents_forBatch(form_id):
    sql = "SELECT s.id \
             FROM students s \
             JOIN students_by_form sbf ON s.id = sbf.student_id \
            WHERE s.schYr_to <='%s' \
              AND form_id = %d" % (gVar.schYr, form_id)
    res = getList(sql)
    if res : ids = ",".join(res)
    else: ids = ''
    
    course_level = courseId_forBatch(form_id)
    sql = "SELECT s.id \
             FROM students s \
             JOIN students_by_form sbf ON s.id = sbf.student_id \
            WHERE '%s' BETWEEN s.register_schYr AND s.exit_schYr \
              AND rereg_course_id = %d \
              AND NOT FIND_IN_SET(s.id, '%s') \
                           " % (gVar.schYr, course_level, ids)
    return getAllDict(sql)
    
def recomended_classSize(course_id):
    sql = "SELECT recomended_class_size \
             FROM courses \
            WHERE id = %d" % course_id
    return getDig(sql)

#-   S     ---------------------------------------------------------------------

def selectedItems(listCtrl):
    """    Gets the selected items for the list control.
    Selection is returned as a list of selected indices,
    low to high.
    """
    selection = []
    index = listCtrl.GetFirstSelected()
    selection.append(index)
    while len(selection) != listCtrl.GetSelectedItemCount():
      index = listCtrl.GetNextSelected(index)
      selection.append(index)

    return selection

def schoolID_forLevel(course_level):
    sql = "SELECT school_id \
             FROM course_levels \
            WHERE course_level = %d  " % (course_level, )
    #rint sql
    try:    return getOneDict(sql)['school_id']
    except: return 0

def schoolID_forCourse(course_id):
    sql = "SELECT cl.school_id \
             FROM courses c \
             JOIN course_levels cl ON c.course_level = cl.level \
            WHERE c.id = %d  " % course_id
    #rint sql
    try:    return getOneDict(sql)['school_id']
    except: return 0
    
def schoolID_forBatch(form_id):
    sql = "SELECT cl.school_id \
             FROM course_levels cl \
	     JOIN courses c ON cl.level = c.course_level \
             JOIN forms   f ON c.id = f.course_id \
            WHERE f.id =%d" % form_id
    return getDig(sql)

def schoolID_forExculSet(exculset_id):
    sql = "SELECT school_id \
             FROM excuric_schedule \
            WHERE id =%d" % exculset_id
    return getDig(sql)



def schoolName(id): # working May 2012
    sql = "SELECT name \
             FROM schools \
            WHERE id = %d" % id
    return getStr(sql)

    res = getOneDict(sql)
    name, school_type = res['name'], res['school_type']
    t = "%s: %s" % (name, school_type)
    return t

def schoolInfo(school_id):
    sql = "SELECT * FROM schools WHERE id = %d" % school_id
    return getOneDict(sql)


def schYr_forBatch(form_id):
    sql = "SELECT schYr \
             FROM forms  \
            WHERE id =%d" % form_id
    return getDig(sql)


def schYr():
    return
    gVar.schYr  = int(datetime.datetime.today().year)
    # $rint "datetime.datetime.today().year ", gVar.schYr
    #rint 'get school year'
    month = int(datetime.datetime.today().month)
    #rint "datetime.datetime.today().month ", month
    #if month > 6: gVar.schYr +=1
    return gVar.schYr

def shipName(ship_id): # working May 2012
    if ship_id:
        sql = " SELECT name \
                  FROM ships \
                 WHERE id = %d" % int(ship_id)
        return getStr(sql)
    else: return ''
     
def sortedList(list, on=0):
    if list: return sorted(list, key=lambda item: item[on])
    else:    return []



# ---------------  subjects -----------------------


def subjectTitle_forStudyGroup(studygroup_id):
    sql = " SELECT subject_title \
              FROM subjects st \
              JOIN studygroups sg ON st.id = sg.subject_title_id \
             WHERE sg.id = %d" % studygroup_id
    return getStr(sql)
    

def subjectTitle(subject_title_id):
    sql = " SELECT subject_title \
              FROM subjects \
             WHERE id = %d" % subject_title_id
    return getStr(sql)


# ------------------   studygroups   -----------------------
def studygroupPopulation(studygroup_id):
    return len(studentIDs_inStudygroup(studygroup_id))
    
def studygroupPool(studygroup_id):
    studygroup_pool = []
    sql = "SELECT form_ids  \
             FROM studygroups   \
            WHERE id = %d" % studygroup_id
    #rint sql
    form_ids = getStr(sql).split(',')
    if form_ids: 
        for form_id in form_ids:
            groupName = "groupName" # row['groupName']
            if groupName == 'Entire':
                pass# studygroup_population += form_population(form_id)
            else:
                pass
                # $rint "how to do divisions"
                #sql ="SELECT f.`studentIDs` FROM form_division_students f \
                #        WHERE f.`division`=%s AND f.`form_id`=%d" %(groupName, form_id)
                #row  = getOneDict(sql)    
                #listOfIDs = row['studentIDs'].split(',')
                #$rint '3 listOfIDs=', listOfIDs
                #listOfIDs = removeWithdrawnStudents(listOfIDs)
                #studygroup_population  += len(listOfIDs)
    return studygroup_pool

def studygroupData(studygroup_id):
    '''sql = "SELECT student_id \
             FROM studygroup_students sgs \
             JOIN studygroups sg ON sg.ig = sgs.studygroup_id \
            WHERE sg.id = %d" % studygroup_id
    
    sql = "SELECT id, staff_id \
             FROM studygroups \
            WHERE id = %d" % studygroup_id
    x= getOneDict(sql)'''
    return "????"

def studygroupName(sg_id):
    sql = " SELECT st.subject_title \
              FROM studygroups sg \
              JOIN subjects st ON st.id= sg.subject_title_id \
             WHERE sg.id =%d" % sg_id
    #rint sql
    return getStr(sql)

def studygroupTeacher(sg_id):
    sql = " SELECT s.name \
              FROM studygroups sg \
              JOIN staff s ON s.id = sg.staff_id\
             WHERE sg.id =%d" % sg_id
    #rint sql
    return getStr(sql)

def studygroups_forLevel(level):
    sql = " SELECT s.name \
              FROM studygroups sg \
              JOIN subjects        s ON s.id= sg.subject_id\
              JOIN forms           f ON FIND_IN_SET(f.id, sg.form_ids) \
	      JOIN courses         c ON c.id = f.course_id \
              JOIN course_levels  cl ON cl.level = c.course_level \
             WHERE cl.level = %d" % level
    return getAllDict(sql)

#...........  students  ........................
def studentsLeaving_courseTitle(course_level):
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
	      JOIN courses            c ON c.id =   f.course_id \
             WHERE c.course_level = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr \
               AND f.rereg_status = 'leave'" % (course_level, gVar.schYr)
    return getList(sql)

def studentsLeaving_course(course_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
	      JOIN courses            c ON c.id = f.course_id \
              JOIN course_levels     cl ON cl.level = c.course_level \
             WHERE c.id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr \
               AND f.rereg_status = 'leave'" % (course_id, gVar.schYr)
    return getList(sql)

def students_reregPaid_inBatch_nextCourse(form_id, course_level):
    sql = " SELECT s.id, name \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN course_students   cs ON s.id = cs.student_id \
             WHERE %d BETWEEN s.register_schYr AND s.exit_schYr \
               AND f.id =%d \
               AND sbf.rereg_status = 'paid' \
               AND sbf.rereg_course_id = %d" % (gVar.schYr, form_id, course_level)
    return getAllDict(sql)

def students_reregPaid_inBatch(form_id):
    sql = " SELECT s.id, name \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
             WHERE %d BETWEEN s.register_schYr AND s.exit_schYr \
               AND sbf.rereg_status = 'paid' " % (form_id, gVar.schYr)
    return getAllDict(sql)

def students_reregStatus_inBatch(form_id):
    school_id = schoolID_forBatch(form_id)
    sql ="SELECT s.id, sbf.rereg_status, s.name, n.nis, sbf.rereg_course_id \
            FROM students s \
            JOIN students_by_form sbf ON s.id = sbf.student_id \
            JOIN forms              f ON f.id = sbf.form_id \
       LEFT JOIN nis                n ON s.id = n.student_id \
           WHERE sbf.form_id = %d \
             AND '%s' BETWEEN s.register_schYr AND s.exit_schYr \
             AND f.schYr = %d \
             AND n.school_id = %d GROUP BY s.id" % (int(form_id), gVar.schYr, gVar.schYr, school_id)
    return getAllCol(sql) 
 
def students_reregStatus_untransfered_inBatch(form_id):
    sql = " SELECT s.id, sbf.rereg_status, s.first_name, s.last_name, n.nis \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN nis                n ON s.id = n.student_id \
             WHERE sbf.form_id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (int(form_id), gVar.schYr)
    return getAllCol(sql)



def studentDetails_id(student_id): # working May 2012
    sql = "SELECT * \
             FROM students \
            WHERE id = %d" % int(student_id)
    return getOneDict(sql)

def student_callName_id(student_id):
    sql = "SELECT callname \
             FROM students \
            WHERE id = %d" % int(student_id)
    return getStr(sql)


def student_fullName_nis(nis):
    sql = "SELECT name \
             FROM students s \
             JOIN nis n ON s.id = n.student_id \
            WHERE n.nis = %s" % nis
    return getStr(sql)

def studentFullName(student_id):
    sql = "SELECT name \
             FROM students \
            WHERE id = %d" % student_id
    res = getOneDict(sql)
    if not res : return ''
    
    string = res['name']
    while '  ' in string:
        string = string.replace('  ', ' ')

    return string

def studentSchDetails(student_id):
    sql = "SELECT sbf.form_id, n.nis, s.name, \
                 s.dob, s.gender, s.ship_id, f.course_level, cl.school_id, s.national_no, cl.level \
             FROM students s \
        LEFT JOIN nis                n ON s.id = n.student_id \
             JOIN students_by_form sbf ON sbf.student_id = s.id \
             JOIN forms              f ON sbf.form_id    = f.id \
	     JOIN courses            c ON c.id           = f.course_id \
             JOIN course_levels     cl ON cl.level       = c.course_level \
            WHERE s.id = %d \
              AND f.schYr = %d " % (int(student_id), gVar.schYr)
    #rint sql
    return getOneDict(sql)

def students_forSch(school_id, schYr = gVar.schYr):
    sql ="SELECT s.id, n.nis, s.name, f.name \
                    FROM students s \
               LEFT JOIN nis                n ON s.id = n.student_id \
                    JOIN students_by_form sbf ON s.id = sbf.student_id \
                    JOIN forms              f ON f.id = sbf.form_id \
                   WHERE %d BETWEEN n.schYr_from AND n.schYr_to\
                     AND n.school_id = %d ORDER BY s.id" % (schYr, school_id)
    #rint sql
    return getAllDict(sql)


def studentIDs_forBatch(form_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
             WHERE sbf.form_id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr" % (form_id, gVar.schYr)
    #rint sql
    return getList(sql)

def studentsLeaving_form(form_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
             WHERE f.id = %d \
               AND '%s' BETWEEN s.register_schYr AND s.exit_schYr \
               AND f.rereg_status = 'leave'" % (form_id, gVar.schYr)
    return getList(sql)

def students_forForm(form_id, want='dict'):
    sql = " SELECT s.id, name \
              FROM students s \
              JOIN students_by_form sbf ON sbf.student_id = s.id \
             WHERE sbf.form_id = %d \
               AND %d BETWEEN s.register_schYr AND s.exit_schYr " % (form_id, gVar.schYr)
    if want == 'dict':
        return getAllDict(sql)
    else:
        return getAllCol(sql)
    
def students_inForm(form_id, want='dict'):
    school_id = schoolID_forBatch(form_id)
    sql = " SELECT s.id, s.name, n.nis \
              FROM students s \
              JOIN students_by_form sbf ON sbf.student_id = s.id \
              JOIN nis                n ON s.id = n.student_id \
             WHERE sbf.form_id = %d \
               AND n.school_id = %d \
               AND %d BETWEEN s.register_schYr AND s.exit_schYr " % (form_id, school_id, gVar.schYr)
    if want == 'dict':
        return getAllDict(sql)
    else:
        return getAllCol(sql)

def studentIDs_forExcul(excuric_id):
    sql = "SELECT student_id \
             FROM excuric_students \
            WHERE excuric_id = %d" % int(excuric_id)
    #rint sql,  getList(sql)
    return getList(sql)
        
def students_inLevel(level):
    sql = "SELECT s.id, s.name, n.nis \
             FROM students s \
             JOIN students_by_form cs ON s.id = sbf.student_id \
             JOIN nis               n ON s.id = n.student_id \
	     JOIN courses           c ON c.id = f.course_id \
             JOIN course_levels    cl ON cl.level = c.course_level \
            WHERE cl.level = %s \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (level, gVar.schYr)
    return getAllCol(sql)

def students_matching(name):    
    sql = "SELECT * FROM students WHERE"
    if name:
        sql += " name LIKE '%' " % name
        return getAllDict(sql)
    else:
        return ''


def students_not_in_form(form_id):
    formYr        = schYr_forBatch(form_id)
    course_level  = courseId_forBatch(form_id)
    sql = "SELECT DISTINCT s.id \
             FROM students s \
             JOIN students_by_form sbf ON sbf.student_id = s.id \
        LEFT JOIN forms              f ON f.id = sbf.form_id \
            WHERE (sbf.rereg_course_id = %d OR s.enter_course_id =%d) \
              AND s.id NOT IN (SELECT s.id \
                              FROM students s\
                              JOIN students_by_form sbf ON sbf.student_id = s.id  \
                              JOIN forms              f ON f.id = sbf.form_id \
	                         JOIN courses         c ON c.id = f.course_id \
                              JOIN course_levels     cl ON cl.level = c.course_level \
                             WHERE cl.level = %d)" % (course_level, course_level, course_level)
    #rint sql
    return getList(sql)


def studentIDs_inStudygroup(studygroup_id):
    sql = "SELECT s.id \
             FROM studygroup_students sg \
             JOIN students s ON s.id = sg.student_id \
            WHERE studygroup_id = %d \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr  " % (studygroup_id, gVar.schYr)
    #rint sql
    return getList(sql)

def sql_students_forSch_remaining(school_id, id_set, schYr = gVar.schYr):
    sql ="SELECT s.id, name \
                    FROM students s \
               LEFT JOIN nis n ON s.id = n.student_id \
                   WHERE %d BETWEEN n.schYr_from AND n.schYr_to\
                     AND n.school_id = %d \
                     AND NOT FIND_IN_SET(s.id, '%s') \
                ORDER BY s.id" % (schYr, school_id, id_set)
    #rint sql
    return sql
    #return getAllCol(sql)

def studentIDs_inBatch(form_id, do_filter = False, want = 'dict'):
    sql = "SELECT s.id \
             FROM students s \
             JOIN students_by_form sbf ON sbf.student_id = s.id \
            WHERE sbf.form_id = %d \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (form_id, gVar.schYr)
    
    if do_filter:
        sql +=  "AND sbf.rereg_status = '%s'" % do_filter
    
    sql += " GROUP BY s.id"

    if want == 'dict':
         res = getAllDict(sql)
    elif want == 'list':
         res = getList(sql)
    else:res = getAllCol(sql)
    #rint sql
    return res
     
       
    # new 9 june 2012 --------------------
def studentIDs_joiningCourse(course_id, schYr, do_filter = False,  want = 'dict'): 
    sql = "SELECT s.id \
             FROM students s \
             JOIN courses c ON s.enter_course_id = c.id \
	     JOIN nis     n ON s.id = n.student_id \
            WHERE cl.level = %d \
              AND n.schYr_from = %d" % (course_id, schYr)
    if do_filter:
        sql +=  "AND sbf.admission_status_id = '%s' " % do_filter
    return getRes(sql, 'list')

def studentIDs_inCourse(course_id, do_filter = False,  want = 'dict'): 
    sql = " SELECT s.id \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
             WHERE sbf.course_id = %d \
               AND f.schYr = %d" % (course_id, gVar.schYr)
    if do_filter:
        sql +=  "AND sbf.rereg_status = '%s'" % do_filter
    return getRes(sql, want)

def students_not_in_studygroup(studygroup_id):
    sql = "SELECT student_id \
             FROM students \
            WHERE NOT FIND_IN_SET(s.id, SELECT student_id \
	                                  FROM students_by_studygroup \
					 WHERE studygroup_id = %d)" % studygroup_id
    return getList(sql)


def studygroups_forForm(form_id): 
    sql = "SELECT sg.id, s.name \
             FROM studygroups sg \
             JOIN subjects     s ON s.id = sg.subject_id \
            WHERE FIND_IN_SET(%d, sg.form_ids)" % form_id
    #rint sql
    return getAllDict(sql)

def students_inCourse(course_id): 
    sql = " SELECT s.id, s.name, sbf.rereg_status\
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
             WHERE f.course_id = %d \
               AND f.schYr = %d " % (course_id, gVar.schYr)
    #rint sql
    return getAllDict(sql)

def students_inCourseV(course_id): 
    sql = " SELECT DISTINCT s.id, sbf.rereg_status, s.name \
              FROM students s \
              JOIN students_by_form sbf ON s.id = sbf.student_id \
              JOIN forms              f ON f.id = sbf.form_id \
             WHERE f.course_id = %d  \
                OR (sbf.rereg_course_id = %d AND f.schYr = (%d -1 ) ) \
          GROUP BY s.id" % (course_id, course_id, gVar.schYr)
    #rint sql
    return getAllCol(sql)
 
def studentIDs_forLevel(age_level=0, schYr = 2000, want = 'dict'): 
    sql = "SELECT s.id \
             FROM students s \
             JOIN forms               f ON s.form_id = f.id \
	     JOIN courses             c ON c.id      = f.course_id \
             LEFT JOIN course_levels cl ON c.course_level = cl.level \
            WHERE cl.level = %d \
              AND s.admissiion_year = %d \
              AND '%s' BETWEEN s.register_schYr AND s.exit_schYr " % (int(age_level), schYr, gVar.schYr)
    return getRes(sql, want)

def studentInfoPopup(student_id):
    student_id = int(student_id)
    
    name         = studentFullName(student_id)
    name  = '-'
    course_title = '-'
    name   = '-'
    age          = '-'
    gender       = '-'
    ship         = '-'
    
    if student_id:
        studentDetails = studentSchDetails(student_id)
        if studentDetails:
            school_id    = studentDetails['school_id']
            name  =  schoolName(school_id)
            
            course_level = studentDetails['course_level']
            course_title    =  courseTitle(course_level)
            
            age    = studentDetails['birth_date']
            gender =  gender(studentDetails['gender'])
            ship   =  shipName(studentDetails['ship_id'])
        
        form_id =  formID_forStudent(student_id)
        if form_id: name =  formName(form_id)

    line1 = 'Name: %s,  %s'  % (name, gender)
    line2 = 'DOB: %s,    SHIP: %s'  % (age, ship)
    line3 = 'BATCH: %s, %s, %s' % (name, course_title, name)
    
    mnu_abs = wx.Menu()
    mnu_asbf.AppendItem(wx.MenuItem(mnu_abs, -1, line1))
    mnu_asbf.AppendItem(wx.MenuItem(mnu_abs, -1, line2))
    mnu_asbf.AppendItem(wx.MenuItem(mnu_abs, -1, line3))
        
    #mnu_asbf.AppendSeparator()
    
    return mnu_abs   
        
        
#-   ------ subject ------------------------------------------------------------
def studygroupIDs_forBatch(form_id):
    sql = "SELECT id \
             FROM studygroups \
            WHERE FIND_IN_SET(%d, form_ids)" % int(form_id)
    return getList(sql)
    
def removeDups(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    
    
def studygroups_forForm_forTeacher(form_id, staff_id):
    sql = "SELECT sg.id \
             FROM studygroups sg \
             JOIN subjects s ON s.id = sg.subject_id \
            WHERE sg.staff_id = %d \
            AND FIND_IN_SET(%d, sg.form_ids)" % (staff_id, form_id)
    return getList(sql)

def getStudygroups_forBatch(form_id):
    sql = "SELECT id \
             FROM studygroups \
            WHERE FIND_IN_SET(%d, form_ids)" % (form_id, form_id)
    return getList(sql)

def studygroup_isUsed(studygroup_id):
    sql = " SELECT COUNT(id) \
              FROM studygroups \
             WHERE id = %d" % int(studygroup_id)
    if getDig(sql):
          return True
    else: return False

def subjectTitle_forForm(form_id):
    sql = " SELECT s.name \
              FROM subjects s \
              JOIN studygroups sg ON s.id = sg.subject_id \
             WHERE FIND_IN_SET(%d, sg.form_ids)" % int(form_id)
    return getStr(sql)

#-   T     ---------------------------------------------------------------------
def tableData(tablename):
    sql = "SELECT * \
             FROM %s" % tablename 
    return getAllCol(sql)

def telpNosString(guid): # for entry into a multiline textbox
    sql = "SELECT guid, phoneNo, phone_location \
             FROM phone_numbers \
            WHERE guid = %s" % guid 
    res  = getAllDict(sql)
    list = ''
    if res:
        for row in res:
            list +=row['phone_number'] + "\n"
    return list
    
def telpNoList(guid):# for appending to a list
    sql = "SELECT guid, phone_number, phone_location \
             FROM phone_numbers \
            WHERE guid = %s" % guid
    return getAllDict(sql)

def teacherNames_forSubject(subject_id):
    str=''
    if subject_id:
        teacherID_list, newList= teacherIDs_forSubject(subject_id), []
        for teacher_id in teacherID_list: newList.append(teacherName(id))
        str = ','.join(newList)
    return str

def teachers_forSch(sch_id):
    sql="SELECT id, username \
           FROM staff \
          WHERE employee_category_id = 2"
    return getList(sql)
    
def teachers_otherThan(teacher_list=''):
    sql = " SELECT id, username \
              FROM staff \
             WHERE employee_category_id = 2"
    if teacher_list:
        sql += " AND NOT id IN (%s)" % teacher_list
    return getAllDict(sql)
    
def teachers_forBatch(form_id): # used x 1
    if form_id:
        sql = " SELECT counceler_ids \
                  FROM forms \
                 WHERE id = %d" % form_id
        res = getStr(sql)
    if res:
        staff_ids = res['staff_ids'].split(',')
        return staff_ids
    else: return []

def teacherNames_forBatch(form_id): # used x 2
    staff_id_list = teachers_forBatch(form_id)
    namesList = []
    for staff_id in staff_id_list:
        name = teacherName(staff_id)
        if name:namesList.append(name)
    namesString = ','.join(namesList)
    return namesString
    
def teachers_notInSubjects(testlist=[]):
    newlist=[]
    testlist=','.join(testlist)
    sql = "SELECT id \
             FROM staff \
            WHERE staff_type_id = 1 \
              AND status = True \
              AND NOT FIND_IN_SET(id, %s)" % testlist
    return getList(sql)
 
    
def teacherIDs_forSubject(studygroup_id):
    if not studygroup_id:return []
    sql = "SELECT staff_id \
             FROM studygroups \
            WHERE id = %d" % studygroup_id         
    res = getStr(sql)
    return res.split(',')

def travelsWith(id):
    sql = "SELECT travelsWith \
             FROM traveloptions \
            WHERE travelsWith_id = %d" % id
    return getStr(sql)


#-   U     ---------------------------------------------------------------------
def User_id(username):
    sql = "SELECT id \
             FROM customers \
            WHERE username = '%s'" % username
    return getStr(sql)


#-------------------------------------------------------------------------------
# relating to addresses
#-------------------------------------------------------------------------------
def addressRes(addr_id):
    sql = "SELECT * \
             FROM addresses \
            WHERE id = '%s'" % addr_id
    return getAllDict(sql)
    
def address(addr_id):
    address = ""
    sql = "SELECT * \
             FROM addresses \
            WHERE id = %d" % addr_id
    addr = getOneDict(sql)
     
    if not addr: return address
    addrItems = addr['address'].split(",")
     
    if addr['livesInEstate']:  
        address += EstateAddress(addrItems, addr) 
    else:
        if addr['street']:
            address += "%s, #%s \n" % (addr['street'], addr['houseNo'])
        elif addr['houseNo']:
            address += "%s \n" % ( addr['houseNo'],)    
                # run through items in:, addrItems
    for item_id in addrItems:
        sql = "SELECT * \
                 FROM address_items \
                WHERE id = %d" % item_id
        res = getOneDict(sql)
        if res: 
            type_id = res['itemType_id']
            if type_id < 3:
                pass
            elif type_id == 3: # road
                if addr['rd_km']:
                    address += "%s,  Km.%s \n" % (res[name], str(addr['rd_km']))
                else: address += "%s\n" % (res[name],)   
                 
            elif type_id == 6: # district
                if addr['postCode']:
                    address += "%s Post Code:%s\n" % (
                                res[name], str(addr['postCode']),)
                else: 
                    address += "%s\n" % res[name]
                     
            else:
                address += "%s\n" % (res[name],)
    return address 
    
def estateAddress(addrItems, addr):
    estateAddress = ""
    for item_id in addrItems:
        # find the street in estate
        sql = "SELECT * \
                 FROM address_items \
                WHERE id=%s \
                  AND item_type" % (item_id,)
        res = getOneDict(sql)
        if res: estateAddress += "%s, #%s\n" % (res[name], addr['houseNo'],)
        # find the estate
        sql = "SELECT * \
                 FROM address_items \
                WHERE id = %s \
                  AND item_type=2" % (item_id,)
        res = getOneDict(sql)
        if res: 
            if addr['blockNo']:
                estateAddress += "Block:%s  " % (str(addr['blockNo']),)
            estateAddress += "%s \n" % res[name]
    return estateAddress
    
def addressLine(addr_id):
    address = ""
    sql = "SELECT * \
             FROM addresses \
            WHERE id = %d" % addr_id
    addr = getOneDict(sql)
    if addr:
        if addr['street']:
            address += "%s #%s ," % (addr['street'], addr['houseNo'])
        elif addr['houseNo']: address += "%s, " % addr['houseNo']
            
        addrItems = str(addr['addrItem_id'])
        for item_id in addrItems:
            sql = "SELECT * \
                     FROM address_items \
                    WHERE id=%s" % item_id
            res = getOneDict(sql)
            if res: 
                address += res[name]
                if res['item_type'] == 2: # estate
                    if addr['blockNo']:
                        address += "Block:%s, " % addr['blockNo']
                else:address += ", "
                    
                if res['item_type'] == 3: # road
                    if addr['rd_km']:
                        address += "Km.%s, " % addr['rd_km']
                else:address += ", "
                    
                if res['item_type'] == 6: # district
                    if addr['postCode']:
                        address += "Post Code:%s \n" % addr['postCode']
                else: address += ", "
          
        while address.find(", ,"):        
            address = address.replace(", , ",", ")
        return address.rstrip(',')
    
    else: return " "

def addrItemName(addrItem_id):
    sql = " SELECT name \
              FROM address_items \
             WHERE id = %d" % int(addrItem_id)
    return getStr(sql)

def addrItem(addrItem_id):
    sql = " SELECT * \
              FROM address_items \
             WHERE id = %d" % int(addrItem_id)
    return getOneDict(sql)

def nextItemID(addrItem_id):
    sql = " SELECT next_item_id \
              FROM address_items \
             WHERE id = %d" % int(addrItem_id)
    return getDig(sql)
      
def nextAddrItemName(addrItem_id):
    id = nextItemID(addrItem_id)
    return addrItemName(id)
 
def addrItemTypeName(itemType_id):
    sql = " SELECT name \
              FROM address_item_types \
             WHERE id = %d" % int(itemType_id) 
    return getStr(sql)

def addrItemTypeID(addrItem_id):
    sql = " SELECT item_type \
              FROM address_items \
             WHERE id = %d" % int(addrItem_id)
    return getDig(sql)


# code snipits


'''
result = dict((v[0],v) for v in sorted(L, key=lambda L: L[2])).values()list comprehension

[self.doSomethingWith(x) for x in list]

# remove duplicate from list
list(set(source_list))

sorts
result = dict((v[0],v) for v in sorted(L, key=lambda L: L[2])).values()

list1 = ["1","10","3","22","23","4","2","200"]
# call int(x) on each element before comparing it
list1.sort(key=int)

[{'name':'Homer', 'age':39}, {'name':'Bart', 'age':10}]

from operator import itemgetter
newlist = sorted(list_to_be_sorted, key=itemgetter('name'))
'''


# -----   related to address editing -------------------------


# province for ........... ---------------------


# kelurahan for ........... 
def kelurahanForProvince(province):
    sql = "SELECT kelurahan \
             FROM address_items \
            WHERE province ='%s'  \
            GROUP BY (kelurahan) \
            ORDER BY (kelurahan)" % province
    return getList(sql)

def kelurahanForKabupaten(kabupaten):
    sql = "SELECT kelurahan \
             FROM postcodes \
            WHERE kabupaten ='%s'  \
            GROUP BY (kelurahan) \
            ORDER BY (kelurahan)" % kabupaten
    return getList(sql)

def kelurahanForKecamatanID(kecamatanID):
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type = 'kelurahan' \
              AND next_item_id = %d \
            ORDER BY (name)" % kecamatanID
    return getAllCol(sql)


def kelurahanForKecamatan(kecamatan):
    sql = "SELECT kelurahan \
             FROM postcodes \
            WHERE kecamatan ='%s'  \
            GROUP BY (kelurahan) \
            ORDER BY (kelurahan)" % kecamatan
    return getList(sql)

# kecamatan ----------------------------------
def kecamatanForKabupatenID(kabupatenID):
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type = 'kecamatan' \
              AND next_item_id =%d \
            ORDER BY (name)" % kabupatenID
    #rint sql, getAllCol(sql)
    return getAllCol(sql)

def kecamatanForKelurahanID(kelurahanID):
    sql = "SELECT name \
             FROM address_items \
            WHERE type = 'kelurahan' \
              AND next_item_id =%d \
            ORDER BY (kecamatan)" % kelurahanID
    return getList(sql)

#  kabupaten -------------------------------
def kabupatenForProvinceList(id_list):
    sql = "SELECT id, name \
             FROM address_items \
            WHERE next_item_id IN (%s)" %id_list
    return getAllCol(sql)

def kabupatenForCountryID(countryID):
    # for get list of province ids for country
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type ='province' \
              AND next_item_id = %d" % countryID
    return getAllCol(sql)

def kabupatenForKecamatanID(kecamatanID):
    sql = "SELECT next_item_id \
             FROM address_items \
            WHERE id =%d " % kecamatanID
    #rint sql, getDig(sql)
    kabID = getDig(sql)
    
    sql = "SELECT id, name \
             FROM address_items \
            WHERE id = %d" % kabID
    #rint sql
    return getAllCol(sql)

def kabupatenForKecamatan(kecamatan):
    if kecamatan:
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'kecamatan' \
                  AND name='%s'"  % kecamatan
        idList = getListString(sql)
        
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type = 'province'"
        
    return getAllCol(sql)

def kabupatenForProvinceID(provinceID):
    print 'kabupatenForProvinceID', provinceID
    if not provinceID: return
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type ='kabupaten' \
              AND next_item_id = %d \
            ORDER BY (name)" % provinceID
    print sql, " ; ", getAllCol(sql)
    return getAllCol(sql)





def itemForNextItemID(type, next_item_id):
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type ='%s' \
              AND next_item_id = %d \
            ORDER BY (name)" % (type, next_item_id)
    return getAllDict(sql)








def provincesForKabupatenID(kid):
    if kid:
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'kabupaten' \
                  AND id= %d "  % kid
        iid = getDig(sql)
        
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id =%d" % iid
        #rint sql
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type = 'province'"
        
    return getAllCol(sql)

def provincesForKabupaten(kabupaten=''):
    # it is possible that more one province may exist for a kabupaten name
    if kabupaten:
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'kabupaten' \
                  AND name='%s'"  % kabupaten
        idList = getListString(sql)
        
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type = 'province'"
        
    return getAllCol(sql)


def provincesForCountryID(countryID=0):
    if countryID:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type ='province' \
                  AND next_item_id = %d \
                ORDER BY (name)" % countryID
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type ='province' \
                ORDER BY (name)" 
    #rint sql, getAllCol(sql)
    
    return getAllCol(sql)

def provinceForKabupatenID(kabupatenID):
    sql = "SELECT next_item_id \
             FROM address_items \
            WHERE id = %d" % kabupatenID
    iid = getDig(sql)
    
    sql = "SELECT id, name \
             FROM address_items \
            WHERE id = %d" % iid
    
    
    
    sql = "SELECT id, name \
             FROM address_items \
            WHERE id = (SELECT next_item_id \
             FROM address_items \
            WHERE id = %d)" % kabupatenID
    
    
    #rint sql
    return getAllCol(sql)


def provinceForKecamatanID(kecamatanID):
    sql = "SELECT id \
             FROM address_items \
            WHERE type = 'kabupaten' \
              AND next_item_id = %d \
            ORDER BY (province)" % kecamatanID
    kabList = getList(sql)
    labListStr = ",".join(kabList)
    sql = "SELECT id, name \
             FROM address_items \
            WHERE type = 'province' \
              AND next_item_id IN ('%s') \
            ORDER BY (name)" % labListStr
    #rint sql
    return getAllCol(sql)

def postcodeForKecID(kecamatanID):
    sql = "SELECT postcode \
             FROM address_items \
            WHERE id = %d" % kecamatanID
    return getDig(sql)



# country for ................

def countryForProvinceID(provinceID):
    sql = "SELECT next_item_id FROM address_items WHERE id =%d " % provinceID
    countryID = getDig(sql)
    #rint sql, countryID
    sql = "SELECT id, name \
             FROM address_items \
            WHERE id =%d" % countryID
    return getAllCol(sql)

def countriesForProvinceID(prov_id):
    if prov_id:
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'province' \
                  AND id = %d"  % prov_id
        country_id = getDig(sql)
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id = %d" % country_id
        
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'province' \
                  AND id = %d"  % prov_id
        country_id = getDig(sql)
        
        
        
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id = (SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'province' \
                  AND id = %d)"  % prov_id
        
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type = 'country'"
    
    print sql    , getAllCol(sql)  
    return getAllCol(sql)           

def countriesForProvince(province=''):
    # it is possible that more than one country may exist foa a province name
    # e.g. Edminton

    if province:
        sql = "SELECT next_item_id \
                 FROM address_items \
                WHERE type = 'province' \
                  AND name='%s'"  % province
        idList = getListString(sql)
        
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type = 'country'"
        
    return getAllCol(sql)

