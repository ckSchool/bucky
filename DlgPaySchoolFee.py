import wx, gVar, sys, fetch, loadCmb

import DlgSelectMonthsPeriod

from wx.lib import masked


# -------------------------------------------------------------------

def create(parent):
    return DlgPaySchoolFee(parent)


class DlgPaySchoolFee(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE 
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base = wx.Panel(self, -1)
        self.panel_top         = wx.Panel(self.panel_base, -1)
        self.panel_save_cancel = wx.Panel(self.panel_base, -1)
        self.panel_rereg       = wx.Panel(self.panel_base, -1)
        
        self.chkbox_rereg        = wx.CheckBox(self.panel_rereg, -1, 'Re-register', style = wx.ALIGN_RIGHT)
        self.panel_ctrls_rereg   = wx.Panel(self.panel_rereg, -1)
        
        
        self.choice_rereg_course   = wx.Choice(self.panel_ctrls_rereg,      -1, choices=['a','b','c'])
        self.text_ctrl_rereg       = masked.NumCtrl(self.panel_ctrls_rereg, -1, value=0)
        #self.text_ctrl_rereg_fee   = wx.TextCtrl(self.panel_ctrls_rereg, -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_rereg_total = masked.NumCtrl(self.panel_ctrls_rereg, -1, value=0)
        
        self.text_ctrl_months        = masked.NumCtrl(self.panel_top, -1, value=1)
        self.label_fee_sd            = wx.StaticText(self.panel_top, -1,  'month')
        self.text_ctrl_fee_description = wx.TextCtrl(self.panel_top, -1)
        self.text_ctrl_monthly_fee   = wx.TextCtrl(self.panel_top, -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_total_fees    = masked.NumCtrl(self.panel_top, -1, value=0)
    
        self.static_line_1           = wx.StaticLine(self.panel_base, -1)
        
        self.button_save             = wx.Button(self.panel_save_cancel, -1, "Save")
        self.button_cancel           = wx.Button(self.panel_save_cancel, -1, "Cancel")
    
        self.Bind(wx.EVT_CHOICE,   self,OnSelectcourse, self.choice_rereg_course)
        self.Bind(wx.EVT_CHECKBOX, self.OnChkRereg,     self.chkbox_rereg)
        self.Bind(wx.EVT_TEXT,     self.OnMonthsChange, self.text_ctrl_months)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,         self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnCancel,       self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()
        
              
    def __set_properties(self):
        self.panel_rereg.SetMinSize((-1, 30))
        self.text_ctrl_rereg.SetAllowNegative(False)
        self.text_ctrl_total_fees.SetAllowNegative(False)
        self.text_ctrl_total_fees.SetEditable(False)
        self.text_ctrl_monthly_fee.SetEditable(False)
        self.text_ctrl_fee_description.SetEditable(False)
        self.text_ctrl_months.SetMax(12)
        self.panel_base.SetMinSize((700, 111))
        size = (141,-1)
        self.text_ctrl_months.SetMinSize((50,-1))
        self.choice_rereg_course.SetMinSize((200,23))
        self.OnChkRereg(wx.Event)
        self.SetTitle("Pay School Fee")

    def __do_layout(self):
        sizer_base        = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main        = wx.BoxSizer(wx.VERTICAL)
        
        sizer_top         = wx.BoxSizer(wx.HORIZONTAL)
        sizer_save_cancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_rereg  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ctrls_rereg = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_ctrls_rereg.Add(self.choice_rereg_course, 0, wx.LEFT, 30)
        sizer_ctrls_rereg.AddSpacer((0, 0),             1, wx.EXPAND, 0)
        sizer_ctrls_rereg.Add(self.text_ctrl_rereg,     1, 0, 0)
        #sizer_ctrls_rereg.Add(self.text_ctrl_rereg_fee, 0, 0, 0)
        sizer_ctrls_rereg.Add(self.text_ctrl_rereg_total, 0, 0, 0)
        
        self.panel_ctrls_rereg.SetSizer(sizer_ctrls_rereg)
        
        sizer_rereg.Add(self.chkbox_rereg,       0, wx.ALIGN_CENTER_VERTICAL,0)
        sizer_rereg.Add(self.panel_ctrls_rereg, 1, 0,0)
        self.panel_rereg.SetSizer(sizer_rereg)
        
        sizer_top.Add(self.text_ctrl_months,          0, wx.RIGHT, 5)
        sizer_top.Add(self.label_fee_sd,              0, wx.RIGHT, 15)
        sizer_top.Add(self.text_ctrl_fee_description, 1, 0,0)
        sizer_top.Add(self.text_ctrl_monthly_fee,     0, 0,0)
        sizer_top.Add(self.text_ctrl_total_fees,      0,wx.ALIGN_RIGHT,0)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_save_cancel.Add(self.button_save,       0, 0, 0)
        sizer_save_cancel.Add(self.button_cancel,     0, 0, 0)
        self.panel_save_cancel.SetSizer(sizer_save_cancel)
        
        sizer_main.Add(self.panel_top,         0, wx.BOTTOM | wx.EXPAND, 0)
        sizer_main.Add(self.panel_rereg,       0, wx.BOTTOM | wx.TOP | wx.EXPAND, 0)
        sizer_main.Add(self.static_line_1,     0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        sizer_main.Add(self.panel_save_cancel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Center()
    
    def displayData(self, student_id):
        loadCmb.courses_forYear(self.choice_rereg_course, gVar.schYr)
        
        self.student_id = student_id
        #rint'displayData', student_id
        lastMonthPaid = self.lastMonthPaid()
        
        if lastMonthPaid==12:
            self.panel_rereg.Show()
            self.panel_fees.Hide()
            
        else:
            self.monthFrom = lastMonthPaid + 1
            if lastMonthPaid:
                txt = "%s" % fetch.monthName(self.monthFrom)
                self.text_ctrl_fee_description.SetValue(txt)
                self.text_ctrl_months.SetMax(12-lastMonthPaid)
        
        sql = "SELECT monthly_fee \
                 FROM students_by_form \
                WHERE student_id = %d" % self.student_id
        
        self.monthly_fee = fetch.getDig(sql)
        fee = "{:,}".format(self.monthly_fee)
        self.text_ctrl_monthly_fee.SetValue(fee)
        
        self.OnMonthsChange(wx.Event)
        
        self.Layout
            
    def OnChkRereg(self,evt):
        #rint'OnChkRereg'
        self.panel_ctrls_rereg.Show(self.chkbox_rereg.GetValue())
        self.Layout()
        
    def OnSelectcourse(self, evt):
        course_by_year_id  = fetch.cmbID(self.choice_rereg_course)
        course_fee = "SELECT course_fee FROM courses_by_year WHERE id = course_by_year_id"
        
    def lastMonthPaid(self):
        sql = "SELECT MAX(ii.month_to) \
                 FROM acc_invoices       i \
                 JOIN acc_invoice_items ii ON i.id = ii.invoice_id \
                 JOIN acc_products       p ON p.id = ii.product_id \
                WHERE student_id =%d \
                  AND i.schYr    =%d \
                  AND p.type     = 1 " % (self.student_id, gVar.schYr)
        res = fetch.getDig(sql)
        #rintres
        return  res
            
    def OnSave(self, evt):
        #rint'OnSave'
        self.Close()
        
    def OnCancel(self, evt):
        self.Close()
    
    
    def OnMonthsChange(self, evt):
        months = self.text_ctrl_months.GetValue()
        if months > self.text_ctrl_months.GetMax():
            months = self.text_ctrl_months.GetMax()
            self.text_ctrl_months.SetValue(months)
            
            
        if months > 1:
            txt = "%s till %s" % (fetch.monthName(self.monthFrom), fetch.monthName(self.monthFrom + months -1))
            self.label_fee_sd.SetLabelText('months')
        else:
            txt = "%s" % fetch.monthName(self.monthFrom)
            self.label_fee_sd.SetLabelText('month')
        self.text_ctrl_fee_description.SetValue(txt)
        total = months * self.monthly_fee
        self.text_ctrl_total_fees.SetValue(total)
        
        if  months == self.text_ctrl_months.GetMax():
            #rint'gghfd'
            self.panel_rereg.Show()
        else:
            #rint'jkkk'
            self.panel_rereg.Hide()
        self.Layout()
        

if __name__ == "__main__":
    gVar.schYr = 2014
    app = wx.App(None)
    dlg = create(None)
    try:
        dlg.displayData(1)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
    
    
    
