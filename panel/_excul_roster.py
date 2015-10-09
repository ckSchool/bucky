import wx, gVar, fetch, loadCmb, popup

from PanelExculRosterView import PanelExculRosterView

class panel_excul_roster(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.SetName('panel_excul_roster')
        
        try:    self.statusbar = self.GetTopLevelParent().statusbar
        except: pass
        
        self.label_heading = wx.StaticText(self, -1, 'roster')
        
        self.panel_middle  = PanelExculRosterView(self, -1)
        self.button_edit   = wx.Button(self, -1)
        
        self.button_edit.Bind(wx.EVT_BUTTON,   self.OnEdit)

        self.__do_properties()
        self.__do_layout()
        self.__do_main()
        
    def __do_properties(self):
        self.label_heading.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_heading.SetForegroundColour(gVar.white)

    def __do_layout(self):
        sizer_main         = wx.BoxSizer(orient=wx.VERTICAL)
        
        sizer_main.Add(self.label_heading, 0, wx.EXPAND) 
        sizer_main.Add(self.panel_middle,  1, wx.EXPAND)
        sizer_main.Add(self.button_edit,       0, 0, 0)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        pass
        
    def displayData(self):
        return
        #rint'panel_excul_roster > displayData'
        
        txt = "Students / Activity:  >    %d     Semester:%d    Yr:%d    Day:%d" % (gVar.school_id, gVar.semester, gVar.schYr, gVar.dayNo)
        self.label_heading.SetLabelText(txt)
        self.exculset_id = fetch.exculset_id()
        
        
        self.panel_middle.displayData(self.exculset_id)
   
            


    def OnEdit(self, event):
        event.Skip()


