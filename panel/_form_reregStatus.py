import wx, gVar, loadCmb, fetch, datetime

from myListCtrl import VirtualList as vListCtrl

from panel_student_bio import panel_student_bio

from panel_filter_school_level_form import panel_filter_school_level_form

from DateCtrl import DateCtrl

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

#---------------------------------------------------------------------------

class panel_form_reregStatus(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_top    = wx.Panel(self, -1)
        self.panel_bottom = wx.Panel(self, -1)
        self.panel_left   = wx.Panel(self.panel_bottom, -1)
        self.panel_right  = panel_student_bio(self.panel_bottom, -1)
        
        self.label_heading     = wx.StaticText(self.panel_top, -1, " Current Students ")
        self.panel_filter      = panel_filter_school_level_form(self.panel_top, -1)
        self.vList             = vListCtrl(self.panel_left, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.text_ctrl_records = wx.TextCtrl(self.panel_left, -1, '')
          
        # for wxMSW
        self.vList.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        
        # for wxGTK
        self.vList.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
     
        pub.subscribe(self.displayData,'filter_sch.change')
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.panel_top.SetMinSize((-1, 50))
        self.panel_top.SetMaxSize((-1, 50))
        
        headings = [('id',50),('Name',250),('Regeg Status',150)]
        self.vList.SetColumns(headings)


    def __do_layout(self):
        sizer_main   = wx.BoxSizer( wx.VERTICAL)
        sizer_top    = wx.BoxSizer( wx.VERTICAL)
        sizer_bottom = wx.BoxSizer( wx.HORIZONTAL)
        sizer_left   = wx.BoxSizer( wx.VERTICAL)
        sizer_filter = wx.BoxSizer( wx.HORIZONTAL)
        sizer_date   = wx.BoxSizer( wx.HORIZONTAL)
        
        sizer_top.Add(self.label_heading,          0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_top.Add(self.panel_filter,   0, wx.EXPAND | wx.BOTTOM, 5)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_bottom.Add(self.panel_left,  1, wx.EXPAND, 0)
        sizer_bottom.Add(self.panel_right, 0, 0, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_left.Add(self.vList,                  1, wx.EXPAND, 0)
        sizer_left.Add(self.text_ctrl_records, 0, wx.EXPAND, 0)
        self.panel_left.SetSizer(sizer_left)
        
        sizer_main.Add(self.panel_top,      0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.panel_bottom,   1, wx.EXPAND | wx.BOTTOM, 5)
        
        self.SetSizer(sizer_main)
        self.Layout()
        
    def __do_main(self):
        pub.sendMessage('student.selected')
        
    def displayData(self):          
        if gVar.form_id:     sql = self.f_filter_by_form()
        elif gVar.level:     sql = self.f_filter_by_level()
        elif gVar.school_id: sql = self.f_filter_by_school()
       
        else:
            sql ="SELECT s.id, s.name, sbf.rereg_status \
                    FROM students           s \
                    JOIN students_by_form sbf ON s.id = sbf.student_id \
                    JOIN forms              f ON f.id = sbf.form_id \
                   WHERE f.schYr = %d \
                   ORDER BY f.level , f.name" %(gVar.schYr, )
        
        res = fetch.DATA(sql)
        #rint sql, len(res)
        
        self.vList.SetItemMap(res)
        self.records = len(res)
        if self.records: txt = "Record 1/%d" % self.records
        else:            txt = "No Records"
        self.text_ctrl_records.SetValue(txt)
    
    def f_filter_by_form(self):
        sql ="SELECT s.id, s.name, sbf.rereg_status \
                FROM students           s \
                JOIN students_by_form sbf ON s.id = sbf.student_id \
                JOIN forms              f ON f.id = sbf.form_id \
               WHERE f.id = %d \
               ORDER BY f.level , f.name" %(gVar.form_id, )
        return sql
    
    def f_filter_by_level(self):
        sql ="SELECT s.id, s.name, sbf.rereg_status \
                    FROM students           s \
                    JOIN students_by_form sbf ON s.id = sbf.student_id \
                    JOIN forms              f ON f.id = sbf.form_id \
                   WHERE f.schYr = %d \
                     AND f.level =%d \
                   ORDER BY f.level , f.name" %(gVar.schYr, gVar.level )
        return sql
        
    def f_filter_by_school(self):
        sql ="SELECT s.id, s.name, sbf.rereg_status \
                    FROM students           s \
                    JOIN students_by_form sbf ON s.id = sbf.student_id \
                    JOIN forms              f ON f.id = sbf.form_id \
                   WHERE f.schYr = %d \
                     AND f.school_id =%d \
                   ORDER BY f.level , f.name" %(gVar.schYr, gVar.school_id )
        return sql

    def OnItemSelected(self, evt):
        student_id  = self.vList.GetSelectedID()
        index = self.vList.GetFirstSelected()
        gVar.student_id = int(self.vList.getColumnText(index, 0))
        
        txt = "Record %d/%d" % (index, self.records)
        self.text_ctrl_records.SetValue(txt)
        
        pub.sendMessage('student.selected')


    def OnDblClick(self,evt):
        self.OnRightClick(event)
        
    def OnRightClick(self, event):
        gVar.student_id = self.student_id  = self.vList.get_selected_id()

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnViewDetails, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnEditBookingDetails, id=self.popupID2)

        menu = wx.Menu()
        menu.Append(self.popupID1, "Student Details")
        menu.Append(self.popupID2, "Booking Details")

        self.PopupMenu(menu)
        menu.Destroy()
      