import wx, fetch, loadCmb, gVar, datetime

from myListCtrl import VirtualList as vListCtrl
from my_ctrls   import panel_buttons
from DateCtrl   import DateCtrl

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

#---------------------------------------------------------------------------

class panel_student_list(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_filter_schools      = wx.Panel(self, -1)
        self.checkbox_filter_by_school = wx.CheckBox(self.panel_filter_schools, -1, "School")
        self.choice_schools            = wx.Choice(self.panel_filter_schools,   -1, choices=[])
        self.checkbox_filter_by_course = wx.CheckBox(self.panel_filter_schools, -1, "Courses")
        self.choice_courses            = wx.Choice(self.panel_filter_schools,   -1, choices=[])
        
        self.vList = vListCtrl(self, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        self.text_ctrl_record_count = wx.TextCtrl(self, -1, '')
          
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
        
        self.Bind(wx.EVT_CHOICE,   self.OnSelectSchool, self.choice_schools)
        self.Bind(wx.EVT_CHOICE,   self.OnSelectCourse, self.choice_courses)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckSchool, self.checkbox_filter_by_school)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckCourse, self.checkbox_filter_by_course)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.checkbox_filter_by_school.SetValue(False)
        self.choice_schools.SetMinSize((150,  -1))
        self.choice_courses.SetMinSize((200, -1))
        self.choice_courses.Hide()

    def __do_layout(self):
        sizer_main   = wx.BoxSizer( wx.VERTICAL)
        sizer_filter = wx.BoxSizer( wx.HORIZONTAL)
        
        sizer_filter.Add(self.checkbox_filter_by_school, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_schools,            0, wx.LEFT, 5)
        sizer_filter.Add(self.checkbox_filter_by_course, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_courses,            0, wx.LEFT, 5)
        self.panel_filter_schools.SetSizer(sizer_filter)
        
        sizer_main.Add(self.panel_filter_schools,   0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.vList,                  1, wx.EXPAND, 0)
        sizer_main.Add(self.text_ctrl_record_count, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        
    def __do_main(self):
        self.OnCheckSchool(wx.Event)
        headings = (('id',0),
                    ('Registration Name',200),
                    ('Course',100)) 
        self.vList.SetColumns(headings)
        
    def displayData(self):
        ##rint'resistration_payments ---------------displayData--'
        
        sql = "SELECT s.id, s.name, c.name \
                 FROM students s \
                 JOIN acc_invoices i ON  s.id = i.student_id \
                 JOIN courses      c ON c.id = s.register_course_id  \
                WHERE s.register_schYr = %d " % (gVar.schYr,)
        """
        sql = "SELECT s.id, s.name \
                 FROM students s \
                WHERE s.register_schYr = %d " % (gVar.schYr,)"""

        if self.checkbox_filter_by_course.GetValue():
            ##rint'filter by course'
            course_id = fetch.cmbID(self.choice_courses)
            sql = "%s AND c.id = %d" % (sql,  course_id)
        
        elif self.checkbox_filter_by_school.GetValue():
            ##rint'filter by school'
            school_id = fetch.cmbID(self.choice_schools)
            sql = "%s AND c.school_id = %d" % (sql,  school_id)
            
        ##rintsql 
        res = fetch.DATA(sql)
    
        self.vList.SetItemMap(res)
        self.records = len(res)
        if self.records:
            txt = "Record 1/%d" % self.records
        else:
            txt = "No Records"
        self.text_ctrl_record_count.SetValue(txt)
        
    def OnSelectSchool(self, evt):
        ##rint'OnSelectSchool'
        
        self.loadCourses()
        self.displayData()
    
    def OnSelectCourse(self, evt):
        self.displayData()
    
    def OnCheckSchool(self, evt):
        if self.checkbox_filter_by_school.GetValue():
            sql = "SELECT id, school_type \
                     FROM schools \
                    WHERE isCK = 1"
            loadCmb.gen(self.choice_schools, sql)
            
            self.loadCourses()
        
            self.choice_schools.Show()
            self.checkbox_filter_by_course.Show()
            if self.checkbox_filter_by_course.GetValue():
                self.choice_courses.Show()
        
        else:
            self.choice_schools.Clear()
            self.checkbox_filter_by_course.Hide()
            self.choice_courses.Hide()
            self.choice_schools.Hide()
            
        self.Layout()
        self.displayData()
        
    def loadCourses(self):
        ##rint'loadCourses'
        school_id = fetch.cmbID(self.choice_schools)
        sql = "SELECT c.id, c.name \
                 FROM courses c \
                 JOIN courses_by_year cby ON cby.course_id = c.id \
                WHERE c.school_id = %d \
                  AND cby.schYr = %d" % (school_id, gVar.schYr)
        ##rintsql
        loadCmb.gen(self.choice_courses, sql)
    
    def OnCheckCourse(self, evt):
        if self.checkbox_filter_by_course.GetValue():
            self.choice_courses.Show()
            self.loadCourses()
        else:
            self.choice_courses.Hide()
        self.Layout()
        self.displayData()
 
    def OnItemSelected(self, evt):
        student_id  = self.vList.GetSelectedID()
        index = self.vList.GetFirstSelected()
        gVar.NoInduk = self.vList.getColumnText(index, 1)
        
        txt = "Record %d/%d" % (index, self.records)
        self.text_ctrl_record_count.SetValue(txt)
        
        pub.sendMessage('registrationpayments.studentselected')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        





class payment_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_payments = wx.StaticText(self, -1, "PAYMENTS")
        self.panel_payments = wx.Panel(self, -1)
        self.label_details  = wx.StaticText(self, -1, "DETAILS")
        self.panel_details  = wx.Panel(self, -1)
        self.panel_buttons  = panel_buttons(self, -1)
        
        self.payments_list          = vListCtrl(self.panel_payments,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_payments_botttom = wx.Panel( self.panel_payments, -1)
       
        self.txt_ctrl_pay_records  = wx.TextCtrl(self.panel_payments_botttom, -1, " ")
        self.txt_ctrl_pay_total    = wx.TextCtrl(self.panel_payments_botttom, -1, " ")
        
        self.panel_details_botttom = wx.Panel( self.panel_details, -1)
        self.label_recipt          = wx.StaticText(self.panel_details_botttom, -1, "Recipt No.")
        self.txt_ctrl_details_records = wx.TextCtrl(self.panel_details_botttom, -1, "")
        self.txt_ctrl_details_total   = wx.TextCtrl(self.panel_details_botttom, -1, "")
        
        self.panel_buttons.new.Bind(wx.EVT_BUTTON, self.OnNew,       self.panel_buttons.new )
        self.panel_buttons.edit.Bind(wx.EVT_BUTTON, self.OnEdit,     self.panel_buttons.edit )
        self.panel_buttons.cancel.Bind(wx.EVT_BUTTON, self.OnCancel, self.panel_buttons.cancel )
        
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  self.panel_buttons.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.panel_buttons.save)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.panel_buttons.refresh )
        
       
        pub.subscribe(self.displayData, 'registrationpayments.studentselected')
        
        
        
        tc = (self.txt_ctrl_pay_records,
              self.txt_ctrl_pay_total,
              self.txt_ctrl_details_records,
              self.txt_ctrl_details_total)
        
        for t in tc: t.SetEditable(False)
        self.__layout()
        
        
    
        
    def OnNew(self, evt):
        #rint'ppr OnNew'
        evt.Skip()
        
    def OnEdit(self, evt):
        #rint'ppr OnEdit'
        evt.Skip()
        
    def OnDelete(self, evt):
        evt.Skip()
        #rint'ppr OnDelete'
        
    def OnSave(self, evt):
        evt.Skip()
        #rint'ppr OnSave'
        
    def OnCancel(self, evt):
        #rint'ppr OnCancel'
        evt.Skip()
        
    def OnRefresh(self, evt):
        evt.Skip()
        #rint'ppr OnRefresh'  
          
        
    def __layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_payments        = wx.BoxSizer(wx.VERTICAL)
        sizer_payments_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details         = wx.BoxSizer(wx.VERTICAL)
        
        sizer_payments_bottom.Add(self.txt_ctrl_pay_records, 1, 0, 0)
        sizer_payments_bottom.Add(self.txt_ctrl_pay_total,   0, 0, 0)
        self.panel_payments_botttom.SetSizer(sizer_payments_bottom)
        
        sizer_payments.Add(self.payments_list,          1, 0, 0)
        sizer_payments.Add(self.panel_payments_botttom, 0, 0, 0)
        self.panel_payments.SetSizer(sizer_payments)
        
        sizer_details.Add(self.label_recipt,          1, wx.EXPAND, 0)
        sizer_details.Add(self.txt_ctrl_details_records, 1, 0, 0)
        sizer_details.Add(self.txt_ctrl_details_total,   0, 0, 0)
        self.panel_details.SetSizer(sizer_details)
        
        sizer_main.Add(self.label_payments, 0, 0, 0)
        sizer_main.Add(self.panel_payments, 1, 0, 0)
        sizer_main.Add(self.label_details,  0, 0, 0)
        sizer_main.Add(self.panel_details,  1, 0, 0)
        sizer_main.Add(self.panel_buttons,  0, 0, 0)
        self.SetSizer(sizer_main)
        
    def displayData(self):
        pass
        #rint' reg pay - details'
        







class panel_registration_payments(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.panel_student_list     = panel_student_list(self, -1)
        self.panel_details          = payment_details(self, -1)
 
        self.__set_properties() 
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_main  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_main.Add(self.panel_student_list, 1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_details,      0, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.displayData()
        
    def displayData(self):
        return
        
    def lockdown(self):
        self.panel_student_list.Enable(False)
    
    def unlockdown(self):
        self.panel_student_list.Enable()
