import wx, fetch, loadCmb, gVar


from panel_student_payments             import panel_student_payments
from panel_student_payment_records      import panel_student_payment_records
  
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


class panel_payments(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_heading   = wx.StaticText(self, -1, 'STUDENT PAYMENTS', style = wx.ALIGN_CENTRE_HORIZONTAL)
        self.label_heading.SetBackgroundColour('red')
        
        self.panel_top       = wx.Panel(self, -1)
        self.panel_bottom    = wx.Panel(self, -1)
        
        self.button_payments = wx.Button(self.panel_top, -1, 'PAYMENTS')
        self.button_records  = wx.Button(self.panel_top, -1, 'RECORDS')

        self.panel_payments  = panel_student_payments(self.panel_bottom, -1)#scrolled.ScrolledPanel(self, -1, style=wx.EXPAND)
        self.panel_records   = panel_student_payment_records(self.panel_bottom, -1)
 
        self.Bind(wx.EVT_BUTTON, self.OnPayments, self.button_payments)
        self.Bind(wx.EVT_BUTTON, self.OnRecords,  self.button_records)
        
        self.__set_properties() 
        self.__do_layout()
        self.__do_main()
     
    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_top    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top.Add(self.button_payments,   0, 0, 0)
        sizer_top.Add(self.button_records,    0, 0, 0)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_bottom.Add(self.panel_payments, 1, wx.EXPAND | wx.LEFT, 5)
        sizer_bottom.Add(self.panel_records,  1, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_main.Add(self.label_heading, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_top,     0, wx.EXPAND | wx.ALL, 5)
        sizer_main.Add(self.panel_bottom,  1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.OnPayments(wx.Event)
        self.displayData()
        
    def displayData(self):
        if self.current_view == 'payments':
            self.panel_payments.displayData()
        else:
            self.panel_records.displayData()
        
    def OnPayments(self, evt):
        self.current_view = 'payments'
        self.highlightButton(self.button_payments)
        self.panel_records.Hide()
        self.panel_payments.Show()
        self.Layout()
        
    def OnRecords(self, evt):
        self.current_view = 'records'
        self.highlightButton(self.button_records)
        self.panel_records.Show()
        self.panel_payments.Hide()
        self.Layout()
        
    def highlightButton(self, b):
        self.button_payments.SetBackgroundColour('grey')
        self.button_records.SetBackgroundColour('grey')
        b.SetBackgroundColour('white')
        
    def lockdown(self):
        self.panel_top.Enable(False)
    
    def unlockdown(self, ):
        self.panel_top.Enable()
        
    def viewOnly(self, ):
        self.panel_payments.panel_details.panel_buttons.Hide()
        self.panel_records.panel_details.panel_buttons.Hide()
        
    


