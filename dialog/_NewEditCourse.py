import wx, gVar, loadCmb, fetch

def create(parent):
    return DlgNewEditCourse(parent)
    
class DlgNewEditCourse(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_top              = wx.Panel(self,  -1)
        self.panel_bottom           = wx.Panel(self,  -1)
        self.button_ok              = wx.Button(self, -1, "Enter")
        
        #self.bitmap_course          = wx.StaticBitmap(self.panel_top, -1, wx.Bitmap(".\\images\\48\\subject_48.png", wx.BITMAP_TYPE_ANY))
        self.panel_names            = wx.Panel(self.panel_top,        -1)
        
        self.label_course_name     = wx.StaticText(self.panel_names, -1, "Course Name")
        self.text_ctrl_course_name = wx.TextCtrl(self.panel_names,   -1, "")
        
        #self.label_short            = wx.StaticText(self.panel_names, -1, "Short Name")
        #self.text_ctrl_short_name   = wx.TextCtrl(self.panel_names,   -1, "")
        
        self.sizer_main_staticbox   = wx.StaticBox(self.panel_top,    -1, "")
        
        self.panel_sch              = wx.Panel(self.panel_bottom,     -1)
        
        self.label_sch              = wx.StaticText(self.panel_sch,   -1, "School")
        self.choice_schools         = wx.Choice(self.panel_sch,       -1, choices=[])
        
        self.label_level            = wx.StaticText(self.panel_sch,   -1, "Level/Age")
        self.choice_levels          = wx.Choice(self.panel_sch,       -1, choices=[])
        
        self.sizer_bottom_staticbox = wx.StaticBox(self.panel_bottom, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.OnSchool, self.choice_schools)
        self.Bind(wx.EVT_BUTTON, self.OnSave,  self.button_ok)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        
        self.__do_main()

    def OnClose(self, evt):
        self.EndModal(0)
        
        
    def __set_properties(self):
        self.SetTitle("New Course")
        self.label_course_name.SetMinSize((-1, 13))
        self.label_sch.SetMinSize((64, 13))
        self.choice_schools.SetMinSize((200, 21))
        self.choice_levels.SetMinSize((200, 21))
        self.button_ok.SetMinSize((100, 30))

    def __do_layout(self):
        sizer_base     = wx.BoxSizer(wx.VERTICAL)
        self.sizer_bottom_staticbox.Lower()
        sizer_bottom   = wx.StaticBoxSizer(self.sizer_bottom_staticbox, wx.VERTICAL)
        
        grid_sizer_sch = wx.FlexGridSizer(2, 2, 10, 3)
        
        self.sizer_main_staticbox.Lower()
        sizer_main     = wx.StaticBoxSizer(self.sizer_main_staticbox, wx.HORIZONTAL)

        grid_sizer_names = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_names.Add(self.label_course_name,    0, 0, 0)
        grid_sizer_names.Add(self.text_ctrl_course_name, 0, wx.EXPAND, 0)
        #grid_sizer_names.Add(self.label_short,           0, 0, 0)
        #grid_sizer_names.Add(self.text_ctrl_short_name,  0, wx.EXPAND, 0)
        self.panel_names.SetSizer(grid_sizer_names)
        
        #sizer_main.Add(self.bitmap_course, 0, wx.RIGHT, 15)
        sizer_main.Add(self.panel_names, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.panel_top.SetSizer(sizer_main)

        grid_sizer_sch.Add(self.label_sch,      0, 0, 10)
        grid_sizer_sch.Add(self.choice_schools, 1, 0, 0)
        
        grid_sizer_sch.Add(self.label_level,    0, 0, 10)
        grid_sizer_sch.Add(self.choice_levels,  1, 0, 0)
        
        self.panel_sch.SetSizer(grid_sizer_sch)
        
        sizer_bottom.Add(self.panel_sch,  0, wx.ALL | wx.EXPAND, 5)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_base.Add(self.panel_top,    0, wx.ALL | wx.EXPAND, 10)
        sizer_base.Add(self.panel_bottom, 0, wx.ALL | wx.EXPAND, 10)
        sizer_base.Add(self.button_ok,    0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)
        self.SetSizer(sizer_base)
        
        sizer_base.Fit(self)
        self.Layout()
        self.Center()

    def __do_main(self):
        self.course_id=0
        loadCmb.schools(self.choice_schools, True)
        loadCmb.courseLevels(self.choice_levels)
        loadCmb.courseLevels_forSchool(self.choice_levels, fetch.cmbID(self.choice_schools))
        s = wx.Choice(self, -1, choices =('fg','gf'))
        
  
    def displayData(self, course_id=0):
        self.course_id = course_id
        if course_id:
            
            if not self.displayCourseDetails():
                txt = "no details found for course_id %d" % course_id
                #fetch.msg(txt)
                self.course_id = 0#False #self.editMode = 'new'
  
        txt = ' Course for school year ' + str(gVar.schYr)
        self.SetTitle(txt)
        self.OnSchool()
    
    def displayCourseDetails(self):
        res = fetch.course_info(self.course_id) #course_name, course_level, section_name, school_id, code
        #rint'fetch.course_info:', res
        if not res:
            return False
        self.course_name  = res[0]
        self.course_level = res[1]
        self.school_id    = res[2]
        
        self.origional_name         = '"%s"' % self.course_name
        self.origional_course_level = self.course_level
        self.origional_school_id    = self.school_id
        
        loadCmb.restore(self.choice_schools, self.school_id)
        loadCmb.courseLevels_forSchool(self.choice_levels, self.school_id)
        
        txt = "Edit Course %s" % self.course_name
        self.SetTitle(txt)
         
        self.text_ctrl_course_name.SetValue(self.course_name)
        
        x = self.choice_levels.GetItems()

        loadCmb.restore_str(self.choice_levels, str(self.course_level) )

        return True
    
    def OnSchool(self, event=wx.Event):
        school_id = fetch.cmbID(self.choice_schools)
        loadCmb.courseLevels_forSchool(self.choice_levels, school_id)
        
    def OnCancel(self, event):
        self.id = 0
        self.EndModal(-1)
        
    def courseNameAvailable(self, course_name):
        sql = "SELECT id FROM courses  WHERE course_name = '%s' " % (course_name, )
        duplicates = fetch.getCount(sql)
        if duplicates: return False
        else:          return True
        
    def OnSave(self, event):
        self.course_name  = self.text_ctrl_course_name.GetValue()
        self.course_level = int(self.choice_levels.GetStringSelection())
        self.school_id    = fetch.cmbID(self.choice_schools)
        
        if self.course_name: 
            if self.course_id:
                #rint"Update course id:", self.course_id
                self.updateCourse()
                self.EndModal(wx.ID_OK)
            else:
                if self.courseNameAvailable(self.course_name):
                    #rint"Add new course:" , self.course_name
                    self.insertNewCourse()
                    self.EndModal(wx.ID_OK)
                else:
                    txt = "Course Name Must Be Unique"
                    fetch.msg(txt)
                    return
        else:
            txt = "Must have course title"
            fetch.msg(txt)
 
    def insertNewCourse(self):
        new_id = fetch.next_id('courses')
        
        sql = "INSERT INTO courses (id, course_name, course_level, school_id) \
                    VALUES (%d, '%s',%d, %d) " % (new_id, self.course_name, self.course_level, self.school_id)
        #rintsql
        fetch.updateDBtransaction(sql)

    def updateCourse(self):
        if not (self.course_name  == self.origional_name
            and self.school_id    == self.origional_school_id 
            and self.course_level == self.origional_course_level) :
            sql = " UPDATE courses \
                       SET course_name='%s', course_level=%d, school_id=%d \
                     WHERE id = %d"  % (self.course_name, self.course_level , self.school_id, self.course_id)
            txt = 'This will effect all records past and present'
            #fetch.msg(txt)
            fetch.updateDB(sql)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgNewEditCourse(None)
    try:
        dlg.displayData()
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
