import wx, fetch, loadCmb

student_id = 0

class PanelRegAssesment(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PanelRegAssesment.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.panel_ctrls = wx.Panel(self, -1)
        
        self.label_test_english     = wx.StaticText(self.panel_ctrls, -1, "English")
        self.label_test_maths       = wx.StaticText(self.panel_ctrls, -1, "Maths")
        self.label_test_sci         = wx.StaticText(self.panel_ctrls, -1, "Science")
        self.spinCtrl_eng           = wx.SpinCtrl(self.panel_ctrls, -1, "", min=0, max=100)
        self.spinCtrl_maths         = wx.SpinCtrl(self.panel_ctrls, -1, "", min=0, max=100)
        self.spinCtrl_sci           = wx.SpinCtrl(self.panel_ctrls, -1, "", min=0, max=100)
        self.checkbox_special_needs = wx.CheckBox(self.panel_ctrls, -1, "Special")
        self.label_needs            = wx.StaticText(self.panel_ctrls, -1, "needs")
        self.label_blank            = wx.StaticText(self.panel_ctrls, -1, "")
        
        self.panel_notes            = wx.Panel(self, -1)
        self.label_notes            = wx.StaticText(self.panel_notes, -1, "Notes")
        self.text_ctrl_notes        = wx.TextCtrl(self.panel_notes, -1, "")

        self.__set_properties()
        self.__do_layout()
        self.clearCtrls()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PanelRegAssesment.__set_properties
        self.spinCtrl_eng.SetMinSize((50, -1))
        self.spinCtrl_maths.SetMinSize((50, -1))
        self.spinCtrl_sci.SetMinSize((50, -1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PanelRegAssesment.__do_layout
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        sizer_notes = wx.BoxSizer(wx.VERTICAL)
        sizer_ctrls = wx.FlexGridSizer(3, 3, 5, 5)
        sizer_ctrls.Add(self.label_test_english, 0, 0, 0)
        sizer_ctrls.Add(self.label_test_maths, 0, 0, 0)
        sizer_ctrls.Add(self.label_test_sci, 0, 0, 0)
        sizer_ctrls.Add(self.spinCtrl_eng,   0, 0, 0)
        sizer_ctrls.Add(self.spinCtrl_maths, 0, 0, 0)
        sizer_ctrls.Add(self.spinCtrl_sci,   0, 0, 0)
        sizer_ctrls.Add(self.checkbox_special_needs, 0, 0, 0)
        sizer_ctrls.Add(self.label_needs,    0, 0, 0)
        sizer_ctrls.Add(self.label_blank,    0, 0, 0)
        self.panel_ctrls.SetSizer(sizer_ctrls)
        sizer_main.Add(self.panel_ctrls,  0, wx.LEFT | wx.BOTTOM | wx.EXPAND, 5)
        sizer_notes.Add(self.label_notes, 0, 0, 0)
        sizer_notes.Add(self.text_ctrl_notes, 1, wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        self.panel_notes.SetSizer(sizer_notes)
        sizer_main.Add(self.panel_notes, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        # end wxGlade

    def displayData(self, student_id):
        self.clearCtrls()
        if not student_id:  return
        
        student_details = fetch.admissionDetails(student_id)
        
        admission_test_results = student_details['admission_test_results']
        if admission_test_results:
            scores = admission_test_results.split(',')
            eng  = scores[0]
            math = scores[1]
            sci  = scores[2]
            if scores:
                self.spinCtrl_eng.SetValue(int(eng))
                self.spinCtrl_maths.SetValue(int(math))
                self.spinCtrl_sci.SetValue(int(sci))
        
        needs = student_details['special_needs']
        if not needs: needs= 0
        self.checkbox_special_needs.SetValue(needs)
        
        notes = str(student_details['observation_notes'])
        self.text_ctrl_notes.SetValue(notes)
	self.student_id = student_id
    
    def clearCtrls(self):
        self.spinCtrl_eng.SetValue(0)
        self.spinCtrl_maths.SetValue(0)
        self.spinCtrl_sci.SetValue(0)
        self.checkbox_special_needs.SetValue(0)
        self.text_ctrl_notes.SetValue('')
        
    def save(self, id):
        eng   = self.spinCtrl_eng.GetValue()
        math  = self.spinCtrl_maths.GetValue()
        sci   = self.spinCtrl_sci.GetValue()
        notes = self.text_ctrl_notes.GetValue()
        needs = self.checkbox_special_needs.GetValue()
        
        sql = "  UPDATE students SET \
                        admission_test_results = '%d,%d,%d', \
                        special_needs = %d, \
                        observation_notes = '%s' \
                  WHERE id = %d " % (
                        eng, math, sci,
                        needs,
                        notes,
                        self.student_id)
        ##rintsql
        fetch.updateDB(sql)