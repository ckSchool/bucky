import wx, datetime

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

from ctrl.my_ctrls   import panel_buttons
from ctrl.myListCtrl import VirtualList as vListCtrl

from ctrl.DateCtrl import DateCtrl

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
        self.checkbox_filter_by_form   = wx.CheckBox(self.panel_filter_schools, -1, "Forms")
        self.choice_forms              = wx.Choice(self.panel_filter_schools,   -1, choices=[])
        
        self.vList                     = vListCtrl(self, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        self.text_ctrl_record_count    = wx.TextCtrl(self, -1, '')
          
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
        
        self.Bind(wx.EVT_CHOICE,   self.OnSelectSchool, self.choice_schools)
        self.Bind(wx.EVT_CHOICE,   self.OnSelectForm, self.choice_forms)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckSchool, self.checkbox_filter_by_school)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckCourse, self.checkbox_filter_by_form)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.checkbox_filter_by_school.SetValue(True)
        self.choice_schools.SetMinSize((150,  -1))
        self.choice_forms.SetMinSize((200, -1))

    def __do_layout(self):
        sizer_main   = wx.BoxSizer( wx.VERTICAL)
        sizer_filter = wx.BoxSizer( wx.HORIZONTAL)
        sizer_date   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_filter.Add(self.checkbox_filter_by_school, 0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_schools,            0, wx.LEFT, 5)
        sizer_filter.Add(self.checkbox_filter_by_form,   0, wx.LEFT | wx.ALIGN_BOTTOM, 5)
        sizer_filter.Add(self.choice_forms,              0, wx.LEFT, 5)
        self.panel_filter_schools.SetSizer(sizer_filter)
        
        sizer_main.Add(self.panel_filter_schools,   0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.vList,                  1, wx.EXPAND, 0)
        sizer_main.Add(self.text_ctrl_record_count, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        
    def __do_main(self):
        headings = (('id',0),
                        ('student_id',100),
                        ('Name',100),
                        ('Form',100))    
        self.vList.SetColumns(headings)
        
        sql = "SELECT id, name \
                 FROM schools \
                WHERE isCK = 1"
        loadCmb.schDiv(self.choice_schools) #, sql)
        
        self.loadForms()
        self.displayData()
 
    def displayData(self):
        #rint'panel_student_payments ---------------- : displayData'
        
        sql = "SELECT s.id, s.name, f.name \
                 FROM students s \
                 JOIN students_by_form sbf ON s.id = sbf.student_id \
                 JOIN forms              f ON f.id = sbf.form_id  \
                WHERE f.schYr = %d " % (gVar.schYr,)
        #rint sql
        if self.checkbox_filter_by_form.GetValue():
            #rint 'filter by form'
            form_id = fetch.cmbID(self.choice_forms)
            sql = "%s AND f.id = %d" % (sql,  form_id)
        
        elif self.checkbox_filter_by_school.GetValue():
            #rint 'filter by school'
            school_id = fetch.cmbID(self.choice_schools)
            sql = "%s AND f.school_id = %d" % (sql,  school_id)
        
        #rint sql
            
        res = fetch.DATA(sql)
    
        self.vList.SetItemMap(res)
        self.records = len(res)
        if self.records:
            txt = "Record 1/%d" % self.records
        else:
            txt = "No Records"
        self.text_ctrl_record_count.SetValue(txt)
        
    def OnSelectSchool(self, evt):
        school_id = fetch.cmbID(self.choice_schools)
        sql = "SELECT id, name \
                 FROM forms \
                WHERE school_id = %d \
                  AND schYr = %d" % (school_id, gVar.schYr)
        loadCmb.gen(self.choice_forms, sql)
        self.displayData()
    
    def OnSelectForm(self, evt):
        #rint'OnSelectForm'
        self.displayData()
    
    def OnCheckSchool(self, evt):
        if self.checkbox_filter_by_school.GetValue():
            self.choice_schools.Show()
            self.checkbox_filter_by_form.Show()
            if self.checkbox_filter_by_form.GetValue():
                self.choice_forms.Show()
        
        else:
            #self.choice_schools.Clear()
            self.checkbox_filter_by_form.Hide()
            self.choice_forms.Hide()
            self.choice_schools.Hide()
            
        self.Layout()
        self.displayData()
        
    def loadForms(self):
        school_id = fetch.cmbID(self.choice_schools)
        """sql = "SELECT id, name \
                 FROM forms \
                WHERE school_id = %d \
                  AND schYr =%d" % (school_id, gVar.schYr)"""
        loadCmb.forms_forSchool(self.choice_forms, school_id)
        #loadCmb.gen(self.choice_forms, sql)
    
    def OnCheckCourse(self, evt):
        #rint'OnCheckCourse'
        if self.checkbox_filter_by_form.GetValue():
            self.choice_forms.Show()
            self.loadForms()
        else:
            self.choice_forms.Hide()
        self.Layout()
        self.displayData()

    def OnItemSelected(self, evt):
        #rint'OnItemSelected'
        student_id   = self.vList.GetSelectedID()
        index        = self.vList.GetFirstSelected()
        gVar.student_id = self.vList.getColumnText(index, 1)
        
        txt = "Record %d/%d" % (index, self.records)
        self.text_ctrl_record_count.SetValue(txt)
        
        pub.sendMessage('student_payments.studentselected')












class payment_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_payments = wx.StaticText(self, -1, "PAYMENTS")
        self.panel_payments = wx.Panel(self, -1)
        self.label_details  = wx.StaticText(self, -1, "DETAILS")
        self.panel_payment_details  = wx.Panel(self, -1)
        self.panel_buttons  = panel_buttons(self, -1)
        
        self.payments_list          = vListCtrl(self.panel_payments,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_payments_botttom = wx.Panel( self.panel_payments, -1)
       
        self.txt_ctrl_pay_records  = wx.TextCtrl(self.panel_payments_botttom, -1, " ")
        self.txt_ctrl_pay_total    = wx.TextCtrl(self.panel_payments_botttom, -1, "", style=wx.TE_RIGHT)
        
        self.details_list          = vListCtrl(self.panel_payment_details,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_details_botttom = wx.Panel( self.panel_payment_details, -1)
        
        self.txt_ctrl_details_records = wx.TextCtrl(self.panel_details_botttom, -1, "")
        self.txt_ctrl_details_total   = wx.TextCtrl(self.panel_details_botttom, -1, "", style=wx.TE_RIGHT)
       
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnPaymentItemSelected, self.payments_list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDetailItemSelected,  self.details_list)
 
        self.panel_buttons.new.Bind(wx.EVT_BUTTON,    self.OnNew,    self.panel_buttons.new )
        self.panel_buttons.edit.Bind(wx.EVT_BUTTON,   self.OnEdit,   self.panel_buttons.edit )
        self.panel_buttons.cancel.Bind(wx.EVT_BUTTON, self.OnCancel, self.panel_buttons.cancel )
        
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  self.panel_buttons.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.panel_buttons.save)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.panel_buttons.refresh )
        
        tc = [self.txt_ctrl_pay_records,
              self.txt_ctrl_pay_total,
              self.txt_ctrl_details_records,
              self.txt_ctrl_details_total ]
        
        for t in tc: t.SetEditable(False)
        self.__layout()
 
        pub.subscribe(self.displayData, 'student_payments.studentselected')

        self.pay_records = 0
        self.detail_records = 0
        
        self.__properties()
        self.__layout()
    
    def __properties(self):
        self.text_ctrls = (self.txt_ctrl_pay_records,
              self.txt_ctrl_pay_total,
              self.txt_ctrl_details_records,
              self.txt_ctrl_details_total)
        
        for t in self.text_ctrls:
            t.SetEditable(False)
            
        headings = (('index', 0), ('Recipt No',120), ('Date',120), ('Amount', 120, wx.LIST_FORMAT_RIGHT))#, ('name',100), ('name',100))
        self.payments_list.SetColumns(headings)
        
        headings = (('index', 0), ('Item',220), ('Amount', 120, wx.LIST_FORMAT_RIGHT))#, ('name',100), ('name',100))
        self.details_list.SetColumns(headings)
        
    def __layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_payments        = wx.BoxSizer(wx.VERTICAL)
        sizer_payments_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details         = wx.BoxSizer(wx.VERTICAL)
        sizer_details_bottom  = wx.BoxSizer(wx.HORIZONTAL)

        sizer_payments.Add(self.payments_list,          1, wx.EXPAND, 0)
        sizer_payments.Add(self.panel_payments_botttom, 0, wx.EXPAND, 0)
        self.panel_payments.SetSizer(sizer_payments)
        
        sizer_payments_bottom.Add(self.txt_ctrl_pay_records, 1, 0, 0)
        sizer_payments_bottom.Add(self.txt_ctrl_pay_total,   0, 0, 0)
        self.panel_payments_botttom.SetSizer(sizer_payments_bottom)
        
        sizer_details.Add(self.details_list,          1, wx.EXPAND, 0)
        sizer_details.Add(self.panel_details_botttom, 0, wx.EXPAND, 0)
        self.panel_payment_details.SetSizer(sizer_details)
        
        sizer_details_bottom.Add(self.txt_ctrl_details_records, 1, 0, 0)
        sizer_details_bottom.Add(self.txt_ctrl_details_total,   0, 0, 0)
        self.panel_details_botttom.SetSizer(sizer_details_bottom)
        
        sizer_main.Add(self.label_payments, 0, 0, 0)
        sizer_main.Add(self.panel_payments, 1, wx.EXPAND, 0)
        sizer_main.Add(self.label_details,  0, 0, 0)
        sizer_main.Add(self.panel_payment_details,  1, wx.EXPAND | wx.BOTTOM, 10)
        sizer_main.Add(self.panel_buttons,  0, 0, 0)
        self.SetSizer(sizer_main)

    def OnNew(self, evt):
        #rint'psp OnNew'
        self.GetParent().lockdown()
        evt.Skip()
        
    def OnEdit(self, evt):
        #rint'edit'
        sid = self.payments_list.GetId_firstSelected()
        ##rint'sid',sid
        if sid>0:
            self.payments_list.Enable(False)
            self.GetParent().lockdown()
            evt.Skip()
        
    def OnDelete(self, evt):
        pass
        #rint'psp OnDelete'
        
    def OnSave(self, evt):
        self.GetParent().uklockdown()
        #rint'psp OnSave'
        
    def OnCancel(self, evt):
        #rint'psp OnCancel'
        self.GetParent().uklockdown()
        self.payments_list.Enable()
        evt.Skip()
        
    def OnRefresh(self, evt):
        pass
        #rint'psp OnRefresh'  
        
    def displayData(self):
        pass
        sql = "SELECT acc_invoices.ck_ref, \
                        Format(invoices.date, 'DD-MM-YYYY'), \
                        Format(int(invoice_items.amount),'#,###') \
                 FROM invoices i \
                 JOIN invoice_items ii ON i.ck_ref = ii.ck_ref \
                WHERE i.student_id = '%s' \
                  AND i.schYr= %d" % (gVar.student_id, gVar.schYr)
        
        myDict = fetch.DATA_STR(sql)
        self.payments_list.SetItemMap(myDict)
        
        self.pay_records = pay_records = len(myDict)
        
        if pay_records:
              txt = "Record: 1/%d" % pay_records
        else: txt = 'No Records'
        self.txt_ctrl_pay_records.SetValue(txt)
        
        sql = "SELECT Format(int(SUM(invoice_items.amount)),'#,###') \
                 FROM invoices i \
                 JOIN invoice_items ii ON i.ck_ref = ii.ck_ref \
                WHERE i.student_id = '%s' \
                  AND i.schYr= %d" % (gVar.student_id, gVar.schYr)

        res = fetch.getStr(sql)
        self.txt_ctrl_pay_total.SetValue(res)
        
    def OnDetailItemSelected(self, evt):
        index = self.details_list.GetFirstSelected()
        if self.detail_records:
              txt = "Record: %d/%d" % (index+1, self.detail_records)
        else: txt = 'No Records'
        self.txt_ctrl_details_records.SetValue(txt)
        
    def OnPaymentItemSelected(self, evt):
        pid   = self.payments_list.GetSelectedID()
        index = self.payments_list.GetFirstSelected()
        reciptNo = self.payments_list.getColumnText(index, 1)
        
        if self.pay_records:
              txt = "Record: %d/%d" % (index+1, self.pay_records)
        else: txt = 'No Records'
        self.txt_ctrl_pay_records.SetValue(txt)
        
        sql = "SELECT ii.product_id,  ii.name,    ii.other, \
                      ii.date_from,   ii.date_to, ii.month_from, pd.month_to, \
                      ii.price, Format(int(pd.amount),'#,###') AS amount, ii.item_name \
                 FROM invoices  i \
                 JOIN invoice_items ii ON i.id = ii.invoice_id \
                WHERE i.ck_ref='%s'" % reciptNo  # Format(int(invoice_items.amount),'#,###')

        mylist = fetch.getAllDict(sql)
        
        index = 0
        myDict = {}
    
        for row in mylist:
            name_value = [index, ]
            # prepare name
            item_name =row['item_name']
            if item_name:
                name_value.append(item_name)
            # perpare value
            name_value.append(row['amount'])
            
            #name_value[0]     = index
            name_value        = tuple(name_value)
            
            myDict[index] = name_value
            index +=1
        
        self.details_list.SetItemMap(myDict)
        
        self.detail_records = len(myDict)
        if myDict:
              txt = "Record: 1/%d" % self.detail_records
        else: txt = 'No Records'
        self.txt_ctrl_details_records.SetValue(txt)
        
        sql = "SELECT Format(SUM(amount),'#,###') \
                 FROM invoice_items  \
                WHERE ck_ref='%s'" % reciptNo 
        #rintsql
        self.txt_ctrl_details_total.SetValue(str(fetch.getStr(sql)))
        






class panel_student_payments(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_student_list     = panel_student_list(self, -1)#scrolled.ScrolledPanel(self, -1, style=wx.EXPAND)
        self.panel_details          = payment_details(self, -1)
 
        self.pp = self.GetParent().GetParent()
        self.__set_properties() 
        self.__do_layout()
        self.__do_main()
        
    def lockdown(self):
        self.panel_student_list.Enable(False)
        self.pp.panel_top.Enable(False)
        
        
        
    def uklockdown(self):
        self.panel_student_list.Enable()
        self.pp.panel_top.Enable()
        

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_main  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.panel_student_list, 1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_details,      0, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.panel_student_list.displayData()
        
    def displayData(self):
        #rint'panel_student_payments -- displayData'
        self.panel_student_list.displayData()
        
        
        
        
        
        


