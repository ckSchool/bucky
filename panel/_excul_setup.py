import wx, gVar, fetch, loadCmb

from wx.lib.pubsub      import setupkwargs
from wx.lib.pubsub      import pub

import DlgExculActivityListEditor
import DlgExculSessionSetter

from myListCtrl import VirtualList

class panel_excul_sessions(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        pub.subscribe(self.displayData, 'dateChanged')
        
        heading = (('',10), ('Unallocated Students',110), ('',10))
        
        self.panel_top       = wx.Panel(self, -1)
        self.button_edit     = wx.Button(self.panel_top, -1, "( Edit session schedule )")#, style=wx.NO_BORDER  | wx.ALIGN_TOP)
        self.label_sessions  = wx.StaticText(self.panel_top, -1, " ")
        self.panel_lists     = wx.Panel(self, -1)
        self.panel_monday    = wx.Panel(self.panel_lists, 9001)
        self.panel_tuesday   = wx.Panel(self.panel_lists, 9002)
        self.panel_wednesday = wx.Panel(self.panel_lists, 9003)
        self.panel_thursday  = wx.Panel(self.panel_lists, 9004)
        self.panel_friday    = wx.Panel(self.panel_lists, 9005)
        self.panel_list_spc  = wx.Panel(self.panel_lists, -1)
        self.label_monday    = wx.StaticText(self.panel_monday,    -1, "Monday")
        self.label_tuesday   = wx.StaticText(self.panel_tuesday,   -1, "Tuesday")
        self.label_wednesday = wx.StaticText(self.panel_wednesday, -1, "Wednesday")
        self.label_thursday  = wx.StaticText(self.panel_thursday,  -1, "Thursday")
        self.label_friday    = wx.StaticText(self.panel_friday,    -1, "Friday")
        
        self.list_ctrl_mon  = VirtualList(self.panel_monday,    heading, style = wx.LC_HRULES) 
        self.list_ctrl_tue  = VirtualList(self.panel_tuesday,   heading, style = wx.LC_HRULES) 
        self.list_ctrl_wed  = VirtualList(self.panel_wednesday, heading, style = wx.LC_HRULES) 
        self.list_ctrl_thu  = VirtualList(self.panel_thursday,  heading, style = wx.LC_HRULES) 
        self.list_ctrl_fri  = VirtualList(self.panel_friday,    heading, style = wx.LC_HRULES)
        
        self.list_panels    = [self.panel_monday, self.panel_tuesday, self.panel_wednesday, self.panel_thursday, self.panel_friday]
        self.list_labels    = [self.label_monday, self.label_tuesday, self.label_wednesday, self.label_thursday, self.label_friday]
        self.list_ctrl_list = [self.list_ctrl_mon, self.list_ctrl_tue, self.list_ctrl_wed,   self.list_ctrl_thu,  self.list_ctrl_fri]
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

        pub.subscribe(self.displayData, 'exculFilter.changed')
        
        for l in self.list_ctrl_list:
            l.Bind(wx.EVT_CONTEXT_MENU, self.OnOpenPopup)
            
        self.Bind(wx.EVT_BUTTON, self.OnEdit, self.button_edit)
        self.button_edit.Bind(wx.EVT_MOUSE_EVENTS, self.OnButtonEditMouseEvent )
        #self.button_edit.SetAuthNeeded(True)
        
    def OnButtonEditMouseEvent(self, event, c = gVar.white):
        if event.GetEventType() == 10037: c = gVar.barkleys
        self.button_edit.SetForegroundColour(c)   

    def __set_properties(self):
        symbols={"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR,  "i_idx":wx.ART_QUESTION}
        heading = (('id',0,0), ('Title',100,0), ('Teacher',100,0))
        
        self.SetBackgroundColour(wx.Colour(47, 47, 79))
        self.button_edit.SetBackgroundColour(wx.Colour(47, 47, 79))
        self.button_edit.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_sessions.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_sessions.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        for l in self.list_labels: l.SetForegroundColour(gVar.white)
        
        for list_ctrl in self.list_ctrl_list:
            list_ctrl.initList(symbols, heading)
            list_ctrl.SetMinSize((200,-1))
            list_ctrl.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Times New Roman'))
        
    def __do_layout(self):
        sizer_main      = wx.BoxSizer(wx.VERTICAL)
        
        sizer_monday    = wx.BoxSizer(wx.VERTICAL)
        sizer_tuesday   = wx.BoxSizer(wx.VERTICAL)
        sizer_wednesday = wx.BoxSizer(wx.VERTICAL)
        sizer_thursday  = wx.BoxSizer(wx.VERTICAL)
        sizer_friday    = wx.BoxSizer(wx.VERTICAL)
        
        sizer_top       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_lists     = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top.Add(self.label_sessions, 0, wx.LEFT, 20)
        sizer_top.Add(self.button_edit,    0, wx.LEFT, 20)
        self.panel_top.SetSizer(sizer_top)
        
        for p in self.list_panels: sizer_lists.Add(p, 0, wx.ALL | wx.EXPAND, 20)
        
        sizer_monday.Add(self.label_monday,  0, 0, 0)
        sizer_monday.Add(self.list_ctrl_mon, 0, 0, 0)
        self.panel_monday.SetSizer(sizer_monday)
        
        sizer_tuesday.Add(self.label_tuesday,  0, 0, 0)
        sizer_tuesday.Add(self.list_ctrl_tue, 0, 0, 0)
        self.panel_tuesday.SetSizer(sizer_tuesday)
        
        sizer_wednesday.Add(self.label_wednesday,  0, 0, 0)
        sizer_wednesday.Add(self.list_ctrl_wed, 0, 0, 0)
        self.panel_wednesday.SetSizer(sizer_wednesday)
        
        sizer_thursday.Add(self.label_thursday,  0, 0, 0)
        sizer_thursday.Add(self.list_ctrl_thu, 0, 0, 0)
        self.panel_thursday.SetSizer(sizer_thursday)
        
        sizer_friday.Add(self.label_friday,  0, 0, 0)
        sizer_friday.Add(self.list_ctrl_fri, 0, 0, 0)
        self.panel_friday.SetSizer(sizer_friday)    
                         
        sizer_lists.Add(self.panel_list_spc, 1, wx.EXPAND, 0)
        self.panel_lists.SetSizer(sizer_lists)
        
        sizer_main.Add(self.panel_top,   0, wx.ALL,    0)
        sizer_main.Add(self.panel_lists, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.makePopupMenu()

    def displayData(self):
        dayNos = fetch.exculSchedule_forSchSemYr(gVar.school_id, gVar.semester)

        for panel in self.list_panels: panel.Hide()
        if dayNos:
            for day in dayNos:
                panel = self.list_panels[day-1]
                panel.Show()
                self.listActivities(day)
                
            self.Layout()
            txt = "%d Sessions for %s, Semester %d, %d " % (len(dayNos), gVar.school_id, gVar.semester, gVar.schYr)
                
        else:
            txt = "NO Sessions for %s, Semester %d, %d " % (gVar.school_id, gVar.semester, gVar.schYr)
            self.statusbar.SetStatusText(txt, 2)
            
        self.label_sessions.SetLabelText(txt)
        
    def listActivities(self, day):
        list_ctrl = self.list_ctrl_list[day-1]
        res = fetch.excul_groups_forSchSemYr(day, gVar.semester, gVar.school_id)
        
        newlist = []
        for row in res: newlist.append((row[0], row[2], row[4]))
        
        res = tuple(newlist)
        list_ctrl.SetItemMap(fetch.build_dictionary(res))
            
    def OnEdit(self, event): 
        dlg=DlgExculSessionSetter.create(None)
        try:
            dlg.displayData(gVar.school_id, gVar.semester)
            if dlg.ShowModal() == wx.OK:
                self.displayData()
        finally:
            dlg.Destroy()
            
    def OnEditList(self, evt):
        exculset_id = fetch.exculset_id()
        dlg=DlgExculActivityListEditor.create(None)
        try:
            dlg.displayData(exculset_id)
            if dlg.ShowModal() == wx.OK:
                self.displayData()
        finally:
            dlg.Destroy()
            
    def OnOpenPopup(self, evt):
        gVar.dayNo = evt.GetEventObject().GetParent().GetId() - 9000
        self.PopupMenu(self.mnu_abs)
    
    def makePopupMenu(self): # make a menu
        self.mnu_abs = wx.Menu()
        
        #if fetch.hasPermission('AddStudent'):
        item = wx.MenuItem(self.mnu_abs, -1, "Edit Activity List")
        self.Bind(wx.EVT_MENU, self.OnEditList, item)
        self.mnu_abs.AppendItem(item)