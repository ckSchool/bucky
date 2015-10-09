import wx, gVar, fetch, loadCmb

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from myListCtrl import VirtualList

headings = (('item no',0),('group id',0),('subject',140),('staff id',0),('teacher',150),('pop',30),('loc',30))
        
      
class panel_excul_set_days(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.SetBackgroundColour(gVar.barkleys)
        
        self.panel_filter = wx.Panel(self, -1)
        self.panel_main   = wx.Panel(self, -1)
        
        self.label_semester   = wx.StaticText(self.panel_filter, -1, "Semester")
        self.choice_semester  = wx.Choice(self.panel_filter, -1, choices=["1", "2"])
        self.label_school     = wx.StaticText(self.panel_filter, -1, "School")
        self.choice_school    = wx.Choice(self.panel_filter, -1, choices=["SD","SM"])
        
        sizer_filter  = wx.BoxSizer()
        sizer_filter.Add(self.label_semester)
        sizer_filter.Add(self.choice_semester)
        sizer_filter.Add(self.label_school)
        sizer_filter.Add(self.choice_school)
        self.panel_filter.SetSizer(sizer_filter)
        
        self.panel_left    = wx.Panel(self.panel_main, -1)
        self.vListStudents = VirtualList(self.panel_main)
        
        self.panel_upper_left = wx.Panel(self.panel_left, -1)
        self.panel_lower_left = wx.Panel(self.panel_left, -1)
    
        self.checkbox_dict_mon  = wx.CheckBox(self.panel_upper_left, -1, "Mon ")
        self.checkbox_dict_tue  = wx.CheckBox(self.panel_upper_left, -1, "Tue ")
        self.checkbox_dict_wed  = wx.CheckBox(self.panel_upper_left, -1, "Wed ")
        self.checkbox_dict_thur = wx.CheckBox(self.panel_upper_left, -1, "Thur")
        self.checkbox_dict_fri  = wx.CheckBox(self.panel_upper_left, -1, "Fri ")
        self.button_save        = wx.Button(self.panel_upper_left,   -1, "Save")
        
        self.checkboxs = [self.checkbox_dict_mon,
                          self.checkbox_dict_tue,
                          self.checkbox_dict_wed,
                          self.checkbox_dict_thur,
                          self.checkbox_dict_fri]
        index = 1
        for chkbox in self.checkboxs:
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckbox, chkbox)
            chkbox.SetName(str(index))
            index += 1
            
        self.Bind(wx.EVT_BUTTON, self.OnSave,     self.button_save)
        self.Bind(wx.EVT_CHOICE, self.OnSemesterSchoolChange, self.choice_semester)
        self.Bind(wx.EVT_CHOICE, self.OnSemesterSchoolChange, self.choice_school)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        pass
    
    def OnCheckbox(self, evt):
        pass
    
    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_upper_left      = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_lower_left = wx.BoxSizer(wx.VERTICAL)
        
        for chkbox in self.checkboxs:
            sizer_upper_left.Add(chkbox, 0, wx.LEFT, 20)
        sizer_upper_left.Add(self.button_save, 0, wx.LEFT, 20)
        self.panel_upper_left.SetSizer(sizer_upper_left)
        
        self.panel_lower_left.SetSizer(self.sizer_lower_left)
        
        sizer_left.Add(self.panel_upper_left, 0, wx.TOP,  20)
        sizer_left.Add(self.panel_lower_left, 0, 0, 0)
        self.panel_left.SetSizer(sizer_left)
        
        sizer_main.Add(self.panel_left,       0, wx.EXPAND | wx.ALL, 20)
        sizer_main.Add(self.vListStudents,    1, wx.EXPAND | wx.ALL, 20)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_filter, 0, wx.EXPAND, 0)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        
    def __do_main(self):
        loadCmb.fillCmb(self.choice_school, ((2, "SD"), (3,"SM")))
        gVar.school_id = 2
        loadCmb.restore(self.choice_school, 2)
        self.choice_semester.Select(0)
        gVar.semester = 1
        loadCmb.restore_str(self.choice_semester, '1')
        
        self.displayData()
        
    def OnSemesterSchoolChange(self, evt):
        self.displayData()
        
    def OnSchool(self, evt):
        self.displayData()
        
    def purgeSizer(self, sizer):
        sizers_children = self.sizer_lower_left.GetChildren()
        self.sizer_lower_left.Clear()
        for child in sizers_children:
            self.sizer_lower_left.Remove(0)
            child.Destroy()
        self.sizer_lower_left.Clear()
        print "children remaining=", len(self.sizer_lower_left.GetChildren())
        #self.sizer_lower_left.Destroy()
        #self.sizer_lower = wx.BoxSizer(wx.VERTICAL)
        #self.panel_lower_left.SetSizer(self.sizer_lower)
        self.Layout()
    
    def displayData(self):
        self.Hide()
        self.Show()
        self.Refresh()
        gVar.semester = int(fetch.cmbValue(self.choice_semester))
       
        if fetch.cmbValue(self.choice_school)=="SD":
              gVar.school_id = 2
        else: gVar.school_id = 3
            
        self.list_of_lists={}
        self.purgeSizer(self.sizer_lower_left)

        res = fetch.exculSchedule_forSchSemYr(gVar.school_id, gVar.semester, gVar.schYr)

        for chkbox in self.checkboxs:
            chkbox.Freeze()
            chkbox.SetValue(False)
            chkbox.Thaw()
            
        for row in res:
            schedule_id, day = row['id'], row['day']
            self.checkboxs[day-1].SetValue(True)
            
            # create panel with heading & listCtrl
            newListCtrl = VirtualList(self.panel_lower_left, -1)
            columns=((str(schedule_id),50),(str(schedule_id),50),('c',50),('d',50),('e',50),('f',50))
            newListCtrl.SetColumns(columns)
           
            #self.list_of_lists[day-1] = newListCtrl
            self.sizer_lower_left.Add(newListCtrl, 0, wx.BOTTOM, 10)
            
            data = self.getScheduleData(schedule_id)
            data = {0: (schedule_id, str(schedule_id), 'yyyyy', 'zz', 'aaaa')}
            newListCtrl.SetItemMap(data)
            
        self.Layout()
        
    def getScheduleData(self, schedule_id):
        data = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        print schedule_id, '  >  exculGroupsDATA_forScheduleID > ', data
        return data
            
    def OnSave(self, evt):
        pass
    
    def OnReset(self, evt):
        pass
    