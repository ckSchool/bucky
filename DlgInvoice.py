import wx, gVar, datetime,  calendar, time, fetch

from PanelInvoice  import PanelInvoice
from DateCtrl      import DateCtrl as PanelDatePicker

def create(parent):
    return DlgInvoice(parent)

class DlgInvoice(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.PanelNewInvoice        = wx.Panel(self, -1)
        
        self.panel_heading          = wx.Panel(self, -1)
        self.label_heading          = wx.StaticText(self.panel_heading, -1, "new invoice")
        self.panel_top              = wx.Panel(self, -1)
        self.panel_inv_details      = wx.Panel(self.panel_top, -1)
        self.label_student          = wx.StaticText(  self.panel_inv_details, -1, "Student")
        self.text_ctrl_student_name = wx.TextCtrl(    self.panel_inv_details, -1, style = wx.TE_READONLY)
        self.label_date             = wx.StaticText(  self.panel_inv_details, -1, "Date")
        self.date_picker_ctrl       = PanelDatePicker(self.panel_inv_details, -1)
        self.label_invoice_no       = wx.StaticText(  self.panel_inv_details, -1, "Invoice No.")
        self.text_ctrl_invoice_no   = wx.TextCtrl(    self.panel_inv_details, -1, "",  style = wx.TE_READONLY)
        self.panel_spc1             = wx.Panel(       self.panel_inv_details, -1)
        
        # causing iCCP unknown sRGB profile error
        self.bitmap_button_client = wx.BitmapButton(self.panel_top, -1, wx.Bitmap(".\\images\\64\\teacher 64.png", wx.BITMAP_TYPE_ANY))
        
        self.PanelInvoice    = PanelInvoice(self, -1)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_inv_client = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_details = wx.FlexGridSizer(4, 2, 10, 10)
        sizer_heading = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_heading.Add(self.label_heading, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        self.panel_heading.SetSizer(sizer_heading)
        
        grid_sizer_details.Add(self.label_student, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_RIGHT, 5)
        grid_sizer_details.Add(self.text_ctrl_student_name, 1, wx.TOP , 5)
        grid_sizer_details.Add(self.label_date, 0, wx.RIGHT | wx.ALIGN_RIGHT, 5)
        grid_sizer_details.Add(self.date_picker_ctrl, 1, wx.EXPAND, 0)
        grid_sizer_details.Add(self.label_invoice_no, 0, wx.LEFT | wx.ALIGN_RIGHT, 20)
        grid_sizer_details.Add(self.text_ctrl_invoice_no, 0, 0, 0)
        grid_sizer_details.Add(self.panel_spc1, 1, wx.EXPAND, 0)
        
        self.panel_inv_details.SetSizer(grid_sizer_details)
        grid_sizer_details.AddGrowableCol(1)
        
        sizer_inv_client.Add(self.panel_inv_details, 1, wx.EXPAND, 0)
        sizer_inv_client.Add(self.bitmap_button_client, 0, wx.RIGHT, 15)
        self.panel_top.SetSizer(sizer_inv_client)
        
        sizer_main.Add(self.panel_heading, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_top, 0, wx.ALL | wx.EXPAND, 5)
        
        self.PanelNewInvoice.SetSizer(sizer_main)

        sizer.Add(self.PanelNewInvoice, 0, wx.EXPAND, 0)
        sizer.Add(self.PanelInvoice, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        
        self.Centre()
        
    def __set_properties(self):
        self.SetMinSize((800, 500))
        self.SetSize((800, 500))
        
        self.text_ctrl_student_name.SetMinSize((250,21))
        self.SetBackgroundColour((224, 224, 224))
        self.label_heading.SetForegroundColour((255, 255, 255))
        self.label_heading.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_heading.SetMinSize((-1,30))
        self.panel_heading.SetBackgroundColour((47, 47, 47))

        self.text_ctrl_invoice_no.SetMinSize((250, 25))
        self.bitmap_button_client.SetSize(self.bitmap_button_client.GetBestSize())
    
    def __do_main(self):
        pass
        

    def displayData(self):
        
        self.student_id = student_id = gVar.student_id
        
        
        self.invoice_id = fetch.nextID('acc_invoices"')
        mnth  = 1
        mnth  = str(mnth).zfill(2)
        invNo = str(self.invoice_id).zfill(5)
        
        self.invoice_no = '%d.%s.%s' % (gVar.schYr, mnth, invNo) 
        
        self.text_ctrl_invoice_no.SetValue(self.invoice_no)
        
        
        self.date_picker_ctrl.setDateToday()
        
        name = fetch.studentFullName(student_id)
        self.text_ctrl_student_name.SetValue(str(name))
        self.PanelInvoice.displayData(self.student_id)
        self.PanelInvoice.invoice_id=self.invoice_id
        
  
    def invoiceData(self):
        print self.date_picker_ctrl.GetMSDbReadyValue()   
        datestr = self.date_picker_ctrl.GetMSDbReadyValue()
        return (self.student_id, datestr, self.invoice_no)    
        
    def onAdd(self):
        self.Layout()


if __name__ == "__main__":
    gVar.schYr = 2015
    gVar.student_id = 5
    
    app = wx.App(None)
    dlg = create(None)
    dlg.displayData()
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()