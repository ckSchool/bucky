import wx, gVar, fetch, loadCmb

def create(parent):
    return DlgNewEditExculActivity(parent)
    
class DlgNewEditExculActivity(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_main      = wx.Panel(self, -1)
        self.panel_middle    = wx.Panel(self.panel_main, -1)
        
        self.label_heading   = wx.StaticText(  self.panel_middle, -1, "")
        self.bitmap_activity = wx.StaticBitmap(self.panel_middle, -1,
                                                wx.Bitmap(".\\images\\48\\subject_48.png",
                                                wx.BITMAP_TYPE_ANY))
        
        self.label_activity  = wx.StaticText(self.panel_middle, -1, "Activity")
        self.choice_activity = wx.Choice(self.panel_middle,     -1, choices=[])
        self.button_add_subject = wx.Button(self.panel_middle,  -1, "+")
        
        self.label_teacher   = wx.StaticText(self.panel_middle, -1, "Teacher")
        self.choice_teacher  = wx.Choice(self.panel_middle,     -1, choices=[])
        self.button_add_teacher = wx.Button(self.panel_middle,  -1, "+")
        
        self.button_enter    = wx.Button(self.panel_main,       -1, "Enter")

        self.Bind(wx.EVT_BUTTON, self.OnEnter,  self.button_enter)
        
        self.__set_properties()
        self.__do_layout()  
        self.__do_main()

    def __set_properties(self):
        self.SetTitle("Extra Curricular Activity")
        self.label_activity.SetMinSize((64, 16))
        self.choice_activity.SetMinSize((200, 21))
        self.choice_teacher.SetMinSize((200, 21))
        self.button_enter.SetMinSize((100, 30))
        self.button_add_subject.SetMaxSize((23, 23))
        self.button_add_teacher.SetMaxSize((23, 23))

    def __do_layout(self):
        sizer_base       = wx.BoxSizer(wx.VERTICAL)
        sizer_main       = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_names = wx.FlexGridSizer(3, 3, 10, 3)
        
        grid_sizer_names.Add(self.bitmap_activity, 0, 0, 0)
        grid_sizer_names.Add(self.label_heading,   0, 0, 0)
        grid_sizer_names.AddSpacer(wx.Size(8, 8))

        grid_sizer_names.Add(self.label_activity,     0, 0, 0)
        grid_sizer_names.Add(self.choice_activity,    0, wx.EXPAND, 0)
        grid_sizer_names.Add(self.button_add_subject, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        
        grid_sizer_names.Add(self.label_teacher,      0, 0, 0)
        grid_sizer_names.Add(self.choice_teacher,     1, wx.BOTTOM | wx.EXPAND, 0)
        grid_sizer_names.Add(self.button_add_teacher, 0, wx.ALIGN_TOP, 0)
        self.panel_middle.SetSizer(grid_sizer_names)
        
        sizer_main.Add(self.panel_middle, 0, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(self.button_enter, 0, wx.ALL | wx.ALIGN_CENTRE, 20)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_main,   0, wx.ALL, 10)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        
        self.SetSize((600,-1))
        self.Fit()
        self.Layout()
        self.Center()

    def __do_main(self):
        self.activity_id, self.teacher_id = 0, 0
    
    def displayData(self, exculset_id=0, excul_id=0):
        if not exculset_id:  self.EndModal(0)
        
        self.exculset_id = exculset_id
        self.excul_id    = excul_id
        self.editMode    = (excul_id>0)
        
        info = fetch.exculsetinfo(exculset_id)
        if not info: self.EndModal(0)
        
        self.setTitle(info)
        
        if self.editMode: self.loadExculData(exculset_id, excul_id)
        
        loadCmb.excul_subjectsPool(self.choice_activity, self.exculset_id, self.activity_id)
        loadCmb.exculTeacherPool(self.choice_teacher,     self.exculset_id, self.teacher_id)
        
    def setTitle(self, info):
        school, day, semester, schYr = info
        txt = "Exculset id:%d, %s, %s, Sem.%d, %d \n" % (self.exculset_id, school, day, semester, schYr)
        self.label_heading.SetLabel(txt)
        
    def loadExculData(self, exculset_id, excul_id):
        excul_info = fetch.excul_info(excul_id)
        if excul_info:
            self.activity_id = excul_info['activity_id']
            activity_title   = fetch.excul_activityTitle(self.activity_id)
            
            self.teacher_id  = excul_info['employee_id']
            employee_name    = fetch.employeeName(self.teacher_id)
            
            txt = self.label_heading.GetLabelText()
            txt += "Editing Activity: %s.  Teacher:%s" % (activity_title,  employee_name)

            self.label_heading.SetLabel(txt)
        
    def OnEnter(self, event):
        activity_id = fetch.cmbID(self.choice_activity)
        
        if not activity_id:
            fetch.msg("! Must have an activity selected !")
            return
        
        teacher_id  = fetch.cmbID(self.choice_teacher)
        
        if self.editMode:
            self.update(activity_id, teacher_id)
            self.EndModal(wx.ID_OK)
            
        else:
            if self.insertNewActivity(activity_id, teacher_id):
                self.EndModal(wx.ID_OK)

    def update(self, activity_id, teacher_id):
        if activity_id == self.activity_id and teacher_id == self.teacher_id:
            # ' no changes made '
            return True
        
        sql = "UPDATE excul SET activity_id =%d, employee_id= %d \
                WHERE id = %d"  % (activity_id, teacher_id, self.excul_id)
        #rintsql
        return fetch.updateDB(sql)
    
    def insertNewActivity(self, activity_id, teacher_id):
        sql = "INSERT INTO excul \
                       SET exculset_id =%d, activity_id =%d, employee_id= %d"  % (
                           self.exculset_id, activity_id, teacher_id)
        #rintsql
        return fetch.updateDB(sql)
    
    
        
if __name__ == '__main__':
    gVar.schYr = 2014
    app = wx.App(redirect=False)
    dlg = DlgNewEditExculActivity(None)
    try:
        dlg.displayData(1, 0)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
