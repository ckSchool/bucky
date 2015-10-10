import wx, gVar, fetch

import wx.lib.mixins.listctrl as  listmix
import wx.lib.agw.ultimatelistctrl as ULC

import sys
import time

#----------------------------------------------------------------------
# The panel you want to test (TestVirtualList)
#----------------------------------------------------------------------

startdata = {1 : ("", "", "")}

class VirtualList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, log):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
        self.log=log
	
        #adding some art
        self.il = wx.ImageList(16, 16)
        a={"sm_up":"GO_UP","sm_dn":"GO_DOWN","w_idx":"WARNING","e_idx":"ERROR","i_idx":"QUESTION"}
        for k,v in a.items():
            s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (k,v)
            exec(s)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        #adding some attributes (colourful background for each item rows)
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")
        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")
        self.attr3 = wx.ListItemAttr()
        self.attr3.SetBackgroundColour("purple")

        #building the columns
	# number of colums must exactly match
	# items in data row
	headerTup = startdata[1]
	#self.setColumnHeaders(headerTup)
        '''self.InsertColumn(0, " ")
        self.InsertColumn(1, " ")
        self.InsertColumn(2, " ")
	self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 220)
        self.SetColumnWidth(2, 100)'''

        #These two should probably be passed to init more cleanly
        #setting the numbers of items = number of elements in the dictionary
        self.setNewData(startdata, headerTup )
        
        self.mixins()
	
        #sort by genre (column 2), A->Z ascending order (1)
        self.SortListItems(2, 1)

        #events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
	
    def setColumnHeaders(self, HEADER):
	#rint "HEADER:", HEADER
	self.DeleteAllColumns()
	colNo = 0
        for row in HEADER:
            #column_heading = row[0]
            self.InsertColumn(colNo, str(row))
            colNo += 1
	    
    def setNewData(self, DATA, HEADER):
	self.DeleteAllItems()
	
        if HEADER: self.setColumnHeaders(HEADER)
            
	self.itemDataMap  = DATA
	self.itemIndexMap = DATA.keys()
	self.SetItemCount(len(DATA))
	
    def SetVirtualData(self, row, col, value):
	#rint row, col, value
	pass
    
    def mixins(self):
	#mixins
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, 6)

    def OnColClick(self,event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        txt = ('OnItemSelected: "%s", "%s", "%s", "%s"\n' %
                           (self.currentItem,
                            self.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2)))
	#rint txt
        #self.log.WriteText(txt)
	#rint 'event ',event
	#if event.GetEvent() == wx.EVT_LEFT_DCLICK:
	#    student_id = self.GetItemText(self.currentItem)
	self.GrandParent.OnItemSelected(event)

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
	student = self.itemDataMap[self.currentItem]
	#rint 'self.currentItem=', self.currentItem
	
        txt =("OnItemActivated: %s\nTopItem: %s\n" %
                           (self.GetItemText(self.currentItem), self.GetTopItem()))
	student_id = self.GetItemText(self.currentItem)
	
	self.GrandParent.OnPopup(student, event)

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        self.log.WriteText("OnItemDeselected: %s" % evt.m_itemIndex)


    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        return self.itemDataMap[index][col]


    def OnGetItemImage(self, item):
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]

        if   genre=="Rock":    return self.w_idx
        elif genre=="Jazz":    return self.e_idx
        elif genre=="New Age": return self.i_idx
        else:                  return -1

    def OnGetItemAttr(self, item):
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]
	
	if index % 2: return self.attr2
	else:         return self.attr1
		
        if   genre=="Rock":    return self.attr2
        elif genre=="Jazz":    return self.attr1
        elif genre=="New Age": return self.attr3
        else:                  return None

    #---------------------------------------------------
    # Matt C, 2006/02/22
    # Here's a better SortItems() method --

    # the ColumnSorterMixin.__ColumnSorter() method already handles the ascending/descending,
    # and it knows to sort on another column if the chosen columns have the same value.

    def SortItems(self, sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        
        # redraw the list
        self.Refresh()

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
        

def selectedItemIndex(listview):
    if listview.GetFirstSelected() != -1:
        index = listview.GetFirstSelected()
    else: index=0
    return index

def selectedItemsList(listCtrl):
    #rint 'selectedItemsList'
    selection = []
    index = listCtrl.GetFirstSelected()
    #rint index
    if index > -1:
        #rint index
        selection.append(index)
        while len(selection) != listCtrl.GetSelectedItemCount():
            index = listCtrl.GetNextSelected(index)
            selection.append(index)

    return selection

def selectedItemID(listview):
    #rint '  listview: ' , listview
    index = listview.GetFirstSelected()
    #rint index
    if index > -1:
        x = listview.GetItemText(index)
        #rint 'GetItemText=', x
        return int(x)
    
    else:
        return 0
    
    id = -1
    index = listview.GetFirstSelected()
    #rint 'got index', index
    if index != -1:
        #rint listview.GetItemText(index)
        id = int(listview.GetItemText(index))
    return id

def selected_id_title(listview):
    data=''
    index = listview.GetFirstSelected()
    if index != -1:
        data = listview.GetItemText(index) 
    return data

def populateWithList(list_ctrl, res, selected_id=0 ): 
    list_ctrl.DeleteAllItems()
    if not res:
	#rint 'no res'
	return
    #rint'populateWithList ',res
    for row in res:
	#rint'row:', row
        fieldCount = len(str(row).split(',')) 
        item_id = str(row[0])
	#rint'lv item_id', item_id
        index = list_ctrl.Append(item_id)
	#rint'index', index
        list_ctrl.SetStringItem(index, 0, item_id)
        if int(item_id)==selected_id: reselectIndex = index
        if fieldCount > 1:
            for col in range(1, fieldCount):
                colCount = list_ctrl.ColumnCount  
                if colCount < col: list_ctrl.Append('new col')
                if row[col]:
                    list_ctrl.SetStringItem(index, col, str(row[col]))
    decorateBanding(list_ctrl)

def populate(list_ctrl, sql):
    selected_id   = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    
    res = fetch.getAll_col(sql) # 1st col must be 'id'
    if res: populateWithList(list_ctrl, res, selected_id)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()

def GetSelectedItems(listCtrl):
    """ Gets the selected items for the list control.
        Selection is returned as a list of selected indices,
        low to high.
    """
    selection = []
    if listCtrl.GetSelectedItemCount() == 0: return selection
    
    index = listCtrl.GetFirstSelected()
    selection.append(index)
    while len(selection) <= listCtrl.GetSelectedItemCount():
        index = listCtrl.GetNextSelected(index)
        selection.append(index)

    return selection

def formatColumns(list_ctrl, header):
    list_ctrl.DeleteAllColumns()
    colNo = 0
    for heading in header:
        if len(heading) == 3:
            title, col_width, col_format = heading
            if not col_format: col_format = 0
        elif len(heading) == 2:
            title, col_width = heading
            title = str(title)
            try:    col_width = int(col_width)
            except: col_width = 50
            col_format =0
        
        list_ctrl.InsertColumn(col=colNo, format=col_format, width= col_width, heading=title )
        colNo +=1

def headings_list_ctrl_RegistrationsForSchYr(list_ctrl):
    header = [  ('Student ID',      20, wx.LIST_FORMAT_LEFT),
                ('ID',              50, wx.LIST_FORMAT_LEFT),
                ('Name',           200, wx.LIST_FORMAT_LEFT),
                ('Level',           60, wx.LIST_FORMAT_LEFT),
                ('Status',          60, wx.LIST_FORMAT_LEFT),
                ('Booking',         60, wx.LIST_FORMAT_LEFT),
                ('Observation_date',60, wx.LIST_FORMAT_LEFT),
                ('Offering_letter', 60, wx.LIST_FORMAT_LEFT),
                ('Admission_fee',   60, wx.LIST_FORMAT_LEFT)]
    formatColumns(header)
    

def populateList(list_ctrl,  DATA):
    for row in DATA:
        if list_ctrl.GetColumnCount() != len(row):
            #rint 'list_ctrl.GetColumnCount() != len(row):', list_ctrl.GetColumnCount()
            #rint 'len(row):', len(row), '    row:', row
            return
        
        colNo = 0
        for item in row:
            if colNo == 0:
                index = list_ctrl.Append(`item`)
            list_ctrl.SetStringItem(index, colNo, str(item))
            colNo +=1
    decorateBanding(list_ctrl)
    
def populate_list_ctrl_RegistrationsForSchYr(list_ctrl, schYr, filter=''):
    list_ctrl.DeleteAllItems()
    #rint 'populate_list_ctrl_RegistrationsForSchYr'
    sql = " SELECT s.id, first_name, booking_date, observation_date, \
            offering_letter_date, admision_fee_date, c.name, \
            FROM students s \
            JOIN courses c ON s.enter_course_id = c.id \
            WHERE s.exit_year <='%s' \
            AND s.reg_year = %d \
            %s \
            ORDER BY s.id " % (gVar.schYr, schYr, filter,)
    
    list = fetch.getList(sql)
    
    #rint sql, '  :  ', list
    for row in list:
        student_id = row("s.id")
        index = list_ctrl.Append(str(student_id))           # key = student_id
        list_ctrl.SetStringItem(index, 0, str(student_id) ) # display student_id 
        list_ctrl.SetStringItem(index, 2, row['first_name'])
        list_ctrl.SetStringItem(index, 3, row['cl.name']) #form year
        admision_fee_date = row['admision_fee_date']
        if admision_fee_date == True:
            status = 'accepted'
        else:
            status = 'rejected'
        list_ctrl.SetStringItem(index, 4, status) #Status
        list_ctrl.SetStringItem(index, 5, row['booking_date']) #booking_date
        list_ctrl.SetStringItem(index, 6, row['observation_date']) #observation_date
        list_ctrl.SetStringItem(index, 6, row['offering_letter_date']) #offering_letter_date
        list_ctrl.SetStringItem(index, 7, admision_fee_date) #admission_fee_date                
                                                  
    decorateBanding(list_ctrl)
    
    return

def populateWithListEmployees(list_ctrl, employeeIDs):
    list_ctrl.DeleteAllItems()
    if not teacherIDs : return
    #rint 'populateWithListTeachers;',teacherIDs
    for employee_id in employeeIDs:
        #rint 'staff_id=',staff_id
        employeeName = fetch.employeeName(employee_id)
        index = list_ctrl.Append(str(employee_id))
        list_ctrl.SetStringItem(index, 0, str(employee_id) )       # display staff_id
        #if staff_id==selected_id: reselectIndex = index
         
        list_ctrl.SetStringItem(index, 1, employeeName)     # full name   
    decorateBanding(list_ctrl)
        
def populateExculTeachers(list_ctrl, employeeIDs):
    return
    #rint "populateExculTeachers: teacherIDs:", teacherIDs
    list_ctrl.DeleteAllItems()
    if not employeeIDs : return
    #rint 'teacherIDs', teacherIDs
    for employee_id in employeeIDs:
        employeeName = fetch.employeeName(int(employee_id))
        #rint 'teacher_id;', teacher_id, ' name=', teacherName
        if employeeName:
            index = list_ctrl.Append(str(employee_id))
            list_ctrl.SetStringItem(index, 0, str(employee_id)) 
            list_ctrl.SetStringItem(index, 1, employeeName) 
    decorateBanding(list_ctrl) 
        
def populateEmployees(list_ctrl, employeeIDs=0):      
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()
    
    #if not employeeIDs:
    sql = "SELECT id, first_name FROM employees WHERE status > 0"
	
    employees = fetch.getAll_dict(sql)
    #rint sql, employees
           
    if not employees : return

    for employee in employees: 
        employee_id  = employee['id']
	employee_name  = employee['first_name']
        #sql = "SELECT first_name FROM employees\
        #        WHERE id = %d" % employee_id
        #row = fetch.getOne_dict(sql)

        #employeeName = fetch.employeeName(employee_id)
        
        index = list_ctrl.Append(str(employee_id))
        list_ctrl.SetStringItem(index, 0, str(employee_id) )   # display staff_id
        if employee_id == selected_id: reselectIndex = index
         
        list_ctrl.SetStringItem(index, 1, employee_name)      # full name
        list_ctrl.SetStringItem(index, 2, row['first_name'])  # short name 
        #rint "lv.py (line 121): teacher_id;", teacher_id
        batch_name = fetch.batchName_forMentor(int(employee_id))
        list_ctrl.SetStringItem(index, 3, batch_name)          # form
         
        #list_ctrl.SetStringItem(index, 4, row['approbation'])# approbation
    
    list_ctrl.Select(reselectIndex)     
    decorateBanding(list_ctrl)
    list_ctrl.SetFocus()
    #rint'lv employees done'


def populateSubjectsAndAspects(list_ctrl, sql):
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()
    return
    # #rint sql
    res = fetch.getAll_dict(sql) # 1st col must be 'id'
    # rint res
    if res:
        for row in res:
            fieldCount = len(str(row).split(',')) 
             
            subject_title_id = row['id']
            index = list_ctrl.Append(str(subject_title_id))
            if subject_title_id == selected_id: reselectIndex = index
             
            list_ctrl.SetStringItem(index, 0, str(subject_title_id))
            list_ctrl.SetStringItem(index, 1, str(row['subject_title']))
            list_ctrl.SetStringItem(index, 2, str(row['short']))
            aspectIDs = row['aspectIDs']
            if aspectIDs:
                aspectList=[]
                aspectIDsList = aspectIDs.split(',')
                for id in aspectIDsList:
                    aspectList.append(fetch.aspectTitle(int(id)))
                list_ctrl.SetStringItem(index, 3, ','.join(aspectList))
                
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()
    
def populateSubjects(list_ctrl, sql):
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()
    
    # rint sql
    res = fetch.getAll_dict(sql) # 1st col must be 'id'
    #rint res
    if res:
        for row in res:
            #rint row
            fieldCount = len(str(row).split(',')) 
             
            subject_title_id = row['id']
            index = list_ctrl.Append(str(subject_title_id))
            if subject_title_id == selected_id: reselectIndex = index
             
            list_ctrl.SetStringItem(index, 0, str(subject_title_id))
            list_ctrl.SetStringItem(index, 1, str(row['subject_title']))
            list_ctrl.SetStringItem(index, 2, str(row['short']))
            
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()
     
def populateDivisions(list_ctrl, form_id):
    sql = "SELECT divisions FROM batches WHERE d=%d" % int(form_id)
    res = fetch.getOne_dict(sql)
    list_ctrl.DeleteAllItems()
    if res:
        g_newDivString = res['divisions']
        if g_newDivString:
            divArray = g_newDivString.split(',')
            for row in divArray:
                index = list_ctrl.Append(str(0)) 
                list_ctrl.SetStringItem(index, 0, row)
                
                
def populateCourses(list_ctrl, res):
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()

    if not res: return
    for row in res:
        course_id = row['id']
        index = list_ctrl.Append(str(course_id))
        if course_id == selected_id: reselectIndex = index 
        list_ctrl.SetStringItem(index, 0, str(course_id))
        courseTitle = row['course_title']
        list_ctrl.SetStringItem(index, 1, str(courseTitle))
 
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()
    
    
def populateClasses(list_ctrl, sql):
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()

    res = fetch.getAll_dict(sql) # 1st col must be 'id'
    if res:
        for row in res:
            fieldCount = len(str(row).split(',')) 
             
            lesson_id = row['id']
            index = list_ctrl.Append(str(lesson_id))
            if lesson_id == selected_id: reselectIndex = index 
            list_ctrl.SetStringItem(index, 0, str(lesson_id))
            
            subjectTitle = fetch.subjectTitle(row['subject_title_id'])
            list_ctrl.SetStringItem(index, 1, str(subjectTitle))
 
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()
  
def populateActivities(list_ctrl, activityIDs):
    list_ctrl.DeleteAllItems()
    if not activityIDs: return
    
    for activity_id in activityIDs:
        
        index = list_ctrl.Append(str(activity_id))
        #rint 'index ', index
        list_ctrl.SetStringItem(index, 0, str(activity_id))
        title = fetch.activityTitle(activity_id)
        #rint activity_id, " : title " , title
        list_ctrl.SetStringItem(index, 1, title)

    decorateBanding(list_ctrl)
    list_ctrl.Select(0)
  
def populateExcul(list_ctrl, session_id):
    list_ctrl.DeleteAllItems()
    if not session_id: return
    
    studentList   = []
    selected_id   = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)

    studentId_list = fetch.studentIDs_forExcul(session_id)
    if not studentId_list: return []
    
    index=0
    for student_id in studentId_list:
	#rint student_id
	index = list_ctrl.Append(str(student_id))
	list_ctrl.SetStringItem(index, 0, str(student_id))
	name = fetch.studentFullName(student_id)
	list_ctrl.SetStringItem(index, 1, name)
	
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus() 
    return studentId_list
   
def populateExculRemainingStudents(list_ctrl, student_list):
    #rint 'populateExculRemainingStudents=', list_ctrl
    list_ctrl.DeleteAllItems()
    for student_id in student_list:
        index = list_ctrl.Append(str(student_id))
        list_ctrl.SetStringItem(index, 0, str(student_id))
        name = fetch.studentFullName(student_id)
        list_ctrl.SetStringItem(index, 1, name)
    
    decorateBanding(list_ctrl)    
    
            
def decorateBanding(list_ctrl):
    c = list_ctrl.ItemCount
    if not c: return
    for index in range(c): 
        if (index%2)==0: 
            list_ctrl.SetItemBackgroundColour(index,wx.Colour(215, 215, 235))
        else:
            list_ctrl.SetItemBackgroundColour(index,wx.Colour(255, 255, 255))
   
def populateStudentsForBatch(list_ctrl, batch_id):
    studentList=[]
    selected_id   = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    
    list_ctrl.DeleteAllItems()
    if batch_id:
        slist = fetch.students_inBatch(batch_id)
        index=0
        for row in slist:
            student_id = row['id']
	    #rint 'str(student_id)', str(student_id)
            index = list_ctrl.Append(str(index))
	    name = fetch.studentFullName(student_id)
	    
            list_ctrl.SetStringItem(index, 0, str(student_id))
            list_ctrl.SetStringItem(index, 1, name)
            
    decorateBanding(list_ctrl)
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()  
   
        
def populateStudentsForLesson(list_ctrl, lesson_id):
    studentList=[]
    selected_id = selectedItemID(list_ctrl)
    reselectIndex = selectedItemIndex(list_ctrl)
    list_ctrl.DeleteAllItems()
    if lesson_id:
        slist = fetch.studentIDs_inStudygroup(lesson_id)
        index=0
        for student_id in slist:
            index = list_ctrl.Append(str(student_id))
            list_ctrl.SetStringItem(index, 0, str(student_id))
            name = fetch.studentFullName(student_id)
            list_ctrl.SetStringItem(index, 1, name)
            if (index%2)==0: 
                list_ctrl.SetItemBackgroundColour(index,wx.Colour(215, 215, 235))
    list_ctrl.Select(reselectIndex) 
    list_ctrl.SetFocus()

def makeDataObject(list_ctrl, event): 
    """ Put together a data object for drag-and-drop _from_ this list. """

    # Create the data object: Just use plain text.
    data = wx.PyTextDataObject()
    idx = event.GetIndex()
    lvItem = list_ctrl.GetItem(idx)
    
    id = lvItem.GetText()
    title = list_ctrl.GetItem(idx,1).GetText()
    
    if list_ctrl.Name == 'lc_activities':
        itemType = 'activity'
    elif list_ctrl.Name == 'lc_teachers':
        itemType = 'teacher'
    
    txt = '%s`%s`%s' % (id, title, itemType) 
    
    data.SetText(txt)

    # Create drop source and begin drag-and-drop.
    dropSource = wx.DropSource(list_ctrl.Parent)
    dropSource.SetData(data)
    res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

    # If move, we want to remove the item from this list.
    if res == wx.DragMove:
        # It's possible we are dragging/dropping from this list to this list.  In which case, the
        # index we are removing may have changed...

        # Find correct position.
        pos = list_ctrl.FindItem(idx, id)
        list_ctrl.DeleteItem(pos) 
        
        
class ListDrop(wx.PyDropTarget):
    """ Drop target for simple lists. """

    def __init__(self, setFn):
        """ Arguments:
         - setFn: Function to call on drop.
        """
        wx.PyDropTarget.__init__(self)
        self.setFn = setFn
        
        #rint self

        # specify the type of data we will accept
        self.data = wx.PyTextDataObject()
        self.SetDataObject(self.data)


    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object
        if self.GetData():
            self.setFn(x, y, self.data.GetText())

        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d 