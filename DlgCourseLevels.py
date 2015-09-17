import wx, gVar, fetch, loadCmb

from myListCtrl import VirtualList 

class DlgCourseLevels(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.list_ctrl_course_levels = VirtualList(self)
        
        self.panel_buttons = wx.Panel(self, -1)
        self.label_spc1    = wx.StaticText(self.panel_buttons, -1, "")
        self.button_add    = wx.Button(self.panel_buttons,     -1, "Add")
        self.button_delete = wx.Button(self.panel_buttons,     -1, "Delete")
        self.label_scp2    = wx.StaticText(self.panel_buttons, -1, "")

        self.Bind(wx.EVT_BUTTON, self.OnAdd,    self.button_add)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.button_delete)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        self.SetTitle("Course Levels")
        self.list_ctrl_course_levels.SetMinSize((300,400))

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_buttons.Add(self.label_spc1,    1, 0, 0)
        sizer_buttons.Add(self.button_add,    0, wx.RIGHT, 5)
        sizer_buttons.Add(self.button_delete, 0, wx.LEFT, 5)
        sizer_buttons.Add(self.label_scp2,    1, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_main.Add(self.list_ctrl_course_levels, 1, wx.ALL | wx.EXPAND, 5)
        sizer_main.Add(self.panel_buttons,           0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        self.Centre()
        
    def __do_main(self, ):
        columns =  ( ('id',0),  ('Level', 80), ('Title', 150) )
        self.list_ctrl_course_levels.SetColumns(columns)
        self.displayData()
        
        
    def displayData(self):
        res = fetch.courses_levels_all_DATA()
        print res
        if not res:
            msg = "No courses levels found"
            
            fetch.msg(msg)
        else:
            self.list_ctrl_course_levels.SetItemMap(res)
            
        self.list_ctrl_course_levels.SortListItems(1)
        
    def OnAdd(self, evt):
        print 'OnAdd open DlgLevelEditor'
    
    def OnDelete(self, evt):
        print 'OnDelete'
        
        level_id = self.list_ctrl_course_levels.GetSelectedID()
        level = fetch.level_level_id(level_id)
        
        if fetch.level_unused(level_id):
            sql = "DELETE FROM course_levels WHERE level = %d" % level
            print 'fetch.updateDB(', sql, ')'
            self.displayData()
        else:
            courses = fetch.courses_forLevel(level)
            print courses
            print 'Level in use by courses ' , courses
            
    
if __name__ == "__main__":
    app = wx.App(0)
    dialog_1 = DlgCourseLevels(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
