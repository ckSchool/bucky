import wx, fetch, loadCmb,  datetime

from DateCtrl      import DateCtrl
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import wx.grid as gridlib

class gridLedger(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        self.CreateGrid(5, 6)
 
        self.DisableDragRowSize()
        self.DisableDragColSize()
        
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.currentRow = 0

    def setRowCursor(self, r):
        self.SetRowLabelValue(self.currentRow, '')
        self.currentRow = r
        self.SetRowLabelValue(r, '>')
        
    def OnLabelLeftClick(self, evt):
        r, c, p = evt.GetRow(), evt.GetCol(), evt.GetPosition()
        if r>-1:
            self.setRowCursor(r)
            self.GetParent().GetParent().OnSelectCell(evt)
            evt.Skip()
            
    def OnSelectCell(self, evt):
        r, c = evt.GetRow(), evt.GetCol()
        self.setRowCursor(r)
        pos =(r,c)
        pub.sendMessage('ledger.item_selected', pos=pos)
        
        
class panel_ledger(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_top  = wx.Panel(self, -1)
        
        self.panel_top_left   = wx.Panel(self, -1)
        self.panel_top_dates  = wx.Panel(self, -1)
        self.panel_top_saldo  = wx.Panel(self, -1)

        self.label_heading    = wx.StaticText(self.panel_top_left, -1, "LEDGER") #, style=wx.ALIGN_CENTER_HORIZONTAL)
        self.panel_filter     = wx.Panel(self.panel_top_left, -1)
        
        self.label_period         = wx.StaticText(self.panel_top_dates, -1, "Period")
        self.panel_period         = wx.Panel(self.panel_top_dates, -1)
        
        self.label_account        = wx.StaticText(self.panel_filter, -1, "Account")
        self.choice_account       = wx.Choice(self.panel_filter,     -1, choices=[])
        
        self.datepicker_ctrl_from = DateCtrl(self.panel_period, -1)
        self.label_to             = wx.StaticText(self.panel_period, -1, "s/d")
        self.datepicker_ctrl_to   = DateCtrl(self.panel_period, -1)
        
        self.label_balance             = wx.StaticText(self.panel_top_saldo, -1, "Start Balance")
        self.text_ctrl_opening_balance = wx.TextCtrl(self.panel_top_saldo,   -1, "", style=wx.ALIGN_RIGHT)
        self.label_closing_balance     = wx.StaticText(self.panel_top_saldo, -1, "End Balance")
        self.text_ctrl_closing_balance = wx.TextCtrl(self.panel_top_saldo,   -1, "", style=wx.ALIGN_RIGHT)
        
        self.panel_list             = wx.Panel(self, -1, style = wx.SIMPLE_BORDER)

        self.grid                   = gridLedger(self.panel_list)#grid(self.panel_list, style = wx.LC_HRULES | wx.LC_VRULES |wx.LC_SINGLE_SEL)
        self.panel_list_status      = wx.Panel(self.panel_list, -1)#, style = wx.SUNKEN_BORDER)
        self.text_ctrl_records      = wx.TextCtrl(self.panel_list_status,   -1, "", style = wx.SIMPLE_BORDER)
        self.text_ctrl_credit_total = wx.TextCtrl(self.panel_list_status,   -1, "", style = wx.SIMPLE_BORDER | wx.ALIGN_RIGHT)
        self.text_ctrl_debit_total  = wx.TextCtrl(self.panel_list_status,   -1, "", style = wx.SIMPLE_BORDER | wx.ALIGN_RIGHT)
        self.list_spc               = wx.StaticText(self.panel_list_status, -1, "")
        
        self.panel_bottom           = wx.Panel(self, -1)
        self.label_ref_ck           = wx.StaticText(self.panel_bottom,    -1, "CK Ref.")
        self.text_ctrl_ref_ck       = wx.TextCtrl(self.panel_bottom,      -1, "")
        self.label_ref_supplier     = wx.StaticText(self.panel_bottom,    -1, "Supplier Ref.")
        self.text_ctrl_ref_supplier = wx.TextCtrl(self.panel_bottom,      -1, "")
        self.button_refresh         = wx.Button(self.panel_bottom,        -1, "Refresh")
        self.label_spc              = wx.StaticText(self.panel_bottom,    -1, "")
        
        tc = (self.text_ctrl_opening_balance, self.text_ctrl_closing_balance,
              self.text_ctrl_credit_total, self.text_ctrl_debit_total, 
              self.text_ctrl_ref_ck, self.text_ctrl_ref_supplier, self.text_ctrl_records)
        for t in tc: t.SetEditable(False),
        
        self.Bind(wx.EVT_CHOICE, self.OnAccountSelected, self.choice_account)
        pub.subscribe(self.DateChange,   'DateCtrl.date_change')
        pub.subscribe(self.OnSelectCell, 'ledger.item_selected')
        
        self.__set_properties()
        self.__do_layout()
        
        self._do_main()
        
    def setupGrid(self , colHeadings):
        col = 0
        for h in colHeadings:
            self.grid.SetColLabelValue(col, h[0])
            self.grid.SetColSize(col, h[1])
            col+= 1
    
        self.grid.DisableDragColSize() 
        self.grid.EnableEditing(False) 
        self.grid.SetRowLabelSize(23)
        self.grid.ForceRefresh()
        
    def __set_properties(self):
        self.panel_top.SetMinSize((-1, 50))
        self.panel_top.SetMaxSize((-1, 50))
        colHeadings = ( ('',            00),
                        ('Date',        90),
                        ('Transaction',640),
                        ('Details',    0),
                        ('Debit',       70),
                        ('Credit',      70) )
                    
        self.setupGrid(colHeadings)
        
        self.panel_list.SetMaxSize((940,-1))

        self.text_ctrl_debit_total.SetMinSize((70,-1))
        self.text_ctrl_credit_total.SetMinSize((70,-1))
        
        self.text_ctrl_opening_balance.SetMinSize( (120,-1))
        self.text_ctrl_closing_balance.SetMinSize((120,-1))
        
        self.list_spc.SetMinSize((18, -1))
        self.choice_account.SetMinSize((230, 21))

    def __do_layout(self):
        sizer_main    = wx.BoxSizer(wx.VERTICAL)
        sizer_top       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top_left  = wx.BoxSizer(wx.VERTICAL)
        sizer_top_dates = wx.BoxSizer(wx.VERTICAL)
        sizer_period    = wx.BoxSizer(wx.HORIZONTAL)
        
  
        sizer_saldo     = wx.FlexGridSizer(2, 2, 3, 3)
        sizer_filter    = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_list_status = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_list      = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom    = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top.Add(self.panel_top_left,  0, 0, 0)
        sizer_top.Add(self.panel_top_dates, 0, 0, 0)
        sizer_top.Add(self.panel_top_saldo, 0, 0, 0)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_filter.Add(self.label_account,  0, 0, 0)
        sizer_filter.Add(self.choice_account, 0, 0, 0)
        self.panel_filter.SetSizer(sizer_filter)
        
        sizer_top_dates.Add(self.label_period, 0, 0, 0)
        sizer_top_dates.Add(self.panel_period, 0, 0, 0)
        self.panel_top_dates.SetSizer(sizer_top_dates)
        
        sizer_period.Add(self.datepicker_ctrl_from, 0, 0, 0)
        sizer_period.Add(self.label_to,             0, wx.LEFT, 5)
        sizer_period.Add(self.datepicker_ctrl_to,   0, 0, 0)
        self.panel_period.SetSizer(sizer_period)
        
        sizer_saldo.Add(self.label_balance,             0, 0, 0)
        sizer_saldo.Add(self.text_ctrl_opening_balance, 0, 0, 0)
        sizer_saldo.Add(self.label_closing_balance,     0, 0, 0)
        sizer_saldo.Add(self.text_ctrl_closing_balance, 0, 0, 0)
        self.panel_top_saldo.SetSizer(sizer_saldo)
        
        sizer_top_left.Add(self.label_heading, 0, 0, 0)
        sizer_top_left.Add(self.panel_filter)
        self.panel_top_left.SetSizer(sizer_top_left)

        sizer_bottom.Add(self.label_ref_ck,           0, 0, 0)
        sizer_bottom.Add(self.text_ctrl_ref_ck,       0, 0, 0)
        sizer_bottom.Add(self.label_ref_supplier,     0, 0, 0)
        sizer_bottom.Add(self.text_ctrl_ref_supplier, 0, 0, 0)
        sizer_bottom.Add(self.label_spc,              0, 0, 0)
        sizer_bottom.Add(self.button_refresh,         0, 0, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_list_status.Add(self.text_ctrl_records,      1, 0, 0)
        sizer_list_status.Add(self.text_ctrl_credit_total, 0, 0, 0)
        sizer_list_status.Add(self.text_ctrl_debit_total,  0, 0, 0)
        sizer_list_status.Add(self.list_spc,               0, wx.EXPAND, 0)
        self.panel_list_status.SetSizer(sizer_list_status)
        
        sizer_list.Add(self.grid,               1, wx.EXPAND, 0)
        sizer_list.Add(self.panel_list_status,  0, wx.EXPAND, 0)
        self.panel_list.SetSizer(sizer_list)
        
        sizer_main.Add(self.panel_top,    0, wx.EXPAND | wx.BOTTOM | wx.LEFT, 5)
        sizer_main.Add(self.panel_list,   1, wx.EXPAND | wx.LEFT, 5)
        sizer_main.Add(self.panel_bottom, 0, wx.EXPAND | wx.LEFT, 5)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
         
    def _do_main(self):
        sql = "SELECT id, name FROM acc_accounts "
        loadCmb.gen(self.choice_account, sql)
        #rintsql
        self.dateTo   = datetime.date.today()
        self.dateFrom = self.dateTo - datetime.timedelta(days=365)
        
        self.datepicker_ctrl_from.SetValue(self.dateFrom)
        self.datepicker_ctrl_to.SetValue(self.dateTo)
        
        
    def getVars(self):
        if self.dateTo:
            newto = self.dateTo + datetime.timedelta(days=1)
            y, m, d = newto.year, newto.month, newto.day
            dateto  = '%d-%d-%d' % (y, m, d)
        else:
            dateto = ''
            
        if self.dateFrom:
            y, m, d = self.dateFrom.year, self.dateFrom.month, self.dateFrom.day
            datefrom  = '%d-%d-%d' % (y, m, d)
        else:
            datefrom = ''
        
        account_id = fetch.cmbID(self.choice_account)
        
        return (account_id, datefrom, dateto)
        
    def displayData(self):
        account_id, datefrom, dateto = self.getVars()
        #rint'displayData', account_id, datefrom, dateto
        if datefrom and dateto:
            sql = "SELECT j.id, j.transaction_date, j.title,  j.details, \
                   FORMAT(IIF (ji.debit = True,  ji.amount,), '#,##0') AS Debit  , \
                   FORMAT(IIF (ji.debit = False, ji.amount,), '#,##0') AS Credit \
                     FROM acc_journal j \
                     JOIN acc_journal_items d ON j.id = ji.journal_id \
                     JOIN acc_supliers      s ON j.supplier_id = s.id \
                    WHERE j.transaction_date BETWEEN '%s' AND '%s' \
                      AND j.account_id = %d \
                    ORDER BY j.transaction_date ASC " % (datefrom, dateto, account_id)
         
        elif datefrom and not dateto:
            sql = "SELECT j.id, j.transaction_date, j.title,  j.details, \
                            FORMAT(IIF (ji.debit = True,  ji.amount,), '#,##0') AS Debit  , \
                            FORMAT(IIF (ji.debit = False, ji.amount,), '#,##0') AS Credit \
                     FROM acc_journal j \
                     JOIN acc_journal_items d ON j.id = ji.journal_id \
                     JOIN acc_supliers      s ON j.supplier_id = s.id \
                    WHERE j.transaction_date => '%s' \
                      AND j.account_id = %d \
                    ORDER BY j.transaction_date ASC" % (datefrom, account_id)
            
        elif not datefrom and dateto:
            sql = "SELECT j.id, j.transaction_date, j.title,  j.details, \
                            FORMAT(IIF (ji.debit = True,  ji.amount,), '#,##0') AS Debit  , \
                            FORMAT(IIF (ji.debit = False, ji.amount,), '#,##0') AS Credit \
                    FROM acc_journal  j \
                    JOIN acc_journal_items d ON j.id = ji.journal_id \
                    JOIN acc_supliers      s ON j.supplier_id = s.id \
                   WHERE j.transaction_date <= '%s' \
                    AND  j.account_id = %d \
                    ORDER BY j.transaction_date ASC" % (dateto, account_id)
            
        else:
            sql = "SELECT j.id, j.transaction_date, j.title,  j.details, \
                            FORMAT(IIF (ji.debit = True,  ji.amount,), '#,##0') AS Debit  , \
                            FORMAT(IIF (ji.debit = False, ji.amount,), '#,##0') AS Credit \
                     FROM acc_journal  j \
                     JOIN acc_journal_items  d ON j.id = ji.journal_id \
                     JOIN acc_supliers       s ON j.supplier_id = s.id  \
                      AND j.account_id = %d \
                    ORDER BY j.transaction_date ASC" % (account_id,)
         
        res = fetch.getAllDict(sql)
        self.records = len(res)
        #rint sql,  self.records
        #rint res
        
        if self.records:
            txt = "Record: 1/%d " % self.records
        else:
            txt = "Record: 0/0 "
        self.text_ctrl_records.SetLabelText(txt)
        
        self.records  = len(res)
        gridrows = self.grid.GetNumberRows()
        
        pos = 0
        if gridrows > self.records:
            extrarows = gridrows - self.records
            self.grid.DeleteRows(pos, extrarows)
        else:
            extrarows = self.records - gridrows 
            self.grid.InsertRows(pos, extrarows)
            
        self.Layout()
            
        rowNo = 0
        
        for row in res:
            #rint row
            Kode, date, Transaksi, Keterangan, Debit, Credit  = row['id'], row['Expr1001'], row['title'], row['details'], row['Debit'], row['Credit'], 
            self.grid.SetRowLabelValue(rowNo, '')
            
            self.grid.SetCellValue(rowNo, 0, str(Kode))
            self.grid.SetCellValue(rowNo, 1, str(date))
            self.grid.SetCellValue(rowNo, 2, str(Transaksi)+str(Keterangan))
            #self.grid.SetCellValue(rowNo, 3, str(Keterangan))
            self.grid.SetCellValue(rowNo, 4, str(Debit))
            self.grid.SetCellValue(rowNo, 5, str(Credit))
            
            self.grid.SetCellAlignment(rowNo, 4, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            self.grid.SetCellAlignment(rowNo, 5, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            rowNo += 1
        
        self.text_ctrl_opening_balance.SetValue(self.digitgroup(self._getStartBalance(account_id, datefrom, dateto )))
        self.text_ctrl_closing_balance.SetValue(self.digitgroup(self._GetEndBalance(account_id, datefrom, dateto )))
        
        credit = self.digitgroup(self._sumCredit(account_id, datefrom, dateto ))
        
        debit = self.digitgroup(self._sumDebit(account_id, datefrom, dateto ))
        
        self.text_ctrl_credit_total.SetValue(credit)
        self.text_ctrl_debit_total.SetValue(debit)
    
    def intWithCommas(self, x):
        if type(x) not in [type(0), type(0L)]:
            raise TypeError("Parameter must be an integer.")
        if x < 0:
            return '-' + intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)


    def digitgroup(self, x):
        if type(x) not in [type(0), type(0L)]:
            raise TypeError("Parameter must be an integer.")
        if x < 0:
            return '-' + self.intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)
    
    def _sumDebit(self, account_id, datefrom, dateto ):
        if datefrom and dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal  j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date BETWEEN '%s' AND '%s' \
                      AND ji.account_id = %d \
                      AND ji.debit = True  " % (datefrom, dateto, account_id)
            
        elif datefrom and not dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date > '%s \
                      AND ji.account_id = %d \
                      AND ji.debit = True  " % (datefrom, account_id)
        elif not datefrom and dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal  j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date < '%s' \
                      AND ji.account_id = %d \
                      AND ji.debit = True  " % (dateto, account_id)
        else:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal  j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE ji.account_id = %d \
                      AND ji.debit = True  " % (account_id,)
        return fetch.getSum(sql)
    
    def _sumCredit(self,account_id, datefrom, dateto ):
        if datefrom and dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal j \
                     JOIN journal_items ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date BETWEEN '%s' AND '%s' \
                      AND ji.account_id = %d \
                      AND ji.debit = False  " % (datefrom, dateto, account_id)
            
        elif datefrom and not dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal  j \
                     JOIN acc_journal_items  ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date > '%s' \
                      AND ji.account_id = %d \
                      AND ji.debit = False  " % (datefrom, account_id)
            
        elif not datefrom and dateto:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE j.transaction_date < AND '%s' \
                      AND ji.account_id = %d \
                      AND ji.debit = False  " % (dateto, account_id)
        else:
            sql = "SELECT SUM(ji.amount) \
                     FROM acc_journal  j \
                     JOIN acc_journal_items ji ON j.id = ji.journal_id \
                    WHERE ji.account_id = %d \
                      AND ji.debit = False  " % (account_id,)
        return fetch.getSum(sql)
        
    def OnAccountSelected(self, evt):
        self.displayData()
        
    def DateChange(self):
        #rint'DateChange'
        self.dateTo   = self.datepicker_ctrl_to.GetDbReadyValue()
        self.dateFrom = self.datepicker_ctrl_from.GetDbReadyValue()
        self.displayData()
        
    def _getStartBalance(self, account_id, datefrom, dateto ):
        #rint'_getStartBalance' , account_id, datefrom, dateto
        sql = "SELECT SUM(ji.amount) \
                 FROM acc_journal  j \
                 JOIN acc_journal_items  d ON j.id = ji.journal_id \
                WHERE ji.account_id = %d" % account_id
        
        if datefrom:
            sql += "  AND j.transaction_date < '%s' " % datefrom

        sqldebit  = sql + " AND ji.debit =  True "
        sqlcredit = sql + " AND ji.debit =  False"
        
        debit  = fetch.getSum(sqldebit)
        credit = fetch.getSum(sqlcredit)
        #rint'debit', debit,'     credit',credit
        return (credit-debit)
    
    def _GetEndBalance(self, account_id, datefrom, dateto ):
        sql = "SELECT SUM(ji.amount) \
                 FROM acc_journal j \
                 JOIN acc_journal_items d ON j.id = ji.acc_journal_id \
                WHERE ji.account_id = %d" % account_id
        if dateto:
            sql += " AND   j.transaction_date < '%s' " % dateto
        
        sqldebit  = sql + " AND ji.debit =  True "
        sqlcredit = sql + " AND ji.debit =  False"
        
        return (fetch.getSum(sqlcredit)-fetch.getSum(sqldebit))
    
    def OnSelectCell(self, pos):
        #rint'OnSelectCell', pos
        row, col = pos
        if not row or not col: return
        
        sid = self.grid.GetCellValue(row, 0)
        txt = 'Record: %s/%s' % (row+1, self.records)
        self.text_ctrl_records.SetValue(txt)
        
        
        if sid:
            sql = "SELECT ck_ref,  supplier_ref \
                     FROM acc_journal  \
                    WHERE id = %d" % int(sid)
            res = fetch.getOneDict(sql)
            #rintsql, res
            if res:
                ck_ref,  supplier_ref = res['ck_ref'], res['supplier_ref']
                self.text_ctrl_ref_ck.SetValue(str(ck_ref))
                self.text_ctrl_ref_supplier.SetValue(str(supplier_ref))

 
