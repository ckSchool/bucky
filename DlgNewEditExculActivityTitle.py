import wx, gVar, fetch, loadCmb

def create(parent):
    return DlgNewEditExculActivityTitle(parent)
    
class DlgNewEditExculActivityTitle(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_top = wx.Panel(self, -1)
        self.bitmap_activity        = wx.StaticBitmap(self.panel_top, -1, wx.Bitmap(".\\images\\48\\subject_48.png", wx.BITMAP_TYPE_ANY))
        self.panel_names            = wx.Panel(self.panel_top, -1)
        self.label_activity_name      = wx.StaticText(self.panel_names, -1, "Activity name")
        self.text_ctrl_activity_name  = wx.TextCtrl(self.panel_names, -1, "")
        self.label_description      = wx.StaticText(self.panel_names, -1, "Description")
        self.text_ctrl_description  = wx.TextCtrl(self.panel_names, -1, "")
        self.sizer_main_staticbox   = wx.StaticBox(self.panel_top, -1, "")
        self.button_enter           = wx.Button(self, -1, "Enter")
        

        self.Bind(wx.EVT_BUTTON, self.OnEnter,  self.button_enter)
        
        self.__set_properties()
        self.__do_layout()  
        self.__do_main()

    def __set_properties(self):
        self.SetTitle("Extra curricular activity")
        self.label_activity_name.SetMinSize((64, 16))
        self.text_ctrl_activity_name.SetMinSize((200, 21))
        self.text_ctrl_description.SetMinSize((200, 21))
        self.button_enter.SetMinSize((100, 30))

    def __do_layout(self):
        sizer_base       = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main_staticbox.Lower()
        sizer_main       = wx.StaticBoxSizer(self.sizer_main_staticbox, wx.VERTICAL)
        grid_sizer_names = wx.FlexGridSizer(2, 2, 10, 3)
        sizer_main.Add(self.bitmap_activity, 0, 0, 0)
        grid_sizer_names.Add(self.label_activity_name, 0, 0, 10)
        grid_sizer_names.Add(self.text_ctrl_activity_name, 0, wx.EXPAND, 10)
        grid_sizer_names.Add(self.label_description, 0, 0, 10)
        grid_sizer_names.Add(self.text_ctrl_description, 1, wx.BOTTOM | wx.EXPAND, 10)
        self.panel_names.SetSizer(grid_sizer_names)
        sizer_main.Add(self.panel_names, 0, wx.ALL | wx.EXPAND, 5)
        self.panel_top.SetSizer(sizer_main)
        sizer_base.Add(self.panel_top, 0, wx.ALL | wx.EXPAND, 10)
        
        sizer_base.Add(self.button_enter, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Center()

    def __do_main(self):
        pass
    
    def displayData(self, activity_id=0):
        self.activity_id = activity_id
        if activity_id: self.editMode = True
        else          : self.editMode = False
        
        self.text_ctrl_activity_name.SetValue(fetch.excul_activityTitle(activity_id))
        self.text_ctrl_description.SetValue('')
        
        #self.loadCmb      
        
    def OnCancel(self, event):
        self.id = 0
        self.EndModal(-1)
        
    def activityNameAvailable(self, activity_name):
        sql = "SELECT * FROM excul_activities WHERE name = '%s'" % (activity_name,)
        if fetch.getDig(sql):
            fetch.ask("Duplicate course name, please try another")
            return False
            
        else:       
            return True
        
    def OnEnter(self, event):
        activity_name = self.text_ctrl_activity_name.GetValue()
        description   = self.text_ctrl_description.GetValue()
        
        if not activity_name:
            txt = "Data not sufficient: must have course name"
            return
        
        if self.editMode:
            self.update(activity_name, description)
            self.EndModal(wx.ID_OK)
            
        else:
            if self.insertNewActivity(activity_name, description):  
                self.EndModal(wx.ID_OK)

    def insertNewActivity(self, activity_name, description):
        if self.activityNameAvailable(activity_name):
            sql = "INSERT INTO excul_activities\
                           SET name ='%s', description ='%s' "  % (activity_name, description)
            #rintsql
            return fetch.updateDB(sql)
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgNewEditExculActivity(None)
    try:
        dlg.displayData(3)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
