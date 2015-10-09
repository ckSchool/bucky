import wx, datetime

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

from ctrl.DateCtrl   import DateCtrl
from ctrl.myListCtrl import VirtualList as vListCtrl
from ctrl.my_ctrls import panel_buttons

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


#---------------------------------------------------------------------------

class panel_student_list(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_filter_dates     = wx.Panel(self, -1)
        self.label_from             = wx.StaticText(self.panel_filter_dates,  -1, "Date")
        self.datepicker_ctrl_from   = DateCtrl(self.panel_filter_dates, -1)
        self.label_to               = wx.StaticText(self.panel_filter_dates, -1, "to")
        self.datepicker_ctrl_to     = DateCtrl(self.panel_filter_dates, -1)
   
        self.vList                  = vListCtrl(self, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.text_ctrl_record_count = wx.TextCtrl(self, -1, '')
          
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
        pub.subscribe(self.DateChange, 'DateCtrl.date_change')
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        pass
    
    def __do_layout(self):
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_date = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_date.Add(self.label_from,            0, wx.LEFT, 5)
        sizer_date.Add(self.datepicker_ctrl_from,  0, wx.LEFT, 5)
        sizer_date.Add(self.label_to,              0, wx.LEFT, 5)
        sizer_date.Add(self.datepicker_ctrl_to,    0, wx.LEFT, 5)
        self.panel_filter_dates.SetSizer(sizer_date)
        
        sizer_main.Add(self.panel_filter_dates,     0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.vList,                  1, wx.EXPAND, 0)
        sizer_main.Add(self.text_ctrl_record_count, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        
    def __do_main(self):
        headings = (('id',0),  
                        ('Receipt No.',100),
                        ('Date',80),
                        ('Registration Name',200),
                        ('Form',100),
                        ('Total',80, wx.LIST_FORMAT_RIGHT))
        self.vList.SetColumns(headings)
        
        self.dateTo   = datetime.date.today()
        self.dateFrom = self.dateTo - datetime.timedelta(days=365)
        
        self.datepicker_ctrl_from.SetValue(self.dateFrom)
        self.datepicker_ctrl_to.SetValue(self.dateTo)
   
    def DateChange(self):
        self.dateTo   = self.datepicker_ctrl_to.GetDatetimeDateValue()
        self.dateFrom = self.datepicker_ctrl_from.GetDatetimeDateValue()
        self.displayData()
    
    def getVars(self):
        if self.dateTo:
            newto = self.dateTo + datetime.timedelta(days=1)
            y, m, d = newto.year, newto.month, newto.day
            dateto  = '%d/%d/%d' % (m, d, y)
        else:
            dateto = ''
            
        if self.dateFrom:
            y, m, d = self.dateFrom.year, self.dateFrom.month, self.dateFrom.day
            datefrom  = '%d/%d/%d' % (m, d, y)
        else:
            datefrom = ''
        
        paymentType_id = ''
        return (paymentType_id, datefrom, dateto)
     
    def displayData(self):
        #rint'panel_registration_payment_records ---------displayData'
        paymentType_id, datefrom, dateto = self.getVars()
    

    def OnItemSelected(self, evt):
        student_id  = self.vList.GetSelectedID()
        index = self.vList.GetFirstSelected()
        gVar.NoInduk = self.vList.getColumnText(index, 1)
        
        txt = "Record %d/%d" % (index, self.records)
        self.text_ctrl_record_count.SetValue(txt)
        
        pub.sendMessage('regpaymentrecords.studentselected')


        
class payment_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_details            = wx.Panel(self, -1)
        self.panel_buttons            = panel_buttons(self, -1)
        
        self.label_details            = wx.StaticText(self, -1, 'DETAILS')
        self.details_list             = vListCtrl(self.panel_details,  style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        self.panel_details_botttom    = wx.Panel( self.panel_details, -1)
        
        self.txt_ctrl_details_records = wx.TextCtrl(self.panel_details_botttom, -1, "")
        self.txt_ctrl_details_total   = wx.TextCtrl(self.panel_details_botttom, -1, "")
        
        self.panel_buttons.new.Bind(wx.EVT_BUTTON, self.OnNew,       self.panel_buttons.new )
        self.panel_buttons.edit.Bind(wx.EVT_BUTTON, self.OnEdit,     self.panel_buttons.edit )
        self.panel_buttons.cancel.Bind(wx.EVT_BUTTON, self.OnCancel, self.panel_buttons.cancel )
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  self.panel_buttons.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.panel_buttons.save)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.panel_buttons.refresh )
        
       
        tc = (self.txt_ctrl_details_records,
              self.txt_ctrl_details_total)
        
        for t in tc: t.SetEditable(False)
        self.__layout()
        
    def __layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_details         = wx.BoxSizer(wx.VERTICAL)
        sizer_details_bottom  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_details_bottom.Add(self.txt_ctrl_details_records, 1, 0, 0)
        sizer_details_bottom.Add(self.txt_ctrl_details_total,   0, 0, 0)
        self.panel_details_botttom.SetSizer(sizer_details_bottom)
        
        sizer_details.Add(self.details_list,          1, wx.EXPAND, 0)
        sizer_details.Add(self.panel_details_botttom, 0, wx.EXPAND, 0)
        self.panel_details.SetSizer(sizer_details)
        
        sizer_main.Add(self.label_details,  0, 0, 0)
        sizer_main.Add(self.panel_details,  1, 0, 0)
        sizer_main.Add(self.panel_buttons,  0, 0, 0)
        self.SetSizer(sizer_main)
        
    def OnNew(self, evt):
        #rint'prpr OnNew'
        evt.Skip()
        
    def OnEdit(self, evt):
        #rint'prpr OnEdit'
        evt.Skip()
        
    def OnDelete(self, evt):
        evt.Skip()
        #rint'rppr OnDelete'
        
    def OnSave(self, evt):
        evt.Skip()
        #rint'rppr OnSave'
        
    def OnCancel(self, evt):
        #rint'prpr OnCancel'
        evt.Skip()
        
    def OnRefresh(self, evt):
        evt.Skip()
        #rint'prpr OnRefresh'  
        
        
        
        
        
        
        
        
        
        
class panel_registration_payment_records(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.panel_student_list     = panel_student_list(self, -1)#scrolled.ScrolledPanel(self, -1, style=wx.EXPAND)
        self.panel_details          = payment_details(self, -1)
        
        self.__set_properties() 
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        pass
 
    def __do_layout(self):
        sizer_main  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_main.Add(self.panel_student_list, 1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_details,      0, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.displayData()
        
    def displayData(self):
        return
    
        
    def lockdown(self):
        self.panel_student_list.Enable(False)
    
    def unlockdown(self):
        self.panel_student_list.Enable()
        
