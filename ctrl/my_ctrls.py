import wx, string

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


ALPHA_ONLY     = 1
DIGIT_ONLY     = 2
ALPHA_OR_DIGIT = 3

from    wx.lib import masked


class Validator(wx.PyValidator):
    def __init__(self, flag=ALPHA_OR_DIGIT, allow_spaces=True):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.allow_spaces = allow_spaces
        
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return Validator(self.flag, self.allow_spaces)

    def OnChar(self, event):
        key = event.GetKeyCode()

        if self.allow_spaces:
            if key <= wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
                event.Skip()
                return
        else:
            if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
                event.Skip()
                return

        if self.flag == ALPHA_OR_DIGIT:
            if key==".":
                event.Skip()
                return
            
            if chr(key) in string.letters or chr(key) in string.digits:
                event.Skip()
                return
        
        if self.flag == ALPHA_ONLY and chr(key) in string.letters:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():   wx.Bell()

        return
    
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
        
        self.Bind(wx.EVT_BUTTON, self.OnNew,    self.new)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,   self.edit)
        # self.Bind(wx.EVT_BUTTON, self.OnDelete, self.delete)
        # self.Bind(wx.EVT_BUTTON, self.OnSave,   self.save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer.Add(self.new,     0, 0, 0)
        sizer.Add(self.edit,    0, 0, 0)
        sizer.Add(self.delete,  0, 0, 0)
        sizer.Add(self.save,    0, 0, 0)
        sizer.Add(self.cancel,  0, 0, 0)
        sizer.Add(self.refresh, 0, 0, 0)
        self.SetSizer(sizer)
        
        self.reset()
        
    def OnNew(self, evt):
        #rint'pbut new'
        self.Lockout()
        evt.Skip()
        
    def OnEdit(self, evt):
        #rint'pbut edit'
        self.Lockout()
        
    def OnCancel(self, evt):
        self.reset()
        
    def reset(self):
        self.new.Enable() 
        self.edit.Enable() 
        self.delete.Enable() 
        self.save.Enable(False) 
        self.cancel.Enable(False) 
        self.refresh.Enable()
        # pub.sendMessage('unlockdown')
        
    def Lockout(self):
        #rint' sendMessage(lockdown)'
        # pub.sendMessage('lockdown')
        self.new.Enable(False) 
        self.edit.Enable(False) 
        self.delete.Enable(False) 
        self.save.Enable() 
        self.cancel.Enable() 
        self.refresh.Enable(False)
    