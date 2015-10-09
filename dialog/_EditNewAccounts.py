import wx

import fetch

class DlgNewEditAccount_(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base      = wx.Panel(self, -1)
        self.label_title     = wx.StaticText(self.panel_base, -1, "Account name")
        self.text_ctrl_title = wx.TextCtrl(self.panel_base,   -1, "")
        #self.label_short     = wx.StaticText(self.panel_base, -1, "Short")
        #self.text_ctrl_short = wx.TextCtrl(self.panel_base,   -1, "")
        self.static_line     = wx.StaticLine(self.panel_base, -1)
        self.button_ok       = wx.Button(self.panel_base,     -1, "OK")

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnEnter, self.button_ok)

    def __set_properties(self):
        self.SetTitle("Account name")
        self.text_ctrl_title.SetMinSize((300, 21))
        #self.text_ctrl_short.SetMinSize((150, -1))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.label_title, 0, 0, 0)
        sizer_main.Add(self.text_ctrl_title, 0, wx.EXPAND, 0)
        #sizer_main.Add(self.label_short, 0, wx.TOP, 10)
        #sizer_main.Add(self.text_ctrl_short, 0, 0, 0)
        sizer_main.Add(self.static_line, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        sizer_main.Add(self.button_ok, 0, wx.EXPAND, 0)
        self.panel_base.SetSizer(sizer_main)
        sizer_base.Add(self.panel_base, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Center()
        
    def displayData(self, account_id=0):
        self.account_id = account_id
        if account_id:
            editmode = True
            self.account_name = fetch.account_name(account_id)
            
        else:
            self.editmode = False
            self.account_name = ''
        
    def OnEnter(self, evt):
        name = self.text_ctrl_title.GetValue()
        if not name: return
        
        if self.editmode():
            if name != self.account_name:
                self.update(name)
            
        else:self.insert(name)
        
    def update(self, name):
        sql = "UPDATE accounts SET name ='%s' WHERE id =%d"
        self.Close()
    
    def insert(self, name):
        if not self.exists(name):
            sql = "INSERT INTO accounts SET name ='%s'"
            pass
            self.Close()
        else:
            fetch.msg("Account name exists, please try another")
        
def create(parent):
    return DlgNewEditAccount_(parent)        
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = create(None)
    try:
        dlg.displayData(1)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
    app.MainLoop()