import wx

import data.gVar    as gVar

from panel.guardian_data import panel_guardian_data

class panel_edit_guardian(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_l = wx.Panel(self, -1)
        self.panel_r = wx.Panel(self, -1)
        
        self.panel_top    = wx.Panel(self.panel_l, -1)
        
        self.button_back  = wx.Button(    self.panel_top, -1, "< Back")
        self.pcs1         = wx.StaticText(self.panel_top, -1, "")
        self.button_save  = wx.Button(    self.panel_top, -1, "Save")
        self.button_edit  = wx.Button(    self.panel_top, -1, "Edit")
        
        self.panel_contact  = panel_guardian_data(self.panel_l, -1)
  
        self.Bind(wx.EVT_BUTTON, self.OnBack,     self.button_back)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,     self.button_edit)
        self.Bind(wx.EVT_BUTTON, self.OnSave,     self.button_save)
  
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        self.button_save.Hide()
        self.panel_top.Hide()
        

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btns = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        
        sizer_btns.Add(self.button_back,   0, wx.LEFT, 0)
        sizer_btns.Add(self.pcs1,          1, wx.EXPAND, 0)
        sizer_btns.Add(self.button_edit,   0, wx.ALIGN_RIGHT, 10)
        sizer_btns.Add(self.button_save,   0, wx.ALIGN_RIGHT, 10)
        self.panel_top.SetSizer(sizer_btns)
        
        sizer_main.Add(self.panel_top,     0 ,0 ,0)
        sizer_main.Add(self.panel_contact, 1 , wx.ALL | wx.EXPAND, 10)
        self.panel_l.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_l, 1, wx.EXPAND | wx.LEFT, 15)
        sizer_base.Add(self.panel_r, 1 ,0, 0)
        self.SetSizer(sizer_base)
        
        self.Layout()
        
    def __do_main(self):
        self.panel_contact.enableCtrls(False)
    
    def displayData(self):
        #rint'displayData'
        pass
    
    def OnBack(self, evt):
        self.panel_contact.enableCtrls(False)
        self.GetTopLevelParent().goBack()
        
    def OnEdit(self, evt):
        #rint'edit'
        
        """
        if self.button_edit.GetLabelText()=='Cancel':
            self.button_edit.SetLabelText('Edit')
            self.enableCtrls(False)
            self.button_save.Hide()
        else:
            self.enableCtrls()
            self.button_edit.SetLabelText('Cancel')
            self.button_save.Show()
        self.Refresh()
        self.Layout()
        """
        
        self.panel_contact.enableCtrls()
        pass

    def OnSave(self, evt):
        #rint'save'
        pass