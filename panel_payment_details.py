import wx, gVar, fetch, loadCmb, datetime

from my_ctrls   import panel_buttons
from DateCtrl   import DateCtrl
from myListCtrl import VirtualList as vListCtrl

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from wx.lib.masked import NumCtrl

import DlgPayments

#---------------------------------------------------------------------------


class panel_payment_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_payments           = wx.StaticText(self, -1, "PAYMENTS")
        self.panel_payments           = wx.Panel(self, -1)
        self.label_details            = wx.StaticText(self, -1, "DETAILS")
        self.panel_payment_details    = wx.Panel(self, -1)
        self.panel_buttons            = panel_buttons(self, -1)
        
        self.listctrl_payments        = vListCtrl(self.panel_payments,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_payments_botttom   = wx.Panel( self.panel_payments, -1)
       
        self.txt_ctrl_pay_records     = wx.TextCtrl(self.panel_payments_botttom, -1, " ")
        self.num_ctrl_pay_total       = NumCtrl(self.panel_payments_botttom, -1)
        
        self.listctrl_details         = vListCtrl(self.panel_payment_details,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_details_botttom    = wx.Panel( self.panel_payment_details, -1)

        self.txt_ctrl_details_records = wx.TextCtrl(self.panel_details_botttom, -1, "")
        self.num_ctrl_details_total   = NumCtrl(self.panel_details_botttom, -1)
       
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnPaymentItemSelected, self.listctrl_payments)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDetailItemSelected,  self.listctrl_details)
 
        self.panel_buttons.new.Bind(wx.EVT_BUTTON,    self.OnNew,    self.panel_buttons.new )
        self.panel_buttons.edit.Bind(wx.EVT_BUTTON,   self.OnEdit,   self.panel_buttons.edit )
        self.panel_buttons.cancel.Bind(wx.EVT_BUTTON, self.OnCancel, self.panel_buttons.cancel )
        
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  self.panel_buttons.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.panel_buttons.save)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.panel_buttons.refresh )
        
        tc = [self.txt_ctrl_pay_records,
              self.num_ctrl_pay_total,
              self.txt_ctrl_details_records,
              self.num_ctrl_details_total ]
        
        for t in tc: t.SetEditable(False)
        self.__layout()
 
        #pub.subscribe(self.displayData, 'student_payments.studentselected')

        self.pay_records = 0
        self.detail_records = 0
        
        self.__properties()
        self.__layout()
        self.__do_main()
    
    def __properties(self):
        #self.panel_buttons.Hide()
        self.text_ctrls = (self.txt_ctrl_pay_records,
              self.num_ctrl_pay_total,
              self.txt_ctrl_details_records,
              self.num_ctrl_details_total)
        
        for t in self.text_ctrls:
            t.SetEditable(False)
            
        headings = (('index', 0), ('Recipt No',120), ('Date',120), ('Amount', 120, wx.LIST_FORMAT_RIGHT))#, ('name',100), ('name',100))
        self.listctrl_payments.SetColumns(headings)
        
        headings = (('index', 0), ('Item',220), ('Amount', 120, wx.LIST_FORMAT_RIGHT))#, ('name',100), ('name',100))
        self.listctrl_details.SetColumns(headings)
        
        self.SetMinSize((-1, 500))
        
    def __layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_payments        = wx.BoxSizer(wx.VERTICAL)
        sizer_payments_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details         = wx.BoxSizer(wx.VERTICAL)
        sizer_details_bottom  = wx.BoxSizer(wx.HORIZONTAL)

        sizer_payments.Add(self.listctrl_payments,      1, wx.EXPAND, 0)
        sizer_payments.Add(self.panel_payments_botttom, 0, wx.EXPAND, 0)
        self.panel_payments.SetSizer(sizer_payments)
        
        sizer_payments_bottom.Add(self.txt_ctrl_pay_records, 1, 0, 0)
        sizer_payments_bottom.Add(self.num_ctrl_pay_total,   0, 0, 0)
        self.panel_payments_botttom.SetSizer(sizer_payments_bottom)
        
        sizer_details.Add(self.listctrl_details,      1, wx.EXPAND, 0)
        sizer_details.Add(self.panel_details_botttom, 0, wx.EXPAND, 0)
        self.panel_payment_details.SetSizer(sizer_details)
        
        sizer_details_bottom.Add(self.txt_ctrl_details_records, 1, 0, 0)
        sizer_details_bottom.Add(self.num_ctrl_details_total,   0, 0, 0)
        self.panel_details_botttom.SetSizer(sizer_details_bottom)
        
        sizer_main.Add(self.label_payments, 0, 0, 0)
        sizer_main.Add(self.panel_payments, 1, wx.EXPAND, 0)
        sizer_main.Add(self.label_details,  0, 0, 0)
        sizer_main.Add(self.panel_payment_details,  1, wx.EXPAND | wx.BOTTOM, 10)
        sizer_main.Add(self.panel_buttons,  0, 0, 0)
        self.SetSizer(sizer_main)
      
        
    def __do_main(self):
        #rint'p_p_d > do_main'
        self.enableCtrls(False)
        
    def clearCtrls(self):
        pass
    
    def enableCtrls(self, flag=True):
        self.listctrl_details.Enable(flag)
        self.listctrl_payments.Enable(flag)
        for t in self.text_ctrls:
            t.SetEditable(flag)
            
    def disableCtrls(self):
        #rint'panel_payment_details > disableCtrls'
        self.enableCtrls(False)


    def OnNew(self, evt):
        dlg = DlgPayments.create(None)
        try:
            dlg.displayData(gVar.student_id)
            dlg.ShowModal()
            self.displayData(self.student_id)
        finally:
            dlg.Destroy()  
        
    def OnEdit(self, evt):
        #rint'edit'
        invoice_id = self.listctrl_payments.GetSelectedID()
        #rint'invoice_id', invoice_id
        if invoice_id:
            dlg = DlgPayments.create(None)
            try:
                #dlg.displayData(gVar.student_id)
                dlg.displayInvDetails(invoice_id)
                dlg.ShowModal()
                self.displayData(self.student_id)
            finally:
                dlg.Destroy() 
        
    def OnDelete(self, evt):
        pass
        #rint'psp OnDelete'
        
    def OnSave(self, evt):
        pass
        # self.GetParent().uklockdown()
        #rint'psp OnSave'
        
    def OnCancel(self, evt):
        #rint'ppd OnCancel'
        self.listctrl_payments.Enable()
        evt.Skip()
        
    def OnRefresh(self, evt):
        pass
        #rint'psp OnRefresh'  
        
    def displayData(self, student_id):
        #rint'panel_payment_details > displayData > student_id',student_id
        self.student_id = student_id
        sql = "SELECT i.id, i.ck_ref, \
          DATE_FORMAT(i.`date`,'%e %M %Y'), \
               FORMAT(i.amount, '#,###') \
                 FROM acc_invoices i "
        sql += "WHERE i.student_id = '%s' \
                  AND i.schYr= %d" % (student_id, gVar.schYr)

        myDict = fetch.DATA(sql)

        self.listctrl_payments.SetItemMap(myDict)
        self.listctrl_payments.Enable()
        self.listctrl_details.DeleteAllItems()
        self.pay_records = pay_records = len(myDict)
        
        if pay_records:
              txt = "Record: 1/%d" % pay_records
        else: txt = 'No Records'
        self.txt_ctrl_pay_records.SetValue(txt)
        
        sql = "SELECT SUM(ii.total_amount) \
                 FROM acc_invoices i \
                 JOIN acc_invoice_items ii ON ii.invoice_id = i.id \
                WHERE i.student_id = %d \
                  AND i.schYr= %d" % (gVar.student_id, gVar.schYr)
        
        total_amount = fetch.getDig(sql)
        self.num_ctrl_pay_total.SetValue(total_amount)
        
    def OnDetailItemSelected(self, evt):
        #rint'OnDetailItemSelected'
        rid   = self.listctrl_details.GetSelectedID()
        index = self.listctrl_details.GetFirstSelected()
        
    def OnPaymentItemSelected(self, evt):
        #rint'          OnPaymentItemSelected'
        pid   = self.listctrl_payments.GetSelectedID()
        index = self.listctrl_payments.GetFirstSelected()
        invoice_id = int(self.listctrl_payments.getColumnText(index, 0))
        
        sql = "SELECT id, item_name,  \
                      date_from, date_to, month_from, month_to, \
                      item_name, price, Format(total_amount,'#,###') AS  total_amount\
                 FROM acc_invoice_items \
                WHERE invoice_id=%d" % invoice_id  
        mylist = fetch.getAllDict(sql)
        
        if mylist:#self.pay_records:
              txt = "Record: %d/%d" % (index+1, len(mylist)) #self.pay_records)
              self.listctrl_details.Enable()
        else: txt = 'No Records'
        
        self.txt_ctrl_pay_records.SetValue(txt)
  
        index = 0
        myDict = {}
    
        for row in mylist:
            name_value = [index, ]
            # prepare name
            item_name =row['item_name']
            if item_name:
                name_value.append(item_name)
            # perpare value
            name_value.append(row['total_amount'])
            
            #name_value[0]     = index
            name_value        = tuple(name_value)
            
            myDict[index] = name_value
            index +=1
        
        self.listctrl_details.SetItemMap(myDict)
        
        self.detail_records = len(myDict)
        if myDict:
              txt = "Record: 1/%d" % self.detail_records
        else: txt = 'No Records'
        self.txt_ctrl_details_records.SetValue(txt)
        
        sql = "SELECT SUM(total_amount) \
                 FROM acc_invoice_items  \
                WHERE invoice_id = %d" % invoice_id 
        #rintsql
        self.num_ctrl_details_total.SetValue(fetch.getDig(sql))
        

