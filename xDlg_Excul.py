
import wx

from PanelExculPool    import PanelExculPool
from PanelExculRoster  import PanelExculRoster
from PanelExculCreator import PanelExculCreator as PanelExculActivitiesScheduler


def create(parent):
    return Dlg_ExculEditor(parent)

[wxID_DLG_EXCULEDITOR, wxID_DLG_EXCULEDITORB_1, wxID_DLG_EXCULEDITORB_2, 
 wxID_DLG_EXCULEDITORB_3, wxID_DLG_EXCULEDITORB_4, wxID_DLG_EXCULEDITORB_5, 
 wxID_DLG_EXCULEDITORP_1, wxID_DLG_EXCULEDITORP_2, wxID_DLG_EXCULEDITORP_3, 
 wxID_DLG_EXCULEDITORP_4, wxID_DLG_EXCULEDITORP_5, 
 wxID_DLG_EXCULEDITORP_SWITCHPANEL, 
] = [wx.NewId() for _init_ctrls in range(12)]

class Dlg_ExculEditor(wx.Dialog):
    _custom_classes =  {'wx.Panel': ['PanelExculRoster',
                                     'PanelExculActivitiesScheduler',
                                     'PanelExculPool']}
    def _init_coll_bxs_mainLayout_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.p_switchPanel, 0, border=0,
              flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_1, 1, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_2, 1, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_3, 1, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_4, 1, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_5, 1, border=0, flag=wx.EXPAND | wx.ALL)

    def _init_coll_bxs_swithBtns_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.b_1, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.b_2, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.b_3, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.b_4, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.b_5, 0, border=10, flag=wx.ALL)

    def __do_layout(self):
        # generated method, don't edit
        self.bxs_mainLayout = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.bxs_swithBtns = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_bxs_mainLayout_Items(self.bxs_mainLayout)
        self._init_coll_bxs_swithBtns_Items(self.bxs_swithBtns)

        self.SetSizer(self.bxs_mainLayout)
        self.p_switchPanel.SetSizer(self.bxs_swithBtns)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLG_EXCULEDITOR,
              name='Dlg_ExculEditor', parent=prnt, pos=wx.Point(399, 262),
              size=wx.Size(1031, 632), style=wx.DEFAULT_DIALOG_STYLE,
              title='Populate extra curricular classes')
        self.SetClientSize(wx.Size(1023, 604))

        self.p_3 = wx.Panel(id=wxID_DLG_EXCULEDITORP_3, name='p_3', parent=self,
              pos=wx.Point(465, 0), size=wx.Size(185, 604),
              style=wx.TAB_TRAVERSAL)
        self.p_3.SetBackgroundColour(wx.Colour(202, 166, 247))

        self.p_switchPanel = wx.Panel(id=wxID_DLG_EXCULEDITORP_SWITCHPANEL,
              name='p_switchPanel', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(95, 604), style=wx.TAB_TRAVERSAL)
        self.p_switchPanel.SetBackgroundColour(wx.Colour(217, 192, 220))

        self.p_1 = PanelExculActivitiesScheduler(self, -1)
        self.p_1.SetBackgroundColour(wx.Colour(214, 243, 239))

        self.p_2 = PanelExculRoster(self, -1)
        self.p_2.SetBackgroundColour(wx.Colour(243, 219, 169))

        self.p_4 = wx.Panel(id=wxID_DLG_EXCULEDITORP_4, name='p_4', parent=self,
              pos=wx.Point(650, 0), size=wx.Size(185, 604),
              style=wx.TAB_TRAVERSAL)
        self.p_4.SetBackgroundColour(wx.Colour(222, 253, 159))

        self.b_1 = wx.Button(id=wxID_DLG_EXCULEDITORB_1, label='Scheduler',
              name='b_1', parent=self.p_switchPanel, pos=wx.Point(10, 10),
              size=wx.Size(72, 72), style=0)
        self.b_1.Bind(wx.EVT_BUTTON, self.OnB_SwitchPanel_Click,
              id=wxID_DLG_EXCULEDITORB_1)

        self.b_2 = wx.Button(id=wxID_DLG_EXCULEDITORB_2,
              label='Students\n    for\nactivities', name='b_2',
              parent=self.p_switchPanel, pos=wx.Point(10, 102), size=wx.Size(72,
              72), style=0)
        self.b_2.Bind(wx.EVT_BUTTON, self.OnB_SwitchPanel_Click,
              id=wxID_DLG_EXCULEDITORB_2)

        self.b_3 = wx.Button(id=wxID_DLG_EXCULEDITORB_3, label='Sessions',
              name='b_3', parent=self.p_switchPanel, pos=wx.Point(10, 194),
              size=wx.Size(72, 72), style=0)
        self.b_3.Bind(wx.EVT_BUTTON, self.OnB_SwitchPanel_Click,
              id=wxID_DLG_EXCULEDITORB_3)

        self.b_4 = wx.Button(id=wxID_DLG_EXCULEDITORB_4, label='Creator',
              name='b_4', parent=self.p_switchPanel, pos=wx.Point(10, 286),
              size=wx.Size(72, 72), style=0)
        self.b_4.Bind(wx.EVT_BUTTON, self.OnB_SwitchPanel_Click,
              id=wxID_DLG_EXCULEDITORB_4)

        self.b_5 = wx.Button(id=wxID_DLG_EXCULEDITORB_5,
              label='Resource\n allocator', name='b_5',
              parent=self.p_switchPanel, pos=wx.Point(10, 378), size=wx.Size(75,
              70), style=0)
        self.b_5.Bind(wx.EVT_BUTTON, self.OnB_SwitchPanel_Click,
              id=wxID_DLG_EXCULEDITORB_5)

        self.p_5 = PanelExculPool(self, -1)

        self.__do_layout()

    def __init__(self, parent):
        global g_semester_no, g_schYr
        self._init_ctrls(parent)
        
        self.SetSize((1020,600))
        self.Center()
        self.selectPanel(self.p_1)
        
    def selectPanel(self, p):
        self.p_1.Hide()
        self.p_2.Hide()
        self.p_3.Hide()
        self.p_4.Hide()
        self.p_5.Hide()
        
        p.Show()
        
    def OnB_SwitchPanel_Click(self, event):
        obj  = event.GetEventObject()
        id   = obj.GetId() 
        name = obj.GetName()
        ##rintname
        if   name == 'b_1': self.selectPanel(self.p_1)
        elif name == 'b_2': self.selectPanel(self.p_2)
        elif name == 'b_3': self.selectPanel(self.p_3)
        elif name == 'b_4': self.selectPanel(self.p_4)
        elif name == 'b_5': self.selectPanel(self.p_5)
       
        ##rintname
        self.Layout()
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = create(None)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
