import wx,  gVar
import fetchodbc as fetch

from PanelStudentDataViewerNB import PanelStudentDataViewerNB as NB

def create(parent):
    return DlgSelectParent(parent)
    
class DlgSelectParent(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_details = wx.Panel(self, -1)
        self.button_ok     = wx.Button(self, -1, "OK")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOK, self.button_ok)

    def __set_properties(self):
        self.SetTitle("Select Parent")
        
        

    def __do_layout(self):
        
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_ctrls = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.panel_details, 1, wx.EXPAND, 0)
        sizer_main.Add(self.button_ok, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        self.SetSize((200, 720))
        self.Center()
        
    def displayData(self, student_id=0):
        self.student_id = student_id
        self.panel_details.displayData(student_id)
        self.panel_details.enableCtrls()
        #self.panel_details.button_guardian.Hide()
        
        
    def OnOK(self, event):
        msg = "This will overwrite existing data /n Procede?"
        ans = wx.MessageBox(msg, "Via Function", wx.YES_NO | wx.ICON_QUESTION)
        #rint 'ans = ', ans
        if  ans == 2:
            self.panel_details.saveDetails()
            self.Close()
            
        else:
            pass

if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgSelectParent(None, -1)
    try:
        dlg.ShowModal()
    finally:  dlg.Destroy()
    app.MainLoop()
