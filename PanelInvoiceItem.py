import wx, gVar, loadCmb, fetch
from wx.lib.pubsub       import setupkwargs
from wx.lib.pubsub       import pub

from wx.lib.masked import NumCtrl
from MyChoice      import MyChoice as P_Choice

import DlgEditNewAccounts as DlgNewEditAccount

class PanelInvoiceItem(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.panel_item_left        = wx.Panel(self, -1)
        self.panel_qnty             = wx.Panel(self.panel_item_left, -1)
        self.button_delete          = wx.BitmapButton(self.panel_qnty, -1, wx.Bitmap(".\\images\\16\\New folder\\editorLine.gif", wx.BITMAP_TYPE_ANY))
        self.num_ctrl_qnty          = NumCtrl(self.panel_qnty, -1, 1)
        self.combo_box_account      = P_Choice(self.panel_qnty, -1)
        self.label_save_as_item     = wx.StaticText(self.panel_item_left, -1, "-")
        self.text_ctrl_description  = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_LINEWRAP | wx.TE_READONLY)
        self.panel_item_total       = wx.Panel(self, -1)
        self.num_ctrl_price         = NumCtrl(self.panel_item_total, -1,  style = wx.TE_READONLY)
        self.combo_box_tax          = wx.ComboBox(self.panel_item_total, -1, choices=[], style=wx.CB_DROPDOWN)
        
        self.panel_spc1             = wx.StaticText(self, -1, ' ')
        
        self.panel_total            = wx.Panel(self, -1)
        self.num_ctrl_total         = NumCtrl( self.panel_total, -1, style = wx.TE_READONLY)
        self.combo_box_pay_method   = wx.Choice(self.panel_total, -1, choices=[])#= wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        self.Layout()
        
        self.Bind(wx.EVT_TEXT_ENTER, self.qntyUpdated, self.num_ctrl_qnty)
        
        self.Bind(wx.EVT_BUTTON,   self.OnRemove,    self.button_delete)
        self.Bind(wx.EVT_COMBOBOX, self.OnAccount,   self.combo_box_account)
        self.Bind(wx.EVT_COMBOBOX, self.OnTax,       self.combo_box_tax)
        self.Bind(wx.EVT_TEXT,     self.qntyUpdated, self.num_ctrl_qnty)
        self.Bind(wx.EVT_TEXT,     self.updateTotal, self.num_ctrl_price)
        
        self.__do_main()
        
    
    def __set_properties(self):
        self.button_delete.SetSize(self.button_delete.GetBestSize())
        self.num_ctrl_qnty.SetMinSize( (50, -1))
        self.combo_box_account.SetMinSize((120, 21))
        self.label_save_as_item.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.text_ctrl_description.SetMinSize((300, 45))
        self.num_ctrl_price.SetMinSize((120, 21))
        self.combo_box_tax.SetMinSize(  (120, 21))
        self.num_ctrl_total.SetMinSize((120, -1))
        self.num_ctrl_qnty.SetMin(1)

    def __do_layout(self):       
        sizer_qnty       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_item_qnty  = wx.BoxSizer(wx.VERTICAL)
        sizer_item_price = wx.BoxSizer(wx.VERTICAL)
        sizer_item       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_total      = wx.BoxSizer(wx.VERTICAL)
        
        sizer_qnty.Add(self.button_delete, 0, wx.LEFT, 5)
        sizer_qnty.Add(self.num_ctrl_qnty,      0, wx.LEFT, 5)
        sizer_qnty.Add(self.combo_box_account,  0, wx.LEFT, 5)
        self.panel_qnty.SetSizer(sizer_qnty)
        
        sizer_item_qnty.Add(self.panel_qnty,         0, wx.EXPAND, 0)
        sizer_item_qnty.Add(self.label_save_as_item, 0, 0, 0)
        self.panel_item_left.SetSizer(sizer_item_qnty)
        
        sizer_item_price.Add(self.num_ctrl_price, 0, wx.BOTTOM, 5)
        sizer_item_price.Add(self.combo_box_tax,   0, 0, 0)
        self.panel_item_total.SetSizer(sizer_item_price)
        
        sizer_total.Add(self.num_ctrl_total,       0, 0, 0)
        sizer_total.Add(self.combo_box_pay_method, 0, wx.EXPAND, 0)
        self.panel_total.SetSizer(sizer_total)
        
        sizer_item.Add(self.panel_item_left,       0, wx.EXPAND, 0)
        sizer_item.Add(self.text_ctrl_description, 0, wx.LEFT | wx.RIGHT, 10)
        sizer_item.Add(self.panel_item_total,      0, wx.EXPAND, 0)
        sizer_item.Add(self.panel_spc1,            1, wx.EXPAND, 0)
        sizer_item.Add(self.panel_total,        1, wx.ALIGN_RIGHT | wx.RIGHT, 5)
        self.SetSizer(sizer_item)
        
    def __do_main(self):
        print ' do main'
        
        methods = {1:'Cash', 2:'Mandiri'}
        for key in methods:
            self.combo_box_pay_method.Append(methods[key], key)
        self.combo_box_pay_method.Select(0)
        self.combo_box_tax.Select(1)
        self.product_id = 0
        
        loadCmb.tax(self.combo_box_tax)

        sql ="SELECT id, name \
                FROM acc_accounts \
               WHERE %d <= closed_yr" % gVar.schYr
        self.combo_box_account.initChoices(sql, 'New Account', DlgNewEditAccount)
    
    
    def qntyUpdated(self,evt):
        qnty = self.num_ctrl_qnty.GetValue()

        if qnty <1: self.num_ctrl_qnty.SetValue(1)
        
        if self.Monthly:
            self.doMonthly(qnty)

        self.updateTotal(evt)
        
    def doMonthly(self, qnty):
        self.monthTo = self.monthFrom + qnty -1

        if self.monthTo > 12:
            self.num_ctrl_qnty.SetValue(1)
            self.monthTo = self.monthFrom + 1
            
        MonthFrom = gVar.monthNames[self.monthFrom]
        description, price = fetch.product_details(self.product_id)
        
        if qnty == 1:
            description = "%s : %s" % (description, MonthFrom)
        else:
            MonthTo = gVar.monthNames[self.monthTo]
            description = "%s : %s to %s" % (description, MonthFrom, MonthTo)
            
        self.text_ctrl_description.SetValue(description) 
        
    def isMonthly(self, iid):
        sql = "SELECT * \
                 FROM acc_products \
                WHERE id = %d \
                  AND recurring_monthly = 1" % iid
        
        if fetch.getCount(sql)>0:
            self.Monthly = True
        else:
            self.Monthly = False
            
        return self.Monthly
        
    def handle_keypress(self, event):
        keycode = event.GetKeyCode()
        if keycode < 255:
            if chr(keycode).isalnum():# Valid alphanumeric character
                event.Skip()
                
    def displayData(self, iid, student_id):
        print 'displayData', iid, student_id
        
        self.product_id = iid
        
        description, price = fetch.product_details(iid)
        
        self.student_id = student_id
        NoInduk = fetch.NoInduk(student_id, gVar.schYr)
        
        if self.isMonthly(iid):
            
            monthFrom = self.getMonthFrom()
            print 'gVar.monthNames[monthFrom]', gVar.monthNames[monthFrom]
            description += ' : ' + gVar.monthNames[monthFrom]
                
        self.text_ctrl_description.SetValue(description)
            
        #self.num_ctrl_qnty.SetValue(1)
        print 'price', price
        self.num_ctrl_price.SetValue(price)
    
    def getMonthFrom(self, ):
        sql = "SELECT MAX(ii.month_from) AS monthFrom, \
                      MAX(ii.month_to)   AS monthTo \
                     FROM acc_invoices i \
                     JOIN acc_invoice_items ii ON i.id = ii.invoice_id \
                    WHERE ii.product_id = %d \
                      AND i.student_id ='%s' \
                      AND i.schYr = %d " % (1, self.student_id, gVar.schYr)
            
        res = fetch.getOneDict(sql)
        print sql, res
        if res:
            monthFrom = res['monthFrom']
            monthTo   = res['monthTo']
            
            if monthTo: self.monthFrom = monthTo + 1
            else:       self.monthFrom = monthFrom + 1
            
        else:
            self.monthFrom = 1
        
        return self.monthFrom
            
                
    def OnRemove(self, event):
        self.GetGrandParent().removeMe(self)
        self.GetTopLevelParent().onAdd()

    def OnAccount(self, event):
        self.updateTotal()

    def OnTax(self, event):  
        self.updateTotal()
        
    def getData(self):
        description = self.text_ctrl_description.GetValue()
        qnty    = self.num_ctrl_qnty.GetValue()
        price   = self.num_ctrl_price.GetValue()
        account = self.combo_box_account.GetID()
        taxCode = fetch.cmbID(self.combo_box_tax)
        net     = qnty*price
        
        return (qnty, description, price,  taxCode, net, account)
    
    def updateTotal(self, evt=0):
        qnty, description, price, units, taxCode, net = self.getData()

        if taxCode == "Tax Included": tax = 0.10
        else: tax =0
        
        grose = price*qnty
        net   = grose - grose*tax
        
        net = ("{:,.0f}".format(net))
        self.num_ctrl_total.SetValue(net)
        
        self.Layout()
        pub.sendMessage('update.invTotal')