import wx, gVar, sys, fetch, loadCmb

from DateCtrl import DateCtrl

import DlgInvoiceItem
import DlgSelectMonthsPeriod

from wx.lib import masked

import wx.grid as gridlib

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

student_id   = 0
NoInduk      = ''
student_name = ''
form_name    = ''
invoice_items = {}
invoice_date  = 'xxxx-xx-xx'
ck_ref  = 'xxxx-xxxx'

size_totals = ((200,-1))
# -------------------------------------------------------------------

class gridCtrl(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        
        headings = ((0, "id", 0),
                    (1, "Quantity",     80),
                    (2, "Description", 600),
                    (3, "Unit Price",  100),
                    (4, "Total",       100))
        
        self.CreateGrid(0, len(headings))
 
        self.DisableDragRowSize()
        self.DisableDragColSize()
        
        self.moveTo = None
    
        self.setGridHeadings(headings)

        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_BOTTOM)
        
        attr1 = gridlib.GridCellAttr()
        attr1.SetAlignment (wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.SetColAttr (1, attr1)
        
        attr2 = gridlib.GridCellAttr()
        attr2.SetAlignment (wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        attr2.SetBackgroundColour(wx.LIGHT_GREY)
        attr2.SetReadOnly(True)
        self.SetColAttr (2, attr2)

        font = self.GetFont()
        font.SetWeight(wx.BOLD)
        attr = gridlib.GridCellAttr()
        attr.SetFont(font)
        attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.ALIGN_RIGHT, -1)
        attr.IncRef()
        #self.SetColAttr(2, attr)
        self.SetColAttr(3, attr)
        self.SetColAttr(4, attr)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.onCellEdit)
    
        self.currentRow = 0
        self.SetRowLabelSize(20)
        
    #----------------------------------------------------------------------
    def OnSize(self, event):
        width, height = self.GetClientSizeTuple()
        self.SetColSize(2, width-300)
        
    def setCellReadOnly(self, r, c):
        self.SetReadOnly(r,c)
        
    def setGridHeadings(self, colHeadings):
        for h in colHeadings:
            col, txt, width = h
            self.SetColLabelValue(col,  txt)
            self.SetColSize(col,  width)
         
    def setRowCursor(self, r):
        self.SetRowLabelValue(self.currentRow, '')
        self.currentRow = r
        self.SetRowLabelValue(r, '>')
        
    def OnIdle(self, evt):
        # #rint'OnIdle'
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        evt.Skip()
        
    def appendItem(self, data):
        global invoice_items
        #rint'appendItem', data
        self.AppendRows()
        lastrow = self.GetNumberRows()-1
        product_id = data['product_id']
        
        self.SetCellValue(lastrow,  0, str(product_id))
  
        self.SetCellValue(lastrow,  1, str(data['qnty']))
        self.SetCellEditor(lastrow, 1, gridlib.GridCellNumberEditor())
 
        self.SetCellValue(lastrow,  2, str(data['description']))
        #self.SetCellEditor(lastrow, 2, gridlib.GridCellTextEditor())
        #self.SetReadOnly( lastrow,  2, True)
        
        price = "{:,}".format(data['price'])
        self.SetCellValue(lastrow,  3, price)
        #self.SetReadOnly( lastrow,  4, True)
        #self.SetCellEditor(lastrow, 3, gridlib.GridCellNumberEditor())

        total = "{:,}".format(data['total'])
        self.SetCellValue(lastrow,  4, total)
        #self.SetReadOnly( lastrow,  4, True)
        #self.SetCellEditor(lastrow, 5, gridlib.GridCellNumberEditor())
        
        self.calcTotal()
        
    def deleteRow(self, row):
        self.DeleteRows(int(row))
        
    def update_bus_details(self, months, txt):
        # find which row hold holds bus data
        rows = self.GetNumberRows()
        for row in range(rows):
            
            product_id = self.get_product_id(row)
            product_type_id = fetch.get_product_type_id(product_id)
            if product_type_id == 9:
                self.SetCellValue(row, 2, txt)
    
    def OnSelectCell(self, evt):
        #rint'OnSelectCell'
         
        # Another way to stay in a cell that has a bad value...
        self.row = row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        
        if self.IsCellEditControlEnabled():
            #rint'IsCellEditControlEnabled'
            self.HideCellEditControl()
            self.DisableCellEditControl()
        
        if col ==1:
            value = int(self.GetCellValue(row, col))
            if value < 1 :
                self.SetCellValue(row, col, '1')
                return  # cancels the cell selection

        col = self.GetGridCursorCol()
        #rint'col', col
        if row < 0 or col <0: return
        
        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()
            
        evt.Skip()
        
    def onCellEdit(self, event):
        #rint'onCellEdit'
        '''  When cell is edited, get a handle on the editor widget
             and bind it to EVT_KEY_DOWN  '''
        editor = event.GetControl()        
        editor.Bind(wx.EVT_KEY_DOWN, self.onEditorKey)
        event.Skip()
        
    def onEditorKey(self, evt):
        #rint'onEditorKey'
        #if evt.GetKeyCode() >= 48 and evt.GetKeyCode() <= 57:
        evt.Skip()
        
    def OnCellChange(self, evt):
        col = evt.GetCol()
        #rint"OnCellChange", col
        
        if col == 2 or col == 4: return
        row = evt.GetRow()
        pos = evt.GetPosition()
        
        cellstr = self.GetCellValue(row, col).replace(',','')
        cellval = int(cellstr)
        if col == 1 and cellval==0:return
        
        self.SetCellValue(row, col, format(int(cellstr), '0,.0f'))
        self.calcTotal()
        
        row = self.GetGridCursorRow()
        product_id = self.get_product_id(row)
        product_type_id = fetch.get_product_type_id(product_id)
        
        if product_type_id == 1: # school fee
            #rint' change fee description'
            # prevent excess months
        
        elif product_type_id == 9: # bus fee
            # prevent excess months
            #rint' change bus description'
            pub.sendMessage('bus.grid.change')
        
    def get_product_id(self, row):
        return int(self.GetCellValue(row, 0))
    
    def Populate(self, items):
        #rint'Populate Grid', items
        self.resizeGrid(len(items))
        
        index = 0 
        for key, data in items:
            self.SetCellValue(index, 0, str(key))
            self.SetCellValue(index, 1, data[1])
            self.SetCellValue(index, 2, str(data[2]))
            self.SetCellEditor(index, 2, gridlib.GridCellNumberEditor())

        self.currentItem = 0
        self.calcTotal()

    def SetStringItem(self, index, col, data):
        if col in range(3):
            wx.ListCtrl.SetStringItem(self, index, col, data)
        else:
            try:    datalen = int(2)
            except: return
            wx.ListCtrl.SetStringItem(self, index, col, 's')
            data = 'a'

    def resizeGrid(self, records):
        self.ClearGrid()
        
        gridrows  = self.GetNumberRows()
        rowdiff   = records - gridrows 
        
        if gridrows > records: self.DeleteRows(0, -1*rowdiff)  
        else:                  self.InsertRows(0, rowdiff)
            
    def inGrid(self, pid):
        for row in range(0, self.GetNumberRows()):
            if int(self.GetCellValue(row, 0)) == pid:
                return True
        return False

    def getItemCount(self):
        return self.GetNumberRows()
    
    def calcTotal(self):
        #rint'calcTotal'
        gVar.listCtrl = self.GetName()
        total = 0
        for row in range(0, self.GetNumberRows()):
            
            qnty = self.GetCellValue(row, 1).replace(',','')
            #qnty = qnty
            price = self.GetCellValue(row, 3).replace(',','') 
            #price = price
            
            try:    qnty  = int(qnty)
            except: qnty = 1
            
            try:    price = int(price)
            except: price = 0
            
            sub =  qnty*price
            sub_s = "{:,}".format(sub)
            self.SetCellValue(row, 4, sub_s)
            
            total += sub
            
        gVar.dayNo = total
        #rint'values.totaled', total
        pub.sendMessage('values.totaled') 
        

    
# -------------------------------------------------------------------

def create(parent):
    return DlgPayments(parent)

class panel_invoice_header(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.bitmap_button          = wx.BitmapButton(self, -1, wx.NullBitmap)
        
        self.panel_right            = wx.Panel(self, -1)
        self.label_sid              = wx.StaticText(self.panel_right, -1, "ID")
        self.text_ctrl_NoInduk      = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        self.label_s_name           = wx.StaticText(self.panel_right, -1, "Name")
        self.text_ctrl_student_name = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        self.label_s_form           = wx.StaticText(self.panel_right, -1, "Form")
        self.text_ctrl_student_form = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        
        self.panel_reciept_details  = wx.Panel(self, -1)
        self.label_ckref            = wx.StaticText(self.panel_right, -1, "Receipt No")
        self.text_ctrl_receipt_no   = wx.TextCtrl(  self.panel_right, -1, "")
        self.label_inv_date         = wx.StaticText(self.panel_right, -1, "Date")
        self.text_ctrl_receipt_date = wx.TextCtrl(  self.panel_right, -1, "")
        self.label_spy_tot1         = wx.StaticText(self.panel_right, -1, "Total")
        self.text_ctrl_amount       = wx.TextCtrl(  self.panel_right, -1, "")
        self.label_39               = wx.StaticText(self.panel_right, -1, "-")
        self.text_ctrl_written      = wx.TextCtrl(  self.panel_right, -1, "", style = wx.TE_READONLY)
        
        self.label_spc1 = wx.StaticText(self.panel_right, -1, "")
        self.label_spc2 = wx.StaticText(self.panel_right, -1, "")
        
        self.do_layout()
        
        self.bitmap_button.SetMinSize((100, 120))
        self.text_ctrl_receipt_no.SetMinSize((200, -1))
        
    def do_layout(self):
        sizer_header  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_header_right  = wx.FlexGridSizer(4, 4, 5, 10)
        
        sizer_header.Add(self.bitmap_button, 0, wx.RIGHT, 10)
        sizer_header.Add(self.panel_right, 1, wx.BOTTOM | wx.EXPAND, 20)
        self.SetSizer(sizer_header)
        
        sizer_header_right.Add(self.label_sid,                 0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_NoInduk,         0, 0, 0)
        
        sizer_header_right.Add(self.label_s_name,              0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_student_name,    0, wx.EXPAND, 0)
        
        sizer_header_right.Add(self.label_s_form,              0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_student_form,    0, 0, 0)
        
        sizer_header_right.Add(self.label_ckref,                  0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_receipt_no,      0, 0, 0)
        
        sizer_header_right.Add(self.label_inv_date,                  0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_receipt_date,    0, 0, 0)
        
        sizer_header_right.Add(self.label_spy_tot1,            0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_amount,          1, wx.EXPAND, 0)
        
        sizer_header_right.AddSpacer(0, 0, 0)
        sizer_header_right.AddSpacer(0, wx.EXPAND, 0)
        
        sizer_header_right.Add(self.label_39,          0, 0, 0)
        sizer_header_right.Add(self.text_ctrl_written, 0, wx.EXPAND, 0)
        
        self.panel_right.SetSizer(sizer_header_right)
        sizer_header_right.AddGrowableCol(3)
        
    def display_header(self):
        self.text_ctrl_NoInduk.SetValue(NoInduk)
        self.text_ctrl_student_name.SetValue(student_name)
        self.text_ctrl_student_form.SetValue(form_name)
        self.text_ctrl_receipt_date.SetValue(invoice_date)
        self.text_ctrl_receipt_no.SetValue(ck_ref)
        

# ================================================



class panel_fees(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.monthFrom   = 0
        self.monthly_fee = 0
        
        self.panel_fees             = wx.Panel(self, -1)
        self.label_fees             = wx.StaticText(self.panel_fees, -1, 'School Fee')
        self.chkbox_fees            = wx.CheckBox(self.panel_fees, -1, '')
        self.panel_ctrls_fees       = wx.Panel(self.panel_fees, -1)
        
        self.text_ctrl_months       = masked.NumCtrl(self.panel_ctrls_fees, -1, value=1)
        self.label_fee_sd           = wx.StaticText(self.panel_ctrls_fees, -1,  'month')
        self.text_ctrl_description  = wx.TextCtrl(self.panel_ctrls_fees, -1)
        self.text_ctrl_fee          = masked.NumCtrl(self.panel_ctrls_fees, -1, style = wx.ALIGN_RIGHT)
        self.text_ctrl_total_fees   = masked.NumCtrl(self.panel_ctrls_fees, -1, value=0)
        
        # --------------------------------
        self.panel_rereg           = wx.Panel(self, -1)
        self.label_rereg           = wx.StaticText(self.panel_rereg, -1, 'Re-regester')
        self.chkbox_rereg          = wx.CheckBox(self.panel_rereg, -1, '')
        self.panel_ctrls_rereg     = wx.Panel(self.panel_rereg, -1)
        
        self.label_course          = wx.StaticText(self.panel_ctrls_rereg, -1, 'Join course:')
        self.choice_course         = wx.Choice(self.panel_ctrls_rereg, -1)
        self.text_ctrl_course_fee  = masked.NumCtrl(self.panel_ctrls_rereg, -1, value=0)
        #self.text_ctrl_rereg_total = masked.NumCtrl(self.panel_ctrls_rereg, -1, value=0)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnChRereg,      self.chkbox_rereg)
        self.Bind(wx.EVT_TEXT,     self.OnMonthsChange, self.text_ctrl_months)
        self.Bind(wx.EVT_CHECKBOX, self.OnChFee,        self.chkbox_fees)
        self.Bind(wx.EVT_CHOICE,   self.OnCourse,       self.choice_course)
        
        self.__do_settings()
        self.__do_layout()
        
        loadCmb.courses_forYear(self.choice_course, gVar.schYr)
        self.OnCourse(wx.Event)
        
    def __do_settings(self):
        #rint'__do_settings      crtghfue'
        
        self.text_ctrl_months.SetMinSize((40, -1))
        self.text_ctrl_months.SetMaxSize((40, -1))
        
        self.label_fees.SetMinSize( (70,22))
        self.text_ctrl_fee.SetMaxSize(size_totals)
        self.text_ctrl_total_fees.SetMaxSize(size_totals)
        
        self.text_ctrl_months.SetAllowNegative(False)
        self.text_ctrl_months.SetMax(12)
        self.text_ctrl_fee.SetEditable(False)
        
        self.text_ctrl_description.SetEditable(False)
        self.text_ctrl_total_fees.SetEditable( False)
        
        # ---------------------
        
        self.label_rereg.SetMinSize((70,22))
        self.choice_course.SetMinSize((141,21))
        self.text_ctrl_course_fee.SetMaxSize(size_totals)
        #self.text_ctrl_rereg_total.SetMaxSize(size_totals)
        
        self.text_ctrl_course_fee.SetEditable( False)
        #self.text_ctrl_rereg_total.SetEditable(False)
        self.panel_rereg.Hide()
        
        
    def __do_layout(self):
        sizer_main= wx.BoxSizer(wx.VERTICAL)
        
        sizer_fees        = wx.BoxSizer(wx.HORIZONTAL)
        sizer_rereg       = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_ctrls_fees  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ctrls_rereg = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_ctrls_fees.Add(self.text_ctrl_months,      0, wx.LEFT | wx.RIGHT, 5)
        sizer_ctrls_fees.Add(self.label_fee_sd,          0, wx.RIGHT, 15)
        sizer_ctrls_fees.Add(self.text_ctrl_description, 1, 0, 0)
        sizer_ctrls_fees.AddSpacer((1, 0),               0, 0, 0)
        sizer_ctrls_fees.Add(self.text_ctrl_fee,         0, 0, 0)
        sizer_ctrls_fees.Add(self.text_ctrl_total_fees,  0, 0, 0)
        self.panel_ctrls_fees.SetSizer(sizer_ctrls_fees)
        
        sizer_fees.Add(self.label_fees ,      0,0,0)
        sizer_fees.Add(self.chkbox_fees,      0,0,0)
        sizer_fees.Add(self.panel_ctrls_fees, 1,0,0)
        self.panel_fees.SetSizer(sizer_fees)
        
        # ------------------------------
        
        sizer_ctrls_rereg.Add(self.label_course,          0, wx.LEFT, 45)
        sizer_ctrls_rereg.Add(self.choice_course,         0, wx.LEFT, 10)
        sizer_ctrls_rereg.AddSpacer((0, 0),               1, 0, 0)
        sizer_ctrls_rereg.Add(self.text_ctrl_course_fee,  0, 0, 0)
        #sizer_ctrls_rereg.Add(self.text_ctrl_rereg_total, 0, 0, 0)
        self.panel_ctrls_rereg.SetSizer(sizer_ctrls_rereg)
        
        sizer_rereg.Add(self.label_rereg,       0, 0, 0)
        sizer_rereg.Add(self.chkbox_rereg,      0, 0, 0)
        sizer_rereg.Add(self.panel_ctrls_rereg, 1, 0, 0)
        self.panel_rereg.SetSizer(sizer_rereg)
        
        # ----------------------------
        
        sizer_main.Add(self.panel_fees,  0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_rereg, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        
    def displayData(self, student_id):
        #rint'panel_fees displayData'
        self.student_id = student_id
        self.course_id = fetch.courseID_forStudent(student_id)
        self.monthly_fee = fetch.fee_monthly(self.course_id, gVar.schYr)
        
        lastMonthPaid = fetch.month_last_paid(student_id, gVar.schYr, 1)
        if lastMonthPaid==12:
            self.monthFrom = 0
            self.panel_rereg.Show()
            self.panel_fees.Hide()
        else:
            self.monthFrom = lastMonthPaid + 1
            if lastMonthPaid:
                txt = "%s" % fetch.monthName(lastMonthPaid)
                self.text_ctrl_description.SetValue(txt)
                self.text_ctrl_months.SetMax(12-lastMonthPaid)
  
        fee = "{:,}".format(self.monthly_fee)
        self.text_ctrl_fee.SetValue(fee)
        self.text_ctrl_months.SetMinSize((50, -1))
        self.text_ctrl_months.SetMaxSize((50, -1))
        self.Layout()
        #rint'text_ctrl_months.Refresh()'
        self.text_ctrl_months.SetFocus()
        self.text_ctrl_months.SelectAll()
    
    def OnCourse(self, evt):
        #rint'OnCourse'
        course_id = fetch.cmbID(self.choice_course)
        sql = "SELECT course_fee_monthly \
                 FROM courses_by_year \
                WHERE id =%d" % course_id
        res = fetch.getDig(sql)
        #rint'course_fee_monthly', res
        self.text_ctrl_course_fee.SetValue(str(res))
        self.calcFeeTotal()
        
    def OnMonthsChange(self, evt):
        self.calcFeeTotal()
        
    def calcFeeTotal(self):
        months    = self.text_ctrl_months.GetValue()
        #rintmonths
        
        if months == 12:
            #rint' whole year'
            fee = fetch.fee_yearly(self.course_id, gVar.schYr)
            self.text_ctrl_description.SetValue('One off payment for whole year')
            self.text_ctrl_fee.Hide()
            fee = "{:,}".format(fee)
            self.text_ctrl_total_fees.SetValue(fee)
            
        else:
            self.text_ctrl_fee.Show()
            monthsMax = self.text_ctrl_months.GetMax()
            if months > monthsMax:
                months = monthsMax
                self.text_ctrl_months.SetValue(months)
                
            if months > 1:
                txt = "%s till %s" % (fetch.monthName(self.monthFrom), fetch.monthName(self.monthFrom + months -1))
                self.label_fee_sd.SetLabelText('months')
            else:
                txt = "%s" % fetch.monthName(self.monthFrom)
                self.label_fee_sd.SetLabelText('month')
            self.text_ctrl_description.SetValue(txt)
            self.panel_rereg.Show(months == monthsMax)
            
            fee = months * self.monthly_fee
            # bus_fee = "{:,}".format(self.bus_fee)
            self.text_ctrl_total_fees.SetValue(fee)
            
        self.GetTopLevelParent().Layout()
        
    def OnChFee(self, evt):
        x = self.chkbox_fees.GetValue()
        self.panel_ctrls_fees.Show(x)
        if x:
            self.panel_ctrls_rereg.Show(self.lastMonthPaid == 12)
        else:
            self.panel_rereg.Hide()
        self.calcFeeTotal()    
        self.Layout()
        
    def OnChRereg(self, evt):
        self.panel_ctrls_rereg.Show(self.chkbox_rereg.GetValue())
        self.Layout()
        
    def getTotal(self):
        return (self.text_ctrl_total_fees.GetValue(),  self.text_ctrl_course_fee.GetValue() )
        
        
        
        
        
class DlgPayments(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_base = wx.Panel(self, -1)
        self.panel_base.SetMinSize((800, 550))
        
        self.panel_header = panel_invoice_header(self.panel_base)
        
        self.static_line_1          = wx.StaticLine(self.panel_base, -1)
        self.panel_payments         = wx.Panel(     self.panel_base, -1)
        self.panel_invoice_items    = wx.Panel(     self.panel_base, -1)

        self.panel_fees             = panel_fees(self.panel_invoice_items)
        #self.panel_bus              = panel_bus( self.panel_invoice_items, -1)
        self.panel_bus              = wx.Panel(  self.panel_invoice_items, -1)
        self.grid_product           = gridCtrl(  self.panel_invoice_items)
        self.panel_totals           = wx.Panel(  self.panel_invoice_items, -1)
        
        
        self.choice_bus_from        = wx.Choice(self.panel_bus, -1) 
        self.label_bus_sd           = wx.StaticText(self.panel_bus, -1, '>')
        self.choice_bus_to          = wx.Choice(self.panel_bus, -1)
        self.text_ctrl_bus_details  = wx.TextCtrl(self.panel_bus, -1)
        
        self.label_total            = wx.StaticText(self.panel_totals,     -1, "-")
        self.text_ctrl_grid_total   = wx.TextCtrl(self.panel_totals,       -1, "")
        self.panel_select_product   = wx.Panel(self.panel_invoice_items,   -1)
        self.choice_products        = wx.Choice(self.panel_select_product, -1, choices=[])
        self.button_new_product     = wx.Button(self.panel_select_product, -1, "...")
        self.button_add_to_grid     = wx.Button(self.panel_select_product, -1, "+")
        self.button_delete          = wx.Button(self.panel_select_product, -1, "DELETE")
        
        self.static_line_2          = wx.StaticLine(self.panel_base, -1)
        
        self.panel_save_print_close = wx.Panel(self.panel_base, -1)
        self.button_save            = wx.Button(self.panel_save_print_close, -1, "Save")
        self.button_print_save      = wx.Button(self.panel_save_print_close, -1, "Save & Print")
        self.button_cancel          = wx.Button(self.panel_save_print_close, -1, "Cancel")

        self.Bind(wx.EVT_BUTTON, self.OnSave,       self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnSavePrint,  self.button_print_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,     self.button_cancel)
        self.Bind(wx.EVT_BUTTON, self.OnAdd,        self.button_add_to_grid)
        self.Bind(wx.EVT_BUTTON, self.OnDelete,     self.button_delete)
        self.Bind(wx.EVT_BUTTON, self.OnNewProduct, self.button_new_product)

        self.Bind(wx.EVT_CHOICE, self.OnBusMonthFrom, self.choice_bus_from)
        self.Bind(wx.EVT_CHOICE, self.OnBusMonthTo,   self.choice_bus_to)
        
        self.__do_bus_properties()
        self.__do_bus_layout()
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
  
    def __do_bus_properties(self):    
        min_month = 0
        txt = 'Transport for %s' % 'July'
        self.text_ctrl_bus_details.SetValue(txt)
        self.load_cmb_months(min_month)
        
    def __do_bus_layout(self):
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bus  = wx.BoxSizer(wx.HORIZONTAL)

        sizer_bus.Add(self.choice_bus_from,       0, 0, 0)
        sizer_bus.Add(self.label_bus_sd,          0, wx.LEFT | wx.RIGHT, 5)
        sizer_bus.Add(self.choice_bus_to,         0, 0, 0)
        sizer_bus.Add(self.text_ctrl_bus_details, 1, 0, 0)
        self.panel_bus.SetSizer(sizer_bus)
        
        sizer_main.Add(self.panel_bus, 1, 0, 0)
        self.SetSizer(sizer_main)
        
    def __set_properties(self):
        self.SetMinSize((950, 500))
        self.SetSize((950, 500))
        
        self.button_new_product.SetMinSize((30,24))
        self.button_new_product.SetMaxSize((30,24))
        self.SetTitle("Payments")
        
    def __do_layout(self):
        sizer_base        = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main        = wx.BoxSizer(wx.VERTICAL)
        sizer_product     = wx.BoxSizer(wx.VERTICAL)
        sizer_total       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_payments    = wx.BoxSizer(wx.VERTICAL)
        sizer_select      = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_select_product    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_print_save_cancel = wx.BoxSizer(wx.HORIZONTAL)
        
        grid_sizer_bottom     = wx.FlexGridSizer(4, 2, 5, 5)
        grid_sizer_nonproduct = wx.FlexGridSizer(7, 6, 5, 5)
        
        sizer_total.Add(self.label_total,          1, wx.TOP, 0)
        sizer_total.Add(self.text_ctrl_grid_total, 0, 0, 0)
        self.panel_totals.SetSizer(sizer_total)
        
        sizer_select_product.Add(self.button_new_product, 0, 0, 0)
        sizer_select_product.Add(self.choice_products,    1, wx.RIGHT, 20)
        sizer_select_product.Add(self.button_add_to_grid, 0, 0, 0)
        sizer_select_product.Add(self.button_delete,      0, 0, 0)
        self.panel_select_product.SetSizer(sizer_select_product)
        
        sizer_product.Add(self.panel_fees,           0, wx.EXPAND, 0)
        sizer_product.Add(self.panel_bus,            0, wx.EXPAND, 0)
        sizer_product.Add(self.grid_product,         1, wx.EXPAND, 0)
        sizer_product.Add(self.panel_totals,         0, wx.EXPAND, 0)
        sizer_product.Add(self.panel_select_product, 0, wx.EXPAND, 0)
        self.panel_invoice_items.SetSizer(sizer_product)
        
        sizer_print_save_cancel.Add(self.button_save,       0, 0, 0)
        sizer_print_save_cancel.Add(self.button_print_save, 0, wx.LEFT | wx.RIGHT, 10)
        sizer_print_save_cancel.Add(self.button_cancel,     0, 0, 0)
        self.panel_save_print_close.SetSizer(sizer_print_save_cancel)
        
        sizer_main.Add(self.panel_header,           0, wx.BOTTOM | wx.EXPAND, 0)
        sizer_main.Add(self.static_line_1,          0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_payments,         0, wx.BOTTOM | wx.EXPAND, 10)
        sizer_main.Add(self.panel_invoice_items,    1, wx.EXPAND, 0)
        sizer_main.Add(self.static_line_2,          0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_save_print_close, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        
        self.Layout()

    def __do_main(self):
        self.Center()
        self.panel_bus.Hide()
        self.panel_fees.OnChFee(wx.Event)    
        
    def displayData(self, sid):
        #rint'displayData', sid
        
        global student_id, NoInduk, student_name, form_name
        student_id = sid
        
        NoInduk      = fetch.NoInduk(student_id, gVar.schYr)
        student_name = fetch.studentFullName(student_id)
        form_name    = fetch.formName(fetch.formID_forStudent(student_id))
        
        ck_ref       = 'xxxx-xxx'
        inv_date     = '2015-12-1'
        
        self.panel_header.display_header()
        
        loadCmb.products(self.choice_products)
        self.panel_fees.displayData(student_id)
        inv_total = 0
        invoice_date  = ''
        ck_ref    = ''
        self.invoice_details = {'amount':   inv_total,
                                'ck_ref':   ck_ref,
                                'date':     inv_date,
                                'schYr':    gVar.schYr,
                                'name':     student_name,
                                'NoInduk':  NoInduk,
                                'form_name':form_name}
        
        self.invoice_items = {}
        
        product_type_id = 1 # school fee
        min_month = fetch.month_last_paid(student_id, gVar.schYr, product_type_id)
        self.load_cmb_months(min_month)
        
        self.months = 1
        self.Layout
        
    def load_cmb_months(self, min_month):
        loadCmb.schMonths(self.choice_bus_from, min_month)
        loadCmb.schMonths(self.choice_bus_to, min_month)
        
    def OnBusMonthFrom(self, evt):
        min_month = fetch.cmbID(self.choice_bus_from)
        loadCmb.schMonths(self.choice_bus_to, min_month-1)
        self.bus_details_changed()
        
        
    def OnBusMonthTo(self, evt):
        self.bus_details_changed()
        
        
    def bus_details_changed(self):
        #rint'bus_details_changed'
    
        month_from = fetch.cmbID(self.choice_bus_from)
        month_to   = fetch.cmbID(self.choice_bus_to)
        #rint'month_from=', month_from, '    month_to=', month_to
        
        self.months = months = month_to - month_from +1
    
        #rint'months=', months
        
        if months == 1:
            month = fetch.cmbValue(self.choice_bus_from)
            txt = 'Transport for %s' % month
            
        else:
            month_from = fetch.cmbValue(self.choice_bus_from)
            month_to   = fetch.cmbValue(self.choice_bus_to)
            txt = 'Transport for %s to %s' % (month_from, month_to)
            
        self.text_ctrl_bus_details.SetValue(txt)
        self.grid_product.update_bus_details(months,txt)
        
    def OnSave(self, evt):
        self.post_invoice()
        self.Close()
        
    def OnSavePrint(self, evt):
        data = (self.invoice_details, self.invoice_items)

        import DlgInvoicePreview
        dlg = DlgInvoicePreview.create(None)# , -1, "")
        try:
            dlg.displayPreview(data)
            if dlg.ShowModal():
                #rint'ok'
                self.post_invoice()
                self.Close()
            else:
                #rint'not ok'
        finally:
            #rint'finally'
            dlg.Destroy()
        
        # if print
        
        
    def post_invoice(self):
        #rint'post invoice'
        
    def totaled(self, ):
        grid_total = gVar.dayNo
        monthly_fees, rereg_fee = self.panel_fees.getTotal()
        
        bus_fees    = self.panel_bus.getTotal() 
        
        grand_total = grid_total + monthly_fees + rereg_fee + bus_fees
        grand_total = "{:,}".format(grand_total)
        self.text_ctrl_grid_total.SetValue(grand_total)
    
    def OnCancel(self, evt):
        self.Close()
    
    def is_recurring(self, product_id):
        self.is_recurring = fetch.is_recurring(product_id)
        self.recurring_monthly = fetch.is_recurring_monthly(product_id)
   
    def OnAdd(self, evt):
        #rint'OnAdd'
        product_id = fetch.cmbID(self.choice_products)
        #rint'product_id.GetSelection():', product_id
        if not product_id or self.grid_product.inGrid(product_id):
            return
        
        description     = fetch.cmbValue(self.choice_products)
        price           = fetch.product_price(product_id)
        qnty            = 1
        total           = qnty*price
        product_type_id = fetch.get_product_type_id(product_id)
        
        if product_type_id == 1: # school fee
            #rint' append fee '
            month_no = fetch.month_last_paid(student_id, gVar.schYr, 9)+1
            if month_no > 12:
                self.panel_fees.Hide()
                fetch.msg('month 12 already paid for')
                return
            else:
                self.panel_fees.Show()
            month = fetch.monthName(month_no)
            description = 'Schoolfee for %s' % month
            
            
        elif product_type_id == 9: # bus fee
            #rint' append bus '

            # last paid for month
            # if last month == 12 : return
            month_no = fetch.month_last_paid(student_id, gVar.schYr, 9)+1
            
            if month_no > 12:
                fetch.msg('month 12 already paid for')
                # what we really need to know is if all months have been paid for
                return
            else:
                self.panel_bus.Show()
            self.Layout()
            month = fetch.monthName(month_no)
            description = 'Bus fee for %s' % month

        
        data  = {'product_id':product_id,
                'qnty':qnty,
                'description':description,
                'price':price,
                'total':total}
        self.grid_product.appendItem(data)
        
        r = self.grid_product.GetNumberRows()
        self.grid_product.setCellReadOnly(r, 0)
        

        
        
    def fees_details_changed(self):
        #rint'fees_details_changed'
            
    def OnDelete(self, evt):
        row = self.grid_product.GetSelectedRows()[0]
        #rintrow
        self.grid_product.deleteRow(row)
        
        # if item deleted was school fee
        # hide fees panel
        
        # if item deleted wass bus
        # hide bus panel
    
    def OnNewProduct(self, evt):
        dlg = DlgInvoiceItem.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            loadCmb.products(self.choice_products)
        finally:
            dlg.Destroy()
    
        

if __name__ == "__main__":
    gVar.schYr = 2014
    app = wx.App(None)
    dlg = create(None)
    try:
        dlg.displayData(2)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
    
    
    
