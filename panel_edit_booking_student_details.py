import wx,  gVar, fetch

from PanelStudentDataViewerNB import PanelStudentDataViewerNB as NB


class panel_edit_booking_student_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        #self.button_back   = wx.Button(self, -1, "Back")
        self.panel_details = NB(self, -1)
        self.button_save   = wx.Button(self, -1, "Save")
        
        self.__set_properties()
        self.__do_layout()

        #self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)

    def __set_properties(self):
        pass
        

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        #sizer_main.Add(self.button_back,   0,  wx.ALL, 10)
        sizer_main.Add(self.panel_details, 1, wx.EXPAND, 0)
        sizer_main.Add(self.button_save,   0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer_main)

        
    def displayData(self, student_id=0):
        #rint'displayData ; panel_edit_booking_student_details'
        self.student_id = student_id
        #self.panel_details.displayData(student_id)
        #self.panel_details.enableCtrls()
        #self.panel_details.button_guardian.Hide()
        
        
    def OnSave(self, event):
        msg = "This will overwrite existing data /n Procede?"
        ans = wx.MessageBox(msg, "Via Function", wx.YES_NO | wx.ICON_QUESTION)
        #rint 'ans = ', ans
        if  ans == 2:
            self.panel_details.saveDetails()
        else:
            pass
        
