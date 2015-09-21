import wx, gVar, sys, fetch, loadCmb

import DlgProduct as DlgInvoiceItem
import DlgSelectMonthsPeriod
import DlgInvoicePreview


from DateCtrl import DateCtrl

from wx.lib.masked import NumCtrl  

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

student_id   = 0
NoInduk      = ''
student_name = ''
form_name    = ''
invoice_items = {}
invoice_date  = 'xxxx-xx-xx'
ck_ref  = 'xxxx-xxxx'

totals_size = (200, -1)
qnty_size   = ( 91, -1)
btn1_size   = ( 25, -1)


global_grand_total = 0


def create(parent):
    return DlgPayments(parent)

class panel_invoice_header(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.bitmap_button          = wx.BitmapButton(self, -1, wx.NullBitmap)
        
        self.panel_right            = wx.Panel(self, -1)
        self.label_sid              = wx.StaticText(self.panel_right, -1, "ID")
        self.text_ctrl_NoInduk      = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        self.label_s_name           = wx.StaticText(self.panel_right, -1, "Name")
        self.text_ctrl_student_name = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        self.label_s_form           = wx.StaticText(self.panel_right, -1, "Form")
        self.text_ctrl_student_form = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        
        self.panel_reciept_details  = wx.Panel(self, -1)
        self.label_ckref            = wx.StaticText(self.panel_right, -1, "Receipt No")
        self.text_ctrl_receipt_no   = wx.TextCtrl(  self.panel_right, -1, "")
        self.label_inv_date         = wx.StaticText(self.panel_right, -1, "Date")
        self.text_ctrl_receipt_date = wx.TextCtrl(  self.panel_right, -1, "")
        self.label_spy_tot1         = wx.StaticText(self.panel_right, -1, "Total")
        self.text_ctrl_amount       = NumCtrl(  self.panel_right, -1)
        self.label_39               = wx.StaticText(self.panel_right, -1, "-")
        self.text_ctrl_written      = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        
        self.label_spc1 = wx.StaticText(self.panel_right, -1, "")
        self.label_spc2 = wx.StaticText(self.panel_right, -1, "")
        
        self.do_layout()
        
        self.bitmap_button.SetMinSize((100, 120))
        self.text_ctrl_receipt_no.SetMinSize((200, -1))
        
    def do_layout(self):
        sizer_header  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_header_right  = wx.FlexGridSizer(4, 4, 5, 10)
        
        sizer_header.Add(self.bitmap_button, 0, wx.RIGHT, 10)
        sizer_header.Add(self.panel_right, 1, wx.BOTTOM | wx.EXPAND, 20)
        self.SetSizer(sizer_header)
        
        sizer_header_right.Add(self.label_sid,              0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_NoInduk,      0, 0, 0)
        
        sizer_header_right.Add(self.label_s_name,           0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_student_name, 0, wx.EXPAND, 0)
        
        sizer_header_right.Add(self.label_s_form,           0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_student_form, 0, 0, 0)
        
        sizer_header_right.Add(self.label_ckref,            0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_receipt_no,   0, 0, 0)
        
        sizer_header_right.Add(self.label_inv_date,         0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_receipt_date, 0, 0, 0)
        
        sizer_header_right.Add(self.label_spy_tot1,         0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_amount,       1, wx.EXPAND, 0)
        
        sizer_header_right.AddSpacer(0, 0, 0)
        sizer_header_right.AddSpacer(0, wx.EXPAND, 0)
        
        sizer_header_right.Add(self.label_39,               0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_written,      0, wx.EXPAND, 0)
        
        self.panel_right.SetSizer(sizer_header_right)
        sizer_header_right.AddGrowableCol(3)
        
    def display_header(self):
        self.text_ctrl_NoInduk.SetValue(NoInduk)
        self.text_ctrl_student_name.SetValue(student_name)
        self.text_ctrl_student_form.SetValue(form_name)
        self.text_ctrl_receipt_date.SetValue(invoice_date)
        self.text_ctrl_receipt_no.SetValue(ck_ref)
        

# ================================================

class panel_bus(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.monthFrom   = 0
        self.monthly_fee = 0
        
        self.button_remove           = wx.Button(self, -1, '-')
        self.text_ctrl_months        = NumCtrl(self, -1, value=1)
        self.text_ctrl_from          = wx.StaticText(self, -1, ' Bus service, from ')
        self.choice_bus_from         = wx.Choice(self, -1)
        self.text_ctrl_to            = wx.StaticText(self, -1, ' to ')
        self.choice_bus_to           = wx.Choice(self, -1)
        self.text_ctrl_bus_fee       = NumCtrl(self, -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_total_bus_fee = NumCtrl(self, -1, value=0)
        
        self.Bind(wx.EVT_CHOICE, self.OnBusMonthFrom, self.choice_bus_from)
        self.Bind(wx.EVT_CHOICE, self.OnBusMonthTo,   self.choice_bus_to)
        self.Bind(wx.EVT_BUTTON, self.OnRemove,       self.button_remove)
        
        self.__do_settings()
        self.__do_layout()
        
    def __do_settings(self):
        self.button_remove.SetMinSize(btn1_size)
        
        self.text_ctrl_months.SetMinSize(qnty_size)
        self.text_ctrl_months.SetMaxSize(qnty_size)
        self.text_ctrl_months.SetEditable(False)
        
        self.text_ctrl_months.SetMax(12)
        
        self.text_ctrl_bus_fee.SetEditable(False)
        self.text_ctrl_bus_fee.SetMaxSize(totals_size)
        
        self.text_ctrl_total_bus_fee.SetEditable(False)
        self.text_ctrl_total_bus_fee.SetSize(totals_size)
        self.text_ctrl_total_bus_fee.SetMaxSize(totals_size)
        
    def __do_layout(self):
        sizer_main =  wx.BoxSizer(wx.HORIZONTAL)
   
        sizer_main.Add(self.button_remove,        0, 0, 0)
        sizer_main.Add(self.text_ctrl_months,     0, wx.LEFT | wx.RIGHT, 5)
        sizer_main.Add(self.text_ctrl_from,       0, 0, 0)
        sizer_main.Add(self.choice_bus_from,      0, 0, 0)
        sizer_main.Add(self.text_ctrl_to,         0, 0, 0)
        sizer_main.Add(self.choice_bus_to,        0, 0, 0)
        sizer_main.AddSpacer((1, 0),              1, 0, 0)
        sizer_main.Add(self.text_ctrl_bus_fee,    0, 0, 0)
        sizer_main.Add(self.text_ctrl_total_bus_fee, 0, 0, 0)
        self.SetSizer(sizer_main)

    def displayData(self, student_id, product_id):
        #rint'panel bus fees: displayData'
        self.product_id = product_id
        self.monthly_bus_fee = fetch.bus_fee_monthly(student_id, gVar.schYr)
        lastMonthPaid = fetch.month_last_paid(student_id, gVar.schYr, 1)
        self.months = 1
        if lastMonthPaid:
            self.month_from = lastMonthPaid
        else:
            self.month_from = 1
        self.load_cmb_months(lastMonthPaid)
        self.month_to = self.month_from
        
        #if lastMonthPaid:
        #    txt = "%s" % fetch.monthName(lastMonthPaid)
            
        self.description = 'Bus service for %s' % fetch.cmbValue(self.choice_bus_from)
            
        fee = "{:,}".format(self.monthly_bus_fee)
        self.text_ctrl_bus_fee.SetValue(fee)
        self.calcTotal()
    
    def calcTotal(self):
        months  = self.text_ctrl_months.GetValue()
        self.bus_fee_total = self.monthly_bus_fee * months
        self.text_ctrl_total_bus_fee.SetValue(self.bus_fee_total)
        pub.sendMessage('inv.total_change')
        
    def getTotal(self):
        return self.bus_fee_total
    
    def load_cmb_months(self, min_month):
        loadCmb.schMonths(self.choice_bus_from, min_month)
        loadCmb.schMonths(self.choice_bus_to,   min_month)
        
    def OnBusMonthFrom(self, evt):
        min_month = fetch.cmbID(self.choice_bus_from)
        loadCmb.schMonths(self.choice_bus_to, min_month-1)
        self.bus_details_changed()
        
    def OnBusMonthTo(self, evt):
        self.bus_details_changed()
        
    def bus_details_changed(self):
        #rint'bus_details_changed'
        self.month_from = fetch.cmbID(self.choice_bus_from)
        self.month_to   = fetch.cmbID(self.choice_bus_to)
        self.months       = self.month_to - self.month_from + 1
        self.text_ctrl_months.SetValue(self.months)
        
        if self.months ==1:
            self.description = 'Bus service for %s' % fetch.cmbValue(self.choice_bus_from)
        else:
            self.description = 'Bus service from %s to %s' % (fetch.cmbValue(self.choice_bus_from),
                                                              fetch.cmbValue(self.choice_bus_to))
        self.calcTotal()
        
    def OnRemove(self, evt):
        gVar.widget_id = self.Id
        pub.sendMessage('remove.inv_widget')    
        
    def get_product_id(self):
        return self.product_id
    
    def getdata(self):
        bus_data  = (self.product_id,
                self.months,
                self.description,
                self.monthly_bus_fee,
                self.bus_fee_total,
                self.month_from,
                self.month_to
                )
        #rint'bus_data ', bus_data
        return bus_data


class panel_fees(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.monthFeeFrom = 0
        self.monthly_fee  = 0
        
        self.button_remove          = wx.Button(self, -1, '-')
        self.text_ctrl_months       = NumCtrl(self, -1, value=1)
        self.text_ctrl_description  = wx.TextCtrl(self, -1)
        self.text_ctrl_fee          = NumCtrl(self, -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_total_fees   = NumCtrl(self, -1, value=0)
        
        self.Bind(wx.EVT_TEXT,     self.OnMonthsChange, self.text_ctrl_months)
        self.Bind(wx.EVT_BUTTON, self.OnRemove,       self.button_remove)
        
        self.__do_settings()
        self.__do_layout()
        
        self.monthFeeFrom = 1
        
    def __do_settings(self):
        self.button_remove.SetMinSize(btn1_size)

        self.text_ctrl_months.SetMinSize(qnty_size)
        self.text_ctrl_months.SetMaxSize(qnty_size)
        self.text_ctrl_months.SetAllowNegative(False)
        self.text_ctrl_months.SetMax(12)
        
        self.text_ctrl_description.SetEditable(False)
        
        self.text_ctrl_fee.SetMaxSize(totals_size)
        self.text_ctrl_fee.SetEditable(False)
        
        self.text_ctrl_total_fees.SetMaxSize(totals_size)
        #self.text_ctrl_total_fees.SetMinSize(totals_size)
        self.text_ctrl_total_fees.SetEditable(False)
        
    def __do_layout(self):
        sizer_main =  wx.BoxSizer(wx.HORIZONTAL)
   
        sizer_main.Add(self.button_remove)
        sizer_main.Add(self.text_ctrl_months,      0, wx.LEFT | wx.RIGHT, 5)
        sizer_main.Add(self.text_ctrl_description, 1, 0, 0)
        sizer_main.AddSpacer((1, 0),               0, 0, 0)
        sizer_main.Add(self.text_ctrl_fee,         0, 0, 0)
        sizer_main.Add(self.text_ctrl_total_fees,  0, 0, 0)
        self.SetSizer(sizer_main)
          
        
    def displayData(self, student_id, product_id):
        #rint'-------------------fees ---------displayData-----------'
        self.month_from = 1
        #rint'self.monthFrom', self.month_from
        
        
        self.product_id  = product_id
        self.student_id  = student_id
        self.course_id   = fetch.courseID_forStudent(student_id)
        self.monthly_fee = fetch.fee_monthly(self.course_id, gVar.schYr)
        self.total_fee   = self.monthly_fee
        lastMonthPaid    = fetch.month_last_paid(student_id, gVar.schYr, 1)
        
        if lastMonthPaid:
            #rint' xxxxxxxxxxxxxx '
            self.month_from = lastMonthPaid + 1
        else:
            self.month_from = 1
            
        self.month_to = self.month_from
        
        txt = "months school fee for %s" % fetch.monthName(self.month_from)
        self.description = txt
        self.text_ctrl_description.SetValue(txt)
        self.text_ctrl_months.SetMax(13 - self.month_from)
  
        fee = "{:,}".format(self.monthly_fee)
        self.text_ctrl_fee.SetValue(fee)
        self.calcTotal()
        
    def OnMonthsChange(self, evt):
        if self.text_ctrl_months.GetValue() < 1:
            self.text_ctrl_months.SetValue(1)
        self.calcTotal()
        
    def calcTotal(self):
        self.months = self.text_ctrl_months.GetValue()
        self.month_to = self.month_from + self.months - 1
        if self.months == 12:
            self.total_fee = fetch.fee_yearly(self.course_id, gVar.schYr)
            self.description = 'School fee payment for whole year'
            self.text_ctrl_description.SetValue(self.description)
            
            self.text_ctrl_fee.Hide()
            fee = "{:,}".format(self.total_fee)
            self.text_ctrl_total_fees.SetValue(fee)
            
        else:
            self.text_ctrl_fee.Show()
            monthsMax = self.text_ctrl_months.GetMax()
            if self.months > monthsMax:
                self.months = monthsMax
                self.text_ctrl_months.SetValue(self.months)
                
            if self.months > 1:
                txt = "months school fee from %s till %s" % (fetch.monthName(self.month_from),
                                           fetch.monthName(self.month_from + self.months -1))
            else:
                txt = "months school fee for %s" % fetch.monthName(self.month_from)
            self.description = txt
            self.text_ctrl_description.SetValue(txt)
            
            self.total_fee = self.months * self.monthly_fee
            self.text_ctrl_total_fees.SetValue(self.total_fee )
            
        pub.sendMessage('inv.total_change')
        
    def getTotal(self):
        return self.total_fee
        

    def OnRemove(self, evt):
        gVar.widget_id = self.Id
        pub.sendMessage('remove.inv_widget')    
        
    def get_product_id(self):
        return self.product_id
    
    def getdata(self):
        fee_data = (self.product_id,
                self.months,
                self.description,
                self.monthly_fee,
                self.total_fee,
                self.month_from,
                self.month_to
                )
        #rint'fee data', fee_data
        return fee_data
 
class panel_item(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.button_remove          = wx.Button(self, -1, '-')
        self.text_ctrl_qnty         = NumCtrl(self,   -1, value = 1)
        self.text_ctrl_description  = wx.TextCtrl(self, -1)
        self.text_ctrl_price        = NumCtrl(self,   -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_total        = NumCtrl(self,   -1, value=0)
        
        self.Bind(wx.EVT_TEXT,   self.OnQntyChange, self.text_ctrl_qnty)
        self.Bind(wx.EVT_BUTTON, self.OnRemove,     self.button_remove)
        
        self.__do_settings()
        self.__do_layout()
        
    def __do_settings(self):
        self.button_remove.SetMinSize(btn1_size)
        
        self.text_ctrl_qnty.SetMinSize(qnty_size)
        self.text_ctrl_qnty.SetMaxSize(qnty_size)
        self.text_ctrl_qnty.SetMin(1)
        self.text_ctrl_qnty.SetAllowNegative(False)
        
        self.text_ctrl_price.SetMaxSize(totals_size)
        self.text_ctrl_price.SetEditable(False)
        
        self.text_ctrl_description.SetEditable(False)
        
        self.text_ctrl_total.SetMaxSize(totals_size)
        self.text_ctrl_total.SetEditable(False)
        
    def __do_layout(self):
        sizer_main =  wx.BoxSizer(wx.HORIZONTAL)
   
        sizer_main.Add(self.button_remove)
        sizer_main.Add(self.text_ctrl_qnty,        0, wx.LEFT | wx.RIGHT, 5)
        sizer_main.Add(self.text_ctrl_description, 1, 0, 0)
        sizer_main.AddSpacer((1, 0),               0, 0, 0)
        sizer_main.Add(self.text_ctrl_price,       0, 0, 0)
        sizer_main.Add(self.text_ctrl_total,       0, 0, 0)
        self.SetSizer(sizer_main)
        
    def displayData(self, product_id):
        self.product_id = product_id
        self.description, self.unit_price = fetch.product_details(product_id)
        self.qnty = 1
        self.text_ctrl_description.SetValue(self.description)
        
        price = "{:,}".format(self.unit_price)
        self.text_ctrl_price.SetValue(price)
        self.calcTotal()
        
    def OnQntyChange(self, evt):
        if self.text_ctrl_qnty.GetValue() < 1:
            self.text_ctrl_qnty.SetValue(1)
        self.calcTotal()
        
    def calcTotal(self):
        self.qnty = self.text_ctrl_qnty.GetValue()
        self.total_value = self.qnty * self.unit_price
        total = "{:,}".format(self.total_value)
        self.text_ctrl_total.SetValue(total)
        pub.sendMessage('inv.total_change')
        
    def getTotal(self):
        return self.total_value
        
    def OnRemove(self, evt):
        gVar.widget_id = self.Id
        pub.sendMessage('remove.inv_widget')    
        
    def get_product_id(self):
        return self.product_id
    
    def getdata(self):
        item_data = (self.product_id,
                self.qnty,
                self.description,
                self.unit_price,
                self.total_value,
                0,
                0
                )
        #rint'item_data ', item_data
        return item_data
    
        
class DlgPayments(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.SetMinSize((800, 550))
        
        self.panel_base             = wx.Panel(self, -1)
        
        self.panel_header           = panel_invoice_header(self.panel_base )
        self.static_line_1          = wx.StaticLine(self.panel_base , -1)
        self.panel_main             = wx.Panel(self.panel_base , -1)
        self.static_line_2          = wx.StaticLine(self.panel_base , -1)
        self.panel_save             = wx.Panel(self.panel_base , -1)
        
        self.panel_invoice_items    = wx.Panel(self.panel_main, -1, style = wx.BORDER_SIMPLE)
        self.panel_totals           = wx.Panel(self.panel_main, -1, style = wx.BORDER_SIMPLE)
        self.panel_select_product   = wx.Panel(self.panel_main, -1)
        
        self.label_total            = wx.StaticText(self.panel_totals,     -1, "-")
        self.text_ctrl_grid_total   = NumCtrl(self.panel_totals,    -1)
        
        self.choice_products        = wx.Choice(self.panel_select_product, -1, choices=[])
        self.button_new_product     = wx.Button(self.panel_select_product, -1, "...")
        self.button_add_to_grid     = wx.Button(self.panel_select_product, -1, "+")
        
        self.button_save            = wx.Button(self.panel_save, -1, "Save")
        self.button_print_save      = wx.Button(self.panel_save, -1, "Save & Print")
        self.button_cancel          = wx.Button(self.panel_save, -1, "Cancel")

        self.Bind(wx.EVT_BUTTON, self.OnSave,       self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnSavePrint,  self.button_print_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,     self.button_cancel)
        self.Bind(wx.EVT_BUTTON, self.OnAdd,        self.button_add_to_grid)
        self.Bind(wx.EVT_BUTTON, self.OnNewProduct, self.button_new_product)
        
        pub.subscribe(self.RemoveItem, 'remove.inv_widget')
        pub.subscribe(self.UpdateTotal, 'inv.total_change')
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.text_ctrl_grid_total.SetSize(totals_size)
        
        self.SetMinSize((950, 500))
        self.SetSize((950, 500))
        
        self.button_add_to_grid.SetMinSize(btn1_size)
        self.button_add_to_grid.SetMaxSize(btn1_size)
        
        self.button_new_product.SetMinSize(btn1_size)
        self.button_new_product.SetMaxSize(btn1_size)
        self.SetTitle("Payments")
        
    def __do_layout(self):
        sizer_frame    = wx.BoxSizer(wx.VERTICAL)
        sizer_base     = wx.BoxSizer(wx.VERTICAL)
        sizer_main     = wx.BoxSizer(wx.VERTICAL)
        sizer_items    = wx.BoxSizer(wx.VERTICAL)
        sizer_total    = wx.BoxSizer(wx.HORIZONTAL)      
        sizer_product  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_save     = wx.BoxSizer(wx.HORIZONTAL)
     
        self.sizer_items = sizer_items
        self.panel_invoice_items.SetSizer(sizer_items)
        
        sizer_product.Add(self.button_add_to_grid, 0, 0, 0)
        sizer_product.Add(self.choice_products,    1, wx.RIGHT, 20)
        sizer_product.Add(self.button_new_product, 0, 0, 0)
        self.panel_select_product.SetSizer(sizer_product)
      
        sizer_total.Add(self.label_total,          1, wx.TOP, 0)
        sizer_total.Add(self.text_ctrl_grid_total, 0, 0, 0)
        self.panel_totals.SetSizer(sizer_total)
    
        sizer_main.Add(self.panel_invoice_items,  1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_totals,         0, wx.EXPAND | wx.BOTTOM, 10)
        sizer_main.Add(self.panel_select_product, 0, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)
    
        sizer_save.AddSpacer((1,1), 1,0,0)
        sizer_save.Add(self.button_save,          0, 0, 0)
        sizer_save.Add(self.button_print_save,    0, wx.LEFT | wx.RIGHT, 10)
        sizer_save.Add(self.button_cancel,        0, 0, 0)
        sizer_save.AddSpacer((1,1), 1,0,0)
        self.panel_save.SetSizer(sizer_save)
        
        sizer_base.Add(self.panel_header,         0, wx.BOTTOM | wx.EXPAND, 0)
        sizer_base.Add(self.static_line_1,        0, wx.EXPAND, 0)
        sizer_base.Add(self.panel_main,           1, wx.EXPAND, 0)
        sizer_base.Add(self.static_line_2,        0, wx.EXPAND | wx.TOP, 5)
        sizer_base.Add(self.panel_save,           0, wx.EXPAND | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_base)
        
        sizer_frame.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer_frame)
        self.Layout()

    def __do_main(self):
        self.widget_dict={}
        self.product_id_list = []
        self.load_products()
        self.Center()
        
    def load_products(self):
        loadCmb.products(self.choice_products, self.product_id_list)
        
    def displayData(self, sid):
        """
        sql = "TRUNCATE acc_invoices"
        fetch.updateDB(sql)
        sql = "TRUNCATE acc_invoice_items"
        fetch.updateDB(sql)"""
        
        
        
        global student_id, NoInduk, student_name, form_name
        student_id = sid
        gVar.user_id = 1234
        NoInduk      = fetch.NoInduk(student_id, gVar.schYr)
        student_name = fetch.studentFullName(student_id)
        form_name    = fetch.formName(fetch.formID_forStudent(sid))
        
        self.ck_ref       = 'xxxx-xxx'
        self.inv_date     = '2015-12-1'
        self.grand_total  = 0
        
        self.panel_header.display_header()
        loadCmb.products(self.choice_products)
        
        inv_total    = 0
        self.invoice_details = {'amount':   inv_total,
                                'ck_ref':   self.ck_ref,
                                'date':     self.inv_date,
                                'schYr':    gVar.schYr,
                                'name':     student_name,
                                'NoInduk':  NoInduk,
                                'form_name':form_name}
        
        self.invoice_items = {}
        self.Layout
        
    def displayInvDetails(self, invoice_id):
        sql = "SELECT id, date, ck_ref, student_id, amount, schYr FROM acc_invoices WHERE id = %d" % invoice_id
        res = fetch.getOneDict(sql)
        #rintsql, res
        if not res: return
        
        invoice_date = res["date"]
        ck_ref       = res["ck_ref"]
        student_id   = res["student_id"]
        amount       = res["amount"]
        schYr        = res["schYr"]
        
        self.displayData(student_id)
        
        sql = "SELECT id, item_name,  \
                      date_from, date_to, month_from, month_to, \
                      item_name, price, total_amount\
                 FROM acc_invoice_items \
                WHERE invoice_id=%d" % invoice_id
        
        #rintsql
        
        mylist = fetch.getAllDict(sql)
        return
    
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
        
    def OnSave(self, evt):
        if self.post_invoice():
            self.Close()
        
    def OnSavePrint(self, evt):
        data = (self.invoice_details, self.invoice_items)

        dlg = DlgInvoicePreview.create(None)# , -1, "")
        try:
            dlg.displayPreview(data)
            if dlg.ShowModal():
                #rint'ok'
                self.post_invoice()
                self.Close()
            else:
                pass
                #rint'not ok'
        finally:
            #rint'finally'
            dlg.Destroy()
        # if print
        
    def post_invoice(self):
        #rint'post invoice'
        
        if not self.widget_dict:
            fetch.msg('Can not save - there are not items to record')
            return 0
        
        invoice_id = fetch.nextID('acc_invoices')

        sql = "INSERT INTO acc_invoices (date, ck_ref, amount, student_id, schYr, staff_id) \
               VALUES ('%s', '%s', %d, %d, %d, %d)" % (
                        self.inv_date, self.ck_ref, self.grand_total, student_id, gVar.schYr, gVar.user_id)
        print'fetch.updateDB(sql)', fetch.updateDB(sql)
        print self.inv_date, self.ck_ref, self.grand_total, student_id, gVar.schYr, gVar.user_id
        
        for key in self.widget_dict:
            product_id = key,
            p = self.widget_dict[key]
            product_id, qnty, description, unit_price, total_amount, month_from, month_to = p.getdata()
           
            if product_id == 1 or key == 3:
                sql = "INSERT INTO acc_invoice_items (\
                                    invoice_id, product_id, \
                                    item_name, qnty, \
                                    price, total_amount, \
                                    month_from, month_to) \
                            VALUES ( %d, %d, \
                                    '%s', %d, \
                                     %d,  %d, \
                                     %d, %d)" % (
                                    invoice_id, product_id, 
                                    description, qnty,
                                    unit_price, total_amount,
                                    month_from, month_to)
                                    #rint' bus or fee ', (
                                    #invoice_id, product_id, 
                                    #description, qnty,
                                    #unit_price, total_amount,
                                    #month_from, month_to), sql
         
            else:
                sql = "INSERT INTO acc_invoice_items (\
                                    invoice_id, product_id, item_name, \
                                    qnty,       price,      total_amount) \
                            VALUES (%d, %d, '%s', \
                                    %d, %d,  %d)" % (
                                    invoice_id, product_id, description,
                                    qnty, unit_price, total_amount)
                #rint'item ', sql
                
            fetch.updateDB(sql)
            
        return 1
        
    def UpdateTotal(self, ):
        self.grand_total = 0
        for key in self.widget_dict:
            p = self.widget_dict[key]
            self.grand_total += p.getTotal()
        #grand_total = "{:,}".format(grand_total)    
        self.text_ctrl_grid_total.SetValue(self.grand_total)
    
    def OnCancel(self, evt):
        self.Close()
        
    def RemoveItem(self):
        w_id = gVar.widget_id
        w = self.widget_dict.pop(w_id)
        self.product_id_list.remove(w.get_product_id())
        self.sizer_items.Remove(w)
        w.Destroy()
        self.UpdateTotal()
        self.load_products()
        self.Layout()
         
    def OnAdd(self, evt):
        product_id = fetch.cmbID(self.choice_products)
        #rint'OnAdd    product_id.GetSelection():', product_id
        
        if product_id in self.product_id_list:   return
        product_type_id = fetch.get_product_type_id(product_id)
        
        if product_type_id == 1: # school fee
            month_no = fetch.month_last_paid(student_id, gVar.schYr, 9)+1
            if month_no == 12:
                fetch.msg('month 12 already paid for')
                return
            else:
                p = self.addInvPanel(panel_fees, product_id)
                p.displayData(student_id, product_id)
                
        elif product_type_id == 9: # bus fee
            if fetch.month_last_paid(student_id, gVar.schYr, 9) == 12:
                fetch.msg('Already paid till end of year')
                return
            else:
                p = self.addInvPanel(panel_bus, product_id)  
                p.displayData(student_id, product_id)
        else:
            p = self.addInvPanel(panel_item, product_id)
            p.displayData(product_id)
            
        self.load_products()

    def addInvPanel(self, panel, product_id):
        p = panel(self.panel_invoice_items, -1)
        w_id = p.GetId()
        self.widget_dict[w_id] = p
        
        self.sizer_items.Add(p, 0, wx.EXPAND, 0)
        self.product_id_list.append(product_id)
        self.Layout()
        return p
        
    def fees_details_changed(self):
        pass
        #rint'fees_details_changed'

    def OnNewProduct(self, evt):
        dlg = DlgInvoiceItem.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            loadCmb.products(self.choice_products)
        finally:
            dlg.Destroy()
    
        

if __name__ == "__main__":
    gVar.schYr = 2014
    app = wx.App(None)
    dlg = create(None)
    try:
        dlg.displayInvDetails(1)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
    
    
    
