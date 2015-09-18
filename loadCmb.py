import fetch, gVar, calendar

#--- a --------------------------------------------------------------------------

def admissionStatus(cmb):
    gen(cmb, "SELECT id, status FROM admission_status", 'Any')
    
def assignment(cmb,sql):
    gen(cmb,"")
    
def assignmentTypes(cmb):
    gen(cmb, " SELECT id, catagory  \
                 FROM assignment_catagories \
		ORDER BY catagory", 'Add catagory')
    
def acc_catagories(cmb):
    sql = "SELECT id, name \
                FROM acc_catagories \
	       ORDER BY name"
    gen(cmb, sql)

def acc_invoice_items(cmb,i):
    gen(cmb, "SELECT id, item_name FROM acc_invoice_items")
    
    
# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
def address_items(cmb, addr_item_type, dict={}):
    sql = " SELECT id, name FROM address_items \
             WHERE type = '%s'" % addr_item_type
    gen(cmb, sql)
    
def addrItem(cmb, addr_item_type, dict={}):
    sql = " SELECT id, name \
              FROM address_items \
             WHERE type = '%s'" % addr_item_type
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

def addressItems(cmb, nextItemID):
    itemType = cmb.GetName()
    if nextItemID:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type ='%s' \
                  AND next_item_id = %d \
                ORDER BY (name)" % (itemType, nextItemID)
    else:
        sql = "SELECT id, name \
                 FROM address_items \
                WHERE type ='%s' \
                ORDER BY (name)" % itemType
        
    #rint 'addressItems', sql, fetch.getAllCol(sql)
    gen(cmb, sql, ' ')
    
def addrItemTypes(cmb, id):
    sql = " SELECT id, name \
              FROM address_item_types \
             WHERE id > %d" % id
    ###rint sql
    gen(cmb, sql)
    
    
    
   

#-  b  ------------------------------------------------------------------------- 
 
def blood(cmb):
    gen(cmb, "SELECT id, name FROM blood_types ORDER BY name")
"""
def bookingFees(cmb):
    gen(cmb," SELECT id, amount \
                FROM school_fees \
               WHERE type = 'Booking' \
                 AND validTillYr >= 2010")"""
       
#-  c  ------------------------------------------------------------------------- 
    
def classesOthers_forBatch(cmb, staff_id, batch_id):
    sql = " SELECT s.id, s.name \
              FROM employee_subjects es \
              JOIN subjects s on s.id = es.subject_title_id \
             WHERE es.staff_id <> %d \
               AND s.batch_id = %d \
             GROUP BY s.batch_id" % (staff_id, batch_id)
    genNoBlank(cmb,sql)

"""      
def childStatus(cmb):
    gen(cmb," SELECT id, childStatus FROM childStatuss","")"""
    
def countries(cmb):
    gen(cmb, "SELECT id, name FROM address_items \
               WHERE type = 'country'")

# courses -------------------
def courseTitles(cmb):
    gen(cmb," SELECT id, name FROM courses \
	       ORDER BY course_level")

def courseTitles_forLevel(cmb, course_level=0, first_item=''):
    sql = " SELECT id, name \
              FROM course_levels"
    
    if course_level: sql +=" AND level = %d" % course_level

    return gen(cmb, sql, first_item)

def courseLevels(cmb):
    gen(cmb, "SELECT id, name \
	        FROM course_levels \
	       GROUP BY level \
	       ORDER BY level", '-')

def courseLevels_forSchool(cmb, school_id = 0):
    school_id = int(school_id)

    sql = "SELECT level, name \
	     FROM course_levels"
    
    if school_id > 0: sql += " AND school_id = %d" % school_id
    
    sql += " ORDER BY level"
    #rint sql
    gen(cmb, sql, '')

def courses_forLevel_forYear(cmb, level, yr):
    sql = "SELECT c.id, c.course_title \
	     FROM courses c \
	     JOIN course_levels cl ON cl.level = c.course_level \
	    WHERE cl.level = %d \
	      AND c.schYr = %d \
	    ORDER BY cl.level" % (level, yr)
    #rint sql
    gen(cmb, sql, '')


def courses_forYear(cmb, yr):
    sql = "SELECT c.id, c.name \
	     FROM courses_by_year  cby \
	     JOIN courses c ON c.id = cby.course_id \
	    WHERE cby.schYr = %d \
	    ORDER BY c.level" % yr
    #rintsql
    gen(cmb, sql)

def courses_forSchool_forYear(cmb, school_id=0, yr=0):
    school_id = int(school_id)
    if school_id == 0: return
    sql = "SELECT c.id, c.name \
	     FROM courses c \
	     JOIN course_levels cl ON c.course_level = cl.level \
            WHERE c.schYr = %d \
	      AND cl.school_id = %d \
	    ORDER BY cl.level" % (yr, school_id )
    gen(cmb, sql)

def courseTitles_forSchool(cmb, school_id = 0, first_item=''):
    school_id = int(school_id)

    sql = "SELECT id, level_title \
	     FROM course_levels_forschool \
            WHERE course_level > -5"
    
    if school_id > 0: sql += " AND school_id = %d" % school_id
    
    sql += " ORDER BY level"
    
    gen(cmb, sql, first_item)
    

def courses_minLevel(cmb, level):
    sql = "SELECT id, level_title \
	     FROM course_levels \
            WHERE course_level >= %d \
	    ORDER BY course_level" % (level,)
    gen(cmb, sql)


#---  dddddddddddddddddddddddddddddddddddddddddddddddddddd
def days(cmb):
    dayList = ['Monday','Tuesday','Wednesday','Thursday','Friday'] #fetch.getAllCol(sql)
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
    cmb.Clear()
    cmb.Freeze()  # locks the combo so that other processes are not called
  
    select = 0
    i = 0
    for dayName in dayList:
        cmb.Append(dayName, i)
        if i == origional_id:
            select = i
        i += 1
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select)
    cmb.Thaw()
    
def dayNumbers(cmb, month=0, year=0):
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
    
    cmb.Clear()
    cmb.Freeze()  # locks the combo so that other processes are not called
  
    if month and year:
	for i in range(1, calendar.monthrange(year, month)[1]+1):
	    cmb.Append(str(i), i)
    else:
	for i in range(1,32):
	    cmb.Append(str(i), i)
    
    cmb.Select(0)
    if originalIndex > -1: cmb.Select(select)
    cmb.Thaw()	
	
	
	
	
	
	
# eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee           
def enrollmentFees(cmb):
    sql =" SELECT fee_id, feeAmount \
             FROM school_fees \
            WHERE type = 'enroll' \
              AND schYr = %d" % gVar.schYr
    gen(cmb,sql)

def excul_subjects(cmb,sql):
    gen(cmb," SELECT id, name \
                FROM excul_subjects")
    
def excul_subjectsPool(cmb, excul_id, edited_activity_id=0):
    # collect activity_ids for exculset_id
    sql = " SELECT es.id \
              FROM excul_groups eg \
              JOIN excul_subjects es ON es.id = eg.excul_subject_id \
             WHERE eg.id = %d " % (excul_id, )
    
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
              FROM excul_subjects \
             WHERE NOT FIND_IN_SET(id, %s) \
	     ORDER BY name" % listStr
    #rint sql, fetch.getAllCol(sql)
    fillCmb(cmb, fetch.getAllCol(sql), 'without activity')
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
    
    sql = " SELECT id, name \
              FROM staff \
             WHERE staff_type_id = 2 \
               AND %d BETWEEN join_schYr AND exit_schYr \
               AND NOT FIND_IN_SET(id, %s) \
	     ORDER BY full_name" % (gVar.schYr, listStr)
    fillCmb(cmb, fetch.getAllCol(sql),'without teacher')
    restore(cmb, int(edited_teacher_id))
    
def estates(cmb):
    gen(  "SELECT name \
	     FROM address_items \
	    WHERE type ='estate' \
	    GROUP BY name \
	    ORDER BY name", '-new-')


#   fffffffffffffffffffffffffffffffffffffff
def faiths(cmb):
    gen(cmb, "SELECT id, name FROM faiths")

def forms_byYear_aboveLevel(cmb, schYr, level, first_item=''):
    cmb.Clear()
    if first_item: cmb.Append(first_item, 0)
    sql = " SELECT f.id, f.name \
	      FROM forms f  \
	      JOIN courses        c ON  c.id    = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE f.schYr = %d \
	       AND cl.level >= %d \
             ORDER BY cl.level" % (level, schYr)
    #rint sql
    gen(cmb, sql, first_item)
   
def forms_byYear(cmb, schYr, first_item=''):
    #rint 'loadCmb:batches_forYear'
    cmb.Clear()
    cmb.Append('Without form', 0)
    sql = " SELECT f.id, f._name \
	      FROM forms f \
	      JOIN courses        c ON  c.id = f.course_id \
              JOIN course_titles cl ON cl.id = c.course_title_id \
             WHERE f.schYr = %d \
             ORDER BY cl.course_level" % schYr
    #rint sql
    gen(cmb, sql, first_item)

def form_divisions(cmb, form_id):
    cmb.Clear()
    cmb.Append('Entire', 0)
    
    sql = " SELECT divisions \
              FROM forms \
             WHERE id = %d" % form_id
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
	    
def forms_forCourse(cmb, course_id = 0, first_item = ''):
    sql = " SELECT f.id, f.name \
              FROM forms f \
	      JOIN courses        c ON  c.id    = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE f.schYr = %d " % gVar.schYr
    
    if int(course_id) > 0:
	sql += " AND c.id = %d" % course_id
	
    else:
	sql += " AND cl.course_level > -5 "
	
    sql += " ORDER BY f.name "
    #rint 'batches_forCourse:', sql
    return gen(cmb, sql, first_item)    
    
def forms_forCourseTitle(cmb, course_level = 0, first_item = ''):
    sql = " SELECT f.id, f.name \
              FROM forms f \
	      JOIN courses        c ON  c.id    = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level \
             WHERE fb.schYr = %d " % gVar.schYr
    
    if int(course_title_id) > 0:
	sql += " AND cl.level= %d" % course_level
	
    sql += " ORDER BY f.name "
    return gen(cmb, sql, first_item)
    
def forms_forLevel(cmb, course_level = 0, first_item = ''):
    #rint 'loadCmb: batches_forLevel:'
    sql = " SELECT f.id, f.name, cl.level, cl.level_title, \
              FROM forms f \
	      JOIN courses        c ON  c.id    = f.course_id \
              JOIN course_levels cl ON cl.level = c.course_level "
    
    if int(course_level) > 0:  sql += " AND cl.level = %d" % course_level
    #rint  sql
    return gen(cmb, sql, first_item)
    
def forms_forYear_forLevel(cmb, year, course_level = 0, first_item = ''):
    #rint 'loadCmb: batches_forLevel:'
    sql = " SELECT f.id, f.batch_name, cl.level, cl.level_title \
              FROM forms f \
	      JOIN courses        c ON  c.id = f.course_id \
              JOIN course_levels cl ON cl.id = c.course_title_id \
             WHERE f.schYr = %d " % year
    if int(course_level) > 0:
        sql += " AND cl.level = %d" % course_level

    return gen(cmb, sql, first_item)  
    
    
def forms_forSchool(cmb, school_id = 0, first_item = ''):
    if school_id > 3: school_id = 3
    sql = " SELECT f.id, f.name \
              FROM forms f \
	      JOIN courses        c ON  c.id    = f.course_id \
	      JOIN course_levels cl ON cl.level = c.course_level \
             WHERE cl.school_id = %d \
	       AND  f.schYr = %d \
          ORDER BY cl.level" % (school_id, gVar.schYr)

    gen(cmb, sql, first_item)
     
def forms_forMentor(cmb, staff_id):
    id_list = fetch.batches_forMentor(staff_id)
    #rint 'batches_forMentor , id_list', id_list
    originalIndex = int(cmb.GetSelection())
    if originalIndex > -1:origional_id = cmb.GetClientData(originalIndex) 
    else: origional_id = 0
     
    cmb.Clear()
    if not id_list:return
    cmb.Freeze()  # locks the combo so that other processes are not called
        
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
    cmb.Thaw()
    
    
    
    
    
# gggggggggggggggggggggggggggggggggggggggggggggggg
def gender(cmb):
    cmb.Clear()
    cmb.Append("Gender", 0)
    cmb.Append("male", 1)
    cmb.Append("female", 2)
    cmb.Select(0)

def grading_standards(cmb):
    gen(cmb," SELECT id, standard FROM grading_standards")
                
         
#---  h, i, j, k  ------------------------------------------------------------------------- 
def inv_students(cmb, filter_panel):
    school_id, course_id, form_id = filter_panel.getSelectedIDs()
    #rint 'inv_students', cmb, school_id, course_title_id, batch_id
    
    if form_id:
	sql ="SELECT s.id, s.name \
		FROM students s \
		JOIN students_by_form sbf ON s.id = sbf.student_id \
		JOIN forms              f ON f.id = sbf.form_id \
	       WHERE s.is_active = 1 \
		 AND f.id = %d" % form_id
	
    elif course_id:
	sql ="SELECT s.id, s.name \
		FROM students s \
		JOIN students_by_form sbf ON s.id = sbf.student_id \
		JOIN forms              f ON f.id = sbf.batch_id \
	       WHERE s.is_active = 1 \
		 AND f.course_id = %d" % course_id
	
    sql += " AND register_schYr < %d" % gVar.schYr
    origional_id = fetch.cmbID(cmb)
    dataSet      = fetch.getAllCol(sql)
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
	cmb.Thaw() 
	return origional_id
    else:
	cmb.SetSelection(1)
	cmb.Thaw()
    
           
#---  lllllllllllllllllllllllllllllllllllll 
  
def livesWith(cmb):
    gen(cmb," SELECT id, name FROM guardian_types")


def levels_forSchool(cmb, school_id):
    sql = "SELECT id, name  FROM course_levels "
    
    if school_id:
	sql += " WHERE school_id = %d " % school_id
	    
    sql     += " ORDER BY level"
    gen(cmb, sql)
    
      
                                 
# , m, n, o,  -------------------------------------------------------------------------
def occ(cmb):
    gen(cmb," SELECT id, name FROM occupations ")

         
#---  ppppppppppppppppppp, qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq ------------------------------------------------------------------------- 
   
def pob(cmb):
    gen(cmb," SELECT id, kecamatan FROM kecamatan ORDER BY kecamatan")

def prevSch(cmb):
    gen(cmb," SELECT id, name FROM schools ORDER BY type")
    
def products(cmb, plist=[]):
    if plist:
	liststr =  ",".join("'{0}'".format(n) for n in plist)
	sql = "SELECT id, description \
                 FROM acc_products \
		WHERE NOT id IN (%s) \
		ORDER BY description" % liststr
    else:
	sql = "SELECT id, description FROM acc_products ORDER BY description"
	
    #rintsql
    gen(cmb, sql)

def product_types(cmb):
    gen(cmb,"SELECT id, name FROM acc_product_types ORDER BY name")

def product_accounts(cmb):
    gen(cmb,"SELECT id, name FROM acc_accounts WHERE income = 1 ORDER BY name")
# qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
def qualification(cmb):
    genAdd(cmb," SELECT id, name FROM qualifications ORDER BY qualifications", 'New qualification')
    
    

# rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

def relationship(cmb):
    gen(cmb," SELECT id, name FROM guardian_types")
 
def restore(cmb, origional_id=0):
    #rint'restore', origional_id
    cmb.Freeze()
    if origional_id:
        for y in range(cmb.Count):
            cmb.Select(y) # select first item
	    cmbID = fetch.cmbID(cmb)
            if cmbID == origional_id:
                cmb.Thaw()
                return True
    cmb.Select(0)
    cmb.Thaw()
    return False

def restore_str(cmb, myStr = ''):
    ##rint'myStr', myStr
    cmb.Freeze()
    myStr = str(myStr)
    myStr = myStr.strip()
    idx = cmb.FindString(myStr)
    ##rint'idx=', idx, '   myStr=__', myStr, "___"
    if idx: cmb.Select(idx) # select first item
    else:   cmb.Select(0)
    cmb.Thaw()
    
def regStatus(cmb):
    cmb.Freeze()
    cmb.Append("")
    cmb.Append("leave")
    cmb.Append("retake")
    cmb.Append("stay")
    cmb.Append("paid")
    cmb.Thaw()
 
    
    
#---  s  ------------------------------------------------------------------------- 
    
def suppliers(cmb):
    genNoBlank(cmb, "SELECT id, name FROM acc_suppliers ORDER BY name")
	
def subjects__forTeacher_forBatch(cmb, teacher_id, batch_id, NoBlank=False):
    sql = " SELECT st.id, st.subject_title \
              FROM studygroups sg \
	      JOIN subject_titles st ON sg.subject_title_id = st.id \
             WHERE sg.staff_id = %d \
	       AND sg.batch_id =%d " % (teacher_id, batch_id)
    #rint sql
    if NoBlank:
        genNoBlank(cmb,sql)
    else:
        gen(cmb,sql)

def schYears(cmb):
    gen(cmb,"SELECT id, schYr FROM schYrs")
    
    
def schoolFees_forYr(cmb):
    sql = "SELECT ii.id, item_description \
	        FROM inv_items ii \
		JOIN inv_item_codes iic ON iic.id = ii.item_code \
	       WHERE ii.item_code = 1 \
	         AND ii.valid_till_schYr = %d" % gVar.schYr
    #rint sql	 
    gen(cmb, sql)
    #rint 'loaded cmb schoolFees_forYr', gVar.schYr

def schYrs(cmb, Affix=''):
    genNoId(cmb," SELECT schYr FROM schYrs \
		   ORDER BY schYr", Affix)
    
def schMonths(cmb, min_month=0, first_item=''):
    sql = "SELECT month_number, month_name FROM school_year"
    if min_month:
	sql += " WHERE month_number > %d" % min_month
    sql += " ORDER BY month_number"
    #rintsql
    gen(cmb, sql, first_item)
  
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
    sql = " SELECT id, school_type \
	      FROM schools \
             WHERE isCK = TRUE"
    #rintsql
    genNoBlank(cmb, sql, '')
    
def schools(cmb, ck=True, first=''):
    sql = "SELECT id, name FROM schools "
    if ck: sql +=" WHERE isCK = True"
    #rintsql
    gen(cmb, sql, first)
     
def ship(cmb):
    gen(cmb," SELECT id, name FROM ships", "Ship")

def subjects(cmb):
    gen(cmb," SELECT * FROM subject_titles \
               WHERE NOT is_deleted = True")

def standards(cmb):
    gen(cmb," SELECT a.affective_id, a.affectiveTitle \
                FROM standards a;")
    




#---- t -------------------------------------------------------------------------
    
def teachers(cmb, firsttitle=''):
    genAdd(cmb," SELECT id, first_name FROM employees \
                  WHERE status = TRUE \
		    AND teacher=1", 'New employee')


def travelsWith(cmb):
    gen(cmb," SELECT id, option FROM travel_options")


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
    
    

    
    
    
    
    
    
    
    
    
    
    
    
#-------------------------------------------------------------------------------
def gen(cmb, sql , first_item='') : #sql should be designed to return two items 'id' and 'title'
    ##rint"loadCmb gen:", sql, len(fetch.getAllCol(sql))
    
    origional_id = fetch.cmbID(cmb)
    dataSet      = fetch.getAllCol(sql)
    ##rint'dataSet:' , dataSet
    
    
    cmb.Freeze()  # locks the combo so that other processes are not called
    cmb.Clear()
    if first_item:
	cmb.Append(first_item, 0)
    for row in dataSet:
	#rint 'cmb load ,  id=', row[0],'   str=', row[1]
	cmb.Append(str(row[1]), int(row[0]))
    restored = restore(cmb, origional_id)
    
    cmb.Thaw()    
    if restored: return origional_id
    else:        return 0
 
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
	cmb.Thaw()  
	return origional_id
    else:
	cmb.SetSelection(1)
	cmb.Thaw()
	return  
    
def fillCmb(cmb, dataSet, first_item=''):
    origional_id = fetch.cmbID(cmb)
    cmb.Freeze()  # locks the combo so that other processes are not called
    
    cmb.Clear()
    if first_item:      cmb.Append(first_item,0)
    for row in dataSet: cmb.Append(str(row[1]), row[0])
    restored = restore(cmb, origional_id)
    
    cmb.Thaw()    
    if restored: return origional_id
    else:        return 0

def genNoBlank(cmb, sql, first_item='') :
    #rint 'loadCmb: genNoBlank:', sql, fetch.getAll_dict(sql)
    #sql should be designed to return first two items  'id' , 'title'
    dataSet = fetch.getAllCol(sql)
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
    


def genNoId(cmb, sql , first_item = '') : #sql should be designed to return two items 'id' and 'title'
    try:
        origional_str = fetch.cmbValue(cmb)
    except: origional_str = ''
    
    ##rint'origional_str', origional_str
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
        #restored = restore_str(cmb, origional_str)
        
        cmb.Thaw()    
        if restored: return origional_str
        else:        return 0
    except:
        #rint 'load cmb error'
        return 0   
    cmb.Thaw()
    
    
