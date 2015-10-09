import wx, fetch, loadCmb, gVar
from wx.lib.pubsub import pub

import Dlg_ExculEditor
from PanelFilters import filter_horiz_sch

# order : sessions, roster, scheduler, pool
from PanelExcul        import PanelExcul         as ExculSessions
from PanelExculRoster  import PanelExculRoster   as ExculRoster
from PanelExculCreator import PanelExculCreator  as ExculCreator
from PanelExculPool    import PanelExculPool     as ExculPool

class PanelExculSwitch(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)


        # switch panel
        # order : sessions, roster, scheduler, pool
        self.panel_switch    = wx.Panel(self, -1)
        self.button_sessions = wx.Button(self.panel_switch, -1, "Sessions",                  style=wx.NO_BORDER)
        self.button_roster   = wx.Button(self.panel_switch, -1, "Students\nFor\nActivity",   style=wx.NO_BORDER)
        self.button_creator  = wx.Button(self.panel_switch, -1, "Activity\nFor\nDay",        style=wx.NO_BORDER)
        self.button_pool     = wx.Button(self.panel_switch, -1, "Activity &\nTeacher\nPool", style=wx.NO_BORDER)
        
        
        self.panel_filter    = wx.Panel(self, -1)
        self.choice_school   = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_semester = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_day      = wx.Choice(self.panel_filter, -1, choices=[])
        
        
        self.panel_main      = wx.Panel(self, -1)
        self.panel_sessions  = ExculSessions(self.panel_main, -1)
        self.panel_roster    = ExculRoster(self.panel_main,   -1)
        self.panel_creator   = ExculCreator(self.panel_main,  -1)
        self.panel_pool      = ExculPool(self.panel_main,     -1)
        
        self.choiceCtrls = [self.choice_school,   self.choice_day, self.choice_semester]
        self.switchBtns  = [self.button_sessions, self.button_roster, self.button_creator, self.button_pool]
        self.viewPanels  = [self.panel_sessions,  self.panel_roster,  self.panel_creator,  self.panel_pool]
        
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.OnSchool,    self.choice_school)
        self.Bind(wx.EVT_CHOICE, self.OnSemester,  self.choice_semester)
        self.Bind(wx.EVT_CHOICE, self.OnDay,       self.choice_day)
        
        self.Bind(wx.EVT_BUTTON, self.OnSessions,  self.button_sessions)
        self.Bind(wx.EVT_BUTTON, self.OnRoster,    self.button_roster)
        
        self.Bind(wx.EVT_BUTTON, self.OnScheduler, self.button_creator)
        self.Bind(wx.EVT_BUTTON, self.OnPool,      self.button_pool)

        self.__do_main()

    def __set_properties(self):
        self.SetBackgroundColour(wx.Colour(47, 47, 79))
        self.panel_filter.SetBackgroundColour(gVar.barkleys)
        self.panel_filter.SetMinSize((-1, 28))
        
        font = self.button_sessions.Parent.GetFont()
        font.SetStyle(wx.FONTSTYLE_ITALIC)
        font.Scale(.8)

        #self.label_school.SetForegroundColour(gVar.darkGrey)
        #self.label_school.SetFont(font)
        
        #self.label_semester.SetForegroundColour(gVar.darkGrey)
        #self.label_semester.SetFont(font)
        
        #self.label_day.SetForegroundColour(gVar.darkGrey)
        #self.label_day.SetFont(font)
        
        for c in self.choiceCtrls:
            c.SetMinSize((100, 18))
            c.SetFont(font)

        for btn in self.switchBtns:  btn.SetMinSize((60, 60))

    def __do_layout(self):
        sizer_base   = wx.BoxSizer(wx.VERTICAL)
        sizer_filter = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_switch = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_filter.Add(self.choice_school,   0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 110)
        sizer_filter.Add(self.choice_semester, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_filter.Add(self.choice_day,      0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        self.panel_filter.SetSizer(sizer_filter)
        
        for btn in self.switchBtns:
            sizer_switch.Add(btn, 0, wx.LEFT, 10)
        self.panel_switch.SetSizer(sizer_switch)
        sizer_main.Add(self.panel_switch, 0,  wx.EXPAND, 0)
        
        for pnl in self.viewPanels:
            sizer_main.Add(pnl,  1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_filter, 0, wx.EXPAND)
        sizer_base.Add(self.panel_main,   1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)

    def __do_main(self):
        self.defaultColour = self.choice_day.GetBackgroundColour()
        
        loadCmb.schDiv(self.choice_school)
        loadCmb.days(self.choice_day)

        self.choice_semester.Append('Semester 1', 1)
        self.choice_semester.Append('Semester 2', 2)
        
        self.choice_day.SetSelection(0)
        self.choice_school.SetSelection(2)
        self.choice_semester.SetSelection(0)
        self.selectPanel(0)
        
    def displayData(self):
        self.GetTopLevelParent().showSemester(True)
        gVar.school_id = fetch.cmbID(self.choice_school)
        gVar.semester  = fetch.cmbID(self.choice_semester)
        gVar.day       = fetch.cmbID(self.choice_day)
        pub.sendMessage('exculFilter.changed')
        #rint'exculFilterChanged'
        
    
    def OnSchool(  self, event): self.displayData()
    def OnSemester(self, event): self.displayData()
    def OnDay(     self, event): self.displayData()
    
    def selectPanel(self, idx):
        for btn in self.switchBtns: btn.SetBackgroundColour(self.defaultColour)
        for pnl in self.viewPanels: pnl.Hide()
        
        self.switchBtns[idx].SetBackgroundColour(gVar.barkleys)
        self.viewPanels[idx].Show()
        
        self.Layout()

        #self.label_day.Show(idx>0)
        self.choice_day.Show(idx>0)

    # excul, roster, scheduler, pool]
    def OnSessions(self, event):  self.selectPanel(0)
    def OnRoster(self, event):    self.selectPanel(1)
    def OnScheduler(self, event): self.selectPanel(2)
    def OnPool(self, event):      self.selectPanel(3)