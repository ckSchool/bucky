import wx, gVar, fetch, loadCmb

from panel_guardian_data import panel_guardian_data

from wx.lib.buttons import GenButton

class panel_guardian_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.notebook_tabs = wx.Panel(self, -1)
        self.tab_f = wx.Button(self.notebook_tabs, -1, "Father")
        self.tab_m = wx.Button(self.notebook_tabs, -1, "Mother")
        self.tab_g = wx.Button(self.notebook_tabs, -1, "Guardian")
        
        self.notebook = wx.Panel(self, -1)
        self.notebook_pane_1 = panel_guardian_data(self.notebook, -1)
        self.notebook_pane_2 = panel_guardian_data(self.notebook, -1)
        self.notebook_pane_3 = panel_guardian_data(self.notebook, -1)
        
        self.tabs            = [self.tab_f, self.tab_m, self.tab_g]
        self.notebook_panes  = [self.notebook_pane_1, self.notebook_pane_2, self.notebook_pane_3]
        
        #self.button_edit = wx.Button(self, -1, 'Edit')
        
        self.Bind(wx.EVT_BUTTON, self.OnTab, self.tab_f)
        self.Bind(wx.EVT_BUTTON, self.OnTab, self.tab_m)
        self.Bind(wx.EVT_BUTTON, self.OnTab, self.tab_g)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.tab_f.SetName('f')
        self.tab_m.SetName('m')
        self.tab_g.SetName('g')
        
        for tab in self.tabs:
            tab.SetWindowStyle(style=wx.NO_BORDER)
            if tab.GetName()=='f':  tab.SetBackgroundColour((255, 255, 255))
            else: tab.SetBackgroundColour((240, 250, 255)) 
        
        self.notebook_pane_1.SetName('f')
        self.notebook_pane_2.SetName('m')
        self.notebook_pane_3.SetName('g')
        
        for n in self.notebook_panes:
            if n.GetName() == 'f':   n.Show()
            else:  n.Hide()
                
        self.Layout()

    def __do_layout(self):
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        sizer_tabs  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panes = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_tabs.Add(self.tab_f, 0, 0, 0)
        sizer_tabs.Add(self.tab_m, 0, 0, 0)
        sizer_tabs.Add(self.tab_g, 0, 0, 0)
        self.notebook_tabs.SetSizer(sizer_tabs)
        
        sizer_panes.Add(self.notebook_pane_1, 1, wx.EXPAND, 0)
        sizer_panes.Add(self.notebook_pane_2, 1, wx.EXPAND, 0)
        sizer_panes.Add(self.notebook_pane_3, 1, wx.EXPAND, 0)
        self.notebook.SetSizer(sizer_panes)
        
        sizer_main.Add(self.notebook_tabs, 0, 0, 0)
        sizer_main.Add(self.notebook,      1, wx.EXPAND, 0)
        #sizer_main.Add(self.button_edit,   0, 0, 0)
        self.SetSizer(sizer_main)
        
        self.Layout()
        
    def __do_main(self):
        self.tabname = 'f'
        self.enableCtrls(False)
        self.editing=False
        
    def OnTab(self, evt):
        print 'OnTab'
        if self.editing: return
        
        tab = evt.GetEventObject()
        self.tabname = tab.GetName()
        
        for t in self.tabs:
            if t != tab: t.SetBackgroundColour((240, 250, 255))
            else:        t.SetBackgroundColour((255, 255, 255))
        
        for n in self.notebook_panes:
            if  n.GetName() == self.tabname:
                
                n.Show()
            else:
                n.Hide()
                
        self.Layout()
        
        
    def onlyShow(self, tabname):
        print 'panel_guardian_details > onlyShow', tabname 
        for n in self.notebook_panes:
            if  n.GetName() == self.tabname:
                n.Show()
            else:
                n.Hide()
                
        for tab in self.tabs: tab.Hide()
                
        self.Layout()
        
    def getCurrentTabname(self):
        return self.tabname        
        
    def OnChangePage(self, evt):
        if self.editing:
            evt.Veto()
        
    def clearCtrls(self):
        pass
    
    def enableAllCtrls(self):
        print 'panel_guardian_details > enableAllCtrls'
        for nb in self.notebook_panes:
            nb.Enable()
        
    def enableCtrls(self, state = True):
        print 'panel_guardian_details > enableCtrls'
        if self.IsShown():
            for nb in self.notebook_panes:
                nb.Enable(state)
                
    def disableCtrls(self, state = False):
        if self.IsShown():
            for nb in self.notebook_panes:
                nb.Enable(state)
        
    def displayData(self, student_id):
        self.student_id = student_id
        print 'panel_guardian_details > student_id', student_id
        sql = "SELECT father_id, mother_id, guardian_id FROM students WHERE id=%d" % student_id
        #print sql
        student_details = fetch.getOneDict(sql)
        
 
        father_id   = student_details['father_id']
        mother_id   = student_details['mother_id']
        guardian_id = student_details['guardian_id']
        
        self.notebook_pane_1.displayData('father',   father_id,   self.student_id)
        self.notebook_pane_2.displayData('mother',   mother_id,   self.student_id)
        self.notebook_pane_3.displayData('guardian', guardian_id, self.student_id)
        
    def Save(self):
        for nb in self.notebook_panes:
            if nb.IsShown():
                nb.saveData()

    def OnSave(self, event):
        for nb in self.notebook_panes:
            if nb.IsShown():
                nb.saveData()