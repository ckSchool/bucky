import wx, gVar, loadCmb, fetch

from my_ctrls import Validator

def create(parent):
    return DlgAddrItemEditor(parent)
    
class DlgAddrItemEditor(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base = wx.Panel(self, -1)
        
        self.text_ctrl_item_name = wx.TextCtrl(self.panel_base, -1, "", validator = Validator())
        self.button_save         = wx.Button(self.panel_base,   -1, "Save")
  
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnSave,  self.button_save)
        self.Bind(wx.EVT_CLOSE,  self.OnClose, self)
        
        self.__do_main()

    def OnClose(self, evt):
        self.EndModal(0)
        
    def __set_properties(self):
        self.SetTitle("New Address Item")
        self.button_save.SetMinSize((100, 30))

    def __do_layout(self):
        sizer_base  = wx.BoxSizer(wx.VERTICAL)
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        
        sizer_main.Add(self.text_ctrl_item_name,  0, wx.EXPAND , 0)
        sizer_main.Add(self.button_save,    0, wx.ALL | wx.ALIGN_RIGHT, 20)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer_base)
        self.Layout()
        self.Center()

    def __do_main(self):
        pass
        
  
    def displayData(self, itemID, itemType, nextItem=''):
        if itemID:
            #rint'Dlg item editor > hasid'
            itemName = fetch.addrItemName(itemID)
            txt = 'Editing %s : %s' % (itemType, itemName)
            self.SetTitle(txt)
            self.text_ctrl_item_name.SetValue(itemName)
        else:
            if itemType == 'country':
                txt = 'Create new country'
            else:
                txt = 'Create new %s' % itemType
                if nextItem:
                    txt += ' for: %s' % nextItem
            self.SetTitle(txt)

    def OnSave(self, event):
        self.itemName = self.text_ctrl_item_name.GetValue()
        self.EndModal(wx.ID_OK)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgAddrItemEditor(None)
    try:
        dlg.displayData(0,'Country')
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
