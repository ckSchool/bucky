import wx, fetch, loadCmb, gVar

def create(parent):
    return DlgSchYr(parent)

class DlgSchYr(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_top       = wx.Panel(self, -1)
        self.choice_schYr    = wx.Choice(self.panel_top, -1, choices=[])
        self.button_new_year = wx.Button(self.panel_top, -1, "New Year")
        
        self.panel_bottom = wx.Panel(self, -1)
        self.label_pcs1      = wx.StaticText(self.panel_bottom, -1, "")
        self.button_save     = wx.Button(self.panel_bottom, wx.ID_SAVE, "")
        self.button_cancel   = wx.Button(self.panel_bottom, wx.ID_CANCEL, "")
        self.label_pcs2      = wx.StaticText(self.panel_bottom, -1, "")
        
        self.Bind(wx.EVT_BUTTON, self.OnAddYear, self.button_new_year)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,   self.button_cancel)

        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.SetTitle("Select School Year")
        self.choice_schYr.SetMinSize((120,-1))

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_top    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top.Add(self.choice_schYr,    0, 0, 0)
        sizer_top.Add(self.button_new_year, 0, wx.LEFT, 10)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_bottom.Add(self.label_pcs1,    1, 0, 0)
        sizer_bottom.Add(self.button_save,   0, 0, 0)
        sizer_bottom.Add(self.button_cancel, 0, 0, 0)
        sizer_bottom.Add(self.label_pcs2,    1, 0, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_main.Add(self.panel_top,    1, wx.ALL | wx.EXPAND, 20)
        sizer_main.Add(wx.StaticLine(self, -1), 0, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(self.panel_bottom, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        
        self.Centre()
        
    def __do_main(self):
        loadCmb.schYears(self.choice_schYr)
        self.new_year = 0
        self.schYr = 0
        
    def displayData(self):
        self.schYr = gVar.schYr
        loadCmb.restore_str(self.choice_schYr, str(gVar.schYr))
        
    def OnAddYear(self, evt):
        if not self.new_year:
            res = fetch.getDig( "SELECT MAX(schYr) FROM schYrs" )
            yid = fetch.nextID('schYrs')
            if res :
                self.new_year = res + 1
                self.choice_schYr.Append(str(self.new_year), yid)
                loadCmb.restore(self.choice_schYr, yid)
        else:
            fetch.msg('A new year has already been added. Save First')

    def OnSave(self, evt):
        if self.new_year:
            sql = "INSERT  INTO schYrs (schYr) VALUES (%d)" % self.new_year
            #rintsql
            yid = fetch.updateDB(sql)
            #rintyid
            
        
        self.schYr =  int(self.choice_schYr.GetStringSelection())
                     
        #rintself.schYr
        self.EndModal(0) 
        
        
    def OnCancel(self, evt):
        self.EndModal(0) 
        
if __name__ == "__main__":
    app = wx.App(0)
    dlg = DlgSchYr(None, -1, "")
    app.SetTopWindow(dlg)
    dlg.ShowModal()
    #rintdlg.schYr
    dlg.Destroy()
    app.MainLoop()
