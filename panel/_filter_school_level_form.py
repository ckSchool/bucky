import wx, gVar, loadCmb, fetch

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class panel_filter_school_level_form(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.checkbox_filter_by_school = wx.CheckBox(self, -1, "School")
        self.choice_schools            = wx.Choice(self,   -1,  choices=[])
        
        self.checkbox_filter_by_level  = wx.CheckBox(self, -1, "Level")
        self.choice_levels             = wx.Choice(self,   -1,  choices=[])
        
        self.checkbox_filter_by_form   = wx.CheckBox(self, -1, "Form")
        self.choice_forms              = wx.Choice(self,   -1,  choices=[])
        
        self.Bind(wx.EVT_CHOICE,   self.OnSelectSchool, self.choice_schools)
        self.Bind(wx.EVT_CHOICE,   self.OnSelectLevel,  self.choice_levels)
        self.Bind(wx.EVT_CHOICE,   self.OnSelectForm,   self.choice_forms)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckSchool, self.checkbox_filter_by_school)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckLevel,  self.checkbox_filter_by_level)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckForm,   self.checkbox_filter_by_form)
        
        self.checkbox_filter_by_school.SetValue(False)
        
        self.choice_schools.SetMinSize((200, -1))
        self.choice_levels.SetMinSize((200, -1))
        self.choice_forms.SetMinSize((200, -1))
        
        sizer_filter = wx.BoxSizer( wx.HORIZONTAL)
        
        sizer_filter.Add(self.checkbox_filter_by_school, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_schools,            0, wx.LEFT, 5)
        
        sizer_filter.Add(self.checkbox_filter_by_level, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_levels,            0, wx.LEFT, 5)
        
        sizer_filter.Add(self.checkbox_filter_by_form, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_forms,            0, wx.LEFT, 5)
        self.SetSizer(sizer_filter)
        
        self.checkbox_filter_by_form.Hide()
        self.checkbox_filter_by_level.Hide()
        self.choice_levels.Hide()
        self.choice_forms.Hide()
        self.choice_schools.Hide()
        
    
    def OnCheckSchool(self, evt):
        #rint'Filter > OnCheckSchool'
        if self.checkbox_filter_by_school.GetValue():
            self.choice_schools.Show()
            sql = "SELECT id, name \
                     FROM schools \
                    WHERE isCK = 1"
            #rintsql
            loadCmb.gen(self.choice_schools, sql)
            self.checkbox_filter_by_level.Show()
            self.OnCheckLevel(wx.Event)
            
        else:
            self.checkbox_filter_by_form.SetValue(False)
            self.checkbox_filter_by_level.SetValue(False)
            self.checkbox_filter_by_form.Hide()
            self.checkbox_filter_by_level.Hide()
            self.choice_levels.Hide()
            self.choice_forms.Hide()
            self.choice_schools.Hide()
            
        self.Layout()
        self.displayData()
        
    def OnCheckLevel(self, evt):
        #rint'Filter > OnCheckLevel event'
        if self.checkbox_filter_by_level.GetValue():
            self.choice_levels.Show()
            self.loadLevels()
            
            self.checkbox_filter_by_form.Show()
            self.OnCheckForm(wx.Event)
            
        else:
            self.checkbox_filter_by_form.SetValue(False)
            self.choice_levels.Hide
            self.checkbox_filter_by_form.Hide()
            self.choice_forms.Hide()
        self.Layout()
        self.displayData()
        
    def OnCheckForm(self, evt):
        #rint'Filter > OnCheckForm evt'
        if self.checkbox_filter_by_form.GetValue():
            self.choice_forms.Show()
            self.loadForms()
        else:
            self.choice_forms.Hide()
        self.Layout()
        self.displayData()
                
    def OnSelectSchool(self, evt):
        # self.loadSchools()
        if self.checkbox_filter_by_level.GetValue():
            self.loadLevels()
        if self.checkbox_filter_by_form.GetValue():
            self.loadForms()
        self.displayData()
        
    def OnSelectLevel(self, evt):
        #rint 'OnSelectLevel'
        if self.checkbox_filter_by_form.GetValue():
            #rint 'OnSelectLevel loadForms'
            self.loadForms()
        self.displayData()
        
    def OnSelectForm(self, evt):
        self.displayData()
    
    
    def displayData(self, ):
        if self.checkbox_filter_by_school.GetValue():
              gVar.school_id = fetch.cmbID(self.choice_schools)
        else: gVar.school_id = 0
            
        if self.checkbox_filter_by_level.GetValue():
              level_id   = fetch.cmbID(self.choice_levels)
              gVar.level = fetch.level_level_id(level_id)
        else: gVar.level = 0
        
        if self.checkbox_filter_by_form.GetValue():
              gVar.form_id = fetch.cmbID(self.choice_forms)
        else: gVar.form_id = 0
        
        #rint' send msg'
        self.GetTopLevelParent().Layout()
        pub.sendMessage('filter_sch.change')
    
    
    def loadLevels(self):
        school_id = fetch.cmbID(self.choice_schools)
        sql = "SELECT id, name \
                 FROM course_levels \
                WHERE school_id = %d \
                GROUP BY level \
                ORDER BY level" % (school_id,)
        loadCmb.gen(self.choice_levels, sql)
        loadCmb.levels_forSchool(self.choice_levels, school_id)
        
    def loadForms(self):
        school_id = fetch.cmbID(self.choice_schools)
        level_id  = fetch.cmbID(self.choice_levels)
        level     = fetch.level_level_id(level_id)
        if self.checkbox_filter_by_level.GetValue():
            sql = "SELECT id, name \
                     FROM forms \
                    WHERE level = %d \
                      AND schYr = %d" % (level, gVar.schYr)
        else:
            sql = "SELECT id, name \
                     FROM forms \
                    WHERE school_id = %d \
                      AND schYr = %d" % (school_id, gVar.schYr)
        loadCmb.gen(self.choice_forms, sql)
    
    