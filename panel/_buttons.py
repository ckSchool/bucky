import wx

class panel_buttons(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.new     = wx.Button(self, -1, "New")
        self.edit    = wx.Button(self, -1, "Edit")
        self.delete  = wx.Button(self, -1, "Delete")
        self.save    = wx.Button(self, -1, "Save")
        self.cancel  = wx.Button(self, -1, "Cancel")
        self.refresh = wx.Button(self, -1, "Refresh")
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer.Add(self.new,     1, 0, 0)
        sizer.Add(self.edit,    1, 0, 0)
        sizer.Add(self.delete,  1, 0, 0)
        sizer.Add(self.save,    1, 0, 0)
        sizer.Add(self.cancel,  1, 0, 0)
        sizer.Add(self.refresh, 1, 0, 0)
        self.SetSizer(sizer)
        
    def OnCancel(self):
        self.new.Enable() 
        self.edit.Enable() 
        self.delete.Enable() 
        self.save.Enable(False) 
        self.cancel.Enable(False) 
        self.refresh.Enable()
        
    def LockOut(self):
        self.new.Enable(False) 
        self.edit.Enable(False) 
        self.delete.Enable(False) 
        self.save.Enable() 
        self.cancel.Enable() 
        self.refresh.Enable(False)