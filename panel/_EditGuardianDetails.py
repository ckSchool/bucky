import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb

from PanelGuardianData import PanelGuardianData as panel_guardian

class edit_guardian(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.notebook         = wx.Notebook(self, -1, style=0)
        
        self.notebook_pane_1  = panel_guardian(self.notebook, -1)
        self.notebook_pane_2  = panel_guardian(self.notebook, -1)
        self.notebook_pane_3  = panel_guardian(self.notebook, -1)
        
        self.notebook_panes   = [self.notebook_pane_1, self.notebook_pane_2, self.notebook_pane_3]
        
        self.panel_ctrls        = wx.Panel(self, -1)
        self.panel_spc1         = wx.Panel(self.panel_ctrls, -1)
        self.button_edit_cancel = wx.Button(self.panel_ctrls, -1, "Edit")
        self.panel_spc2         = wx.Panel(self.panel_ctrls, -1)
        self.button_save        = wx.Button(self.panel_ctrls, -1, "Save")
        self.panel_spc3         = wx.Panel(self.panel_ctrls, -1)

        self.__set_properties()
        self.__do_layout()
        self.__do_main()

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.Onpanel_guardian_changePage) 
        self.Bind(wx.EVT_BUTTON, self.OnEditCancel,       self.button_edit_cancel)
        self.Bind(wx.EVT_BUTTON, self.OnSave,             self.button_save)

    def Onpanel_guardian_changePage(self, evt):
        if self.editmode:
            evt.Veto()
            
    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        sizer_ctrls = wx.BoxSizer(wx.HORIZONTAL)
        
        self.notebook.AddPage(self.notebook_pane_1, "Father")
        self.notebook.AddPage(self.notebook_pane_2, "Mother")
        self.notebook.AddPage(self.notebook_pane_3, "Guardian")
        
        sizer_main.Add(self.notebook,            1, wx.EXPAND, 0)
        sizer_ctrls.Add(self.panel_spc1,         2, wx.EXPAND, 0)
        sizer_ctrls.Add(self.button_edit_cancel, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_ctrls.Add(self.panel_spc2,         1, wx.TOP | wx.BOTTOM | wx.EXPAND, 20)
        sizer_ctrls.Add(self.button_save,        0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_ctrls.Add(self.panel_spc3,         2, wx.EXPAND, 0)
        self.panel_ctrls.SetSizer(sizer_ctrls)
        
        sizer_main.Add(self.panel_ctrls,         0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        
        sizer_main.Fit(self)
        self.Layout()
        self.Center()
        
    def __do_main(self):
        self.enableCtrls(False)
        self.editmode=False
        self.button_save.Hide()
        self.Layout()
        
    def enableCtrls(self, state = True):
        for nb in self.notebook_panes:
            nb.Enable(state)
        
    def displayData(self, student_id):
        self.student_id = student_id
        self.notebook_pane_1.displayData(student_id, 0, 'father')
        self.notebook_pane_2.displayData(student_id, 0, 'mother')
        self.notebook_pane_3.displayData(student_id, 0, 'guardian')
        
    def OnEditCancel(self, event):
        if self.button_edit_cancel.GetLabelText()=='Edit':
            self.button_edit_cancel.SetLabelText('Cancel')
            self.editmode = True
            self.button_save.Show()
            for nb in self.notebook_panes:
                nb.Enable(nb.IsShown())
            
        else:
            self.button_edit_cancel.SetLabelText('Edit')
            self.enableCtrls(False)
            self.editmode=False
            self.button_save.Hide()
        self.Layout()

    def OnSave(self, event):
        for nb in self.notebook_panes:
            if nb.IsShown():
                nb.saveData()