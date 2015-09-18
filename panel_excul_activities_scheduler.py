import wx, lv, gVar, fetch, loadCmb

import wx.lib.scrolledpanel as scrolled 

#g_semester_no = 1
insertion     = ''
replace_id    = 0
replaceName   ='' 

class panel_excul_activities_scheduler(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.SetName('panel_excul_activities_scheduler')
        
        self.p_mid = wx.Panel(self, -1)
        self.lv1 = wx.ListView(self.p_mid, -1, style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        self.lv2 = wx.ListView(self.p_mid, -1, style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        self.lv3 = wx.ListView(self.p_mid, -1, style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        
        self.p_header = wx.Panel(self, -1)
        self.l_sch         = wx.StaticText(self.p_header, -1, 'School year')
        self.c_day         = wx.ComboBox(self.p_header,   -1, choices=[])
        self.l_day         = wx.StaticText(self.p_header, -1, 'Day:')
        self.spin_semester = wx.SpinCtrl(self.p_header,   -1, style=wx.SP_ARROW_KEYS)
        self.staticText2   = wx.StaticText(self.p_header, -1, 'School:')
        self.staticText3   = wx.StaticText(self.p_header, -1, 'Semester')
        self.spc_schYr     = wx.SpinCtrl(self.p_header,   -1, initial=gVar.schYr, max=2100, min=2000, style=wx.SP_ARROW_KEYS)
        self.c_schools     = wx.ComboBox(self.p_header,   -1, choices=[])
        
        self.p_footer = wx.Panel(self, -1)
        self.p_footerSpacerMid = wx.Panel(self.p_footer, -1)
        self.p_footerSpacerR   = wx.Panel(self.p_footer, -1)
        self.ts1               = wx.TextCtrl(self.p_footer, -1, '')
        self.ts2               = wx.TextCtrl(self.p_footer, -1, '')
        
        self.b_del  = wx.Button(self.p_footerSpacerMid,- 1, 'Del')
        self.b_edit = wx.Button(self.p_footerSpacerMid, -1,'Edit')
        self.b_add  = wx.Button(self.p_footerSpacerMid, -1, 'Add')
    
        self.b_save = wx.Button(self.p_footerSpacerR, -1, 'Save')
        
        self._init_coll_lv1_Columns(self.lv1)
        self._init_coll_lv2_Columns(self.lv2)
        self._init_coll_lv3_Columns(self.lv3)
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,       self.lv1)
        self.Bind(wx.EVT_LEFT_DCLICK,     self.OnLv1LeftDclick, self.lv1)
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,       self.lv3)
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,       self.lv2)
        self.Bind(wx.EVT_LEFT_DCLICK,     self.OnLv2LeftDclick, self.lv2)
        
        self.Bind(wx.EVT_COMBOBOX, self.OnC_dayCombobox,     self.c_day)
        self.Bind(wx.EVT_SPIN,     self.OnSpc_semesterSpin,  self.spin_semester)
        self.Bind(wx.EVT_SPIN,     self.OnSpc_schYrSpin,     self.spc_schYr)
        self.Bind(wx.EVT_COMBOBOX, self.OnC_schoolsCombobox, self.c_schools)
        
        self.Bind(wx.EVT_BUTTON, self.OnB_delButton,  self.b_del)
        self.Bind(wx.EVT_BUTTON, self.OnB_editButton, self.b_edit)
        self.Bind(wx.EVT_BUTTON, self.OnB_addButton,  self.b_add)
        self.Bind(wx.EVT_BUTTON, self.OnB_saveButton, self.b_save)

        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        #self.p_mid.SetBackgroundColour(wx.Colour(0, 0, 128))
        #self.p_header.SetBackgroundColour(wx.Colour(0, 0, 128))
        #self.l_sch.SetForegroundColour(wx.Colour(255, 255, 255))
        #self.l_day.SetForegroundColour(wx.Colour(255, 255, 255))
        
        #self.spin_semester.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,  False, 'Times New Roman'))
        self.spin_semester.SetRange(1, 2)
        
        #self.staticText2.SetForegroundColour(wx.Colour(255, 255, 255))
        #self.staticText3.SetForegroundColour(wx.Colour(255, 255, 255))

        #self.spc_schYr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))
        #self.p_footer.SetBackgroundColour(wx.Colour(0, 0, 160))
        #self.ts2.SetBackgroundColour(wx.Colour(0, 0, 160))
        #self.ts1.SetBackgroundColour(wx.Colour(0, 0, 128))
    
    def __do_layout(self):
        sizer_main = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_mid   = wx.BoxSizer(orient=wx.HORIZONTAL)

        sizer_mid.AddWindow(self.lv1, 0, wx.EXPAND | wx.ALL, 10)
        sizer_mid.AddWindow(self.lv2, 0, wx.EXPAND | wx.ALL, 10)
        sizer_mid.AddWindow(self.lv3, 0, wx.EXPAND | wx.ALL,10)
        self.p_mid.SetSizer(sizer_mid)
        
        sizer_main.AddWindow(self.p_header, 0, wx.EXPAND | wx.ALL, 0)
        sizer_main.AddWindow(self.p_mid,    1, wx.EXPAND | wx.ALL, 0)
        sizer_main.AddWindow(self.p_footer, 0, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)
  
    def _init_coll_lv3_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id',  width=20)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Teachers', width=200)

    def _init_coll_lv1_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id', width=20)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Activities', width=200)

    def _init_coll_lv2_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id',   width=20)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Activity', width=200)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading='id',   width=20)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT, heading='Teacher', width=-1)

    def __do_main(self):
        loadCmb.schDiv(self.c_schools)
        loadCmb.days(self.c_day)
        
        dt1 = TextDropTarget(self.lv2) # Make this control a Drop Target
        self.lv2.SetDropTarget(dt1)         # Link to Control

        dt2 = TextDropTarget(self.lv2) # Make this control a Drop Target
        self.lv2.SetDropTarget(dt2)    # Link to Control
    
    def displayData(self):
        
        # collect the variables
        gVar.schYr    = self.spc_schYr.Value
        #g_semester_no = self.spin_semester.Value   
        sch_id        = fetch.cmbID(self.c_schools)
        dayNo         = fetch.cmbID(self.c_day)+1
        
        # listOfExcul = fetch.exculFor_sch_semester_say(sch_id, g_semester_no, dayNo)
        # lv.populateWithList(self.lv2, listOfExcul)
        
        # otherActivities = fetch.exculActivitiesOtherThan(listOfExcul)
        #lv.populateWithList(self.lv1, sql)

        # otherTeachers = fetch.exculTeachersOtherThan(listOfExcul)
        #lv.populateWithList(self.lv3, otherTeachers)
        
    def beginDrag(self, event):
        global insertion, replace_id, replaceName 
        lv = event.GetEventObject()
        insertion = 'fail'
        """ Begin a Drag Operation """
        # Create DataObject to holds text to be dragged
        index  = lv.GetFirstSelected()
        if index < 0: return
        
        id     = int(lv.GetItemText(index))
        title  = lv.GetItem(index, 1).GetText()
        source = lv.GetName()
        data   = '%s:%s:%s' % (str(id), str(title), source)
        
        tdo = wx.PyTextDataObject(data)
        #rint'tdo'
        # Create a DropSourceObject, for Drag operation
        tds = wx.DropSource(lv)
        
        # Associate the Data to be dragged with the Drop Source Object
        tds.SetData(tdo)
        
        # Intiate the Drag Operation
        tds.DoDragDrop(True)
        #rint'tds'
        #rint'insertion', insertion
        # if drop was successful remove item from source
        if insertion == 'activityInserted':
            lv.DeleteItem(index)
        
        elif insertion == 'teacherReplaced':
            lv.DeleteItem(index)
            #rint'teacher removed'

            index2 = self.lv3.Append(str(replace_id))
            self.lv3.SetStringItem(index2, 0, str(replace_id))
            self.lv3.SetStringItem(index2, 1, replaceName)
            
        elif insertion == 'teacherInserted':
            #rint'teacher deleted'
            lv.DeleteItem(index)

    def OnLv1LeftDclick(self, event):
        lv = event.GetEventObject()
        index = lv.GetFirstSelected()

        if index > -1:
            id    = lv.GetItem(index, 0).GetText()
            title = lv.GetItem(index, 1).GetText()
            
            indexD = self.lv2.Append(id + '\n\n')
            self.lv2.SetStringItem(indexD, 0, str(id))
            self.lv2.SetStringItem(indexD, 1, title)
            lv.DeleteItem(index)
        
    def OnLv2LeftDclick(self, event):
        lv = event.GetEventObject()
        # display a popup with 3 choices
        # 1: disolve activity
        # 2: remove teacher
        index = lv.GetFirstSelected()
        if index > -1:
            activity_id = lv.GetItem(index, 0).GetText()
            activityName = lv.GetItem(index, 1).GetText()
            
            teacher_id = lv.GetItem(index, 2).GetText()
            teacherName = lv.GetItem(index, 3).GetText()
            
            self.showPopupRemoveChoices(activity_id, activityName, teacher_id, teacherName)

        event.Skip() 
        
        
    def OnMenuDisolveSessionClick(self, event):
        lv = self.lv2
        index = lv.GetFirstSelected()
        if index > -1:
            id    = lv.GetItem(index, 0).GetText()
            title = lv.GetItem(index, 1).GetText()
            idT   = lv.GetItem(index, 2).GetText()
            nameT = lv.GetItem(index, 3).GetText()
            
            indexA = self.lv1.Append(str(id))
            self.lv1.SetStringItem(indexA, 0, str(id))
            self.lv1.SetStringItem(indexA, 1, title)
            
            indexT = self.lv3.InsertStringItem(0, str(idT))
            self.lv3.SetStringItem(indexT, 0, str(idT))
            self.lv3.SetStringItem(indexT, 1, nameT)
                    
            lv.DeleteItem(index)
    
    def OnMenuReleaseTeacherClick(self, event):
        lv = self.lv2
        index = lv.GetFirstSelected()
        if index > -1:
            idT   = lv.GetItem(index, 2).GetText()
            nameT = lv.GetItem(index, 3).GetText()
            
            indexT = self.lv3.InsertStringItem(0, str(idT))
            self.lv3.SetStringItem(indexT, 0, str(idT))
            self.lv3.SetStringItem(indexT, 1, nameT)
                    
            self.lv2.SetStringItem(index, 2, '')
            self.lv2.SetStringItem(index, 3, '')
            
            
            
    def showPopupRemoveChoices(self, activity_id, activityName, teacher_id='', teacherName=''):
        """
        Create and display a popup menu on dbl-click event
        """
        #if not hasattr(self, "popupID1"):
        self.popupID1 = wx.NewId()
        
        # make a menu
        menu = wx.Menu()
        
        # put an icon in the menu
        #item = wx.MenuItem(menu, self.popupID1,"Disolve session")
        #item.Bind(wx.EVT_LEFT_DCLICK, self.OnMenuDisolveSessionClick) 
        self.popupID1 = wx.NewId()
        item = menu.Append(self.popupID1, "Disolve session")
        self.Bind(wx.EVT_MENU, self.OnMenuDisolveSessionClick, item)
        

        if teacher_id:
            self.popupID2 = wx.NewId()
            item = menu.Append(self.popupID2,"Release teacher")
            self.Bind(wx.EVT_MENU, self.OnMenuReleaseTeacherClick, item)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()



    def OnC_schoolsCombobox(self, event):
        self.displayData()

    def OnC_dayCombobox(self, event):
        self.displayData()

    def OnSpc_semesterSpin(self, event):
        self.displayData()

    def OnSpc_schYrSpin(self, event):
        self.displayData()

    def OnB_delButton(self, event):
        event.Skip()

    def OnB_editButton(self, event):
        event.Skip()

    def OnB_addButton(self, event):
        event.Skip()

    def OnB_saveButton(self, event):
        event.Skip()




class TextDropTarget(wx.TextDropTarget):
    
# Define Text Drop Target class             
    """ This object implements Drop Target functionality for Text """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped text """
        # Initialize the wx.TextDropTarget Object
        wx.TextDropTarget.__init__(self)
        # Store the Object Reference for dropped text
        self.obj = obj

    def OnDropText(self, x, y, data):
        global insertion, replace_id, replaceName 
        insertion = 'fail'
        lv_2 = self.obj 
        replace_id, replaceName = '', ''
                                     
        data = str(data).split(':')
        id, title, source = data[0], data[1], data[2]

        destination = lv_2.Name
        
        if source != destination:
              
            """ Implement Text Drop """
            ## When text is dropped, write it into the object specified
            # check to see what is at the drop mouse position
            index, flags = self.obj.HitTest((x, y))
 
            if source == 'lv1': 
                # if data comes from lv_activities              
                # append a new item (write to the first columns)
                index = self.obj.Append(id + '\n\n')
                self.obj.SetStringItem(index, 1, title)
                insertion = 'activityInserted'
                
            elif source == 'lv3':  
                # when the data comes from  lv_teachers          
                # if there is an activity at that position
                if index > -1:
                    # store the ID
                    replace_id  = self.obj.GetItem(index, 2).GetText()
                    replaceName = self.obj.GetItem(index, 3).GetText()
                    if replace_id:    
                        # set new details
                        self.obj.SetStringItem(index, 2, data[0])
                        self.obj.SetStringItem(index, 3, data[1]) 
                        
                        insertion = 'teacherReplaced'  
                        
                    else:
                        self.obj.SetStringItem(index, 2, data[0])
                        self.obj.SetStringItem(index, 3, data[1])
                        
                        insertion = 'teacherInserted'  
