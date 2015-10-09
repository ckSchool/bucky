import wx, fetch, gVar


def create(parent):
    return DlgTemplate(parent)

class DlgTemplate(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base      = wx.Panel(self, -1)
        self.panel_top       = wx.Panel(self.panel_base, -1)

        self.panel_buttons   = wx.Panel(self.panel_base, -1)
        self.button_save     = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel   = wx.Button(self.panel_buttons, -1, "Cancel")
 
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle(" ")

    def __do_layout(self):
        sizer_base      = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main      = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_buttons.Add(self.button_save,   0, 0, 0)
        sizer_buttons.Add(self.button_cancel, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_main.Add(self.panel_top,     1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()
        
        
        
    def displayData(self):
        pass
        
    def OnSave(self, evt):
        self.Close()
    
    def OnCancel(self, evt):
        self.Close()
    

if __name__ == "__main__":
    app = wx.App(None)
    dlg = DlgTemplate(None, -1, "")
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()
