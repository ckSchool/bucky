import wx, fetch, loadCmb, gVar, images

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from operator      import itemgetter

#import DlgExculEditor

from panel_excul_set_days import panel_excul_set_days
from panel_excul_sessions import panel_excul_sessions
from panel_excul_roster   import panel_excul_roster
from panel_excul_pool     import panel_excul_pool
from panel_excul_activities_scheduler import panel_excul_activities_scheduler
"""
class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)

    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)

        if   t1  < t2: return -1
        elif t1 == t2: return 0
        else:          return 1"""
        
        
class panel_excul(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.panel_spc_tl     = wx.Panel(self, -1)
        self.panel_filter     = wx.Panel(self, -1)
        self.panel_buttons    = wx.Panel(self, -1)
        self.panel_panes      = wx.Panel(self, -1)
        
        self.label_semester   = wx.StaticText(self.panel_filter, -1, "Semester")
        self.choice_semester  = wx.Choice(self.panel_filter, -1, choices=["1", "2"])
        self.label_school     = wx.StaticText(self.panel_filter, -1, "School")
        self.choice_school    = wx.Choice(self.panel_filter, -1, choices=["SD","SM"])
        
        self.button_set_days  = wx.Button(self.panel_buttons, -1, "Excul\nBy Day")
        self.button_scheduler = wx.Button(self.panel_buttons, -1, "Scheduler")
        self.button_students  = wx.Button(self.panel_buttons, -1, "Students\nfor\nactivities")
        self.button_sessions  = wx.Button(self.panel_buttons, -1, "Sessions")
        self.button_creator   = wx.Button(self.panel_buttons, -1, "Creator")
        self.button_allocator = wx.Button(self.panel_buttons, -1, "Resource\nallocator")
        
        self.panel_excul_sessions = panel_excul_sessions(self.panel_panes, -1)
        self.panel_excul_set_days = panel_excul_set_days(self.panel_panes, -1)
        self.panel_2              = wx.Panel(self.panel_panes, -1)
        self.panel_excul_roster   = panel_excul_roster(self.panel_panes, -1)
        self.panel_excul_pool     = panel_excul_pool(self.panel_panes, -1)
        self.panel_excul_activities_scheduler = panel_excul_activities_scheduler(self.panel_panes, -1)
        
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_set_days)
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_scheduler)
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_students)
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_sessions)
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_creator)
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.button_allocator)
        
        self.Bind(wx.EVT_CHOICE, self.OnSemester, self.choice_semester)
        self.Bind(wx.EVT_CHOICE, self.OnSchool,   self.choice_school)
   
        self.pane_btn_dict = {
            
            self.button_scheduler: self.panel_excul_activities_scheduler,
            self.button_students:  self.panel_excul_pool, 
            self.button_sessions:  self.panel_excul_sessions,
            self.button_creator:   self.panel_2,
            self.button_allocator: self.panel_excul_roster,
            self.button_set_days:  self.panel_excul_set_days
            }
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        for key in self.pane_btn_dict:
            key.SetMinSize((60, 60))

    def __do_layout(self):
        sizer_main    = wx.FlexGridSizer(2, 2, 5, 5)
        sizer_panes   = wx.BoxSizer()
        sizer_filter  = wx.BoxSizer()
        sizer_buttons = wx.BoxSizer(wx.VERTICAL)
        
        sizer_filter.Add(self.label_semester)
        sizer_filter.Add(self.choice_semester)
        sizer_filter.Add(self.label_school)
        sizer_filter.Add(self.choice_school)
        self.panel_filter.SetSizer(sizer_filter)
        
        newdict = sorted(self.pane_btn_dict.items(), key=lambda x: x[1], reverse=True)
        for key in newdict:
            btn = key[0]
            #rintbtn
        #for btn in self.pane_btn_dict:
            sizer_buttons.Add(btn,  0, wx.ALL, 10)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        for btn in self.pane_btn_dict:
            sizer_panes.Add(self.pane_btn_dict[btn], 1, wx.EXPAND, 0)
        self.panel_panes.SetSizer(sizer_panes)
        
        sizer_main.Add(self.panel_spc_tl,  0, 0, 0)
        sizer_main.Add(self.panel_filter,  0, 0, 0)
        sizer_main.Add(self.panel_buttons, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_panes, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        
    def __do_main(self):
        self.current_panel = self.panel_excul_set_days
        loadCmb.fillCmb(self.choice_school, ((2, "SD"), (3,"SM")))
        gVar.school_id = 2
        loadCmb.restore(self.choice_school, 2)
        #self.choice_semester.Select(0)
        gVar.semester = 1
        loadCmb.restore_str(self.choice_semester, '1')
        self.OnSwitch(self.button_set_days.EventHandler)
        
    def OnSwitch(self, evt):
        #rint'OnSwitch'
        for btn in self.pane_btn_dict:
            p = self.pane_btn_dict[btn]
            if evt.GetId() == btn.GetId():
                self.current_panel = p
                p.Show()
                self.updateDisplay()
                btn.SetBackgroundColour(gVar.barkleys)
            else:
                p.Hide()
                btn.SetBackgroundColour(self.GetBackgroundColour())
        self.Layout()
        
    def updateDisplay(self):
        self.current_panel.displayData()
        
    def OnSemester(self, evt):
        gVar.semester = int(fetch.cmbValue(self.choice_semester))
        self.updateDisplay()
        
    
    def OnSchool(self, evt):
        if fetch.cmbValue(self.choice_school)=="SD":
            gVar.school_id = 2
        else:
            gVar.school_id = 3
        self.updateDisplay()