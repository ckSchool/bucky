import fetch, wx

def studentData(student_id):
    student_id = int(student_id)
    if not student_id: return
    
    name         = fetch.studentFullName(student_id)
    #rint ' popup details for student ', student_id, name
    school_name  = ''
    course_title = ''
    batch_name   = ''
    # bs.batch_id, n.nis, s.first_name, s.middle_name, s.last_name, \
    # s.birth_date, s.gender, s.ship_id, b.course_title_id, ct.school_id, s.national_no, ct.course_level
    studentDetails = fetch.studentSchDetails(student_id)
    age    = ''
    gender = ''
    ship   = ''
    
    if studentDetails:
        school_id    = studentDetails['school_id']
        school_name  = fetch.schoolName(school_id)
        
        course_title_id = studentDetails['course_title_id']
        course_title    = fetch.courseTitle(course_title_id)
        
        age    = studentDetails['birth_date']
        gender = fetch.gender(studentDetails['gender'])
        ship   = fetch.shipName(studentDetails['ship_id'])
    
    batch_id = fetch.batchID_forStudent(student_id)
    if batch_id:
        batch_name   = fetch.batchName(batch_id)

    schDetails(name, school_name, course_title, batch_name, age, gender, ship)
    
def schDetails(name="N/A", school_name="N/A", course_title="N/A", batch_name="N/A", age="N/A", gender="N/A", ship="N/A"):
    msg = "\
    Student name  : %s \n\
    ---------------------------\n\
    School          : %s \n\
    Course          : %s \n\
    Batch            : %s \n\
    DoB               : %s \n\
    Gender          : %s \n\
    Ship               : %s " % (
    name, school_name, course_title, batch_name, str(age), gender, ship)
    
    dlg = wx.MessageDialog(None, msg, "Notice",
                           wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
   
def assignmentDetails(assignment_id):
    pass 
    
def assignments_forClass(class_id):
    # ##rint'assignments_forClass(class_id):',class_id
    className = fetch.className(class_id)
    msg = " Assignments for : %s \n\
            ---------------------------\n" % className
    listOfAssignments = assignmentList_forClass(class_id)
    for item in listOfAssignments:
        item = str(item)
        id = item.split(',')[0]
        date = item.split(',')[1]
        title = item.split(',')[2]
        nextline = 'ID:%s    Date:%s   Title:%s \n' % (id, date, title)
        msg += nextline
    
    dlg = wx.MessageDialog(None, msg, "Notice",
                           wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
    
def assignmentList_forClass(class_id):
    list = []
    list.append((3,'13,Nov','Chapt 1 Vocab Quiz'))
    list.append((3,'15,Nov','Chapt 1 Review'))
    return list
    
    
def gradeEntry(grade):
    msg = str(grade)
    dlg = wx.MessageDialog(None, msg, "Notice",
                           wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()
    
def exculStudentChoices(student_id=1, semester_no=1):
    msg = 'excul'#fetch.exculStudentChoices(student_id, semester_no)
    
    
    dlg = wx.MessageDialog(None, msg, "Notice",
                           wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()   
    
class MyDialog(wx.Dialog):
    def __init__(self, parent, mytitle, msg):
        wx.Dialog.__init__(self, parent, -1, mytitle, size=(250,180))
        entry = wx.TextCtrl(self, -1, value="", size=(600, 200), style = wx.TE_MULTILINE | wx.TE_LINEWRAP )
        entry.Value = msg
        self.Title='Enter comments'
        # assign dialog's entry instance to parent
        parent.entry = entry
        button_ok = wx.Button(self, wx.ID_OK)
        button_cancel = wx.Button(self, wx.ID_CANCEL)
        sizer =  self.CreateTextSizer(mytitle)
        self.SetSizer(sizer)
        sizer.Add(entry, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(button_ok, 0, wx.ALL, 5)
        sizer.Add(button_cancel, 0, wx.ALL, 5)
        self.Fit()
        
class MyPopupMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)

        self.parent = parent

        minimize = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(minimize)
        self.Bind(wx.EVT_MENU, self.OnMinimize, id=minimize.GetId())

    def OnMinimize(self, event):
        self.parent.Iconize()
        
