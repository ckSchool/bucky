import wx, gVar, fetch, loadCmb

def create(parent):
    return DlgCourseEditor(parent)
    
class DlgCourseEditor(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_top              = wx.Panel(self,  -1)
        self.panel_bottom           = wx.Panel(self,  -1)
        self.button_ok              = wx.Button(self, -1, "Enter")
        
        self.bitmap_course          = wx.StaticBitmap(self.panel_top, -1, wx.Bitmap(".\\images\\48\\subject_48.png", wx.BITMAP_TYPE_ANY))
        self.panel_names            = wx.Panel(self.panel_top,        -1)
        
        self.label_course_title     = wx.StaticText(self.panel_names, -1, "Course Name")
        self.text_ctrl_course_name = wx.TextCtrl(self.panel_names,   -1, "")
        
        self.label_short            = wx.StaticText(self.panel_names, -1, "Short Name")
        self.text_ctrl_short_name   = wx.TextCtrl(self.panel_names,   -1, "")
        
        self.sizer_main_staticbox   = wx.StaticBox(self.panel_top,    -1, "")
        
        self.panel_sch              = wx.Panel(self.panel_bottom,     -1)
        
        self.label_sch              = wx.StaticText(self.panel_sch,   -1, "School")
        self.choice_schools         = wx.Choice(self.panel_sch,       -1, choices=[])
        
        self.label_level            = wx.StaticText(self.panel_sch,   -1, "Level")
        self.choice_levels          = wx.Choice(self.panel_sch,       -1, choices=[])
        
        self.sizer_bottom_staticbox = wx.StaticBox(self.panel_bottom, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.OnSchool, self.choice_schools)
        self.Bind(wx.EVT_BUTTON, self.OnEnter,  self.button_ok)
        
        self.__do_main()

    def __set_properties(self):
        self.SetTitle("New Course")
        self.label_course_title.SetMinSize((64, 13))
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
        grid_sizer_names.Add(self.label_course_title,    0, 0, 0)
        grid_sizer_names.Add(self.text_ctrl_course_name, 0, wx.EXPAND, 0)
        grid_sizer_names.Add(self.label_short,           0, 0, 0)
        grid_sizer_names.Add(self.text_ctrl_short_name,  0, wx.EXPAND, 0)
        self.panel_names.SetSizer(grid_sizer_names)
        
        sizer_main.Add(self.bitmap_course, 0, wx.RIGHT, 15)
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
        loadCmb.schDiv(self.choice_schools)
        loadCmb.courseLevels(self.choice_levels)
        
    '''def lock(self, mode):
        if mode:
            self.choice_levels.Disable()
            self.choice_schools.Disable()'''
        
    def displayData(self, course_id=0):
        self.course_id = course_id
        if course_id:
            self.editMode = 'update'
            txt = "no details found for course_id %d" % course_id
            if not self.displayCourseDetails():
                fetch.msg(txt)
                self.editMode = 'new'

        else:
            self.editMode = 'new'
            
        txt = self.editMode + ' course for school year ' + str(gVar.schYr)
        self.SetTitle(txt)
    
    def displayCourseDetails(self):
        res = fetch.course_details(self.course_id) #course_title, course_level, section_name, school_id, code
        if not res:
            return False
        self.course_title_id = res['course_title_id']
        self.course_name     = str(res['name'])
        
        self.code         = str(res['code'])       
        self.school_id    = res['school_id']
        self.course_level = res['level']
        
        self.origional_name         = '"%s"' % self.course_name
        self.origional_code         = '"%s"' % self.code
        self.origional_course_level = self.course_level
        self.origional_school_id    = self.school_id
        self.origional_title_id     = self.course_title_id 

        txt = "Edit Course %s" % self.course_name
        self.SetTitle(txt)
         
        self.text_ctrl_course_name.SetValue(self.course_name)
        self.text_ctrl_short_name.SetValue(self.code)
        
        idx = self.choice_levels.FindString(str(self.course_level))
        self.choice_levels.SetSelection(idx)
        
        loadCmb.restore(self.choice_schools, self.school_id)
        return True
    
    def OnSchool(self, event):
        school_id = fetch.cmbID(self.choice_schools)
        loadCmb.courseLevels_forSchool(self.choice_levels, school_id)
        
    def OnCancel(self, event):
        self.id = 0
        self.EndModal(-1)
        
    def courseNameAvailable(self, course_name):
        sql = 'SELECT id \
                 FROM courses \
                WHERE name = %s \
                  AND schYr =%d' % (course_name, gVar.schYr)
        
        if self.editMode:
            sql += " AND NOT id = %d" % self.course_id
        
        #rint sql
        if fetch.getDig(sql):
            fetch.msg("Duplicate course name for this year, please try another")
            return False
            
        else:       
            return True
        
    def OnEnter(self, event):
        self.course_name  = '"%s"' % self.text_ctrl_course_name.GetValue()
        self.code         = '"%s"' % self.text_ctrl_short_name.GetValue()
        self.course_level = fetch.cmbID(self.choice_levels)
        self.school_id    = fetch.cmbID(self.choice_schools)
        
        if not self.course_title or not self.course_level:
            txt = "Must have course title  and a course level"
            fetch.msg(txt)
            return
        
        elif self.courseNameAvailable(self.course_title):
            if self.editMode == 'update':
                  self.updateCourse()
            else: self.insertNewCourse()
            self.EndModal(wx.ID_OK)
 
    def insertNewCourse(self):
        sql = "INSERT INTO courses \
                  SET name = '%s',  code, schYr = %d, course_title_id =%d" % (
                      self.course_name, self.code, gVar.schYr, self.course_title_id)
        #rint sql
        #fetch.updateDBtransaction(sql)

    def updateCourse(self):
        if not (self.course_name == self.origional_name
            and self.code   == self.origional_code
            and self.school_id    == self.origional_school_id 
            and self.course_level == self.origional_course_level) :
            sql = " UPDATE courses \
                       SET name =%s, code, course_title_id =%d \
                     WHERE id = %d"  % (self.course_name, self.code, self.course_title_id, self.course_id)
            #rint sql
            #fetch.updateDB(sql)
   
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgCourseEditor(None)
    try:
        dlg.displayData(1)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
