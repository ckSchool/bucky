import wx, gVar, fetch, loadCmb


class DlgSelectMonthsPeriod(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_top     = wx.Panel(self, -1)
        #self.label_blank   = wx.StaticText(self.panel_top, -1, "")
        #self.label_heading = wx.StaticText(self.panel_top, -1, "heading")
        self.label_from    = wx.StaticText(self.panel_top, -1, "From")
        self.text_ctrl_from   = wx.TextCtrl(self.panel_top, -1, "1", style=wx.TE_READONLY | wx.NO_BORDER)
        self.label_to      = wx.StaticText(self.panel_top, -1, "To")
        self.choice_to     = wx.Choice(self.panel_top, -1, choices=[])
        self.label_months   = wx.StaticText(self.panel_top, -1, "Months")
        self.text_ctrl_months = wx.TextCtrl(self.panel_top, -1, "1", style=wx.TE_READONLY | wx.NO_BORDER)
        
        self.static_line_1 = wx.StaticLine(self, -1)
        
        self.panel_btns = wx.Panel(self, -1)
        self.label_1    = wx.StaticText(self.panel_btns, -1, "")
        self.button_ok  = wx.Button(self.panel_btns, wx.ID_OK, "")
        self.button_2   = wx.Button(self.panel_btns, wx.ID_CANCEL, "")
        self.label_2    = wx.StaticText(self.panel_btns, -1, "")

        self.__set_properties()
        self.__do_layout()
        self.__do_main()

        self.Bind(wx.EVT_BUTTON, self.OnOk,    self.button_ok)
        self.Bind(wx.EVT_BUTTON, self.OnCanel, self.button_2)
        
        #self.Bind(wx.EVT_CHOICE, self.OnChoiceFrom, self.text_ctrl_from)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceTo, self.choice_to)
        
    
    def OnChoiceTo(self, evt):
        months = fetch.cmbID(self.choice_to) - self.month_from
        self.text_ctrl_months.SetValue(str(months))
        
        
    def __set_properties(self):
        self.SetTitle("Select Payment Period")
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_btns = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_top = wx.FlexGridSizer(4, 2, 5, 5)
        
        grid_sizer_top.Add(self.label_from,       0, 0, 0)
        grid_sizer_top.Add(self.text_ctrl_from,   0, 0, 0)
        grid_sizer_top.Add(self.label_to,         0, 0, 0)
        grid_sizer_top.Add(self.choice_to,        0, 0, 0)
        grid_sizer_top.Add(self.label_months,     0, 0, 0)
        grid_sizer_top.Add(self.text_ctrl_months, 0, wx.EXPAND, 0)
        self.panel_top.SetSizer(grid_sizer_top)
        
        sizer_btns.Add(self.label_1,   1, 0, 0)
        sizer_btns.Add(self.button_ok, 0, 0, 0)
        sizer_btns.Add(self.button_2,  0, 0, 0)
        sizer_btns.Add(self.label_2,   1, 0, 0)
        self.panel_btns.SetSizer(sizer_btns)
        
        sizer_main.Add(self.panel_top,     1, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_btns,    0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        
    def __do_main(self):
        self.MyValues =(1, 2)
        self.monthNames = gVar.monthNames
        
    def MyGetValues(self):
        return (self.month_from, fetch.cmbID(self.choice_to))
    
    def OnOk(self, event):  
        print "Event handler `OnOk' not implemented!"
        event.Skip()

    def OnCanel(self, event):  
        print "Event handler `OnCanel' not implemented!"
        event.Skip()
        
    def displayData(self, month_from=1):
        self.month_from = month_from
        self.text_ctrl_from.SetValue(self.monthNames[month_from])
        for key in self.monthNames:
            if key > 1: self.choice_to.Append(self.monthNames[key],   key)
            
        loadCmb.restore(self.choice_to, 2)

def create(parent):
    return DlgSelectMonthsPeriod(parent)

if __name__ == "__main__":
    app = wx.App(None)
    dialog_1 = DlgSelectMonthsPeriod(None, -1, "")
    dialog_1.displayData(1)
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
    
    
