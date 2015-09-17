import wx, gVar, fetch, loadCmb

from datetime               import date
from DateCtrl               import DateCtrl

tab_selected   = 'white'
tab_unselected = (240,245,250)

class panel_education(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.text_ctrls   = []
        self.choice_ctrls = []
        
        self.panel_education = wx.Panel(self, -1)
        
        self.label_previous_school   = wx.StaticText(self.panel_education, -1, "Previous school")
        self.choice_school           = wx.Choice(self.panel_education,   -1, choices=[])
        self.choice_ctrls.append(self.choice_school)
        
        self.label_Current_status    = wx.StaticText(self.panel_education, -1, "Current status")
        self.data_current_edu_status = wx.TextCtrl(self.panel_education,   -1, "")
        
        self.label_edu_notes         = wx.StaticText(self, -1, "Notes:")
        self.data_edu_notes          = wx.TextCtrl(self,   -1, "")
        
        self.text_ctrls.append(self.data_current_edu_status)
        self.text_ctrls.append(self.data_edu_notes)
        
        sizer_edu      = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_edu = wx.FlexGridSizer(2, 2, 5, 5)
        
        grid_sizer_edu.Add(self.label_previous_school,   0, 0, 0)
        grid_sizer_edu.Add(self.choice_school,           0, 0, 0)
        grid_sizer_edu.Add(self.label_Current_status,    0, 0, 0)
        grid_sizer_edu.Add(self.data_current_edu_status, 0, 0, 0)
        self.panel_education.SetSizer(grid_sizer_edu)
        
        sizer_edu.Add(self.panel_education, 0, wx.EXPAND, 0)
        sizer_edu.Add(self.label_edu_notes, 0, wx.TOP,    8)
        sizer_edu.Add(self.data_edu_notes,  1, wx.EXPAND, 0)
        self.SetSizer(sizer_edu)
        
    def displayData(self, student_id):
        edu_status = 'not yet implimented'     # ??? is this still needed
        edu_notes  = 'not yet implimented'    # ??? seperate quiry on  table "edu_notes"
 
        self.data_current_edu_status.SetValue(edu_status)
        self.data_edu_notes.SetValue(edu_notes)
        
    def enableCtrls(self): 
        for ctrl in self.text_ctrls:   ctrl.SetEditable(True)
        for ctrl in self.choice_ctrls: ctrl.Enable()
        
    def disableCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetEditable(False)
        for ctrl in self.choice_ctrls: ctrl.Enable(False)
          
    def clearCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetLabel('')
        for ctrl in self.choice_ctrls: ctrl.SetSelection(0)
        loadCmb.schools(self.choice_school)
        self.disableCtrls()
        
    def Save(self):
        print 'save education'
        
        