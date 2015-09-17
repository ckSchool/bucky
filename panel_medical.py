import wx, gVar, fetch, loadCmb

from datetime import date
from DateCtrl import DateCtrl

tab_selected   = 'white'
tab_unselected = (240,245,250)

class panel_medical(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.text_ctrls   = []
        self.choice_ctrls = []
        
        self.label_blood_group       = wx.StaticText(self, -1, "Blood group")
        self.choice_blood_group      = wx.Choice(self,     -1, choices=[])
        self.choice_ctrls.append(self.choice_blood_group)
        
        self.label_medical_notes     = wx.StaticText(self,  -1, "Notes:")
        self.data_medical_notes      = wx.TextCtrl(self,    -1, "", style = wx.LB_MULTIPLE)
        self.text_ctrls.append(self.data_medical_notes)
        
        sizer_medical  = wx.BoxSizer(wx.VERTICAL)
        
        sizer_medical.Add(self.label_blood_group,   0, 0, 0)
        sizer_medical.Add(self.choice_blood_group,  0, 0, 0)
        sizer_medical.Add(self.label_medical_notes, 0, wx.TOP, 6)
        sizer_medical.Add(self.data_medical_notes,  1, wx.EXPAND, 0)
        self.SetSizer(sizer_medical)
        
    def enableCtrls(self): 
        for ctrl in self.text_ctrls:   ctrl.SetEditable(True)
        for ctrl in self.choice_ctrls: ctrl.Enable()
        
    def disableCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetEditable(False)
        for ctrl in self.choice_ctrls: ctrl.Enable(False)
  
    def clearCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetLabel('')
        for ctrl in self.choice_ctrls: ctrl.SetSelection(0)
        self.disableCtrls()
        loadCmb.blood(self.choice_blood_group)
        
    def displayData(self, student_id):
        sql = "SELECT b.name \
                 FROM students s \
                 JOIN blood_groups b ON s.blood_type_id = b.id \
                WHERE s.id =%d" % student_id
        blood_group =  fetch.getStr(sql)
        
        self.data_medical_notes.SetValue(str(blood_group))
    
    def Save(self):
        print 'save medical'
        