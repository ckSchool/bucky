import wx, time, datetime 
import DlgDatePicker


def DatePicker(self, current_value, style='dmy'): 
    from datetime import datetime
    # all we have to do is send datetime the day (d) month(m) and year(Y)
    date_object = datetime.strptime(current_value, '%d %m %Y').date()

    dlg = DlgDatePicker.create(None,date_object)
    try:
        if dlg.ShowModal() == wx.ID_OK:
            return DlgDatePicker.PyGetDate(style)
            
    finally: dlg.Destroy()
         
	 
def SmartAddressEditor(self,address=''):
    pass

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
	# '1-6-1999' no good
	# '1/6/1999' no good
	
	print DatePicker(None, '1 6 1999')
	
if __name__ == "__main__":
    app = wx.App(redirect=False)
    MainFrame = MainFrame(None, -1, "")
    app.SetTopWindow(MainFrame)
    MainFrame.Show()
    app.MainLoop()