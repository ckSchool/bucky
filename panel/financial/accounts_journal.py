import wx, fetch, loadCmb, datetime

import DlgTransaction

import wx.grid as gridlib

from DateCtrl import DateCtrl
from my_ctrls import panel_buttons

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


#----------------------------------------------------------------------

class GridJournal(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        self.CreateGrid(12, 7)
 
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
            self.GetParent().OnSelectCell(evt)
            evt.Skip()
            
    def OnSelectCell(self, evt):
        self.row = evt.GetRow()
        self.col = evt.GetCol()
        self.setRowCursor(self.row )
        pub.sendMessage('acc_journal.cell_selected')
        #self.GetParent().GetParent().OnSelectCell(evt)
        evt.Skip()
        
    def get_location(self):
        return (self.row, self.col)
        
    def getSelectedTransactionID(self, ):
        row = self.GetGridCursorRow()
        return int(self.GetCellValue(row, 1))
    
    def groupTranactions(self, ):
        #return
        rows = self.GetNumberRows()
        
        col   = 1; colspread = 1; firstrow = 0
        transaction_id_1 = self.GetCellValue(firstrow, col)
        
        row = 0
        while row < rows:
            transaction_id_2 = self.GetCellValue(row, col)
            
            if row == rows-1 and row > firstrow:
                rowstogroup = row - firstrow + 1
                self.SetCellSize(firstrow, col, rowstogroup, colspread)
                self.SetCellSize(firstrow, col+1, rowstogroup, colspread)

            elif transaction_id_1 != transaction_id_2 and row > firstrow: 
                rowstogroup = row - firstrow
                self.SetCellSize(firstrow, col, rowstogroup, colspread)
                self.SetCellSize(firstrow, col+1, rowstogroup, colspread)
                firstrow = row
                transaction_id_1 = self.GetCellValue(firstrow, col)
            
            row = row + 1
    
    def groupDates(self, ):
        rows = self.GetNumberRows()
        if rows < 2: return
        
        col   = 0; colspread = 1; firstrow = 0
        date1 = self.GetCellValue(firstrow, 0)
        
        row = 1
        while row < rows:
            date2 = self.GetCellValue(row, 0)
            
            if row == rows-1 and row > firstrow:
                rowstogroup = row - firstrow + 1
                self.SetCellSize(firstrow, col, rowstogroup, colspread)

            elif date1 != date2 and row > firstrow: 
                rowstogroup = row - firstrow
                self.SetCellSize(firstrow, col, rowstogroup, colspread)
                firstrow = row
                date1 = self.GetCellValue(firstrow, 0)
            
            row = row + 1
            
        self.groupTranactions()

    def resize(self, res):
        self.ClearGrid()
        self.records  = len(res)
        
        gridrows  = self.GetNumberRows()
        rowdiff   = self.records - gridrows 
        
        if gridrows > self.records:
            #extrarows = gridrows - self.records
            self.DeleteRows(0, -1*rowdiff)
            
        else:
            self.InsertRows(0, rowdiff)

#----------------------------------------------------------
class betweenDates(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.label_from           = wx.StaticText(self,  -1, "Date")
        self.datepicker_ctrl_from = DateCtrl(self, -1)
        self.label_to             = wx.StaticText(self, -1, "to")
        self.datepicker_ctrl_to   = DateCtrl(self, -1)
        self.panel_spc1           = wx.Panel(self, -1)
        self.panel_spc2           = wx.Panel(self, -1)
        
        sizer_date.Add(self.label_from,  0, 0, 0)
        sizer_date.Add(self.datepicker_ctrl_from,  0, 0, 0)
        sizer_date.Add(self.label_to,              0, 0, 0)
        sizer_date.Add(self.datepicker_ctrl_to,    0, 0, 0)
        self.panel_date.SetSizer(sizer_date)





#----------------------------------------------------------
class panel_journal(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_top     = wx.Panel(self, -1)
        
        self.label_heading        = wx.StaticText(self.panel_top,  -1, "JOURNAL")
        self.panel_filter         = wx.Panel(self.panel_top, -1)
        self.label_date           = wx.StaticText(self.panel_filter, -1, "Date")
        self.panel_date           = wx.Panel(self.panel_filter,    -1)
        self.datepicker_ctrl_from = DateCtrl(self.panel_date,      -1)
        self.label_to             = wx.StaticText(self.panel_date, -1, "to")
        self.datepicker_ctrl_to   = DateCtrl(self.panel_date,      -1)
        self.panel_spc1           = wx.Panel(self.panel_filter,    -1)
        self.panel_spc2           = wx.Panel(self.panel_filter,    -1)
        
        self.checkbox_supplier    = wx.CheckBox(self.panel_filter, -1, "Supplier")
        self.choice_supplier      = wx.Choice(self.panel_filter,   -1,  choices=[])
        self.checkbox_division    = wx.CheckBox(self.panel_filter, -1, "Division")
        self.choice_acc_catagory  = wx.Choice(self.panel_filter,   -1,  choices=[])

        self.panel_grid   = wx.Panel(self, -1, style = wx.SIMPLE_BORDER)
        self.grid         = GridJournal(self.panel_grid)
        self.panel_totals = wx.Panel(self.panel_grid, -1)
        
        self.text_ctrl_records      = wx.TextCtrl(self.panel_totals,   -1,'', style = wx.SIMPLE_BORDER)
        self.text_ctrl_total_debit  = wx.TextCtrl(self.panel_totals,   -1,'', style = wx.SIMPLE_BORDER | wx.ALIGN_RIGHT)
        self.text_ctrl_total_credit = wx.TextCtrl(self.panel_totals,   -1,'', style = wx.SIMPLE_BORDER | wx.ALIGN_RIGHT)
        self.total_spc2             = wx.StaticText(self.panel_totals, -1,'')

        self.panel_bottom           = wx.Panel(self, -1)
        self.label_ck_ref           = wx.StaticText(self.panel_bottom, -1, "CK Ref.")
        self.txt_ctrl_ck_ref        = wx.TextCtrl(self.panel_bottom,   -1, " ")
        self.label_supplier_ref     = wx.StaticText(self.panel_bottom, -1, "Supplier Ref.")
        self.txt_ctrl_supplier_ref  = wx.TextCtrl(self.panel_bottom,   -1, " ")
        
        self.label_details    = wx.StaticText(self.panel_bottom, -1, "Details")
        self.txt_ctrl_details = wx.TextCtrl(self.panel_bottom,   -1, "")
        self.label_rspc1      = wx.StaticText(self.panel_bottom, -1, "")
        self.label_rspc2      = wx.StaticText(self.panel_bottom, -1, "")
        
        self.panel_buttons    = wx.Panel(self, -1)
        self.button_new       = wx.Button(self.panel_buttons, -1, "New")
        self.button_edit      = wx.Button(self.panel_buttons, -1, "Edit")
        self.button_refresh   = wx.Button(self.panel_buttons, -1, "Refresh")
        
        self.Bind(wx.EVT_BUTTON, self.OnNew,    self.button_new)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,   self.button_edit)
        
        tc = (self.txt_ctrl_ck_ref, self.txt_ctrl_supplier_ref, self.txt_ctrl_details)
        for t in tc: t.SetEditable(False)        
        
        self.checkbox_supplier.SetValue(True)
        self.checkbox_division.SetValue(True)
        
        pub.subscribe(self.DateChange, 'DateCtrl.date_change')
        pub.subscribe(self.OnSelectCell, 'acc_journal.cell_selected')
        
        self.Bind(wx.EVT_CHECKBOX, self.chk_division, self.checkbox_division)
        self.Bind(wx.EVT_CHECKBOX, self.chk_supplier, self.checkbox_supplier)
        
        self.Bind(wx.EVT_CHOICE, self.OnDivision, self.choice_acc_catagory)
        self.Bind(wx.EVT_CHOICE, self.OnSupplier, self.choice_supplier)
       
        self.__set_properties() 
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.choice_supplier.SetMinSize((100,-1))
        self.choice_acc_catagory.SetMinSize((100,-1))
        
        self.text_ctrl_total_debit.SetMinSize( (100, 23))
        self.text_ctrl_total_credit.SetMinSize((100, 23))
        
        colHeadings = (("Date", 70),("ID", 50),("Description", 454),("Section ID", 80),
                       ("Section", 200),("Debit", 100),("Credit", 100))
        self.setupGrid(colHeadings)
        
        self.panel_top.SetMinSize((-1, 55))
        self.panel_top.SetMaxSize((-1, 55))

    def __do_layout(self):
        sizer_journal  = wx.BoxSizer(wx.VERTICAL)
        sizer_grid     = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom   = wx.FlexGridSizer(2, 4, 10, 5)
        grid_sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        sizer_date     = wx.BoxSizer(wx.HORIZONTAL)
        sizer_totals   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top      = wx.BoxSizer(wx.VERTICAL)
        
        sizer_top.Add(self.label_heading, 0, wx.EXPAND, 0)
        sizer_top.Add(self.panel_filter,  0, wx.EXPAND | wx.ALL, 5)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_buttons.Add(self.button_new,     0, 0, 0)
        sizer_buttons.Add(self.button_edit,    0, 0, 0)
        sizer_buttons.Add(self.button_refresh, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_date.Add(self.datepicker_ctrl_from,  0, 0, 0)
        sizer_date.Add(self.label_to,              0, 0, 0)
        sizer_date.Add(self.datepicker_ctrl_to,    0, 0, 0)
        self.panel_date.SetSizer(sizer_date)
        
        grid_sizer_top.Add(self.label_date,        0, 0, 0)
        grid_sizer_top.Add(self.panel_date,        1, wx.EXPAND, 0)
        grid_sizer_top.Add(self.checkbox_supplier, 0, 0, 0)
        grid_sizer_top.Add(self.choice_supplier,   0, 0, 0)
        grid_sizer_top.Add(self.checkbox_division, 0, 0, 0)
        grid_sizer_top.Add(self.choice_acc_catagory,   0, 0, 0)
        self.panel_filter.SetSizer(grid_sizer_top)
        
        sizer_totals.Add(self.text_ctrl_records,      0, 0, 0)
        sizer_totals.Add(self.text_ctrl_total_debit,  0, 0, 0)
        sizer_totals.Add(self.text_ctrl_total_credit, 0, 0, 0)
        sizer_totals.Add(self.total_spc2,             0, 0, 0)
        self.panel_totals.SetSizer(sizer_totals)
        
        tx = (self.text_ctrl_records,self.text_ctrl_total_debit,self.text_ctrl_total_credit)
        for t in tx: t.SetEditable(False)
    
        sizer_bottom.Add(self.label_ck_ref,          0, 0, 0)
        sizer_bottom.Add(self.txt_ctrl_ck_ref,       0, wx.EXPAND, 0)
        
        sizer_bottom.Add(self.label_details,         0, 0, 0)
        sizer_bottom.Add(self.txt_ctrl_details,      0, wx.EXPAND, 0)
        
        sizer_bottom.Add(self.label_supplier_ref,    0, 0, 0)
        sizer_bottom.Add(self.txt_ctrl_supplier_ref, 0, wx.EXPAND, 0)
        
        sizer_bottom.Add(self.label_rspc1,           0, 0, 0)
        sizer_bottom.Add(self.label_rspc2,           0, 0, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_bottom.AddGrowableCol(1)
        sizer_bottom.AddGrowableCol(3)
        
        sizer_grid.Add(self.grid,         1, wx.EXPAND, 0)
        sizer_grid.Add(self.panel_totals, 0, wx.EXPAND, 0)
        self.panel_grid.SetSizer(sizer_grid)
        
        sizer_journal.Add(self.panel_top,     0, wx.EXPAND | wx.LEFT, 10)
        sizer_journal.Add(self.panel_grid,    1, wx.EXPAND | wx.LEFT, 10)
        sizer_journal.Add(self.panel_bottom,  0, wx.EXPAND | wx.LEFT, 10)
        sizer_journal.Add(self.panel_buttons, 0, wx.EXPAND | wx.LEFT, 10)
        self.SetSizer(sizer_journal)
        sizer_journal.Fit(self)
        self.Layout()
        
    def __do_main(self):
        self.supplier_id = 0
        self.division_id = 0
        
        loadCmb.acc_catagories(self.choice_acc_catagory)
        loadCmb.suppliers(self.choice_supplier)
        
        self.dateTo   = datetime.date.today()
        self.dateFrom = self.dateTo - datetime.timedelta(days=200)
        
        self.datepicker_ctrl_from.SetValue(self.dateFrom)
        self.datepicker_ctrl_to.SetValue(self.dateTo)
        
    def setupGrid(self, colHeadings):
        col = 0
        for h in colHeadings:
            self.grid.SetColLabelValue(col,  h[0])
            self.grid.SetColSize(col,  h[1])
            col+= 1

        self.grid.DisableDragColSize() 
        self.grid.EnableEditing(False) 
        self.grid.SetRowLabelSize(23)
        self.grid.ForceRefresh()
    
    def OnNew(self, evt):
        #rint'OnNew'
        dlg = DlgTransaction.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
        
    def OnEdit(self, evt):
        tid = self.grid.getSelectedTransactionID()
        #rint'OnEdit', tid
        
        dlg = DlgTransaction.create(None)
        try:
            dlg.displayData(tid)
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
        
    def OnDivision(self, evt):
        self.division_id = fetch.cmbID(self.choice_acc_catagory)
        self.displayData()
        
    def OnSupplier(self, evt):
        self.supplier_id = fetch.cmbID(self.choice_supplier)
        self.displayData()
        
    def chk_supplier(self, evt):
        if self.checkbox_supplier.GetValue():
            self.choice_supplier.Enable()
            self.supplier_id = fetch.cmbID(self.choice_supplier)
        else:
            self.choice_supplier.Enable(False)
            self.supplier_id = 0
        self.displayData()
        
    def chk_division(self, evt):
        if self.checkbox_division.GetValue():
            self.choice_acc_catagory.Enable()
            self.division_id = fetch.cmbID(self.choice_acc_catagory)
        else:
            self.division_id = 0
            self.choice_acc_catagory.Enable(False)
        self.displayData()
        
    def OnSelectCell(self):
        #rint'OnSelectCell'
        row, col = self.grid.get_location()
        #row, col = evt.GetRow(), evt.GetCol()
        if not row or not col: return
        tid = self.grid.GetCellValue(row, 1)

        if row:
            txt = "Record:  %d/%d" % (row, self.records)
            self.text_ctrl_records.SetValue(txt)

            sql = "SELECT ck_ref, supplier_ref, details \
                     FROM journal \
                    WHERE id=%d" % int(tid)
            res = fetch.getOneDict(sql)

            ck_ref       = res['ck_ref']
            supplier_ref = res['supplier_ref']
            details      = res['details']
            
            self.txt_ctrl_ck_ref.SetValue(str(ck_ref))
            self.txt_ctrl_supplier_ref.SetValue(str(supplier_ref))
            self.txt_ctrl_details.SetValue(str(details))
        
    def getAccount(self, pid):
        sql = "SELECT Nama FROM Perkiraan WHERE id = %d" % int(pid)
        return fetch.getStr(sql)
    
    def prepareQuery(self):
        sql = "SELECT j.id, j.transaction_date, j.title, j.details, \
                              d.account_id, d.debit, d.amount \
                 FROM acc_journal  j \
                 JOIN acc_journal_items d ON (d.journal_id = j.id) "

        dt = True
        if self.dateFrom and self.dateTo:
            sql += " WHERE j.transaction_date BETWEEN '%s' AND '%s' " % (self.dateFrom, self.dateTo)
        elif self.dateFrom:
            sql += " WHERE j.transaction_date => '%s'" % self.dateFrom
        elif self.dateTo:
            sql += " WHERE j.transaction_date <= '%s'"  % self.dateTo
        else:
            dt = False
        
        sp = ''
        if self.supplier_id:
            sp = " j.supplier_id = %d " % self.supplier_id
            if dt:
                sql += " AND %s " % sp
            else:
                sql += " WHERE %s" % sp
        
        dv = ''        
        if self.division_id:
            dv = " j.division_id = %d " % self.division_id
            if dt or sp:
                sql += " AND %s" % dv
            else:
                sql += " WHERE %s" % dv
        
        sql += " ORDER BY transaction_date, id, account_id "
        return sql
    
    def displayData(self):
        #rint'displayData'
        wx.BeginBusyCursor()
        
        debit_total  = 0; credit_total = 0
        
        sql = self.prepareQuery()
        #rintsql
        res = fetch.getAllDict(sql)
        
        self.resizeGrid(res)
            
        rowNo = 0
        for row in res:
            transactionCode = str(row['id'])
            transactionDate = row['transaction_date']
            transactionData = row['title']
            debit           = row['debit']
            ammount         = row['amount']
            transactionDate = transactionDate.strftime('%m/%d/%Y')
            sectionCode     = row['account_id']
            section         = self.getAccount(sectionCode)
            codestr         = str(sectionCode)
       
            a, b, c, d = (codestr[:1], codestr[1:3], codestr[3:5], codestr[5:])
            k = '%s.%s.%s.%s' % (a, b, c, d)
            
            sectionCode = "%s.%s.%s.%s" % ( a, b, c, d)
    
            kp = "%s - %s" % (sectionCode, section)
            
            self.grid.SetCellValue(rowNo, 0, transactionDate)
            self.grid.SetCellValue(rowNo, 1, transactionCode)
            self.grid.SetCellAlignment(rowNo, 1, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            
            self.grid.SetCellValue(rowNo, 2, transactionData)
            self.grid.SetCellValue(rowNo, 3, sectionCode)
            self.grid.SetCellValue(rowNo, 4, section)
            
            self.grid.SetCellAlignment(rowNo, 3, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            self.grid.SetCellAlignment(rowNo, 5, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            self.grid.SetCellAlignment(rowNo, 6, wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            
            if debit:
                debit_total += ammount
                self.grid.SetCellValue(rowNo, 5, format(ammount, '0,.0f'))
                
            else:
                credit_total += ammount
                self.grid.SetCellValue(rowNo, 6, format(ammount, '0,.0f'))
                
            self.grid.SetRowLabelValue(rowNo, '')    
                
            rowNo += 1

        tot_col_width = 0
        for c in range(0, 5):
            a = self.grid.GetColSize(c)
            tot_col_width += a
            
        debit_total = format(debit_total, '0,.0f')
        self.text_ctrl_records.SetMinSize((tot_col_width + 22,-1))
        
        if self.records:
            txt = "Record:  1/%d" % self.records
        else:
            txt = "No Records"
        pub.sendMessage('accounts.updateSB', val=1, idx=1)
        self.text_ctrl_records.SetValue(txt)
        
        self.text_ctrl_total_debit.SetValue(debit_total )
        credit_total = format(credit_total, '0,.0f')
        self.text_ctrl_total_credit.SetValue(credit_total)
        
        self.grid.groupDates()
        
        wx.EndBusyCursor()
        
    def resizeGrid(self, res):
        #self.grid.resize(res)
        
        self.grid.ClearGrid()
        self.records  = len(res)
        
        gridrows  = self.grid.GetNumberRows()
        rowdiff   = self.records - gridrows 
        
        if gridrows > self.records:
            #extrarows = gridrows - self.records
            self.grid.DeleteRows(0, -1*rowdiff)
            
        else:
            self.grid.InsertRows(0, rowdiff)
            
        self.Layout()
    
    
    def DateChange(self):
        self.dateTo   = self.datepicker_ctrl_to.GetDatetimeDateValue()
        self.dateFrom = self.datepicker_ctrl_from.GetDatetimeDateValue()
        self.displayData()

