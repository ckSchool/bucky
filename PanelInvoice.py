import wx, gVar, fetch, loadCmb

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from wx.lib.masked    import NumCtrl

from PanelInvoiceItem import PanelInvoiceItem

iid_list = []

class PanelInvoice(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_inv_heading   = wx.Panel(self, -1)
        self.label_qnty          = wx.StaticText(self.panel_inv_heading, -1, "Qnty     Account")
        self.label_description   = wx.StaticText(self.panel_inv_heading, -1, "Description")
        self.panel_header_spc    = wx.Panel(self.panel_inv_heading, -1)
        self.label_price         = wx.StaticText(self.panel_inv_heading, -1, "Price")
        self.label_mTotal        = wx.StaticText(self.panel_inv_heading, -1, "Total")
        
        self.panel_invoice_items = wx.Panel(self, -1)
        
        self.static_line         = wx.StaticLine(self, -1)
        self.panel_bottom        = wx.Panel(self, -1)
        self.button_new_item     = wx.Button(self.panel_bottom, -1, "+")
        self.choice_product      = wx.Choice(self.panel_bottom, -1, choices=[])
        self.label_l_tot         = wx.StaticText(self.panel_bottom, -1, "Total")
        self.text_ctrl_total     = NumCtrl(self.panel_bottom,   -1, "0", style= wx.TE_READONLY)
        self.button_enter        = wx.Button(self, -1, "Enter Invoice")

        pub.subscribe(self.updateTotal, 'update.invTotal')
        
        self.Bind(wx.EVT_BUTTON, self.OnNewItem, self.button_new_item)
        self.Bind(wx.EVT_BUTTON, self.OnEnter,   self.button_enter)
        
        self.__set_properties()
        self.__do_layout()
        
        self.invoice_id = 0
        
        sql = "SELECT id, name FROM products"
        loadCmb.gen(self.choice_product, sql)

    def __set_properties(self):
        self.label_qnty.SetBackgroundColour((47, 47, 47))
        self.label_qnty.SetForegroundColour((255, 255, 255))
        self.label_qnty.SetFont(wx.Font(10,   wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        self.label_description.SetMinSize((70, 16))
        self.label_description.SetBackgroundColour((47, 47, 47))
        self.label_description.SetForegroundColour((255, 255, 255))
        self.label_description.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        self.panel_header_spc.SetBackgroundColour((47, 47, 47))
        
        self.label_price.SetMinSize((30, 16))
        self.label_price.SetBackgroundColour((47, 47, 47))
        self.label_price.SetForegroundColour((255, 255, 255))
        self.label_price.SetFont(wx.Font(10,  wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        self.label_mTotal.SetBackgroundColour((47, 47, 47))
        self.label_mTotal.SetForegroundColour((255, 255, 255))
        self.label_mTotal.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL,    0, ""))
        self.panel_inv_heading.SetBackgroundColour((47, 47, 47))
        self.button_new_item.SetMinSize((23, 23))
        self.label_l_tot.SetFont(wx.Font(14,     wx.DEFAULT, wx.NORMAL, wx.BOLD,   0, ""))
        self.text_ctrl_total.SetMaxSize((140, -1))
        self.text_ctrl_total.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD,   0, ""))
        self.panel_bottom.SetFont(wx.Font(8,     wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.button_enter.SetMinSize((100, 30))
        self.button_enter.SetFont(wx.Font(11,  wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
 
        self.choice_product.SetMaxSize((-1, 23))
        
    def __do_layout(self):
        sizer_inv_heading = wx.BoxSizer(wx.HORIZONTAL)
        sizer_inv_heading.Add(self.label_qnty,        0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL,  40)
        sizer_inv_heading.Add(self.label_description, 0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL,  80)
        sizer_inv_heading.Add(self.label_price,       0,  wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 240)
        sizer_inv_heading.Add(self.panel_header_spc,  1,  wx.TOP  | wx.BOTTOM | wx.EXPAND, 4)
        sizer_inv_heading.Add(self.label_mTotal,      0, wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.panel_inv_heading.SetSizer(sizer_inv_heading)
        
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bottom.Add(self.button_new_item,  0, 0, 0)
        sizer_bottom.Add(self.choice_product,   1, wx.EXPAND, 0)
        sizer_bottom.Add(self.label_l_tot,      0, wx.ALIGN_RIGHT, 0)
        sizer_bottom.Add(self.text_ctrl_total,  0, wx.RIGHT, 5)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_inv_items = wx.BoxSizer(wx.VERTICAL)
        self.panel_invoice_items.SetSizer(sizer_inv_items)
        
        sizer_inv = wx.BoxSizer(wx.VERTICAL)
        sizer_inv.Add(self.panel_inv_heading,   0, wx.EXPAND, 0)
        sizer_inv.Add(self.panel_invoice_items, 0, wx.EXPAND, 0)
        sizer_inv.Add(self.static_line,         0, wx.EXPAND, 0)
        sizer_inv.Add(self.panel_bottom,        0, wx.EXPAND | wx.ALL, 3)
        sizer_inv.Add(self.button_enter,      0, wx.ALL | wx.ALIGN_RIGHT, 20)
        self.SetSizer(sizer_inv)
        sizer_inv.Fit(self)
        
        self.number_of_inv_items = 0
        self.sizer_inv_items = sizer_inv_items
    
    def displayData(self, student_id):
        #rint'PanelInvoice - displayData'
        self.student_id = student_id
        iid_list = []

    def removeMe(self, pnl):
        if self.sizer_inv_items.GetItemCount():
            index = self.sizer_inv_items.GetItemIndex(pnl)

            if self.sizer_inv_items.GetChildren():
                iid_list.pop(index)
                self.sizer_inv_items.Hide(index)
                self.sizer_inv_items.Remove(index)
                self.number_of_inv_items -= 1
                self.panel_invoice_items.Layout()
                self.panel_invoice_items.Fit()
                self.Fit()
                self.Layout()
                

            
    def OnNewItem(self, event):
        iid = fetch.cmbID(self.choice_product)
        if not iid in iid_list:
            iid_list.append(iid)
            #iid   = fetch.cmbValue(self.choice_product)

            self.number_of_inv_items += 1
            
            name = "inv%s" % self.number_of_inv_items
            new_inv_item = PanelInvoiceItem(self.panel_invoice_items, -1)
            
            new_inv_item.displayData(iid, self.student_id)
            
            self.sizer_inv_items.Add(new_inv_item, 0, wx.TOP | wx.BOTTOM, 5)
            self.panel_invoice_items.Layout()
            self.panel_invoice_items.Fit()
            self.updateTotal()
            
            self.GetTopLevelParent().onAdd()
            
        
    def OnEnter(self, event):
        #rint' OnEnter '
        # save and close
        sChildren = self.sizer_inv_items.GetChildren()
        inv_data=[]
        total_ammount = self.text_ctrl_total.GetValue()
        for child in sChildren:
            pnl  = child.GetWindow()
                                #  0       1           2     3   4      5    
            data = pnl.getData()#qnty, description, price, tax, net, account_id
            qnty, description, price, tax, net, account_id = data
            
            if data[0] and data[2] and data[4] :
                inv_data.append(data)
                
        
        if not inv_data:
            fetch.ask('no items to record')
            return
            
        sid, date, invoiceNo = self.GetParent().invoiceData()
        

        if self.sizer_inv_items.GetItemCount():
            ##rintself.invoice_id, invoiceNo, self.student_id
            
            ##rintdate, total_ammount, gVar.schYr
            """        
            sql = " INSERT INTO acc_invoices \
                            SET id=%d, ck_ref ='%s', student_id=%d,  \
                                date =%s, ammount = %d, schYr =%d" % (
                                self.invoice_id, invoiceNo, self.student_id,
                                date, total_ammount, gVar.schYr)"""
            
            ck_ref = fetch.ck_ref_last()
            self.ck_ref       = ck_ref
            
            sql = " INSERT INTO acc_invoices \
                            SET id, ck_ref, student_id, date, ammount, schYr \
                         VALUES (%d, '%s', %d, '%s', %d, %d)" % (
                                self.invoice_id, invoiceNo, gVar.student_id,
                                date, total_ammount, gVar.schYr)
            #rintsql
        
            sChildren = self.sizer_inv_items.GetChildren()
            for data in inv_data:
                
                """sql = "INSERT INTO invoice_items \
                          SET invoice_id =%d, \
                              quantity  =%d, description ='%s', \
                              price     =%d, discount    = 0,   tax_code =%d, \
                              net_total =%d, account_id  = %d" % (
                              self.invoice_id, data[0],
                              data[1], data[2],  data[3],
                              data[4], data[5])"""
                              
                discount = 0
                sql = "INSERT INTO invoice_items \
                               SET invoice_id, quantity, description, \
                                   price, discount, tax_code, net_total, account_id  \
                            VALUES (%d, %d, '%s', \
                                    %d, %d,  %d, %d, %d)" % (
                                    self.invoice_id, data[0],data[1],
                                    data[2], discount, data[3], data[4], data[5])
                #rintsql
                #fetch.updateDB(sql)
            
    def updateTotal(self):
        grandTotal=0
        if self.sizer_inv_items.GetItemCount():
            sChildren = self.sizer_inv_items.GetChildren()
            for child in sChildren:
                pnl  = child.GetWindow()
                data = pnl.getData()
                net  = data[4]
                grandTotal += int(net)
            grandTotal = ("{:,.0f}".format(grandTotal))
            self.text_ctrl_total.SetValue(grandTotal)
