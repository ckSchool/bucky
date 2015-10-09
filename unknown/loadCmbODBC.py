import  gVar #, calendar
import fetchodbc as fetch
#--- a --------------------------------------------------------------------------

def admissionStatus(cmb):
    gen(cmb, "SELECT id, status FROM admission_status", 'Any')
    
def standards(cmb):
    gen(cmb," SELECT a.affective_id, a.affectiveTitle \
                FROM standards a;")
    
def grading_standards(cmb):
    gen(cmb," SELECT id, standard \
                FROM grading_standards")
                
def assignment(cmb,sql):
    gen(cmb,"")
    
def assignmentTypes(cmb):
    genAdd(cmb, " SELECT id, catagory  \
                 FROM assignment_catagories \
                ORDER BY catagory", 'Add catagory')
    
def pop(cmb):
    sql = "SELECT id, town FROM towns"
    gen(cmb, sql)
    
def address_items(cmb, addr_item_type, dict={}):
    sql = " SELECT id, name \
              FROM address_items \
             WHERE item_type = '%s'" % addr_item_type
    #rint sql
    #rint fetch.getAll_dict(sql)
    gen(cmb, sql)

def appendRes(cmb, sql):
    index=1
    dict ={}
    res=fetch.getAll_dict(sql)
    for row in res:
        id = row['addrItem_id']
        title = row['name']
        next_id = fetch.nextItemID(id)
        nextItem = fetch.addrItemName(next_id)
        cmb.Append(title, id)
        dict[index] = id
        index += 1
    return dict

def addrItemTypes(cmb, id):
    sql = " SELECT itemType_id, name \
              FROM addressitemtypes \
             WHERE itemType_id > %d" % id
    ###rint sql
    gen(cmb, sql)
    

#-  b  ------------------------------------------------------------------------- 
 
def blood(cmb):
    cmb.Clear()
    cmb.Append("",    0)
    cmb.Append("O-",  1)
    cmb.Append("O",   2)
    cmb.Append("O+",  3)
    cmb.Append("A-",  4)
    cmb.Append("A",   5)
    cmb.Append("A+",  6)

    cmb.Append("B-",  7)
    cmb.Append("B",   8)
    cmb.Append("B+",  9)
    cmb.Append("AB-",10)
    cmb.Append("AB", 11)
    cmb.Append("AB+",12)
    cmb.Select(0)
    
def tax(cmb):
    cmb.Clear()
    cmb.Append("",    0)
    cmb.Append("No tax",  1)
    cmb.Append("Tax Included",   2)
    cmb.Select(0)

def units(cmb):
    cmb.Clear()
    cmb.Append("",    0)
    cmb.Append("Months school fee", 1)
    cmb.Append("Items",  2)
    cmb.Select(0)
   
def batches_forYear_minLevel(cmb, schYr, level, first_item=''):
    cmb.Clear()
    if first_item: cmb.Append(first_item, 0)
    sql = " SELECT b.id, b.batch_name \
              FROM batches b  \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE b.schYr = %d \
               AND cl.course_level >= %d \
             ORDER BY cl.course_level" % (level, schYr)
    #rint sql
    gen(cmb, sql, first_item)
   
def batches_forYear(cmb, schYr=0, first_item=''):
    if schYr==0: schYr=gVar.schYr
    #rint 'loadCmb:batches_forYear'
    cmb.Clear()
    cmb.Append('Without batch', 0)
    sql = " SELECT b.id, b.batch_name \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_titles cl ON cl.id = c.course_title_id \
             WHERE b.schYr = %d \
             ORDER BY cl.course_level" % schYr
    #rint sql
    gen(cmb, sql, first_item)

def batchDivisions(cmb, batch_id):
    cmb.Clear()
    cmb.Append('Entire', 0)
    
    sql = " SELECT divisions \
              FROM batches\
             WHERE id = %d" % batch_id
    divisions = fetch.getStr(sql)
    if not divisions:
        cmb.Select(0)
        return

    list  = row.split(',')
    index = 0
    for set in list:
        groups = set.split('/')
        for group in groups:
            cmb.Append(group, index)
            index += 1
            
def batches_forCourse(cmb, course_id = 0, first_item = ''):
    sql = " SELECT b.id, b.batch_name \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE b.schYr = %d " % gVar.schYr
    
    if int(course_id) > 0:
        sql += " AND c.id = %d" % course_id
        
    else:
        sql += " AND cl.course_level > -5 "
        
    sql += " ORDER BY b.batch_name "
    #rint 'batches_forCourse:', sql
    return gen(cmb, sql, first_item)    
    
def batches_forCourseTitle(cmb, course_level = 0, first_item = ''):
    sql = " SELECT b.id, b.batch_name \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE b.schYr = %d " % gVar.schYr
    
    if int(course_title_id) > 0:
        sql += " AND cl.level= %d" % course_level
        
    else:
        sql += " AND cl.course_level > -5 "
        
    sql += " ORDER BY b.batch_name "
    #rint 'batches_forCourse:', sql
    return gen(cmb, sql, first_item)
    
def batches_forLevel(cmb, course_level = 0, first_item = ''):
    #rint 'loadCmb: batches_forLevel:'
    sql = " SELECT b.id, b.batch_name, cl.level, cl.level_title, \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE cl.course_level  > -5 "
    
    if int(course_level) > 0:  sql += " AND cl.course_level = %d" % course_level
    #rint  sql
    return gen(cmb, sql, first_item)
    
def batches_forYear_forLevel(cmb, year, course_level = 0, first_item = ''):
    #rint 'loadCmb: batches_forLevel:'
    sql = " SELECT b.id, b.batch_name, cl.level, cl.level_title \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels ct ON cl.id = c.course_title_id \
             WHERE cl.course_level  > 0 \
               AND b.schYr = %d " % year
    if int(course_level) > 0:
        sql += " AND cl.course_level = %d" % course_level
    #rint  sql
    return gen(cmb, sql, first_item)  
    
    
def batches_forSchool(cmb, school_id = 0, first_item = ''):
    if school_id > 3: school_id = 3
    sql = " SELECT b.id, b.batch_name \
              FROM batches b \
              JOIN courses c ON c.id = b.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE cl.course_level > -5 \
               AND cl.school_id = %d \
               AND b.schYr =%d \
          ORDER BY cl.course_level" % (school_id, gVar.schYr)

    gen(cmb, sql, first_item)
     
def batches_forMentor(cmb, employee_id):
     
    id_list = fetch.batches_forMentor(employee_id)
    #rint 'batches_forMentor , id_list', id_list
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
     
    cmb.Clear()
    if not id_list:return
    cmb.Freeze  # locks the combo so that other processes are not called
        
    select = 0
    index  = 0
    for id in id_list:
        title = fetch.batchName(id)
        cmb.Append(title, id)
        if id == origional_id:
            select = index
        index += 1
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select)
    cmb.Thaw

def bookingFees(cmb):
    gen(cmb," SELECT fee_id, feeAmount \
                FROM finance_fees \
               WHERE feeType = 'Booking' \
                 AND validTillYr >= 2010")
       
#-  c  ------------------------------------------------------------------------- 
 

def classesOthers_forBatch(cmb, employee_id, batch_id):
    sql = " SELECT s.id, s.name \
              FROM employee_subjects es \
              JOIN subjects s on s.id = es.subject_title_id \
             WHERE es.employee_id <> %d \
               AND s.batch_id = %d \
             GROUP BY s.batch_id" % (employee_id, batch_id)
    
    
    genNoBlank(cmb,sql)
      
def childStatus(cmb):
    gen(cmb," SELECT id, childStatus FROM childStatuss","")

def courseTitles(cmb):
    #rint 'loadCmb, courseTitles'
    sql = " SELECT id, level_title \
              FROM courselevels_forschool \
             WHERE course_level > -5 \
             ORDER BY course_level"
    #rint sql
    return gen(cmb, sql)

def courseTitles_forLevel(cmb, course_level=0, first_item=''):
    #rint 'courseTitles_forLevel_forYear', course_level 
    sql = " SELECT id, level_title \
              FROM course_levels \
             WHERE course_level > -5"
    
    if course_level: sql +=" AND course_level = %s" % course_level

    return gen(cmb, sql, first_item)

def courseLevels(cmb):
    sql = "SELECT course_level, course_title   \
             FROM courses_levels ORDER BY course_level"
    return gen(cmb, sql, '-')

def getKey(item):
    return item[1]

def courseLevels_forSchool(cmb, school_id = 0):
    school_id = int(school_id)
    origional_level = fetch.cmbValue(cmb)
    
    sql = "SELECT course_level, course_title   \
             FROM courses_levels WHERE school_id = %d  ORDER BY course_level" % school_id # 
    #rint sql
    return gen(cmb, sql, '')
    dataSet = set(fetch.getList(sql))
    #rint dataSet
    cmb.Freeze  # locks the combo so that other processes are not called
    cmb.Clear()
    
    index = 0
    for level in dataSet:
        #rint index, level
        cmb.Append(str(level), index)
        index += 1
        
    if not origional_level:
        cmb.SetSelection(0)
    else:
        restored = restore_str(cmb, origional_level)
    cmb.Thaw    
    if restored:
        return origional_level
    else:
        return cmbValue(cmb)
    
    #rint sql
    #return gen(cmb, sql, '')

def courses_forLevel_forYear(cmb, yr, level):
    sql = "SELECT courses.id, courses.course_name \
             FROM courses_by_year  \
            INNER JOIN courses \
               ON (int(courses_by_year.course_id) = int(courses.id)) \
            WHERE courses_by_year.schYr = %d \
            AND courses.course_level =%d\
            ORDER BY courses.course_level" % (yr, level)
    return gen(cmb, sql)


def addressItems(cmb, itemType, nextItemID):
    if nextItemID:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType ='%s' \
                  AND nextItemID = %d \
                ORDER BY (itemName)" % (itemType, nextItemID)
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType ='%s' \
                ORDER BY (itemName)" % itemType
        
    #rint 'addressItems', sql, fetch.getAllCol(sql)
    gen(cmb, sql, ' ')


def estates(cmb):
    sql = "SELECT estate FROM addresses GROUP BY (estate) ORDER BY (estate)"
    res = fetch.getList(sql)
    cmb.SetItems(res)
    cmb.Insert('-new-', 0)
    cmb.Insert('', 0)
    return cmb

"""
def countriesForProvince(province=''):
    if province:
        sql = "SELECT nextItemID \
                 FROM addressItems \
                WHERE itemType = 'province' \
                  AND itemName='%s'"  % province
        iid = fetch.getDig(sql)
        sql = "SELECT itemName \
              FROM addressItems \
              WHERE id = %d" % iid
    
    else:
        sql = "SELECT id, itemName \
                 FROM addressItems \
                WHERE itemType = 'country'"
        
    res = fetch.getList(sql)
    #rint sql, res
    cmb.SetItems(res)
    cmb.Insert('', 0)
    return cmb"""

def countries(cmb):
    sql = "SELECT id, itemName \
             FROM addressItems \
             WHERE itemType = 'country'"
    res = fetch.getList(sql)
    
    cmb.Freeze()
    for row in res:
        cmb.Append(row[1], row[0])
    cmb.Thaw()
    return cmb
#-----------------------------------------------------------------






#-------------------------------------------------------------
def courses_forYear(cmb, yr):
    sql = "SELECT courses.id, courses.course_name, courses.course_level \
             FROM courses_by_year  \
            INNER JOIN courses \
               ON (int(courses_by_year.course_id) = int(courses.id)) \
            WHERE courses_by_year.schYr = %d \
            ORDER BY (courses.course_level)" % yr
    #rint sql
    #rint fetch.getAllDict(sql)
    return gen(cmb, sql) 
    

def NextLevelCourses_forYear(cmb, schYr, level):
    sql = "SELECT courses.id, courses.course_name FROM courses_by_year \
            INNER JOIN courses ON (courses_by_year.course_id = courses.id ) \
            WHERE courses.course_level=%s \
              AND courses_by_year.schYr=%d" % (level, schYr)
    #rint sql
    return gen(cmb, sql)

def courses_forSchool_forYear(cmb, school_id=0, yr=0):
    school_id = int(school_id)
    if school_id == 0: return
    sql = "SELECT c.id, c.course_title \
             FROM courses c \
             JOIN course_levels cl ON c.course_level = c.course_level \
            WHERE c.schYr = %d \
              AND cl.school_id = %d \
            ORDER BY cl.course_level" % (yr, school_id )
    return gen(cmb, sql)

def courseTitles_forSchool(cmb, school_id = 0, first_item=''):
    school_id = int(school_id)

    sql = "SELECT id, level_title \
             FROM course_levels_forschool \
            WHERE course_level > -5"
    
    if school_id > 0: sql += " AND school_id = %d" % school_id
    
    sql += " ORDER BY course_level"
    
    cmb_id = gen(cmb, sql, first_item)
    return cmb_id

def levels_forSchool(cmb, school_id):
    sql = "SELECT id, level_title \
             FROM course_levels"
    
    if school_id: sql += "  WHERE school_id = %d " % school_id
            
    sql += " ORDER BY course_level"
    return gen(cmb, sql)

def courses_minLevel(cmb, level):
    sql = "SELECT id, level_title \
             FROM course_levels \
            WHERE course_level >= %d \
            ORDER BY course_level" % (level,)
    return gen(cmb, sql)

#---  d, e, f, g    ---------------------------------------------------------------------

def days(cmb):
    dayList = ['Monday','Tuesday','Wednesday','Thursday','Friday'] #fetch.getAll_col(sql)
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
    cmb.Clear()
    cmb.Freeze  # locks the combo so that other processes are not called
  
    select = 0
    i = 0
    for dayName in dayList:
        cmb.Append(dayName, i)
        if i == origional_id:
            select = i
        i += 1
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select)
    cmb.Thaw
    
def dayNumbers(cmb, month=0, year=0):
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
    
    cmb.Clear()
    cmb.Freeze  # locks the combo so that other processes are not called
  
    if month and year:
        for i in range(1, calendar.monthrange(year, month)[1]+1):
            cmb.Append(str(i), i)
    else:
        for i in range(1,32):
            cmb.Append(str(i), i)
    
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select)
    cmb.Thaw
    
    
"""def estates(cmb, kelurahan=''):
    if kelurahan:
        pass
    else:
        # 1:number, 2:street, 3:estate, 4:block, 5:road, 6:postcode, 7:kelurahan, 8:kecematan, 9:kabupaten, 10:province, 11:country
        # 2:Jl. Mangga, 4:J1, 1:No. 18, 3:Perumahan Cemara Asri, 4:Deliserdang, 
        sql = "SELECT address FROM OrangTua"""""
    
        
           
def enrollmentFees(cmb):
    sql =" SELECT fee_id, feeAmount \
             FROM school_fees \
            WHERE feeType = 'Enroll' \
              AND validTillYr >= %s" % gVar.schYr
    gen(cmb,sql)

def exculActivities(cmb,sql):
    gen(cmb," SELECT e.exCulActivity_id, e.activityTitle \
                FROM exculactivities e;")
    
def exculActivitiesPool(cmb, exculset_id, edited_activity_id=0):
    # collect activity_ids for exculset_id
    sql = " SELECT ea.id \
              FROM excul ex \
              JOIN excul_activity_titles ea ON ea.id = ex.activity_id \
             WHERE ex.exculset_id = %d " % (exculset_id, )
    
    activityIDs = fetch.getList(sql)

    if edited_activity_id:
        l = []
        for x in activityIDs:
            #rint x
            if not x == edited_activity_id: l.append(x)
        activityIDs = l
        
    activityIDs = [str(x) for x in activityIDs]
    #rint 'activityIDs',activityIDs
        
    listStr = "'%s'" % ','.join(activityIDs)
    
    sql = " SELECT id, name \
              FROM excul_activity_titles \
             WHERE NOT FIND_IN_SET(id, %s) \
             ORDER BY name" % listStr
    #rint sql, fetch.getAll_col(sql)
    fillCmb(cmb, fetch.getAll_col(sql), 'without activity')
    restore(cmb, int(edited_activity_id))
    
def exculTeacherPool(cmb, exculset_id, edited_teacher_id=0):
    exculList  = fetch.excul_groups_forExculSet(exculset_id)
    teacherIDs = [str(x[0]) for x in exculList]

    if edited_teacher_id:
        l = []
        for x in teacherIDs:
            if not x == str(edited_teacher_id): l.append(x)
        teacherIDs = l

    listStr = "'%s'" % ','.join(teacherIDs)
    
    sql = " SELECT id, CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name \
              FROM employees \
             WHERE employee_category_id = 2 \
               AND %d BETWEEN join_schYr AND leave_schYr \
               AND NOT FIND_IN_SET(id, %s) \
             ORDER BY full_name" % (gVar.schYr, listStr)
    fillCmb(cmb, fetch.getAll_col(sql),'without teacher')
    restore(cmb, int(edited_teacher_id))
    
def forYr(cmb, limit):
    for yr in range(2000,limit):
        id = yr
        title = yr
        cmb.Append(str(title),id) 

def faiths(cmb):
    gen(cmb, "SELECT id, faith FROM faiths", ' ')
    
def gender(cmb):
    cmb.Clear()
    cmb.Append(" ", 2)
    cmb.Append("Male",   1)
    cmb.Append("Female", 0)
    cmb.Select(0)

         
#---  h, i, j, k  ------------------------------------------------------------------------- 
  
           
#---  l, m, n, o,  ------------------------------------------------------------------------- 
  
def livesWith(cmb):
    gen(cmb," SELECT p.`id`, p.`name` \
                FROM parent_types p;", ' ')

def lessonsForTeacher(cmb, employee_id, NoBlank=False): # will need modification to cope with multi teachers
    sql = " SELECT s.id, s.name \
              FROM employees_subjects es \
              JOIN subjects s ON s.id = es.subject_title_id \
             WHERE es.employee_id = %d \
             GROUP BY s.id" % employee_id
    if NoBlank:
        genNoBlank(cmb,sql)
    else:
        gen(cmb,sql)
        
def subjects__forTeacher_forBatch(cmb, teacher_id, batch_id, NoBlank=False):
    sql = " SELECT st.id, st.subject_title \
              FROM studygroups sg \
              JOIN subject_titles st ON sg.subject_title_id = st.id \
             WHERE sg.employee_id = %d \
               AND sg.batch_id =%d " % (teacher_id, batch_id)
    #rint sql
    if NoBlank:
        genNoBlank(cmb,sql)
    else:
        gen(cmb,sql)

  
def lessons_forBatch(cmb, batch_id, NoBlank=False):
    sql = "SELECT id, name FROM subjects \
            WHERE batch_id = %d \
            GROUP BY id" % int(batch_id)
    if NoBlank:
        genNoBlank(cmb,sql)
    else:
        gen(cmb,sql)
                                 

def occ(cmb):
    gen(cmb," SELECT o.id, o.occupation \
                FROM occupations o;")

         
#---  p, q, r  ------------------------------------------------------------------------- 

def paymentType(cmb):
    gen(cmb," SELECT p.paymentCode_id, p.paymentTitle \
                FROM paymentcodes p;")
        
def pob(cmb):
    genNoId(cmb," SELECT kabupaten \
                FROM postcodes \
                GROUP BY (kabupaten) \
                ORDER BY (kabupaten)")
    
def schoolFees_forYr(cmb):
    sql = "SELECT ii.id, item_description \
                FROM inv_items ii \
                JOIN inv_item_codes iic ON iic.id = ii.item_code \
               WHERE ii.item_code = 1 \
                 AND ii.valid_till_schYr = %d" % gVar.schYr
    #rint sql    
    gen(cmb, sql)
    #rint 'loaded cmb schoolFees_forYr', gVar.schYr
  
def prevSch(cmb):
    gen(cmb," SELECT id, name \
                FROM schools")

def qualification(cmb):
    genAdd(cmb," SELECT id, qualification \
                FROM qualifications", 'New qualification')
    

def relationship(cmb):
    gen(cmb," SELECT id, p.name  \
                FROM parent_types")
    
def schYrs(cmb, Affix=''):
    genNoId(cmb," SELECT Tahun \
                FROM TahunAjaran ORDER BY (Tahun)", Affix)
    
def restore(cmb, origional_id=0):
    cmb.Freeze()
    try:
        if origional_id:
            for y in range(cmb.GetCount()):
                cmb.Select(y) # select first item
                itemId = fetch.cmbID(cmb)
                if itemId == origional_id:
                    cmb.Thaw()
                    return True
    except:
        pass
    
    cmb.Select(0)
    cmb.Thaw()
    return False



def restore_str(cmb, myStr = ''):
    cmb.Freeze()
    myStr = str(myStr)
    myStr = myStr.strip() # str(myStr.strip())
    idx   = cmb.FindString(myStr)
    if idx: cmb.Select(idx) # select first item
    else:   cmb.Select(0)
    cmb.Thaw()    
#---  s  ------------------------------------------------------------------------- 

def schFees(cmb):
    origionalItem = cmb.GetSelection()
    if origionalItem > -1:  origional_id = cmb.GetClientData(origionalItem)
        
    cmb.Freeze()
    cmb.Clear()
    
    sql = " SELECT fee_id, feeType, feeAmount, description \
              FROM schoolfees \
             WHERE validTillYr >= 2010"
    ###rint sql
    res = fetch.getAll_dict(sql)
    if res:
        cmb.Append('',0)
        for row in res:
            id = row['fee_id']
            title = "%s : %s" % (row['feeType'], row['feeAmount'])
            cmb.Append(title, id)
            
        cmb.Select(0)
    cmb.Thaw()
    
    if origionalItem > 0: cmb.Select(origional_id)
            
def studentSchStatus(cmb):
    gen(cmb," SELECT s.`studentSchStatus_id`, s.`statusTitle` \
                FROM studentschstatus s;")
      
def schDiv(cmb ):
    genNoBlank(cmb," SELECT id, school_type \
                       FROM schools \
                      WHERE isCK = TRUE", '')
    
def schools(cmb, ck='', first=''):
    sql = "SELECT Kode, Nama FROM Sekolah "
    if ck:
        sql += " WHERE isCK = 1"
    #rint sql
    gen(cmb, sql, first)
     
def ship(cmb):
    gen(cmb," SELECT id, name FROM ships", "Ship")

def subjects(cmb):
    gen(cmb," SELECT * FROM subject_titles \
               WHERE NOT is_deleted = True")

#---- t -------------------------------------------------------------------------
    
def teachers(cmb, firsttitle=''):
    genAdd(cmb," SELECT id, first_name \
              FROM employees \
             WHERE status = TRUE AND teacher=1", 'New employee')
    return
    ###rint sql
    
    dataSet = fetch.getAll_dict(sql)
    ###rint dataSet
    originalIndex = int(cmb.GetSelection())
    select = 0
    
    if originalIndex > -1:  origional_id = cmb.GetClientData(originalIndex) 
    else:                   origional_id = 0
        
    
    cmb.Freeze()  # locks the combo so that other events are not called
    cmb.Clear()
    if firsttitle:
        cmb.Append(firsttitle, 0) # add a blank
        
    
    if schid > 0:
        index = 1
        for row in dataSet:
            schIDs = row['schools'].split(',')
            if schid in schIDs:
                id    = row['id']
                title = row['first_name']
                cmb.Append(title, id)
                if id == origional_id: select = index
                index += 1
    else:
        index = 1
        for row in dataSet:
            id = row[0]
            title = str(row[1])
            cmb.Append(title, id)
            if id == origional_id:select = index
            index += 1
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select) 
    cmb.Thaw()


def travelsWith(cmb):
    gen(cmb," SELECT id, option \
                FROM travel_options")


    
#-------------------------------------------------------------------------------
def setItems(cmb, sql , first_item = '') : #sql should be designed to return two items 'id' and 'title'
    try:    origional_str = fetch.cmbValue(cmb)
    except: origional_str = ''
    dataSet      = fetch.getList(sql)

    cmb.Freeze()  # locks the combo so that other processes are not called
    cmb.Clear()
    cmb.AppendItems(dataSet)
    restored = restore_str(cmb, origional_str)
    cmb.Thaw()
    
    if restored: return origional_str
    else:
        if len(dataSet)==1:
            cmb.SetSelection(0)
            return fetch.cmbValue(cmb)
        else:return 0

def genNoId(cmb, sql , first_item = '') : #sql should be designed to return two items 'id' and 'title'
    try:
        origional_str = fetch.cmbValue(cmb)
    except: origional_str = ''
    dataSet      = fetch.getList(sql)
    #rint dataSet
    cmb.Freeze()  # locks the combo so that other processes are not called
    cmb.Clear()
    try:
        if first_item: 
            cmb.Append(first_item, 0)
        x = 1    
        for item in dataSet:
            #rint row
            cmb.Append(str(item), x)
            x += 1
            #if x%10==0: rint x 
        restored = restore_str(cmb, origional_str)
        
        cmb.Thaw()    
        if restored: return origional_str
        else:        return 0
    except:
        #rint 'load cmb error'
        return 0
        
def gen(cmb, sql , first_item='') : #sql should be designed to return two items 'id' and 'title'
    try:    origional_id = fetch.cmbID(cmb)
    except: origional_id=0
    
    dataSet      = fetch.getAllCol(sql)
    
    cmb.Freeze()  # locks the combo so that other processes are not called
    cmb.Clear()
    
    try:
        if first_item:   cmb.Append(first_item, 0)
            
        for row in dataSet:
            ##rint row
            cmb.Append(str(row[1]), row[0])
            
        restored = restore(cmb, origional_id)
        
        cmb.Thaw()
        
        if restored: return origional_id
        else:        return 0
        
    except:
        #rint 'load cmb error'
        cmb.Thaw()
        return 0
    
    cmb.Thaw()

    
def cmbID(cmb):
    itemNo = cmb.GetSelection()
    if itemNo > -1:
        return int(cmb.GetClientData(itemNo))
    return 0

def cmbValue(cmb):
    index= cmb.GetSelection()
    if index > -1:
        try:
            return str(cmb.GetValue(index))
        except:
            return cmb.GetString(index)
    return 0
 
def genAdd(cmb, sql , first_item='') : #sql should be designed to return two items 'id' and 'title'
    
    origional_id = fetch.cmbID(cmb)
    
    dataSet      = fetch.getAllCol(sql)
    cmb.Freeze()  # locks the combo so that other processes are not called
    
    cmb.Clear()
    
    if first_item:
        cmb.Append(first_item, -1)
        cmb.Append('', 0)
    for row in dataSet:
        #rint 'x'
        cmb.Append(str(row[1]), row[0])
    
    restored = restore(cmb, origional_id)
    
    cmb.Thaw()
    
    if restored:
        cmb.Thaw  
        return origional_id
    else:
        cmb.SetSelection(1)
    origional_id = fetch.cmbID(cmb)
    cmb.Freeze()  # locks the combo so that other processes are not called
    #rint 'dataSet:', dataSet
    cmb.Clear()
    if first_item:      cmb.Append(first_item,0)
    for row in dataSet:
        txt, iid = str(row[1]), row[0]
        #rint txt, iid
        cmb.Append(txt , iid)
    restored = restore(cmb, origional_id)
    
    cmb.Thaw()    
    if restored: return origional_id
    else:        return 0

def genNoBlank(cmb, sql, first_item='') :
    #rint 'loadCmb: genNoBlank:', sql, fetch.getAll_dict(sql)
    #sql should be designed to return first two items  'id' , 'title'
    dataSet = fetch.getAll_col(sql)
    origional_id = fetch.cmbID(cmb)
    
    cmb.Freeze()  # locks the combo so that other processes are not called
    
    cmb.Clear()
    if first_item:      cmb.Append(first_item, '0')
    for row in dataSet: cmb.Append(str(row[1]), row[0])
    restore(cmb, origional_id)
    
    cmb.Thaw()

def genAppend(cmb, title, id) : #is designed for two items 'id' and 'title'
    originalIndex = int(cmb.GetSelection())
    cmb.Freeze()  # locks the combo so that other processes are not called

    cmb.Append(title, id)
    cmb.Select(originalIndex)
     
    cmb.Thaw()
    

def regStatus(cmb):
    cmb.Freeze()
    cmb.Append("")
    cmb.Append("leave")
    cmb.Append("retake")
    cmb.Append("stay")
    cmb.Append("paid")
    cmb.Thaw()
 
def inv_students(cmb, filter_panel):
    school_id, course_id, batch_id = filter_panel.getSelectedIDs()
    #rint 'inv_students', cmb, school_id, course_title_id, batch_id
    
    if batch_id:
        sql ="SELECT s.id, s.first_name, s.middle_name, s.last_name \
                FROM students s \
                JOIN batch_students bs ON s.id = bs.student_id \
                JOIN batches b ON b.id = bs.batch_id \
               WHERE s.is_active = 1 \
                 AND b.id = %d" % batch_id
        
    elif course_id:
        sql ="SELECT s.id, s.first_name, s.middle_name, s.last_name \
                FROM students s \
                JOIN batch_students bs ON s.id = bs.student_id \
                JOIN batches b ON b.id = bs.batch_id \
               WHERE s.is_active = 1 \
                 AND b.course_id = %d" % course_id
        
    sql += " AND reg_year < %d" % gVar.schYr
    
    origional_id = fetch.cmbID(cmb)
    
    dataSet      = fetch.getAll_col(sql)
    cmb.Freeze()  # locks the combo so that other processes are not called
    
    cmb.Clear()
    first_item = ""
    if first_item:
        cmb.Append(first_item, -1)
        cmb.Append('', 0)
    for row in dataSet:
        if row[1]: fn = "%s " % row[1]
        else: fn=''
        if row[2]: mn = "%s " %  row[2]
        else: mn = ''
        if row[3]: ln = "%s " %  row[3]
        else: ln=''
        
        ful_name = "%s%s%s" % (fn,mn,ln)
        cmb.Append(ful_name, row[0])
    
    restored = restore(cmb, origional_id)
    
    cmb.Thaw()
    
    if restored:
        return origional_id
    else:
        cmb.SetSelection(1)
    

