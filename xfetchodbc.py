import gVar, re, pyodbc, wx

import warnings, datetime, time, pyodbc, types,  hashlib, random#images,
import DlgDatePicker
        
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

DBfile = 'D:/mdb/master.mdb'

DBfile = 'D:/master2000.mdb'
#conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)

    
#DBfile = '//192.168.0.1/database/master.mdb'
"""con_str = "DRIVER={Microsoft Access Driver (*.mdb)};\
          DBQ=%s;\
          Uid=database;\
          Pwd=32822273" % DBfile"""
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)





cursor = conn.cursor()



"""
cmd = "UPDATE table SET field = %s WHERE id=%s"
curs.execute(cmd, (name, id))

cmd = "INSERT INTO sometable (something) OUTPUT INSERTED.idcolumn VALUES('something')"
cur = con.execute(cmd, something)
"""
    
def rollback():
    conn.rollback()
    
def cursor_execute(sql):
    cursor.execute(sql)
    return  conn.insert_id()
    
    
    
def executemany(sql, data):
    cursor.executemany(sql, data)
    cursor.commit()
    
def updateDB_data(sql, data):
    #rint 'updateDB_data', sql, data
    #cursor.execute("select * from Throughput where DeviceName = ?", data['DeviceName'])
    inserted_id = 0
    try:
        cursor.execute(sql, data)
        conn.commit()
        #inserted_id = conn.insert_id()
        #rint ' success '

    except:
        msg( 'Update failed')
        
    return inserted_id  
    
def accessLastID():
    res = cursor.Execute("SELECT @@IDENTITY")
    return res[0]
    
def updateDB(sql):
    
    #rint sql
    inserted_id = 0
    try:
        cursor.execute(sql)
        conn.commit()
        #inserted_id = conn.insert_id()
        inserted_id = accessLastID

    except:
        msg( 'Update failed')
        
    return inserted_id

def updateDBcommit():
    conn.commit() 

def updateDBtransaction(sql):
    cursor.execute(sql)
    return conn.commit()

def _pydate2wxdate(date):
     import datetime
     assert isinstance(date, (datetime.datetime, datetime.date))
     tt = date.timetuple()
     dmy = (tt[2], tt[1]-1, tt[0])
     return wx.DateTimeFromDMY(*dmy)
 
def _wxdate2pydate(date):
     import datetime
     assert isinstance(date, wx.DateTime)
     if date.IsValid():
          ymd = map(int, date.FormatISODate().split('-'))
          return datetime.date(*ymd)
     else:
          return None
    
def nextID(table):
    sql = "SELECT MAX (Kode) FROM %s" % table
    nextID = getDig(sql) +1
    #rint 'nextID', nextID
    return nextID

def next_id(table_name):
    sql = "SELECT MAX(id) AS x FROM %s " % table_name
    new_id =  getDig(sql) + 1
    return new_id 

#-------------------------------------------------------------------------------

def getAll_dict(sql):
    #rint sql
    try:
        cursor.execute(sql)
        res = cursor.fetchall()

        return res
    except: return ''
    
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
    
def getOneDict(sql):
    ##rint sql
    try:
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = []
        x = cursor.fetchone()
        results.append(dict(zip(columns, x)))
        return results[0]
    except:
        return []

def getOne_dict(sql):
    
    try:
        cursor.execute(sql)
        return cursor.fetchone()
    except:
        return ''
    
def getAllCol(sql):
    
    try:
        cursor.execute(sql)
        res= cursor.fetchall()
        return res
    except:
        return ''    
    
def getOne_col(sql):
    
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except:
        return ''
    
def getCount(sql):
    #rint sql, " getCount:",getAll_dict(sql)
    try:    return len(getAll_dict(sql))
    except: return 0
    
    """
    try:
        mylist = getAll_dict(sql)
        if mylist:
            return len(mylist)

    except:
        return 0"""
    
def getStr(sql):
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:   return res[0]
    except:
        return ''

def getSum(sql):
    try:
        cursor.execute(sql)
        res = cursor.fetchone()
        return int(res[0])
    except:
        return ''
    
def getDig(sql):
    #rint sql
    cursor.execute(sql)
    res = cursor.fetchone()
    try:    return int(res[0])
    except: return 0

def getRes(sql, want = 'dict'):
    if   want=='dict': return getAll_dict(sql)
    elif want=='list': return getList(sql)
    else:              return getCount(sql)
    
def getList(sql, colNo=0):
    alist =[]
    try:
        res =  getAllCol(sql)
        if res:
            for row in res:
                alist.append(row[colNo])
    except:
        pass
    return alist

def getListString(sql, colNo=0):
    alist  = getList(sql, colNo)
    #rint 'alist:', alist
    blist  = [str(x) for x in alist]
    #rint 'blist:', blist
    string = ','.join(blist)
    #rint 'string:',string
    return string

def getListTuples(sql):
    alist =[]
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        for eachitem in res:
            alist.append(eachitem)
    except:
        pass
    return alist
    
#-------------------------------------------------------------------------------
 

#-   A     ---------------------------------------------------------------------
def addNewStudent(user_name, first_name, middle_name, last_name):
    return addNewCustomer(user_name, first_name, middle_name, last_name, 'student')
    
def addNewEmployee(user_name, first_name, middle_name, last_name):
    return addNewCustomer(user_name, first_name, middle_name, last_name, 'employee')
    
def addNewAdmin(user_name, first_name, middle_name, last_name):
    return addNewCustomer(user_name, first_name, middle_name, last_name, 'admin')
    
def addNewGuardian(user_name, first_name, middle_name, last_name):
    return addNewCustomer(user_name, first_name, middle_name, last_name, 'guardian')

def addNewCustomer(user_name, first_name, middle_name, last_name, user_type): # every person entered is in some form a cusomer or 'Customer' 
    if not user_name: return ''
    full_name = "%s %s %s" % (first_name, middle_name, last_name)
    
    temp_password = user_name + '123'
    salt = ''.join(random.choice(ALPHABET) for i in range(8))

    h= hashlib.new('sha1')
    h.update(salt + temp_password)
    hashed_password = h.hexdigest()
    
    guid = hashed_password[:32]

    datetime_now = dtNow()
    sql = "INSERT INTO customers \
              SET guid ='%s', username ='%s', name ='%s', first_name ='%s', middle_name ='%s', last_name ='%s',\
                  salt ='%s', hashed_password ='%s', created_at ='%s',  updated_at ='%s', \
                  id='', notes=''" % (
                  guid, user_name, full_name, first_name, middle_name, last_name,
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

def affectiveIDs_forBatch(batch_id):
    id_list = []
    sql = " SELECT c.affectiveIDs \
              FROM curriculum c \
              JOIN batches b ON b.curriculum_id = c.id \
             WHERE b.id = %d" % batch_id
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
    return getOne_dict(sql)

def assignmentIDs_forStudygroup(studygroup_id, semester_no):
    #rint 'studygroup_id, semester_no', studygroup_id, ' | ', semester_no
    sql = " SELECT a.id \
              FROM assignments a \
             WHERE a.studygroup_id = %d \
               AND a.semester = %d " % (studygroup_id,  semester_no)
    #rint sql
    return getList(sql)
        
def avoidList(batch_id, group):
    sql = "SELECT divisions \
             FROM batches \
            WHERE id = %d" % batch_id
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

#-   B     ---------------------------------------------------------------------
def bloodGroup(blood_id):
    sql = " SELECT bloodType \
              FROM bloodgroups \
             WHERE blood_id =  %s" % blood_id
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

def batchesAndGroups_inStudygroup(studygroup_id): # used x 2
    #???????????????
    sql = " SELECT batch_ids, groups \
              FROM studygroups \
             WHERE id = %d" % studygroup_id
    #rint sql
    row = getOne_dict(sql)
    returnStrings, batches, groups = [],[],[]
    if row:
        batch_ids  = row['batch_ids']
        #batch_Name = batchName(batch_id)
        groups  = row['groups']
        #batches.append(batch_Name)
        groups.append(groupName)
    batch_str = ','.join(batches)
    group_str = ','.join(groups)
    #
    returnStrings.append(batch_str)
    returnStrings.append(group_str)
    return returnStrings

def batchPopulation(class_id):
    sql = "SELECT COUNT(NoInduk) FROM SiswaPerKelas WHERE KKelas = %d" % int(class_id)
    return getDig(sql)
    
def numberOfStudents_reregistering(class_id):
    sql = "SELECT COUNT(NoInduk) FROM SiswaPerKelas \
          WHERE 'continue' IN (SiswaPerKelas.ReregStatus) \
          AND KKelas = %d" % int(class_id)
    return getDig(sql)
    
def numberOfStudents_leaving(class_id):
    sql = "SELECT COUNT(NoInduk) FROM SiswaPerKelas WHERE 'exit' IN (SiswaPerKelas.ReregStatus) \
          AND KKelas = %d" % int(class_id)
    return getDig(sql)
    
def numberOfStudents_retaking(class_id):
    sql = "SELECT COUNT(NoInduk) FROM SiswaPerKelas WHERE  'retake' IN (SiswaPerKelas.ReregStatus) \
             AND KKelas = %d " % int(class_id)
    return getDig(sql)
    #CONTAINS(Description, @SearchWord)

def batches_inStudygroup(studygroup):# not used
    sql = " SELECT batch_ids \
              FROM studygroups \
             WHERE id = %d" % studygroup
    return getStr(sql).split(',')
    
def batches_forSchool(school_id):
    sql = "SELECT b.id, b.batch_name \
             FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE cl.course_level > -5 \
              AND cl.school_id = %d" % school_id
    return getAll_dict(sql)

def batches_forSchool_forYear(school_id, schYr=0):
    sql = "SELECT b.id, b.batch_name \
             FROM batches b  \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE cl.course_level > -5 \
              AND cl.school_id = %d" % school_id
    if schYr:  sql += " AND b.schYr =%d" % schYr
    #rint sql
    return getAll_dict(sql)

def batches_forMentor(employee_id):
    batchesList = []
    sql = " SELECT id \
              FROM batches \
             WHERE schYr = %d \
               AND employee_id = %d" % (gVar.schYr, employee_id,)
    #rint sql
    return getList(sql)

def batchName(batch_id):
    sql = " SELECT Nama \
              FROM Kelas \
             WHERE Kode = %d" % int(batch_id)
    return getStr(sql)
    
    
    sql = " SELECT batch_name \
              FROM batches \
             WHERE id = %d" % int(batch_id)
    return getStr(sql)
    
def batchInfo(batch_id):
    sql = " SELECT batch_name, short, course_id \
              FROM batches \
             WHERE id = %d" % int(batch_id)
    return getOne_dict(sql)

def batchInfo2(batch_id):
    sql = " SELECT b.batch_name, b.short, b.course_id, cl.level_title, cl.course_level, b.course_id \
              FROM batches b \
	      JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE b.id = %d" % int(batch_id)
    return getOne_dict(sql)
    
def batchName_forMentor(employee_id):
    batch_names_string = ''
    batch_ids_list = batches_forMentor(employee_id).strip()
    #rint "batch_ids_list ; ", batch_ids_list
    if batch_ids_list:
        batch_names_list = []
        for batch_id in batch_ids_list:
            #rint "batch_id in batch_ids_list ;", batch_id
            name = batchName(int(batch_id))
            batch_names_list.append(name)
        batch_names_string = ', '.join(batch_names_list)
    return batch_names_string
    
def batchName_forStudent(student_id):
    sql = " SELECT b.batch_name \
              FROM students s \
              JOIN batches b ON b.id = s.batch_id \
             WHERE schYr = %d \
               AND s.id= %d" % (gVar.schYr, int(student_id))
    return getStr(sql)
    
def batchID_forStudent(student_id, schYr = None):
    
    sql = " SELECT batch_id \
              FROM batch_students  \
             WHERE student_id = %d" % student_id
    if schYr:
        sql += " AND schYr = %d" % schyr
    return getDig(sql)  
    
def batchIds_forYear(schYr):
    sql = " SELECT b.id \
              FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON c.course_level = cl.course_level \
             WHERE b.schYr = %d \
               AND cl.course_level > -10 \
               AND b.is_deleted = 0 \
             ORDER BY cl.course_level" % int(schYr)
    return getList(sql)

def batchNames_all():
    sql = " SELECT DISTINCT b.batch_name \
              FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON c.course_level = cl.course_level \
             WHERE cl.course_level > -10 \
             ORDER BY cl.course_level"
    return getList(sql)
    
def batches_byYear(year):
    sql = " SELECT b.id, b.batch_name, cl.course_level \
              FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE b.schYr = %d \
               AND b.is_deleted  = 0\
             ORDER BY cl.course_level" % year
    return getListTuples(sql)

def batches_forLevel_forYear(level, schYr):
    #rint 'batches_forLevel_forYear', level, schYr
    sql ="SELECT b.id, b.batch_name \
            FROM batches b \
	    JOIN courses c ON c.id = b.course_id \
            JOIN course_levels cl ON cl.course_level = c.course_level \
           WHERE cl.course_level  = %d \
             AND b.schYr = %d" % (int(level), int(schYr))
    #rint  '    batches_forLevel_forYear  ', sql
    return getAll_dict(sql)
    
def batch_level(KKelas):
    sql = "SELECT course_level FROM Kelas WHERE Kode =%d" % KKelas
    return getDig(sql)

def batches_pool():
    sql = " SELECT b.id, b.batch_name, c.course_level \
              FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE cl.course_level > -10 \
               AND b.is_deleted  = 0 \
               AND b.schYr = %s \
             GROUP BY b.batch_name \
             ORDER BY c.course_level" % gVar.schYr
    return getListTuples(sql)
    
    
def batches_forCourse(course_id):
    sql = " SELECT b.id, b.batch_name, cl.course_level \
              FROM batches b \
	      JOIN courses c ON c.id = b.course_id \
              JOIN course_levels ct ON cl.course_level = c.course_level \
             WHERE c.id = %d \
               AND b.is_deleted  = False \
               AND b.schYr = %d \
          ORDER BY cl.course_level " % (course_id, gVar.schYr)

    return getAll_dict(sql)    
'''    
def batches_forCourse(course_id, result_type = 'dict'):
    sql = " SELECT b.id, b.batch_name, cl.course_level \
              FROM batches b \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE b.course_id = %d \
               AND b.is_deleted  = False \
               AND b.schYr = %d \
          ORDER BY cl.course_level " % (course_id, gVar.schYr)

    if   result_type =='dict':      return getAll_dict(sql)
    elif result_type =='by column': return getAllCol(sql)
    else:                           return getListTuples(sql)
'''      
def batchCount_forCourse(course_id, result_type = 'dict'):
    sql = " SELECT COUNT( b.id) \
              FROM batches b \
             WHERE b.course_id =%d \
               AND b.is_deleted = False " % (int(course_id),)
    #rint sql
    return getDig(sql)

def build_dictionary_str(mylist):
    #rint 'build_dictionary'
    index  = 0
    myDict = {}
    
    for row in mylist:
        print row
        newrow=[1,]
        for x in row:
            if x: x = str(x)
            else: x = ''
            newrow.append(x)
            
        newrow[0]     = index
        newrow        = tuple(newrow)
        myDict[index] = newrow
        index +=1
    
    #rint 'myDict = ',myDict
    return myDict
    
def build_dictionary(mylist):
    #rint 'build_dictionary'
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
    
    #rint 'myDict = ',myDict
    return myDict

def batchGrades_forStudent(student_id):
    return 'temp','temp','temp'
    
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


def choice(choice):
    itemNo = choice.GetSelection()
    #c = wx.Choice()
    c = choice.GetStringSelection()
    #c = choice.GetLabelText()
    #rint 'itemNo', itemNo, c
    return c

def cmbIDV(cmb):
    return cmbID(cmb),  cmbValue(cmb)

def cmbID(cmb):
    itemNo = cmb.GetSelection()
    #rint 'itemNo',itemNo
    if itemNo > -1:
        x = cmb.GetClientData(itemNo)
        if not x:
            x = 0
        return int(x)
    return 0

def cmbValue(cmb):
    index= cmb.GetSelection()
    if index > -1:
        try:
            return str(cmb.GetValue(index))
        except:
            return cmb.GetString(index)
    return 0

def colNames(tablename):
    sql = " SHOW COLUMNS \
            FROM %s \
            FROM fedena_ultimate" % tablename
    return getAllCol(sql)

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
      
def comment_forBatch(student_id, batch_id, semester_no):
    sql = " SELECT g.comment \
              FROM grades_comments g \
             WHERE g.student_id = %d \
               AND g.batch_id = %d \
               AND g.semester_no = %d" % (
            student_id, batch_id, semester_no)
    return getStr(sql)

def countStudents_newForCourse(next_course_id):
    sql = " SELECT COUNT(s.id) \
              FROM students s \
             WHERE s.enter_course_id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year" % (next_course_id, gVar.schYr)
    return getDig(sql)
    
def countStudents_retakingCourse(next_course_id): 
    sql = " SELECT COUNT(s.id) \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
             WHERE b.course_id = %d \
               AND b.schYr = %d  \
               AND '%s'  BETWEEN s.reg_year AND s.exit_year \
               AND bs.rereg_status = 'retake' " % (next_course_id, gVar.schYr, gVar.schYr)
    return getDig(sql)
    
def countStudents_reregFeePaid_forCourse(next_course_id):
    sql = " SELECT COUNT(s.id) \
              FROM batch_students bs \
              JOIN students s ON bs.student_id = s.id \
             WHERE bs.next_course_id = %d \
               AND s.exit_year <='%s' \
               AND '%s'  BETWEEN s.reg_year AND s.exit_year \
               AND bs.rereg_status = 'paid' "  % (next_course_id, gVar.schYr, gVar.schYr)
    return getDig(sql)

def countStudents_inCourse(course_id):
    sql ="SELECT COUNT(s.id) FROM students s \
            JOIN batch_students bs ON s.id = bs.student_id \
            JOIN batches b ON b.id = bs.batch_id \
            JOIN courses c ON c.id = b.course_id \
           WHERE c.id = %d \
             AND '%s' BETWEEN s.reg_year AND s.exit_year " % (course_id, gVar.schYr)
    #rint sql
    return getDig(sql)
    
def countStudents_inCourseTitle(course_id):
    sql ="SELECT COUNT(s.id) FROM students s \
            JOIN batch_students bs ON s.id = bs.student_id \
            JOIN batches b ON b.id = bs.batch_id \
	        JOIN courses c ON c.id = b.course_id \
           WHERE c.id = %d \
             AND '%s' BETWEEN s.reg_year AND s.exit_year " % (course_id, gVar.schYr)
    return getDig(sql)

# course ..
def course_level(level_id=0):
    sql = " SELECT course_level \
              FROM course_levels WHERE id = %d" % level_id
    return getDig(sql)

def courseLevels_forSchool(school_id):
    res = schoolInfo(school_id)
    min_level = res['min_level']
    max_level = res['max_level']
    return (min_level, max_level)

def regCourseLevels():
    this_year = gVar.schYr
    next_year = gVar.schYr +1
    sql = "SELECT id, course_level \
             FROM courses  \
            WHERE schYr = %d OR schYr = %d \
            GROUP BY course_level \
            ORDER BY course_level " % (this_year, next_year)
    #rint sql
    return getAll_dict(sql)

def courseLevels():
    sql = "SELECT id, course_level \
             FROM course_levels \
            GROUP BY course_level \
            ORDER BY course_level"
    return getAll_dict(sql)

def courses_forSchool_forYear(school_id, yr):
    sql = " SELECT c.id, c.course_title \
              FROM courses c \
	      JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE cl.course_level > -5 \
               AND cl.school_id =%d \
               AND c.schYr = %d  \
             ORDER BY cl.course_level" %(school_id, yr)
    #rint sql
    return getAll_dict(sql)
    
    
def courses_byLevel_tupleList():
    sql = " SELECT c.id, cl.level_title, cl.course_level \
              FROM courses c \
	      JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE cl.course_level > -5 \
               AND cl.is_deleted  = False \
             ORDER BY cl.course_level"
    return getListTuples(sql)
    
def courses_byLevel(result_type = 'dict' ):
    sql = " SELECT c.id, cl.level_title, cl.course_level \
              FROM courses c \
	      JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE cl.course_level > -5 \
               AND cl.is_deleted  = False \
             ORDER BY cl.course_level"
    #rint 'fetch.courses_byLevel:',  sql
    if result_type=='dict':   
          return getAll_dict(sql)
    else: return getAllCol(sql)
                                         
def courseLevel_forCourse(course_id):
    sql = "SELECT cl.course_level \
             FROM course_levels cl \
             JOIN courses c ON cl.course_level = course_level \
            WHERE c.id = %d" % int(course_id)
    return getDig(sql)

def courseLevel_forCourseTitle(courseLevel_forCourseTitle):  
    sql = "SELECT cl.course_level \
             FROM course_levels cl \
             JOIN courses c ON c.course_level = cl.course_level \
            WHERE c.course_title = '%s'" % courseLevel_forCourseTitle
    return getDig(sql)

def courseLevel_id_forStudent(student_id):
    sql = " SELECT cl.course_level \
              FROM students s \
              JOIN batch_students bs ON bs.student_id = s.id \
              JOIN batches b ON bs.batch_id = b.id \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE s.id = %d " % student_id
    return getDig(sql)

def courses_forSchool(school_id):
    sql ="SELECT c.id, c.course_title \
            FROM courses c \
            JOIN course_levels cl ON cl.course_level = c.course_level \
           WHERE cl.school_id =%d \
           GROUP BY c.course_title \
           ORDER BY cl.course_level " % (school_id) #  GROUP BY cl.course_level \
    #rint sql
    return getAll_dict(sql)



def courses_forLevel(level):
    sql ="SELECT c.id, c.course_title \
            FROM courses c \
            JOIN course_levels cl ON c.course_level = cl.course_level \
           WHERE cl.course_level > -5 \
             AND c.schYr = %d \
             AND cl.course_level = %d \
        ORDER BY cl.course_level " % (gVar.schYr, level) #  GROUP BY cl.course_level \
    #rint sql
    return getAll_dict(sql)
    
    


# course id -------------------------
def coursesIDs_all():        # returns:course_level
    sql = " SELECT id \
              FROM courses \
             GROUP BY name \
             ORDER BY name"
    return getList(sql)
    
def courseID_forStudent(student_id):
    sql = " SELECT b.course_level \
              FROM students s \
              JOIN batch_students bs ON bs.student_id = s.id \
              JOIN batches b ON bs.batch_id = b.id \
             WHERE s.id = %d " % student_id
    return getDig(sql)

def courseId_forBatch(batch_id):
    sql = "SELECT c.id \
             FROM courses c \
             JOIN batches b ON c.id = b.course_id \
            WHERE b.id = %d \
              AND c.schYr =%d" % (int(batch_id), gVar.schYr)
    #rint sql
    return getDig(sql)

def course_id_forTitleYear(course_title, schYr):
    sql ="SELECT id FROM courses WHERE course_title = '%s' AND schYr =%d" % (course_title, schYr,)
    #rint sql
    return getDig(sql)
# course title -----------------------------


def courseTitles_details():
    sql = " SELECT id, course_title, section_name, course_level \
              FROM courses \
             WHERE course_level > -5 \
             GROUP BY course_level \
             ORDER BY course_level"
    return getAll_dict(sql)

def course_level_info(course_level):
    if not course_level: return {}
    sql = " SELECT level_title, course_level, school_id, \
              FROM course_levels cl \
             WHERE id = %d " % (course_level, )
    #rint sql
    return getAll_dict(sql)

def course_name(course_id): 
    if not course_id: return ''
    sql = " SELECT course_name \
              FROM courses \
             WHERE id = %d " % (course_id,)
    return getStr(sql)
    
def course_info(course_id): 
    if not course_id: return {}
    sql = " SELECT course_name, course_level, school_id \
              FROM courses \
             WHERE id = %d " % (course_id,)
    #rint sql
    return getOne_dict(sql)

def levels_forSchool(school_id):
    sql ="SELECT cl.course_level, cl.level_title \
            FROM courses c \
            JOIN course_levels cl ON cl.course_level = c.course_level \
       LEFT JOIN schools sch ON sch.id = cl.school_id \
           WHERE cl.course_level > -5 \
             AND c.schYr = %d \
             AND cl.school_id =%d \
        GROUP BY cl.course_level \
        ORDER BY cl.course_level " % (gVar.schYr, school_id) #  GROUP BY cl.course_level \
    #rint ' levels_forSchool :',sql, getAll_dict(sql)
    return getAll_dict(sql)

def levelTitle(course_level):
    sql = "SELECT level_title \
             FROM course_levels \
            WHERE id = %d " % course_level
    return getStr(sql)

def courseTitle_forCourse(course_id):
    sql = "SELECT course_title  \
             FROM courses  \
            WHERE id = %d " % course_id
    return getStr(sql)
               
def courseTitles_forLevel(course_level):
    #rint 'courseTitles_forLevel', course_level, yr
    sql = " SELECT cl.course_level, cl.level_title \
              FROM course_levels cl \
             WHERE cl.course_level = %s \
               AND cl.is_deleted = 0 \
          ORDER BY level_title" % (course_level,)
    return getAll_dict(sql)


def levelTitle_level(course_level):  # returms:course_title
    sql = " SELECT cl.level_title \
              FROM course_levels cl  \
             WHERE cl.course_level = %d" % course_level
    return getStr(sql)

def course_level_forBatch(batch_id):
    sql = "SELECT c.course_level \
             FROM batches b\
	     JOIN courses c ON c.id = b.course_id \
            WHERE b.id = %d" % int(batch_id)
    return getDig(sql)

def courseTitles():
    sql = "SELECT cl.course_level, cl.level_title \
             FROM course_levels cl \
            ORDER BY cl.course_level"
    return getAll_dict(sql) 

#-   D     --------------------------------------------------------------------
def DATA_STR(sql):
    return build_dictionary_str(getAllCol(sql))

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
              FROM employees \
             WHERE id = %d" % id
    return getOne_dict(sql)

def employeeName(employee_id):
    if not employee_id:return ''
    sql = "SELECT CONCAT_WS(' ', first_name, middle_name, last_name) as name \
             FROM employees \
            WHERE id = %s" % employee_id
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
              JOIN batch_students bs ON bs.student_id = s.id\
              JOIN batches b ON bs.batch_id = b.id \
             WHERE s.enter_school_year <= %s \
               AND b.school_id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year \
             LIMIT 40" % (gVar.schYr, sch_id, gVar.schYr )
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

def excul_activityIDs():
    sql = " SELECT id, name \
              FROM excul_activities"
    return getAll_dict(sql)

def excul_info(excul_id):
    sql = " SELECT employee_id, activity_id \
              FROM excul \
             WHERE id=%d" % int(excul_id)
    return getOne_dict(sql)
                                
def excul_groups_forSchSemYr(dayNo, semester, sch_id):
    sql = " SELECT ex.id, ea.id, ea.name, e.id, CONCAT_WS(' ', e.first_name, e.middle_name, e.last_name) AS teacher_name \
              FROM excul ex \
              JOIN exculsets es             ON es.id = ex.exculset_id \
         LEFT JOIN excul_activity_titles ea ON ea.id = ex.activity_id \
         LEFT JOIN employees e              ON e.id  = ex.employee_id \
             WHERE es.day = %d AND es.semester = %d AND es.schYr = %d AND es.school_id = %d " % (
                   dayNo, semester, gVar.schYr, sch_id)
    #if getAllCol(sql): rint sql
    return getAllCol(sql)

def exculsetinfo(set_id):
    sql = " SELECT s.school_name, d.day, es.semester, es.schYr FROM exculsets es \
              JOIN schools s ON s.id = es.school_id \
              JOIN days d    ON d.id = es.day \
             WHERE es.id = %d" % set_id
    return getOne_col(sql)
    
def excul_groups_forExculSet(set_id):
    sql = " SELECT ex.id, ea.id, ea.name, e.id, CONCAT_WS(' ', e.first_name, e.middle_name, e.last_name) AS teacher_name \
              FROM excul ex \
              JOIN exculsets es             ON es.id = ex.exculset_id \
         LEFT JOIN excul_activity_titles ea ON ea.id = ex.activity_id \
         LEFT JOIN employees e              ON e.id  = ex.employee_id \
             WHERE es.id = %d " % (set_id, )
    #rint sql
    return getAllCol(sql)

def exculSchedule_forSchSemYr(school_id, semester_no):
    sql = " SELECT day \
              FROM exculsets \
             WHERE semester = %d \
               AND school_id = %d \
               AND schYr = %d" % (semester_no, school_id, gVar.schYr)
    #rint sql
    return getList(sql)

def excul_activityTitle_forExcul(excul_id):
    sql = "SELECT et.name \
             FROM excul_activity_titles et \
             JOIN excul e ON et.id = e.activity_id \
            WHERE e.id = %d" % int(excul_id)
    #rint sql
    return getStr(sql)


def excul_activityTitle(activity_id):
    sql = "SELECT name \
             FROM excul_activity_titles \
            WHERE id = %d" % int(activity_id)
    return getStr(sql)  

def excul_activityPool(listOfActivityIDs):
    listOfActivityIDs = [str(x[0]) for x in listOfActivityIDs]
    #rint 'listOfActivityIDs', listOfActivityIDs
    listStr = "'%s'" % ','.join(listOfActivityIDs)
    sql = " SELECT id, name \
              FROM excul_activity_titles \
              WHERE NOT FIND_IN_SET(id, %s)" % listStr
    #rint sql
    return getAllCol(sql)

def excul_teacherPool(teacherIDs):
    teacherIDs = [str(x[0]) for x in teacherIDs]
    listStr = "'%s'" % ','.join(teacherIDs)
    sql = " SELECT id, CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name \
              FROM employees \
             WHERE employee_category_id = 2 \
               AND %d BETWEEN join_schYr AND leave_schYr \
               AND NOT FIND_IN_SET(id, %s)" % (gVar.schYr, listStr)
    #rint sql
    return getAllCol(sql)

def exculset_id():
    sql = " SELECT id \
              FROM exculsets \
             WHERE day = %d\
               AND semester = %d \
               AND school_id = %d \
               AND schYr = %d" % (gVar.dayNo, gVar.semester, gVar.school_id, gVar.schYr)
    return getDig(sql)
  
#-   F     ---------------------------------------------------------------------
def faith(id):
    sql = " SELECT name \
              FROM religions \
             WHERE id = %s" % id
    return getStr(sql)

def feeType(id):
    sql = " SELECT feeTitle \
              FROM feetypes \
             WHERE feeType_id = %s" % id
    return getStr(sql) 

def fees(yr):
    sql = "SELECT fee_id, feeType, feeAmount, description \
             FROM schoolfees \
            WHERE validTillYr >=%s" % yr
    return getAll_dict(sql)

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

#-  G     ----------------------------------------------------------------------
def gender(g):# converts db.res to str or str to db ready entry
    gender =""
    if g =="m":     gender = "Male"
    if g =="Male":  gender = "m"
    if g =="f":     gender = "Female"
    if g =="Female":gender = "m"
    return gender

def gradingStandard(standard_id):
    sql = "SELECT standard FROM grading_standards WHERE id = %d" % int(standard_id)
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

def gradeAverage_forBatch(student_id, batch_id, semester_no):
    total = 0
    count = 0
    studygroups = studygroups_forBatch(batch_id)
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

def guid(student_id):
    sql = "SELECT guid FROM students WHERE id =%d" % student_id
    return getStr(sql)
    
def gradesForAssignment(student_id, assignment_id):    
    # rint student_id, assignment_id
    sql = "SELECT g.gradeT, g.gradeP \
             FROM grades_academic g \
            WHERE g.assignment_id=%d \
              AND g.student_id = %d" % (int(assignment_id), int(student_id))
    return getOne_dict(sql)                  

def hasPermission(feature):
    sql = "SELECT ep.id FROM employee_privileges ep \
             JOIN privileges p ON p.id = ep.privilege_id \
            WHERE ep.employee_id =  %d \
              AND p.name = '%s'" % (gVar.user_id, feature)
    #rint sql , fetch.getAll_dict(sql)
    if getAll_dict(sql):
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

#---------------------------------------------------------------------------
def image_resize( ctrl, image, size, padding):
    ctrl.SetSize(size)
    if total:
        w = size[0] - padding*2
        h = size[1] - padding*2
        bmp = image_scale(image, w, h)
        ctrl.SetBitmap(bmp)



# province for ........... ---------------------

def provincesForCountryID(countryID):
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType ='province' \
              AND nextItemID = %d \
            ORDER BY (itemName)" % countryID
    #rint sql, getAllCol(sql)
    
    return getAllCol(sql)


"""
def provincesForCountry(country):
    sql = "SELECT province \
             FROM postcodes \
            WHERE country = '%s' \
            GROUP BY (province) \
            ORDER BY (province)" % country
    
    sql = "SELECT id FROM addressItems WHERE itemName ='%s'" % country
    country_id = getDig(sql)

    sql = "SELECT itemName FROM addressItems WHERE itemType ='province' AND nextItemID = %d" % country_id
    #rint sql
    
    return getList(sql)"""


def provinceForKabupatenID(kabupatenID):
    sql = "SELECT nextItemID FROM addressItems WHERE id = %d" % kabupatenID
    iid = getDig(sql)
    
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE id = %d" % iid
    #rint sql
    return getAllCol(sql)

def kabupatenForProvinceList(id_list):
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE nextItemID IN (%s)" %id_list
    return getAllCol(sql)

def proviceForKecamatanID(kecamatanID):
    sql = "SELECT id \
             FROM addressItems \
            WHERE itemType = 'kabupaten' \
            AND nextItemID = %d \
            ORDER BY (province)" % kecamatanID
    kabList = getList(sql)
    labListStr = ",".join(kabList)
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType = 'province' \
            AND nextItemID IN ('%s') \
            ORDER BY (itemName)" % labListStr
    #rint sql
    return getAllCol(sql)

"""    
def proviceForKecamatan(kecamatan):
    sql = "SELECT province \
             FROM postcodes \
            WHERE kecamatan = '%s' \
            GROUP BY (province) \
            ORDER BY (province)" % kecamatan
    return getList(sql)"""
"""    
def proviceForKelurahan(kelurahan):
    sql = "SELECT province \
             FROM postcodes \
            WHERE kelurahan = '%s' \
            GROUP BY (province) \
            ORDER BY (province)" % kelurahan
    return getList(sql)"""
"""
def postcodeForKec(kecamatan):
    sql = "SELECT postcode \
             FROM postcodes \
            WHERE kecamatan ='%s'" % kecamatan
    return getDig(sql)"""

def postcodeForKecID(kecamatanID):
    sql = "SELECT postcode \
             FROM addressItems \
            WHERE id = %d" % kecamatanID
    return getDig(sql)


def kabupatenForCountryID(countryID):
    # for get list of province ids for country
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType ='province' \
              AND nextItemID = %d" % countryID
    return getAllCol(sql)

"""def kabupatenForCountry(country):
    # get country id
    sql = "SELECT id FROM addressItems WHERE itemName ='%s'" % country
    country_id = getDig(sql)
    
    sql = "SELECT itemName FROM addressItems WHERE itemType ='province' AND nextItemID = %d" % country_id
    #rint sql
    
    return getList(sql)"""

def kabupatenForKecamatanID(kecamatanID):
    sql = "SELECT nextItemID \
             FROM addressItems \
            WHERE id =%d " % kecamatanID
    #rint sql, getDig(sql)
    kabID = getDig(sql)
    
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE id = %d" % kabID
    #rint sql
    return getAllCol(sql)

def kabupatenForKecamatan(kecamatan):
    if kecamatan:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'kecamatan' \
                  AND itemName='%s'"  % kecamatan
        idList = getListString(sql)
        
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'province'"
        
    return getAllCol(sql)
"""
def kabupatenForKecamatan(kecamatan):
    sql = "SELECT kabupaten \
                 FROM postcodes \
                WHERE kecamatan = '%s' \
                GROUP BY (kabupaten) \
                ORDER BY (kabupaten)" % kecamatan
    #rint sql
    return getList(sql)"""

def kabupatenForProvinceID(provinceID):
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType ='kabupaten' \
              AND nextItemID = %d \
            ORDER BY (itemName)" % provinceID
    #rint sql, " ; ", getAllCol(sql)
    return getAllCol(sql)

"""
def kabupatenForProvince(province):
    sql = "SELECT kabupaten \
             FROM postcodes \
            WHERE province ='%s' \
            GROUP BY (kabupaten) \
            ORDER BY (kabupaten)" % province
    return getList(sql)"""

def itemForNextItemID(itemType, nextItemID):
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType ='%s' \
              AND nextItemID = %d \
            ORDER BY (itemName)" % (itemType, nextItemID)
    return getAllDict(sql)
"""
def kabupatenForKelurahan(kelurahan):
    sql = "SELECT kabupaten \
             FROM postcodes \
            WHERE kelurahan ='%s' \
            GROUP BY (kabupaten) \
            ORDER BY (kabupaten)" % kelurahan
    return getList(sql)"""

# country for ................

def countryForProvinceID(provinceID):
    sql = "SELECT nextItemID FROM addressItems WHERE id =%d " % provinceID
    countryID = getDig(sql)
    #rint sql, countryID
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE id =%d" % countryID
    return getAllCol(sql)
    
#   kecamatan for .......
"""
def kecamatanForProvince(province):
    sql = "SELECT kecamatan \
             FROM postcodes \
            WHERE province ='%s' \
            GROUP BY (kecamatan) \
            ORDER BY (kecamatan)" % province
    return getList(sql)"""

def kecamatanForKabupatenID(kabupatenID):
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType = 'kecamatan' \
              AND nextItemID =%d \
            ORDER BY (itemName)" % kabupatenID
    #rint sql, getAllCol(sql)
    return getAllCol(sql)

"""
def kecamatanForKabupaten(kabupaten):
    sql = "SELECT kecamatan \
                 FROM postcodes \
                WHERE kabupaten = '%s' \
                GROUP BY (kecamatan) \
                ORDER BY (kecamatan)" % kabupaten
    return getList(sql)"""
    
def kecamatanForKelurahanID(kelurahanID):
    sql = "SELECT itemName \
             FROM addressItems \
            WHERE itemType = 'kelurahan' \
              AND nextItemID =%d \
            ORDER BY (kecamatan)" % kelurahanID
    return getList(sql)   
"""        
def kecamatanForKelurahan(kelurahan):
    sql = "SELECT kecamatan \
             FROM postcodes \
            WHERE kelurahan ='%s' \
            GROUP BY (kecamatan) \
            ORDER BY (kecamatan)" % kelurahan
    return getList(sql)"""

def provincesForKabupatenID(kid):
    if kid:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'kabupaten' \
                  AND id= %d "  % kid
        iid = getDig(sql)
        
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE id =%d" % iid
        #rint sql
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'province'"
        
    return getAllCol(sql)

def provincesForKabupaten(kabupaten=''):
    # it is possible that more one province may exist for a kabupaten name
    if kabupaten:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'kabupaten' \
                  AND itemName='%s'"  % kabupaten
        idList = getListString(sql)
        
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'province'"
        
    return getAllCol(sql)

def countriesForProvinceID(iid):
    if iid:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'province' \
                  AND id = %d"  % iid
        cid = getDig(sql)
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE id = %d" % cid
        #rint sql
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'country'"
        
    return getAllCol(sql)           

def countriesForProvince(province=''):
    # it is possible that more than one country may exist foa a province name
    # e.g. Edminton

    if province:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'province' \
                  AND itemName='%s'"  % province
        idList = getListString(sql)
        
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE id IN (%s)" % idList
        #rint sql
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'country'"
        
    return getAllCol(sql)

# kelurahan for ........... 
def kelurahanForProvince(province):
    sql = "SELECT kelurahan \
             FROM addressItems \
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
    sql = "SELECT id, itemName \
             FROM addressItems \
            WHERE itemType = 'kelurahan' \
              AND nextItemID = %d \
            ORDER BY (itemName)" % kecamatanID
    return getAllCol(sql)


def kelurahanForKecamatan(kecamatan):
    sql = "SELECT kelurahan \
             FROM postcodes \
            WHERE kecamatan ='%s'  \
            GROUP BY (kelurahan) \
            ORDER BY (kelurahan)" % kecamatan
    return getList(sql)


#-   L     ---------------------------------------------------------------------
def levelName(level):
    sql = " SELECT level_title \
              FROM course_levels \
             WHERE id = %d" % level
    return getStr(sql)



# ...................................................................

def livesWith(guardian_id):
    #rint '  guardian_id   '  , guardian_id
    if guardian_id :
        sql = " SELECT name \
                  FROM guardians \
                 WHERE id = %d" % int(guardian_id)
        return getStr(sql)
    else: return ''
    
#.......................................................
def ask(txt):
    return wx.MessageBox(txt, 'Info', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)

def msg(txt):
    return wx.MessageBox(txt, 'Info', wx.OK | wx.ICON_INFORMATION)

def classCount_forCourse(course_id): # returns 'number_of_classes_next_schYr'
    sql = " SELECT COUNT(b.id) \
              FROM batches b\
             WHERE b.course_id = %d AND b.schYr =%d" % (course_id, gVar.schYr)
    return getDig(sql)

def currentCourse(student_id):
    sql = " SELECT cl.level_title \
              FROM course_levels cl \
	         JOIN courses c ON cl.course_level = c.course_level \
              JOIN batches b ON c.id = b.course_id \
              JOIN batch_students bs ON b.id = bs.batch_id \
             WHERE bs.student_id = %d \
               AND b.schYr =%d" % (int(student_id), gVar.schYr)
    return getStr(sql)
# ........................................

def nextCourse(student_id):
    if not student_id: return ''
    sql = " SELECT cl.level_title \
              FROM course_levels cl \
	         JOIN courses c ON cl.course_level = c.course_level \
              JOIN batch_students bs ON c.id = bs.next_course_id \
             WHERE bs.student_id = %d \
               AND b.schYr = %d" % (int(student_id), (gVar.schYr+1))
    return getStr(sql)

def nis(student_id):
    sql = "SELECT nis FROM nis \
            WHERE student_id =%d \
              AND %d BETWEEN admission_year AND withdrew_year" % (student_id, gVar.schYr)
    return getStr(sql)


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
    sql = " SELECT first_name \
              FROM guardians \
             WHERE id = %d" % id
    return getStr(sql)

def parentDetails(id):
    sql = " SELECT * \
              FROM guardians \
             WHERE id = %s" % id
    return getOne_dict(sql)

def phoneNos(id):# for appending to a list (almost duplicate of telpNoList
    sql = " SELECT phone_number \
              FROM phone_numbers \
             WHERE guid = %s"

def population_ofBatch(batch_id, do_filter = '', want = 'dict'):
    #rint batch_id, do_filter , want
    sql = "SELECT COUNT(s.id) \
             FROM students s \
             JOIN batch_students bs ON bs.student_id = s.id \
            WHERE bs.batch_id = %d \
              AND %d BETWEEN s.reg_year AND s.exit_year " % (int(batch_id), gVar.schYr)
    
    if do_filter:  sql +=  " AND bs.rereg_status = '%s' " % do_filter
    #rint sql
    return getDig(sql)

def previous_school_id(nis):
    
    sql = "SELECT previous_school_id FROM nis WHERE nis = '%s'" % nsi

#-   R     ---------------------------------------------------------------------
def registeredStudents(bool, yr): # returns list (students_id)
    # looks for students that are registering
    # for the school but are not yet active
    sql = "SELECT id \
             FROM students \
            WHERE admision_status = 'paid' \
              AND reg_year = %d \
              AND '%s' BETWEEN s.reg_year AND s.exit_year " % (yr, gVar.schYr) 
    return getAll_dict(sql)

def re_registrationDetails_forBatch(batch_id):
    batch_id = int(batch_id)
    batchDetails = []
    #  batch_id, 'batch', batchName, population, leaving, retake, may_stay, reregistered, paid
    batchDetails.append(batch_id)
    batchDetails.append('batch')
    
    batchDetails.append(batchName(batch_id))
    
    population = population_ofBatch(batch_id, '', 'count')
    batchDetails.append(population)
   
    leaving = population_ofBatch(batch_id, 'leave', 'count')
    batchDetails.append(leaving)
    
    retake = population_ofBatch(batch_id, 'retake', 'count')
    batchDetails.append(retake)
    
    may_stay = population - leaving - retake
    batchDetails.append(may_stay)
    
    reregistered = population_ofBatch(batch_id, 'stay', 'count')
    batchDetails.append(reregistered) 
     
    paid = population_ofBatch(batch_id, 'paid', 'count')
    batchDetails.append(paid)
    return batchDetails

def reregList_forBatch(batch_id, sqlfilter = False):  
    # returns tuple list (students_id, first_name, rereg_status, rereg_course_id)
    # of existing students in batch
    sql = " SELECT s.id, s.first_name, bs.rereg_status, bs.rereg_course_id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
             WHERE bs.batch_id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year " % (batch_id, gVar.schYr)
    if sqlfilter:
        sql += " AND bs.rereg_status = %d" % sqlfilter
    return getAll_dict(sql)

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
    sql = "SELECT s.id, s.first_name, cl.course_level, cl.level_title, cs.id, bs.rereg_status, bs.next_course_id, b.id \
             FROM students s \
             JOIN batch_students bs ON bs.student_id = s.id \
             JOIN batches b ON b.id = bs.batch_id  \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE s.id = %d \
              AND c.schYr = %d" % (int(student_id), yr)
    return getOne_dict(sql)

def reregDetails_forStudent(student_id):
        sql ="SELECT s.first_name, bs.id as bs_id, bs.rereg_status, bs.next_course_id, b.id as batch_id \
                FROM students s \
                JOIN batch_students bs ON bs.student_id = s.id \
                JOIN batches b ON b.id = bs.batch_id  \
               WHERE s.id = %d AND b.schYr = %d " % (student_id, gVar.schYr)
        return getOne_dict(sql)
        
def regStatus(re_reg_id):
    data = studentRegDetails(re_reg_id)
    return data['isEnrolled']   
  
def removeWithdrawnStudents(listOfIDs): 
    x = ','.join(listOfIDs)
    listOfIDs = "'%s'" % x
    sql = "SELECT * \
             FROM students \
            WHERE FIND_IN_SET(id, %s) \
              AND '%s' BETWEEN s.reg_year AND s.exit_year " % (listOfIDs, gVar.schYr)
    return getList(sql)
  
def reverseList(list):
    newList=[]
    i = len(list) 
    for idx in range(i):  
        x = i-idx-1
        newList.append(list[x])
    return newList
            
def roamingStudents_forBatchLevel(batch_id):
    level = batchInfo2(batch_id)['course_level']
    
    sql = "SELECT s.id \
             FROM students s \
             JOIN batch_students bs ON s.id = bs.student_id \
             JOIN batches b ON b.id = bs.batch_id \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE '%s' BETWEEN s.reg_year AND s.exit_year \
              AND course_level = %d " % (gVar.schYr, level,)

def roamingStudents_forBatch(batch_id):
    sql = "SELECT s.id \
             FROM students s \
             JOIN batch_students bs ON s.id = bs.student_id \
            WHERE s.withdrew_year <='%s' \
              AND batch_id = %d" % (gVar.schYr, batch_id)
    res = getList(sql)
    if res : ids = ",".join(res)
    else: ids = ''
    
    course_level = courseId_forBatch(batch_id)
    sql = "SELECT s.id \
             FROM students s \
             JOIN batch_students bs ON s.id = bs.student_id \
            WHERE '%s' BETWEEN s.reg_year AND s.exit_year \
              AND next_course_id = %d \
              AND NOT FIND_IN_SET(s.id, '%s') \
                           " % (gVar.schYr, course_level, ids)
    return getAll_dict(sql)
    
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
    try:    return getOne_dict(sql)['school_id']
    except: return 0

def schoolID_forCourse(course_id):
    sql = "SELECT cl.school_id \
             FROM courses c \
             JOIN course_levels cl ON c.course_level = cl.course_level \
            WHERE c.id = %d  " % course_id
    #rint sql
    try:    return getOne_dict(sql)['school_id']
    except: return 0
    
def schoolID_forBatch(batch_id):
    sql = "SELECT cl.school_id \
             FROM course_levels cl \
	        JOIN courses c ON cl.course_level = c.course_level \
             JOIN batches b ON c.id = b.course_id \
            WHERE b.id =%d" % batch_id
    return getDig(sql)

def schoolID_forExculSet(exculset_id):
    sql = "SELECT school_id \
             FROM exculsets \
            WHERE id =%d" % exculset_id
    return getDig(sql)

def schoolName(id): # working May 2012
    if not id: return ''
    sql = "SELECT school_name \
             FROM schools \
            WHERE id = %d" % id
    return getStr(sql)

    res = getOne_dict(sql)
    school_name, school_type = res['school_name'], res['school_type']
    t = "%s: %s" % (school_name, school_type)
    return t

def schoolInfo(school_id):
    if not id: return ''
    sql = "SELECT * FROM schools WHERE id = %d" % school_id
    return getOne_dict(sql)


def schYr_forBatch(batch_id):
    sql = "SELECT schYr \
             FROM batches  \
            WHERE id =%d" % batch_id
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
              FROM subject_titles st \
              JOIN studygroups sg ON st.id = sg.subject_title_id \
             WHERE sg.id = %d" % studygroup_id
    return getStr(sql)
    

def subjectTitle(subject_title_id):
    sql = " SELECT subject_title \
              FROM subject_titles \
             WHERE id = %d" % subject_title_id
    return getStr(sql)


# ------------------   studygroups   -----------------------
def studygroupPopulation(studygroup_id):
    return len(studentIDs_inStudygroup(studygroup_id))
    
def studygroupPool(studygroup_id):
    studygroup_pool = []
    sql = "SELECT batch_ids  \
             FROM studygroups   \
            WHERE id = %d" % studygroup_id
    #rint sql
    batch_ids = getStr(sql).split(',')
    if batch_ids: 
        for batch_id in batch_ids:
            groupName = "groupName" # row['groupName']
            if groupName == 'Entire':
                pass# studygroup_population += batch_population(batch_id)
            else:
                pass
                # $rint "how to do divisions"
                #sql ="SELECT f.`studentIDs` FROM form_division_students f \
                #        WHERE f.`division`=%s AND f.`batch_id`=%d" %(groupName, batch_id)
                #row  = getOne_dict(sql)    
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
    
    sql = "SELECT id, employee_id \
             FROM studygroups \
            WHERE id = %d" % studygroup_id
    x= getOne_dict(sql)'''
    return "????"

def studygroupName(sg_id):
    sql = " SELECT st.subject_title \
              FROM studygroups sg \
              JOIN subject_titles st ON st.id= sg.subject_title_id \
             WHERE sg.id =%d" % sg_id
    #rint sql
    return getStr(sql)

def studygroupTeacher(sg_id):
    sql = " SELECT CONCAT_WS(' ', first_name, middle_name, last_name) as name \
              FROM studygroups sg \
              JOIN employees e ON e.id= sg.employee_id\
             WHERE sg.id =%d" % sg_id
    #rint sql
    return getStr(sql)

def studygroups_forLevel(level):
    sql = " SELECT st.subject_title \
              FROM studygroups sg \
              JOIN subject_titles st ON st.id= sg.subject_id\
              JOIN batches b ON FIND_IN_SET(b.id, sg.batch_ids) \
	        JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE cl.course_level = %d" % level
    return getAll_dict(sql)

#...........  students  ........................
def studentsLeaving_courseTitle(course_level):
    sql = " SELECT s.id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
	        JOIN courses c ON c.id = b.course_id \
             WHERE c.course_level = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year \
               AND b.rereg_status = 'leave'" % (course_level, gVar.schYr)
    return getList(sql)

def studentsLeaving_course(course_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
	         JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.course_level = c.course_level \
             WHERE c.id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year \
               AND b.rereg_status = 'leave'" % (course_id, gVar.schYr)
    return getList(sql)

def students_reregPaid_inBatch_nextCourse(batch_id, course_level):
    sql = " SELECT s.id, first_name, s.middle_name, s.last_name \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN course_students cs ON s.id = cs.student_id \
             WHERE %d BETWEEN s.reg_year AND s.exit_year \
               AND b.id =%d \
               AND bs.rereg_status = 'paid' \
               AND bs.next_course_id = %d" % (gVar.schYr, batch_id, course_level)
    return getAll_dict(sql)

def students_reregPaid_inBatch(batch_id):
    sql = " SELECT s.id, first_name, s.middle_name, s.last_name \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
             WHERE %d BETWEEN s.reg_year AND s.exit_year \
               AND bs.rereg_status = 'paid' " % (batch_id, gVar.schYr)
    return getAll_dict(sql)

def students_reregStatus_inBatch(batch_id):
    school_id = schoolID_forBatch(batch_id)
    sql ="SELECT s.id, bs.rereg_status, s.first_name, s.last_name, n.nis, bs.next_course_id \
            FROM students s \
            JOIN batch_students bs ON s.id = bs.student_id \
            JOIN batches b ON b.id = bs.batch_id \
       LEFT JOIN nis n ON s.id = n.student_id \
           WHERE bs.batch_id = %d \
             AND '%s' BETWEEN s.reg_year AND s.exit_year \
             AND b.schYr = %d \
             AND n.school_id = %d GROUP BY s.id" % (int(batch_id), gVar.schYr, gVar.schYr, school_id)
    return getAllCol(sql) 
 
def guardianRelationship(student_id):
    sql = "SELECT HubunganWali FROM CSiswa WHERE Kode =%d" % student_id
    return getStr(sql)
    
def students_reregStatus_untransfered_inBatch(batch_id):
    sql = " SELECT s.id, bs.rereg_status, s.first_name, s.last_name, n.nis \
              FROM students s \
              JOIN batch_students  bs ON s.id = bs.student_id \
              JOIN nis n ON s.id = n.student_id \
             WHERE bs.batch_id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year " % (int(batch_id), gVar.schYr)
    return getAllCol(sql)

def cSiswaDetails(student_id):
    sql = "SELECT * \
             FROM CSiswa \
            WHERE Kode = %d" % int(student_id)
    #rint sql
    return getOneDict(sql)
    

def studentDetails_id(student_id):
    sql = "SELECT * \
             FROM Siswa \
            WHERE CKID = '%d'" % int(student_id)
    #rint sql
    return getOneDict(sql)

def student_callName_id(student_id):
    sql = "SELECT callname \
             FROM students \
            WHERE id = %d" % int(student_id)
    return getStr(sql)


def student_fullName_nis(nis):
    sql = "SELECT CONCAT_WS(' ', first_name, middle_name, last_name) as name \
             FROM students s \
             JOIN nis n ON s.id =n.student_id \
            WHERE n.nis = %s" % nis
    return getStr(sql)

def studentFullName(student_id):
    sql = "SELECT CONCAT_WS(' ', first_name, ' ', middle_name, ' ', last_name) as full_name \
           FROM students \
           WHERE id = %d" % student_id
    res = getOne_dict(sql)
    if not res : return ''
    
    string = res['full_name']
    while '  ' in string:
        string = string.replace('  ', ' ')

    return string

def NoInduk(schYr, student_id):
    sql = "SELECT Siswa.NoInduk FROM Siswa \
            INNER JOIN SiswaPerKelas  \
               ON SiswaPerKelas.NoInduk = Siswa.NoInduk  \
            WHERE SiswaPerKelas.TahunAjaran = %d \
              AND Siswa.id = %d" % (schYr, student_id )
    print sql
    return getStr(sql)

def product_details(priduct_id):
    sql = "SELECT description, price FROM products WHERE id =%d" % int(priduct_id)
    res = getOneDict(sql)
    if res:
        return (res['description'], res['price'])
    else:
        return ('','')


def studentNames(student_id):
    sql = "SELECT first_name, middle_name, last_name \
             FROM students \
            WHERE id = %d" % student_id
    
    return getOne_col(sql)


'''def studentNames_studentID(student_id):
    sql = "SELECT first_name, middle_name, last_name \
           FROM students \
           WHERE id = %d" % student_id
    return getOne_dict(sql)'''

def studentSchDetails(student_id):
    sql = "SELECT bs.batch_id, n.nis, s.first_name, s.middle_name, s.last_name, \
                 s.birth_date, s.gender, s.ship_id, b.course_level, cl.school_id, s.national_no, cl.course_level \
             FROM students s \
        LEFT JOIN nis n ON s.id = n.student_id \
             JOIN batch_students bs ON bs.student_id = s.id \
             JOIN batches b ON bs.batch_id = b.id \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE s.id = %d \
              AND b.schYr = %d " % (int(student_id), gVar.schYr)
    #rint sql
    return getOne_dict(sql)

def students_forSch(school_id, schYr = gVar.schYr):
    sql ="SELECT s.id, n.nis, s.first_name, s.middle_name, s.last_name, b.batch_name \
                    FROM students s \
               LEFT JOIN nis n ON s.id = n.student_id \
                    JOIN batch_students bs ON s.id = bs.student_id \
                    JOIN batches b ON b.id = bs.batch_id \
                   WHERE %d BETWEEN n.admission_year AND n.withdrew_year\
                     AND n.school_id = %d ORDER BY s.id" % (schYr, school_id)
    #rint sql
    return getAll_dict(sql)


def studentIDs_forBatch(batch_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
             WHERE bs.batch_id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year" % (batch_id, gVar.schYr)
    #rint sql
    return getList(sql)

def studentsLeaving_batch(batch_id):
    sql = " SELECT s.id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
             WHERE b.id = %d \
               AND '%s' BETWEEN s.reg_year AND s.exit_year \
               AND b.rereg_status = 'leave'" % (batch_id, gVar.schYr)
    return getList(sql)

def students_forBatch(batch_id, want='dict'):
    sql = " SELECT s.id, CONCAT(s.first_name, ' ', s.middle_name, ' ', s.last_name) \
              FROM students s \
              JOIN batch_students bs ON bs.student_id = s.id \
             WHERE bs.batch_id = %d \
               AND %d BETWEEN s.reg_year AND s.exit_year " % (batch_id, gVar.schYr)
    if want == 'dict':
        return getAll_dict(sql)
    else:
        return getAllCol(sql)
    
def students_inBatch(batch_id, want='dict'):
    school_id = schoolID_forBatch(batch_id)
    sql = " SELECT s.id, s.first_name, s.middle_name, s.last_name, n.nis \
              FROM students s \
              JOIN batch_students bs ON bs.student_id = s.id \
              JOIN nis n ON s.id = n.student_id \
             WHERE bs.batch_id = %d \
               AND n.school_id = %d \
               AND %d BETWEEN s.reg_year AND s.exit_year " % (batch_id, school_id, gVar.schYr)
    if want == 'dict':
        return getAll_dict(sql)
    else:
        return getAllCol(sql)

def studentIDs_forExcul(excul_id):
    sql = "SELECT student_id \
             FROM excul_students \
            WHERE excul_id = %d" % int(excul_id)
    #rint sql,  getList(sql)
    return getList(sql)
        
def students_inLevel(level):
    sql = "SELECT s.id, s.first_name, s.middle_name, s.last_name, n.nis \
             FROM students s \
             JOIN batch_students cs ON s.id = bs.student_id \
             JOIN nis n ON s.id = n.student_id \
	        JOIN courses c ON c.id = b.course_id \
             JOIN course_levels cl ON cl.course_level = c.course_level \
            WHERE cl.course_level = %s \
              AND '%s' BETWEEN s.reg_year AND s.exit_year " % (level, gVar.schYr)
    return getAllCol(sql)

def students_matching(firstName, middleName, lastName, birthDate):    
    sql = 'SELECT * FROM students'
    
    if firstName or middleName or lastName:
        sql = "SELECT * FROM students WHERE"
        if firstName:
            sql += " CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + firstName + "%'"
            if middleName:
                sql += " OR CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + middleName + "%'"
                if lastName:
                    sql += " OR CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + lastName + "%'"
            else:
                if lastName:
                    sql += " OR CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + lastName + "%'"
            
        else:
            if middleName:
                sql += " CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + middleName + "%'"
                if lastName:
                    sql += " OR CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + lastName + "%'"
                       
            else:
                sql += " CONCAT(first_name, ' ', middle_name, ' ', last_name)  LIKE '%" + lastName + "%'"

        res = getAll_dict(sql)
        
        x = len(res)
        #rint x, ' records found'
        return res
    
    else:
        return ''


def students_not_in_batch(batch_id):
    batchYr    = schYr_forBatch(batch_id)
    course_level  = courseId_forBatch(batch_id)
    sql = "SELECT DISTINCT s.id \
             FROM students s \
             JOIN batch_students bs ON bs.student_id = s.id \
        LEFT JOIN batches b ON b.id = bs.batch_id \
            WHERE (bs.next_course_id = %d OR s.enter_course_id =%d) \
              AND s.id NOT IN (SELECT s.id \
                              FROM students s\
                              JOIN batch_students bs ON bs.student_id = s.id  \
                              JOIN batches b ON b.id = bs.batch_id \
	                         JOIN courses c ON c.id = b.course_id \
                              JOIN course_levels cl ON cl.course_level = c.course_level \
                             WHERE cl.course_level = %d)" % (course_level, course_level, course_level)
    #rint sql
    return getList(sql)


def studentIDs_inStudygroup(studygroup_id):
    sql = "SELECT s.id FROM studygroup_students sg \
             JOIN students s ON s.id = sg.student_id \
            WHERE studygroup_id = %d \
              AND '%s' BETWEEN s.reg_year AND s.exit_year  " % (studygroup_id, gVar.schYr)
    #rint sql
    return getList(sql)

def sql_students_forSch_remaining(school_id, id_set, schYr = gVar.schYr):
    sql ="SELECT s.id, CONCAT_WS(' ', first_name, middle_name, last_name) as full_name \
                    FROM students s \
               LEFT JOIN nis n ON s.id = n.student_id \
                   WHERE %d BETWEEN n.admission_year AND n.withdrew_year\
                     AND n.school_id = %d \
                     AND NOT FIND_IN_SET(s.id, '%s') \
                ORDER BY s.id" % (schYr, school_id, id_set)
    #rint sql
    return sql
    #return getAllCol(sql)

def studentIDs_inBatch(batch_id, do_filter = False, want = 'dict'):
    sql = "SELECT s.id \
             FROM students s \
             JOIN batch_students bs ON bs.student_id = s.id \
            WHERE bs.batch_id = %d \
              AND '%s' BETWEEN s.reg_year AND s.exit_year " % (batch_id, gVar.schYr)
    
    if do_filter:
        sql +=  "AND bs.rereg_status = '%s'" % do_filter
    
    sql += " GROUP BY s.id"

    if want == 'dict':
         res = getAll_dict(sql)
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
	     JOIN nis n ON s.id = n.student_id \
            WHERE cl.course_level = %d \
              AND n.admission_year = %d" % (course_id, schYr)
    if do_filter:
        sql +=  "AND bs.admission_status_id = '%s' " % do_filter
    return getRes(sql, 'list')

def studentIDs_inCourse(course_id, do_filter = False,  want = 'dict'): 
    sql = " SELECT s.id \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches ON b.id = bs.batch_id \
             WHERE bs.course_id = %d \
               AND b.schYr = %d" % (course_id, gVar.schYr)
    if do_filter:
        sql +=  "AND bs.rereg_status = '%s'" % do_filter
    return getRes(sql, want)

def students_not_in_studygroup(studygroup_id):
    sql = "SELECT student_id FROM students \
            WHERE NOT FIND_IN_SET(s.id, SELECT student_id \
	                                 FROM studygroup_students \
					              WHERE studygroup_id = %d)" % studygroup_id
    return getList(sql)


def studygroups_forBatch(batch_id): 
    sql = "SELECT sg.id, st.subject_title \
             FROM studygroups sg \
             JOIN subject_titles st ON st.id = sg.subject_title_id \
            WHERE FIND_IN_SET(%d, sg.batch_ids)" % batch_id
    #rint sql
    return getAll_dict(sql)

def students_inCourse(course_id): 
    sql = " SELECT s.id, s.first_name, s.middle_name, s.last_name, bs.rereg_status\
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
             WHERE b.course_id = %d \
               AND b.schYr = %d " % (course_id, gVar.schYr)
    #rint sql
    return getAll_dict(sql)

def students_inCourseV(course_id): 
    sql = " SELECT DISTINCT s.id, bs.rereg_status, s.first_name, s.middle_name, s.last_name \
              FROM students s \
              JOIN batch_students bs ON s.id = bs.student_id \
              JOIN batches b ON b.id = bs.batch_id \
             WHERE b.course_id = %d  \
                OR (bs.next_course_id = %d AND b.schYr = (%d -1 ) ) \
          GROUP BY s.id" % (course_id, course_id, gVar.schYr)
    #rint sql
    return getAllCol(sql)
 
def studentIDs_forLevel(age_level=0, schYr = 2000, want = 'dict'): 
    sql = "SELECT s.id \
             FROM students s \
             JOIN batches b ON s.batch_id = b.id \
	        JOIN courses c ON c.id = b.course_id \
             LEFT JOIN course_levels cl ON c.course_level = cl.course_level \
            WHERE cl.course_level = %d \
              AND s.admissiion_year = %d \
              AND '%s' BETWEEN s.reg_year AND s.exit_year " % (int(age_level), schYr, gVar.schYr)
    return getRes(sql, want)

def studentInfoPopup(student_id):
    student_id = int(student_id)
    
    name         = studentFullName(student_id)
    school_name  = '-'
    course_title = '-'
    batch_name   = '-'
    age          = '-'
    gender       = '-'
    ship         = '-'
    
    if student_id:
        studentDetails = studentSchDetails(student_id)
        if studentDetails:
            school_id    = studentDetails['school_id']
            school_name  =  schoolName(school_id)
            
            course_level = studentDetails['course_level']
            course_title    =  courseTitle(course_level)
            
            age    = studentDetails['birth_date']
            gender =  gender(studentDetails['gender'])
            ship   =  shipName(studentDetails['ship_id'])
        
        batch_id =  batchID_forStudent(student_id)
        if batch_id: batch_name =  batchName(batch_id)

    line1 = 'Name: %s,  %s'  % (name, gender)
    line2 = 'DOB: %s,    SHIP: %s'  % (age, ship)
    line3 = 'BATCH: %s, %s, %s' % (batch_name, course_title, school_name)
    
    mnu_abs = wx.Menu()
    mnu_abs.AppendItem(wx.MenuItem(mnu_abs, -1, line1))
    mnu_abs.AppendItem(wx.MenuItem(mnu_abs, -1, line2))
    mnu_abs.AppendItem(wx.MenuItem(mnu_abs, -1, line3))
        
    #mnu_abs.AppendSeparator()
    
    return mnu_abs   
        
        
#-   ------ subject ------------------------------------------------------------
def studygroupIDs_forBatch(batch_id):
    sql = "SELECT id \
             FROM studygroups \
            WHERE FIND_IN_SET(%d, batch_ids)" % int(batch_id)
    return getList(sql)
    
def removeDups(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    
    
def studygroups_forBatch_forTeacher(batch_id, employee_id):
    sql = "SELECT sg.id \
             FROM studygroups sg\
             JOIN subject_titles st ON st.id = sg.subject_title_id \
            WHERE sg.employee_id = %d \
            AND FIND_IN_SET(%d, sg.batch_ids)" % (employee_id, batch_id)
    return getList(sql)

def getStudygroups_forBatch(batch_id):
    sql = "SELECT id \
             FROM studygroups \
            WHERE FIND_IN_SET(%d, batch_ids)" % (batch_id, batch_id)
    return getList(sql)

def studygroup_isUsed(studygroup_id):
    sql = " SELECT COUNT(id) \
              FROM studygroups \
             WHERE id = %d" % int(studygroup_id)
    if getDig(sql):
          return True
    else: return False

def subjectTitle_forBatch(batch_id):
    sql = " SELECT st.subject_title \
              FROM subjects_titles st \
              JOIN studygroups sg ON st.id = sg.subject_id \
             WHERE FIND_IN_SET(%d, sg.batch_ids)" % int(batch_id)
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
    res  = getAll_dict(sql)
    list = ''
    if res:
        for row in res:
            list +=row['phone_number'] + "\n"
    return list
    
def telpNoList(guid):# for appending to a list
    sql = "SELECT guid, phone_number, phone_location \
             FROM phone_numbers \
            WHERE guid = %s" % guid
    return getAll_dict(sql)

def teacherNames_forSubject(subject_id):
    str=''
    if subject_id:
        teacherID_list, newList= teacherIDs_forSubject(subject_id), []
        for teacher_id in teacherID_list: newList.append(teacherName(id))
        str = ','.join(newList)
    return str

def teachers_forSch(sch_id):
    sql="SELECT id, username \
           FROM employees \
          WHERE employee_category_id = 2"
    return getList(sql)
    
def teachers_otherThan(teacher_list=''):
    sql = " SELECT id, username \
              FROM employees \
             WHERE employee_category_id = 2"
    if teacher_list:
        sql += " AND NOT id IN (%s)" % teacher_list
    return getAll_dict(sql)
    
def teachers_forBatch(batch_id): # used x 1
    if batch_id:
        sql = " SELECT employee_ids \
                  FROM batches \
                 WHERE id = %d" % batch_id
        res = getStr(sql)
    if res:
        employee_ids = res['employee_ids'].split(',')
        return employee_ids
    else: return []

def teacherNames_forBatch(batch_id): # used x 2
    employee_id_list = teachers_forBatch(batch_id)
    namesList = []
    for employee_id in employee_id_list:
        name = teacherName(employee_id)
        if name:namesList.append(name)
    namesString = ','.join(namesList)
    return namesString
    
def teachers_notInSubjects(testlist=[]):
    newlist=[]
    testlist=','.join(testlist)
    sql = "SELECT id \
             FROM employees \
            WHERE teacher = 1\
              AND status = True \
              AND NOT FIND_IN_SET(id, %s)" % testlist
    return getList(sql)
 
    
def teacherIDs_forSubject(studygroup_id):
    if not studygroup_id:return []
    sql = "SELECT enployee_id \
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
    return getAll_dict(sql)
    
def address(addr_id):
    address = ""
    sql = "SELECT * \
             FROM addresses \
            WHERE id = %d" % addr_id
    addr = getOne_dict(sql)
     
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
        res = getOne_dict(sql)
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
        res = getOne_dict(sql)
        if res: estateAddress += "%s, #%s\n" % (res[name], addr['houseNo'],)
        # find the estate
        sql = "SELECT * \
                 FROM address_items \
                WHERE id = %s \
                  AND item_type=2" % (item_id,)
        res = getOne_dict(sql)
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
    addr = getOne_dict(sql)
    if addr:
        if addr['street']:
            address += "%s #%s ," % (addr['street'], addr['houseNo'])
        elif addr['houseNo']: address += "%s, " % addr['houseNo']
            
        addrItems = str(addr['addrItem_id'])
        for item_id in addrItems:
            sql = "SELECT * \
                     FROM address_items \
                    WHERE id=%s" % item_id
            res = getOne_dict(sql)
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
    sql = " SELECT itemName \
              FROM addressItems \
             WHERE id = %d" % int(addrItem_id)
    return getStr(sql)

def addrItem(addrItem_id):
    sql = " SELECT * \
              FROM address_items \
             WHERE id = %d" % int(addrItem_id)
    return getOne_dict(sql)

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
