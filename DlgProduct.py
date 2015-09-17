import wx, fetch, datetime, loadCmb

from DateCtrl import DateCtrl

from wx.lib.masked import NumCtrl

def create(parent):
    return DlgInvoiceItem(parent)

class DlgInvoiceItem(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base = wx.Panel(self, -1)
    
        self.panel_top  = wx.Panel(self.panel_base, -1)
        
        self.label_40        = wx.StaticText(self.panel_top, -1, "Description")
        self.text_ctrl_description = wx.TextCtrl(self.panel_top, -1, "", style=wx.TE_MULTILINE)
        
        self.label_41        = wx.StaticText(self.panel_top, -1, "Price")
        self.text_ctrl_price = NumCtrl(self.panel_top,   -1)
        
        self.label_42        = wx.StaticText(self.panel_top, -1, "Valid From")
        self.panel_from_till = wx.Panel(self.panel_top, -1)
        self.datectrl_from   = DateCtrl(self.panel_from_till, -1)
        self.datectrl_from.SetName('from')
        self.label_43        = wx.StaticText(self.panel_from_till, -1, " till ")
        self.datectrl_to     = DateCtrl(self.panel_from_till, -1)
        self.datectrl_to.SetName('to')
        
        self.label_recurring = wx.StaticText(self.panel_top, -1, "Recurring")
        self.panel_recurring =  wx.Panel(self.panel_top, -1)
        self.checkbox_is_recurring = wx.CheckBox(self.panel_recurring, -1, '')
        self.checkbox_monthly = wx.CheckBox(self.panel_recurring, -1, ' Monthly', style= wx.ALIGN_RIGHT)
        
        self.label_type      = wx.StaticText(self.panel_top, -1, "Type")
        self.choice_type     = wx.Choice(self.panel_top, -1, choices=[])
        
        self.panel_buttons   = wx.Panel(self.panel_base, -1)
        self.button_save     = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel   = wx.Button(self.panel_buttons, -1, "Cancel")
 
        self.Bind(wx.EVT_CHECKBOX, self.chk_recurring, self.checkbox_is_recurring)
        self.Bind(wx.EVT_BUTTON,   self.OnSave, self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnCancel, self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.text_ctrl_description.SetMinSize((300,100))
        self.SetTitle("Add Product")
        self.datectrl_from.checkbox.SetValue(False)
        self.datectrl_to.checkbox.SetValue(False)
        self.checkbox_is_recurring.SetValue(0)
        self.checkbox_monthly.Hide()

    def __do_layout(self):
        sizer_base      = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main      = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_from_till = wx.BoxSizer(wx.HORIZONTAL)
        sizer_recurring = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer      = wx.FlexGridSizer(5, 2, 5, 5)

        sizer_from_till.Add(self.datectrl_from, 0, 0, 0)
        sizer_from_till.Add(self.label_43,      0, 0, 0)
        sizer_from_till.Add(self.datectrl_to,   0, 0, 0)
        self.panel_from_till.SetSizer(sizer_from_till)
        
        sizer_recurring.Add(self.checkbox_is_recurring, 0, 0, 0)
        sizer_recurring.Add(self.checkbox_monthly,      0, wx.LEFT, 20)
        self.panel_recurring.SetSizer(sizer_recurring)
        
        grid_sizer.Add(self.label_40,        0, 0, 0)
        grid_sizer.Add(self.text_ctrl_description, 0, wx.EXPAND, 0)
        
        grid_sizer.Add(self.label_41,        0, 0, 0)
        grid_sizer.Add(self.text_ctrl_price, 0, wx.EXPAND, 0)
        
        grid_sizer.Add(self.label_42,        0, 0, 0)
        grid_sizer.Add(self.panel_from_till, 0, 0, 0)
        
        grid_sizer.Add(self.label_recurring, 0, 0, 0)
        grid_sizer.Add(self.panel_recurring, 0, 0, 0)
        
        grid_sizer.Add(self.label_type, 0, 0, 0)
        grid_sizer.Add(self.choice_type, 0, 0, 0)
        
        self.panel_top.SetSizer(grid_sizer)
        grid_sizer.AddGrowableCol(1)
        
        sizer_buttons.Add(self.button_save,   0, 0, 0)
        sizer_buttons.Add(self.button_cancel, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_main.Add(self.panel_top,     1, wx.EXPAND, 0)
        line = wx.StaticLine(self.panel_base, -1)
        sizer_main.Add(line, 0,  wx.TOP | wx.EXPAND, 10)
        sizer_main.Add(self.panel_buttons, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()
        
    def __do_main(self,):
        loadCmb.product_types(self.choice_type)
        
    def displayData(self):
        pass
    
    def chk_recurring(self, evt):
        if self.checkbox_is_recurring.GetValue():
            self.checkbox_monthly.Show()
        else:
            self.checkbox_monthly.SetValue(0)
            self.checkbox_monthly.Hide()
        
        
        self.Layout()
        
    def OnSave(self, evt):
        description  = self.text_ctrl_description.GetValue()
        price        = self.text_ctrl_price.GetValue()
        is_recurring = self.checkbox_is_recurring.GetValue()
        monthly      = self.checkbox_monthly.GetValue()
        valid_from   = self.datectrl_from.GetDbReadyValue()
        valid_to     = self.datectrl_to.GetDbReadyValue()
        product_type = fetch.cmbID(self.choice_type)
        if not price or not description:
            fetch.msg('Not all fields complete')
        
    
        print "values",  description, price, is_recurring, monthly, valid_from, valid_to, product_type
        
        if fetch.is_unique_product(description):
            sql = "INSERT INTO acc_products \
                              (description, price, is_recurring, \
                               recurring_monthly, valid_from, valid_to, type_id) \
                        VALUES ('%s', %d, %d, %d, '%s', '%s', %d) " % (
                                description, int(price), is_recurring,
                                monthly, valid_from, valid_to, product_type)
            print sql
            fetch.updateDB(sql)
        self.Close()
    
    def OnCancel(self, evt):
        self.Close()
    

if __name__ == "__main__":
    app = wx.App(None)
    dlg = DlgInvoiceItem(None, -1, "")
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()
