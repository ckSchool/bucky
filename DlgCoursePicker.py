import wx, gVar, fetch, loadCmb

gVar.schYr = 2015

from myListCtrl import VirtualList

import DlgCourseEditor

class DlgCoursePicker(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_top = wx.Panel(self, -1)
        
        self.panel_left  = wx.Panel(self.panel_top, -1)
        self.panel_right = wx.Panel(self.panel_top, -1)
        
        self.label_left               = wx.StaticText(self.panel_left, -1, "Course Pool")
        self.list_ctrl_all_courses    = VirtualList(self.panel_left)#, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.button_new               = wx.Button(self.panel_left, -1, "+" )
        
        self.label_right              = wx.StaticText(self.panel_right, -1, "Courses For Year")
        self.list_ctrl_course_by_year = VirtualList(self.panel_right)#, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.label_spc_right          = wx.StaticText(self.panel_right, -1, "" )
        
        self.panel_buttons = wx.Panel(self, -1)
        self.label_spc1    = wx.StaticText(self.panel_buttons, -1, "")
        self.button_save   = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel = wx.Button(self.panel_buttons, -1, "Cancel")
        self.label_spc2    = wx.StaticText(self.panel_buttons, -1, "")
        
        self.Bind(wx.EVT_BUTTON, self.OnNewCourse,  self.button_new)
        self.Bind(wx.EVT_BUTTON, self.OnSave,  self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,  self.button_cancel)

        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def OnNewCourse(self, evt):
        pass
    
    def OnSave(self, evt):
        pass
    
    
    def OnCancel(self, evt):
        pass

    def __set_properties(self):
        self.SetTitle("Course Picker")
        self.list_ctrl_all_courses.SetMinSize(   (200, 400))
        self.list_ctrl_course_by_year.SetMinSize((200, 400))

    def __do_layout(self):
        sizer_main    = wx.BoxSizer(wx.VERTICAL)
        sizer_top     = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left    = wx.BoxSizer(wx.VERTICAL)
        sizer_right   = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_left.Add(self.label_left,            0, 0, 0)
        sizer_left.Add(self.list_ctrl_all_courses, 1, 0, 0)
        sizer_left.Add(self.button_new,            0, 0, 0)
        self.panel_left.SetSizer(sizer_left)
        
        sizer_right.Add(self.label_right,              0, 0, 0)
        sizer_right.Add(self.list_ctrl_course_by_year, 1, 0, 0)
        sizer_right.Add(self.label_spc_right,          0, 0, 0)
        self.panel_right.SetSizer(sizer_right)
        
        sizer_top.Add(self.panel_left,  1, wx.ALL | wx.EXPAND, 5)
        sizer_top.Add(self.panel_right, 1, wx.ALL | wx.EXPAND, 5)
        self.panel_top.SetSizer(sizer_top)
        
        
        sizer_buttons.Add(self.label_spc1, 1, 0, 0)
        sizer_buttons.Add(self.button_save, 0, wx.RIGHT, 5)
        sizer_buttons.Add(self.button_cancel, 0, wx.LEFT, 5)
        sizer_buttons.Add(self.label_spc2, 1, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        
        sizer_main.Add(self.panel_top, 1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_buttons, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_main)
        
        sizer_main.Fit(self)
        
        self.Layout()
        self.Centre()
        
    def __do_main(self, ):
        columns = (('id', 0),('Course Pool', 120), ('Level',70))
        self.list_ctrl_all_courses.SetColumns(columns)
        
        res = fetch.courses_DATA()
        if not res:
            msg = "No courses for found"
            fetch.msg(msg)
        else:
            self.list_ctrl_all_courses.SetItemMap(res)
            
            
        x = 'Courses for %d' % gVar.schYr
        columns = (('id', 0), (x, 120), ('Level',70))
        self.list_ctrl_course_by_year.SetColumns(columns)
        
        res = fetch.courses_for_year_DATA(gVar.schYr)
        if not res:
            msg = "No courses for found"
            fetch.msg(msg)
        else:
            self.list_ctrl_course_by_year.SetItemMap(res)
    

if __name__ == "__main__":
    app = wx.App(0)
    dialog_1 = DlgCoursePicker(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
