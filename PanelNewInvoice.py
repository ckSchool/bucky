import wx, datetime, calendar, time, gVar
import loadCmbODBC as loadCmb
import fetchodbc   as fetch


#from PanelInvoice       import PanelInvoice as PanelTheInvoice

from DateCtrl       import DateCtrl as PanelDatePicker

class PanelNewInvoice(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.student_id=0
        self.panel_heading        = wx.Panel(self, -1)
        self.label_heading        = wx.StaticText(self.panel_heading, -1, "new invoice")
        self.panel_top            = wx.Panel(self, -1)
        self.panel_inv_details    = wx.Panel(self.panel_top, -1)
        self.label_student        = wx.StaticText(  self.panel_inv_details, -1, "Student")
        self.combo_box_student    = wx.TextCtrl(    self.panel_inv_details, -1, style = wx.TE_READONLY)
        self.label_date           = wx.StaticText(  self.panel_inv_details, -1, "Date")
        self.panel_date           = PanelDatePicker(self.panel_inv_details, -1)
        self.label_invoice_no     = wx.StaticText(  self.panel_inv_details, -1, "Invoice No.")
        self.text_ctrl_invoice_no = wx.TextCtrl(    self.panel_inv_details, -1, "00000002",  style = wx.TE_READONLY)
        self.panel_spc1           = wx.Panel(       self.panel_inv_details, -1)
        self.bitmap_button_client = wx.BitmapButton(self.panel_top, -1, wx.Bitmap(".\\images\\64\\teacher 64.png", wx.BITMAP_TYPE_ANY))
        
        #self.panel_inv_holder     = PanelTheInvoice(self, -1)

        self.__set_properties()
        self.__do_layout()

        #self.Bind(wx.EVT_TEXT, self.OnInvID, self.text_ctrl_invoice_no)

        self.__do_main()

    def __set_properties(self):
        self.combo_box_student.SetMinSize((250,21))
        self.SetBackgroundColour((224, 224, 224))
        self.label_heading.SetForegroundColour((255, 255, 255))
        self.label_heading.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_heading.SetMinSize((-1,30))
        self.panel_heading.SetBackgroundColour((47, 47, 47))

        self.text_ctrl_invoice_no.SetMinSize((250, 25))
        self.bitmap_button_client.SetSize(self.bitmap_button_client.GetBestSize())
        #self.panel_inv_holder.SetBackgroundColour(wx.Colour(255, 255, 255))


    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_inv_client = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_details = wx.FlexGridSizer(4, 2, 10, 10)
        sizer_heading = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_heading.Add(self.label_heading, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        self.panel_heading.SetSizer(sizer_heading)
        
        grid_sizer_details.Add(self.label_student, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_RIGHT, 5)
        grid_sizer_details.Add(self.combo_box_student, 1, wx.TOP , 5)
        grid_sizer_details.Add(self.label_date, 0, wx.RIGHT | wx.ALIGN_RIGHT, 5)
        grid_sizer_details.Add(self.panel_date, 1, wx.EXPAND, 0)
        grid_sizer_details.Add(self.label_invoice_no, 0, wx.LEFT | wx.ALIGN_RIGHT, 20)
        grid_sizer_details.Add(self.text_ctrl_invoice_no, 0, 0, 0)
        grid_sizer_details.Add(self.panel_spc1, 1, wx.EXPAND, 0)
        #grid_sizer_details.Add(self.button_settings, 0, wx.BOTTOM, 5)
        self.panel_inv_details.SetSizer(grid_sizer_details)
        grid_sizer_details.AddGrowableCol(1)
        
        sizer_inv_client.Add(self.panel_inv_details, 1, wx.EXPAND, 0)
        sizer_inv_client.Add(self.bitmap_button_client, 0, wx.RIGHT, 15)
        self.panel_top.SetSizer(sizer_inv_client)
        
        sizer_main.Add(self.panel_heading, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_top, 0, wx.ALL | wx.EXPAND, 5)
        #sizer_main.Add(self.panel_inv_holder, 1, wx.ALL | wx.EXPAND, 20)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        pass

    def displayData(self, student_id):
        self.student_id = student_id
        p = self.GetTopLevelParent().panel_filter1
        
        loadCmb.inv_students(self.combo_box_student, p)
        loadCmb.restore(self.combo_box_student, student_id)
        
    def invoiceData(self):
        invoice_no = self.text_ctrl_invoice_no.GetValue()
        day, month, year = self.panel_date.getDate()       
        date = datetime.date(year, month, day)
        return (self.student_id, date, invoice_no)
        
    """
    def OnInvID(self, event):  # wxGlade: PanelNewInvoice.<event_handler>
        #rint "Event handler `OnInvID' not implemented!"
        event.Skip()"""

        
