import wx, fetch

from wx.lib.masked import NumCtrl

def create(parent):
    return DlgInvoiceItem(parent)

class DlgInvoiceItem(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base = wx.Panel(self, -1)
    
        self.panel_top  = wx.Panel(self.panel_base, -1)
        self.label_40   = wx.StaticText(self.panel_top, -1, "Description")
        self.text_ctrl_description = wx.TextCtrl(self.panel_top, -1, "")# , style=wx.TE_MULTILINE)
        
        self.label_41        = wx.StaticText(self.panel_top, -1, "Price")
        self.text_ctrl_price = NumCtrl(self.panel_top, -1, value=0)
        self.text_ctrl_price.SetAllowNegative(False)
        
        self.panel_buttons   = wx.Panel(self.panel_base, -1)
        
        self.button_save     = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel   = wx.Button(self.panel_buttons, -1, "Cancel")
        
        self.Bind(wx.EVT_BUTTON, self.onSave,   self.button_save)
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.text_ctrl_description.SetMinSize((300,-1))
        self.SetTitle("Add Product")

    def __do_layout(self):
        sizer_base    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main    = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer    = wx.FlexGridSizer(4, 2, 5, 5)
        
        grid_sizer.Add(self.label_40,        0, 0, 0)
        grid_sizer.Add(self.text_ctrl_description, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_41,        0, 0, 0)
        grid_sizer.Add(self.text_ctrl_price, 0, 0, 0)
        self.panel_top.SetSizer(grid_sizer)
        grid_sizer.AddGrowableCol(1)
        
        sizer_buttons.Add(self.button_save,   0, 0, 0)
        sizer_buttons.Add(self.button_cancel, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_main.Add(self.panel_top,     1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()
        
    def displayData(self):
        pass
        
    def onSave(self, evt):
        description = self.text_ctrl_description.GetValue()
        price       = int(self.text_ctrl_price.GetValue())
        
        if not description or not price:
            fetch.msg("Price or description missing ")
    
        elif fetch.is_unique_product(sql):
            fetch.msg('description not unique')
        
        else:
            sql = "INSERT INTO acc_products \
                              (description, price)  \
                       VALUES ('%s', %d)" % (
                              description, price)
            #rintsql
            fetch.updateDB(sql)
            self.Destroy()
    
    def onCancel(self, evt):
        self.Destroy()
    
if __name__ == "__main__":
    app = wx.App(None)
    dlg = DlgInvoiceItem(None, -1, "")
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()
