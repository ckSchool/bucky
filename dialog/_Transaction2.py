import wx, gVar, sys, fetch, loadCmb

import  wx.lib.mixins.listctrl  as  listmix
import  wx.grid as gridlib


from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from DateCtrl import DateCtrl


class CustomNumValidator(wx.PyValidator):  
    """ Validator for entering custom low and high limits """
    def __init__(self):
        super(CustomNumValidator, self).__init__()

    def Clone(self):
        return CustomNumValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        if text.isdigit():
            return True
        else:
            wx.MessageBox("Please enter numbers only", "Invalid Input",
            wx.OK | wx.ICON_ERROR)
        return False

    def TransferToWindow(self):
        return True
    
    def TransferFromWindow(self):
        return True


class MyCellEditor(gridlib.PyGridCellEditor):
    """
    This is a sample GridCellEditor that shows you how to make your own custom
    grid editors.  All the methods that can be overridden are shown here.  The
    ones that must be overridden are marked with "*Must Override*" in the
    docstring.
    """
    def __init__(self):
        #rint"MyCellEditor ctor\n"
        gridlib.PyGridCellEditor.__init__(self)


    def Create(self, parent, id, evtHandler):
        """
        Called to create the control, which must derive from wx.Control.
        *Must Override*
        """
        #rint"MyCellEditor: Create\n"
        self._tc = wx.TextCtrl(parent, id, "")
        self._tc.SetInsertionPoint(0)
        self.SetControl(self._tc)

        if evtHandler:
            self._tc.PushEventHandler(evtHandler)


    def SetSize(self, rect):
        """
        Called to position/size the edit control within the cell rectangle.
        If you don't fill the cell (the rect) then be sure to override
        PaintBackground and do something meaningful there.
        """
        #rint"MyCellEditor: SetSize %s\n"# % rect)
        self._tc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
                               wx.SIZE_ALLOW_MINUS_ONE)


    def Show(self, show, attr):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        #rint"MyCellEditor: Show(self, %s, %s)\n" #% (show, attr))
        super(MyCellEditor, self).Show(show, attr)


    def PaintBackground(self, rect, attr, x):
        """
        Draws the part of the cell not occupied by the edit control.  The
        base  class version just fills it with background colour from the
        attribute.  In this class the edit control fills the whole cell so
        don't do anything at all in order to reduce flicker.
        """
        #rint"MyCellEditor: PaintBackground\n"


    def BeginEdit(self, row, col, grid):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        #rint"MyCellEditor: BeginEdit (%d,%d)\n"# % (row, col))
        self.startValue = grid.GetTable().GetValue(row, col)
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()
        self._tc.SetFocus()
        
        # For this example, select the text
        self._tc.SetSelection(0, self._tc.GetLastPosition()) 
        
    def EndEdit(self, row, col, grid, oldVal):
        """
        End editing the cell.  This function must check if the current
        value of the editing control is valid and different from the
        original value (available as oldval in its string form.)  If
        it has not changed then simply return None, otherwise return
        the value in its string form.
        *Must Override*
        """
        #rint "MyCellEditor: EndEdit (%s)\n" #% oldVal)
        val = self._tc.GetValue()
        if val != oldVal:
            return val
        else:
            return None
        

    def ApplyEdit(self, row, col, grid):
        """
        This function should save the value of the control into the
        grid or grid table. It is called only after EndEdit() returns
        a non-None value.
        *Must Override*
        """
        #rint"MyCellEditor: ApplyEdit (%d,%d)\n" #% (row, col))
        val = self._tc.GetValue()
        grid.GetTable().SetValue(row, col, val) # update the table

        self.startValue = ''
        self._tc.SetValue('')
        

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        *Must Override*
        """
        #rint"MyCellEditor: Reset\n"
        self._tc.SetValue(self.startValue)
        self._tc.SetInsertionPointEnd()


    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
        #rint"MyCellEditor: IsAcceptedKey: %d\n"# % (evt.GetKeyCode()))

        ## We can ask the base class to do it
        #return super(MyCellEditor, self).IsAcceptedKey(evt)

        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)


    def StartingKey(self, evt):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        import string

        #rint "MyCellEditor: StartingKey %d\n"# % evt.GetKeyCode())
        key = evt.GetKeyCode()
        ch = None
        if key in [ wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3, 
                    wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7, 
                    wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
                    ]:

            ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

        elif key < 256 and key >= 0 and chr(key) in string.printable:
            ch = chr(key)

        if ch is not None:
            # For this example, replace the text.  Normally we would append it.
            #self._tc.AppendText(ch)
            self._tc.SetValue(ch)
            self._tc.SetInsertionPointEnd()
        else:
            evt.Skip()


    def StartingClick(self):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
        #rint"MyCellEditor: StartingClick\n"


    def Destroy(self):
        """final cleanup"""
        #rint"MyCellEditor: Destroy\n"
        super(MyCellEditor, self).Destroy()


    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        #rint"MyCellEditor: Clone\n"
        return MyCellEditor(self.log)





class gridCtrl(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent)
        self.CreateGrid(0, 3)
 
        self.DisableDragRowSize()
        self.DisableDragColSize()
        
        self.moveTo = None
        
        self.SetColLabelValue(0, "id")
        self.SetColLabelValue(1, "Details")
        self.SetColLabelValue(2, "Value")
        
        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_BOTTOM)
        
        attr1 = gridlib.GridCellAttr()
        attr1.SetAlignment (wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.SetColAttr (2, attr1)
        
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.onCellEdit)
 
    
        self.currentRow = 0
        self.SetRowLabelSize(20)
        
        
    #----------------------------------------------------------------------
    def onCellEdit(self, event):
        #rint'onCellEdit'
        '''
        When cell is edited, get a handle on the editor widget
        and bind it to EVT_KEY_DOWN
        '''        
        editor = event.GetControl()        
        editor.Bind(wx.EVT_KEY_DOWN, self.onEditorKey)
        event.Skip()
        
    def onEditorKey(self, evt):
        if evt.GetKeyCode() >= 48 and evt.GetKeyCode() <= 57:     evt.Skip()
        
    def setGridHeadings(self, colHeadings):
        col = 0
        for h in colHeadings:
            self.SetColLabelValue(col,  h[0])
            self.SetColSize(col,  h[1])
            col+= 1
            
    def setRowCursor(self, r):
        self.SetRowLabelValue(self.currentRow, '')
        self.currentRow = r
        self.SetRowLabelValue(r, '>')
        
    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        evt.Skip()
        
    def appendItem(self, data):
        #rint'appendItem', data
        self.AppendRows()
        lastrow = self.GetNumberRows()
        #rint'lastrow', lastrow
        self.SetCellValue(lastrow-1, 0, str(data[0]))
        self.SetCellValue(lastrow-1, 1, str(data[1]))
        self.SetCellValue(lastrow-1, 2, str(data[2]))
        self.SetCellEditor(lastrow-1, 2, gridlib.GridCellNumberEditor())
        
    def deleteRow(self, row):
        self.DeleteRows(row)
    
    def OnSelectCell(self, evt):
        #rint'OnSelectCell'
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
        if row < 0 or col <0: return
        
        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()
            
        evt.Skip()
        
    def OnCellChange(self, evt):
        #rint"OnCellChange: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition())
        cellstr = self.GetCellValue(evt.GetRow(), evt.GetCol())
        cellstr = cellstr.replace(',','')
        self.SetCellValue(evt.GetRow(), evt.GetCol(), format(int(cellstr), '0,.0f'))
        self.calcTotal()
        
    def getSelectedTransactionID(self, ):
        row = self.GetGridCursorRow()
        return int(self.GetCellValue(row, 1))
    
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
        
        if gridrows > records:
            self.DeleteRows(0, -1*rowdiff)
            
        else:
            self.InsertRows(0, rowdiff)

    def getItemCount(self):
        return self.GetNumberRows()
    
    def calcTotal(self):
        #rint'calcTotal'
        gVar.listCtrl = self.GetName()
        total = 0
        for row in range(0, self.GetNumberRows()):
            #rintrow
            v =  self.GetCellValue(row, 2)
            #rint'v', v
            amount = int(v.replace(',',''))
            total += amount
        gVar.dayNo = total
        #rint'values.totaled', total
        pub.sendMessage('values.totaled') 
        

def create(parent):
    return DlgTransaction(parent)
    
class DlgTransaction(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.panel_top                 = wx.Panel(self, -1)
        
        self.panel_trans_details       = wx.Panel(self.panel_top, -1)
        self.label_date                = wx.StaticText(self.panel_trans_details, -1, "Date")
        self.datepicker_ctrl_1         = DateCtrl(self.panel_trans_details, -1)
        self.label_spc_date            = wx.StaticText(self.panel_trans_details, -1, "")
        
        self.label_trans_descript      = wx.StaticText(self.panel_trans_details, -1, "Transaction \nDescription")
        self.text_ctrl_description   = wx.TextCtrl(self.panel_trans_details,   -1, "", style = wx.TE_MULTILINE)
        self.label_spc_trans           = wx.StaticText(self.panel_trans_details, -1, "")
        
        self.label_ckrefno             = wx.StaticText(self.panel_trans_details, -1, "CK Ref.")
        self.text_ctrl_ckrefno         = wx.TextCtrl(self.panel_trans_details,   -1, "")
        self.checkbox_pettycash        = wx.CheckBox(self.panel_trans_details,   -1, "Petty Cash")
        #self.checkbox_pettycash         = wx.StaticText(self.panel_trans_details, -1, "")
        
        self.label_supplierrefno       = wx.StaticText(self.panel_trans_details, -1, "Supplier Ref")
        self.text_ctrl_supplierrefno   = wx.TextCtrl(self.panel_trans_details,   -1, "")
        self.label_spc_supplierrefno   = wx.StaticText(self.panel_trans_details, -1, "")
        
        self.checkbox_supplier         = wx.StaticText(self.panel_trans_details, -1, "Supplier")
        self.choice_supplier           = wx.Choice(self.panel_trans_details,     -1, choices=[])
        self.button_supplier_new       = wx.Button(self.panel_trans_details,     -1, "New")
        
        self.checkbox_division         = wx.StaticText(self.panel_trans_details, -1, "Division")
        self.choice_division           = wx.Choice(self.panel_trans_details,     -1, choices=[])
        self.button_division_new       = wx.Button(self.panel_trans_details,     -1, "New")
        
        self.panel_debits              = wx.Panel(self.panel_top, -1, style = wx.SIMPLE_BORDER)
        self.grid_debits               = gridCtrl(self.panel_debits)
        self.grid_debits.SetName('d')
        
        self.panel_debits_edit         = wx.Panel(self.panel_debits, -1)
        self.text_ctrl_debit_records   = wx.TextCtrl(self.panel_debits_edit, -1, "")
        self.text_ctrl_debit_total     = wx.TextCtrl(self.panel_debits_edit, -1, "", style = wx.ALIGN_RIGHT)
        
        self.panel_debits_add          = wx.Panel(self.panel_top, -1)
        self.choice_debits             = wx.Choice(self.panel_debits_add, -1, choices=[])
        self.button_debits_add         = wx.Button(self.panel_debits_add, -1, "Add")
        self.button_debits_delete      = wx.Button(self.panel_debits_add, -1, "Delete")
        
        self.panel_credits             = wx.Panel(self.panel_top, -1, style = wx.SIMPLE_BORDER)
        self.grid_credits              = gridCtrl(self.panel_credits)
        self.grid_credits.SetName('c')
        
        self.panel_credits_totals      = wx.Panel(self.panel_credits, -1)
        self.text_ctrl_credits_records = wx.TextCtrl(self.panel_credits_totals, -1, "")
        self.text_ctrl_credits_total   = wx.TextCtrl(self.panel_credits_totals, -1, "", style = wx.ALIGN_RIGHT)
        
        self.panel_credits_add         = wx.Panel(self.panel_top, -1)
        self.choice_credits            = wx.Choice(self.panel_credits_add, -1, choices=[])
        self.button_credits_add        = wx.Button(self.panel_credits_add, -1, "Add")
        self.button_credits_delete     = wx.Button(self.panel_credits_add, -1, "Delete")
        
        self.panel_bottom              = wx.Panel(self, -1)
        self.panel_spc_bottom_l        = wx.Panel(self.panel_bottom, -1)
        self.button_save               = wx.Button(self.panel_bottom, -1, "Save")
        self.button_cancel             = wx.Button(self.panel_bottom, -1, "Cancel")
        self.panel_spc_bottom_r        = wx.Panel(self.panel_bottom, -1)
        
        self.Bind(wx.EVT_BUTTON, self.OnNewSupplier,  self.button_supplier_new)
        self.Bind(wx.EVT_BUTTON, self.OnNewDivision,  self.button_division_new)
        
        self.Bind(wx.EVT_BUTTON, self.OnAddDebit,     self.button_debits_add)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteDebit,  self.button_debits_delete)
        self.Bind(wx.EVT_BUTTON, self.OnAddCredit,    self.button_credits_add)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteCredit, self.button_credits_delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,         self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnClose,        self.button_cancel)
        
        self.Bind(wx.EVT_CLOSE,  self.OnClose, self)
        
        self.grid_debits.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)

        pub.subscribe(self.TransTotal, 'values.totaled') 
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        psize=(420,200)
        self.panel_debits.SetMinSize(psize)
        self.panel_credits.SetMinSize(psize)
        
        self.button_division_new.SetMaxSize((50,-1))
        self.button_supplier_new.SetMaxSize((50,-1))
        
        self.SetTitle("New Transaction")
        
        self.button_save.SetMinSize((100, -1))
        self.button_cancel.SetMinSize((100, -1))
        self.datepicker_ctrl_1.checkbox.Hide()
        
        self.grid_debits.setGridHeadings( (('Key',0), ('Debit', 279), ('Amount', 115)))
        self.grid_credits.setGridHeadings((('Key',0),('Credit', 279), ('Amount', 115)))
        self.Layout()

    def __do_layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom          = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top             = wx.BoxSizer(wx.VERTICAL)
        sizer_credits         = wx.BoxSizer(wx.VERTICAL)
        sizer_credits_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_credits_totals  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_debits          = wx.BoxSizer(wx.VERTICAL)
        sizer_debits_buttons  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_debits_totals   = wx.BoxSizer(wx.HORIZONTAL)
        
        grid_sizer_details    = wx.FlexGridSizer(6, 3, 5, 5)
        
        grid_sizer_details.Add(self.label_ckrefno,           0, 0, 0)
        grid_sizer_details.Add(self.text_ctrl_ckrefno,       0, wx.EXPAND, 0)
        grid_sizer_details.Add(self.checkbox_pettycash,       0, 0, 0)
        
        grid_sizer_details.Add(self.checkbox_division,       0, 0, 0)
        grid_sizer_details.Add(self.choice_division,         0, wx.EXPAND, 0)
        grid_sizer_details.Add(self.button_division_new,     0, 0, 0)
        
        grid_sizer_details.Add(self.label_date,              0, 0, 0)
        grid_sizer_details.Add(self.datepicker_ctrl_1,       0, 0, 0)
        grid_sizer_details.Add(self.label_spc_date,          0, 0, 0)
        
        grid_sizer_details.Add(self.label_trans_descript,    0, 0, 0)
        grid_sizer_details.Add(self.text_ctrl_description, 0, wx.EXPAND, 0)
        grid_sizer_details.Add(self.label_spc_trans,         0, 0, 0)
        
        grid_sizer_details.Add(self.checkbox_supplier,       0, 0, 0)
        grid_sizer_details.Add(self.choice_supplier,         0, wx.EXPAND, 0)
        grid_sizer_details.Add(self.button_supplier_new,     0, 0, 0)
        
        grid_sizer_details.Add(self.label_supplierrefno,     0, 0, 0)
        grid_sizer_details.Add(self.text_ctrl_supplierrefno, 1, wx.EXPAND, 0)
        grid_sizer_details.Add(self.label_spc_supplierrefno, 0, 0, 0)
        
        #grid_sizer_details.Add(self.label_description,       0, 0, 0)
        #grid_sizer_details.Add(self.text_ctrl_description,   0, wx.EXPAND, 0)
        #grid_sizer_details.Add(self.label_spc_description,   0, 0, 0)
        self.panel_trans_details.SetSizer(grid_sizer_details)
        
        grid_sizer_details.AddGrowableCol(1)
        #grid_sizer_details.AddGrowableCol(2)
        
        sizer_debits_totals.Add(self.text_ctrl_debit_records, 1, wx.EXPAND, 0)
        sizer_debits_totals.Add(self.text_ctrl_debit_total,   0, 0, 0)
        self.panel_debits_edit.SetSizer(sizer_debits_totals)
        
        sizer_debits_buttons.Add(self.choice_debits,        1, wx.RIGHT, 5)
        sizer_debits_buttons.Add(self.button_debits_add,    0, wx.RIGHT, 5)
        sizer_debits_buttons.Add(self.button_debits_delete, 0, 0, 0)
        self.panel_debits_add.SetSizer(sizer_debits_buttons)
        
        sizer_debits.Add(self.grid_debits,       1, wx.EXPAND, 0)
        sizer_debits.Add(self.panel_debits_edit, 0, wx.EXPAND, 0)
        self.panel_debits.SetSizer(sizer_debits)
        
        sizer_credits_totals.Add(self.text_ctrl_credits_records, 1, wx.EXPAND, 0)
        sizer_credits_totals.Add(self.text_ctrl_credits_total,   0, 0, 0)
        self.panel_credits_totals.SetSizer(sizer_credits_totals)
        
        sizer_credits_buttons.Add(self.choice_credits,        1, wx.RIGHT, 5)
        sizer_credits_buttons.Add(self.button_credits_add,    0, wx.RIGHT, 5)
        sizer_credits_buttons.Add(self.button_credits_delete, 0, 0, 0)
        self.panel_credits_add.SetSizer(sizer_credits_buttons)
        
        sizer_credits.Add(self.grid_credits,         1, wx.EXPAND, 0)
        sizer_credits.Add(self.panel_credits_totals, 0, wx.EXPAND, 0)
        self.panel_credits.SetSizer(sizer_credits)
        
        sizer_top.Add(self.panel_trans_details, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        sizer_top.Add(self.panel_debits,        1, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        sizer_top.Add(self.panel_debits_add,    0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        sizer_top.Add(self.panel_credits,       0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        sizer_top.Add(self.panel_credits_add,   0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_bottom.Add(self.panel_spc_bottom_l, 1, wx.EXPAND, 0)
        sizer_bottom.Add(self.button_save,        0, 0, 0)
        sizer_bottom.Add(self.button_cancel,      0, 0, 0)
        sizer_bottom.Add(self.panel_spc_bottom_r, 1, wx.EXPAND, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_main.Add(self.panel_top,    0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_bottom, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
        self.Layout()
        self.Center()

    def __do_main(self):
        self.journal_id    = 0
        self.debit_total  = 0
        self.credit_total = 0
        
    def displayData(self, jid=0):
        self.journal_id = jid
        self.loadSuppliers()
        self.loadDivisions()
        self.loadAccounts()
        
        if self.journal_id:
            txt = 'Edit Transaction No. %d' % self.journal_id
            self.SetTitle(txt)
            
            sql = "SELECT id, date, name + description AS description, \
                          ck_ref, supplier_ref, suppier_id, division_id \
                     FROM acc_journal \
                    WHERE id = %d" % self.journal_id
            res = fetch.getOneDict(sql)
            #rintsql, res

            
            self.text_ctrl_ckrefno.SetValue(res['ck_ref'])
            self.datepicker_ctrl_1.SetValue(res['date'])
            self.text_ctrl_description.SetValue(res['description'])
            self.text_ctrl_supplierrefno.SetValue(res['supplier_ref'])
            
            loadCmb.restore(self.choice_supplier, res['suppier_id'])
            loadCmb.restore(self.choice_division, res['division_id'])
            
            
            self.listDebitItems()
            self.listCreditItems()
            
    def formatSectionCode(self, code):
        codestr = str(code)
        a, b, c, d = (codestr[:1], codestr[1:3], codestr[3:5], codestr[5:])
        k = '%s.%s.%s.%s' % (a, b, c, d)
        sectionCode = "%s.%s.%s.%s" % ( a, b, c, d)
        return sectionCode
    
    def listItems(self, grid, debit):
        sql = "SELECT p.id, p.name, j.amount \
                 FROM acc_journal j  \
                 JOIN acc_journal_items jd ON j.id = jd.journal_id) \
                 JOIN acc_accounts       p ON p.id = jd.account_id) \
                WHERE j.id =%d \
                  AND jd.debit=%s" % (self.journal_id, debit)
        res = fetch.getAllDict(sql)
        idx = 0; mylist = {} 
        
        for row in res:
            account_id = row['id']
            sectionCode = self.formatSectionCode(account_id)
            total = format(row['amount'], '0,.0f') #amount = row['amount']
            details = "%s : %s" % (sectionCode, row['name'])
            mylist[idx] = (account_id, details, total)
            idx += 1
            
        grid.Populate(mylist.items())
        
        
    def listDebitItems(self):
        self.listItems(self.grid_debits, True)
            
    def listCreditItems(self):
        self.listItems(self.grid_credits, False)
    
    def TransTotal(self):
        #rint'TransTotal', gVar.listCtrl
        if gVar.listCtrl == 'd':
            self.debit_total = gVar.dayNo
            #rint'self.debit_total', self.debit_total
            self.text_ctrl_debit_total.SetValue(format(gVar.dayNo, '0,.0f'))
        else:
            self.credit_total = gVar.dayNo
            #rint'self.credit_total', self.credit_total
            self.text_ctrl_credits_total.SetValue(format(gVar.dayNo, '0,.0f'))
            
        self.Layout()
    
    def onItemSelected(self, event):
        #rint'onItemSelected', event.GetColumn()
        currentItem = event.m_itemIndex
        #rintcurrentItem
        
    def OnBeginLabelEditCredit(self, event):
        #rint'OnBeginLabelEditCredit'
        if event.GetColumn() != 2:
            event.Veto()
            #event.Skip()
        
    def OnBeginLabelEditDebit(self, event):
        #rint'OnBeginLabelEditDebit'
        if event.GetColumn() != 2:
            event.Veto()
            #event.Skip()
 
    def loadSuppliers(self):
        #rint'loadSuppliers'
        sql = "SELECT id, name \
                 FROM acc_suppliers ORDER BY name"
        loadCmb.gen(self.choice_supplier, sql, ' ')
        
    def loadDivisions(self):
        #rint'loadDivisions'
        sql = "SELECT id, name \
                 FROM acc_divisions ORDER BY name"
        loadCmb.gen(self.choice_division, sql, ' ')
        
    def loadAccounts(self):
        sql = " SELECT  id, CONCAT(\
                        Mid(code, 1,1), '.', \
                        Mid(code, 2,2), '.', \
                        Mid(code, 4,2), '.', \
                        Mid(code, 6,2), ':  ', name) AS title\
                   FROM acc_accounts ORDER BY id"
        #rintsql
        loadCmb.gen(self.choice_credits, sql, ' ')
        loadCmb.gen(self.choice_debits, sql, ' ')
        
               
    def OnNewSupplier(self, evt):
        #rint"open dlgTextEntry 'new supplier' "
        dlg = wx.TextEntryDialog(self, 'Supplier Name', 'New Supplier Name', '')
 
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name:
                sql = "SELECT name \
                         FROM acc_suppliers \
                        WHERE name = '%s'" % new_name
                if fetch.getCount(sql):
                    msg = "Sorry supplier '%s' already exists" % new_name
                    fetch.msg(msg)
                else:
                    sql = "INSERT INTO acc_suppliers \
                                       (name) \
                                VALUES ('%s')" % new_name
                    fetch.updateDB(sql)
                    self.loadSuppliers()
                    loadCmb.restore_str(self.choice_supplier, new_name)
            
                    
    def OnNewDivision(self, evt):
        dlg = wx.TextEntryDialog(self, 'division name', 'New division name', '')
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if new_name:
                sql = "SELECT name \
                         FROM acc_divisions \
                        WHERE name = '%s'" % new_name
                if fetch.getCount(sql):
                    msg = "Sorry division '%s' already exists" % new_name
                    fetch.msg(msg)
                else:
                    sql = "INSERT INTO acc_divisions \
                                       (name) \
                                VALUES ('%s')" % (new_name)
                    #rintsql
                    fetch.updateDB(sql)
                    self.loadDivisions()
                    loadCmb.restore_str(self.choice_division, new_name)
        dlg.Destroy()
        
        # update combo
        
    def id_in_grid(self, test_id, grid):
        z = grid.GetNumberRows()
        for x in range(0, z) :
            #rintx
            iid = int(grid.GetCellValue(x, 0))
            #rint'list ctrl id = ', iid
            if int(iid) == int(test_id) : return True
        return False   
        
    def OnAddDebit(self, evt):
        #rint'Add debit'
        
        account_id = fetch.cmbID(self.choice_debits)
        gVar.listCtrl = 'd'
        
        if self.id_in_grid(account_id, self.grid_debits): return
        if self.id_in_grid(account_id, self.grid_credits):
            fetch.msg('can add this account, already in credits')
            return
        
        account    = fetch.cmbValue(self.choice_debits)
        self.grid_debits.appendItem((account_id, account, 0))
        
        self.grid_debits.calcTotal()   

        
    def OnAddCredit(self, evt):
        #rint'Add credit'
        gVar.listCtrl = 'c'
        account_id=fetch.cmbID(self.choice_credits)
  
        if self.id_in_grid(account_id, self.grid_credits): return
        
        if self.id_in_grid(account_id, self.grid_debits):
            fetch.msg('can add this account, already in debits')
        
        account = fetch.cmbValue(self.choice_credits)
        #rint'OnAddCredit', account
        
        self.grid_credits.appendItem((account_id, account, 0))
        self.grid_credits.calcTotal()

  
    def OnDeleteDebit(self, evt):
        #rint'OnDeleteDebit'
        gVar.listCtrl = 'd'
        grid = self.grid_debits
        self.deleteRow(grid)    
        
    def OnDeleteCredit(self, evt):
        #rint'OnDeleteCredit'
        gVar.listCtrl = 'c'
        grid = self.grid_credits
        self.deleteRow(grid)
        
    def deleteRow(self, grid):
        rows = grid.GetSelectedRows()
        #rint'GetSelectedRows', rows
        if len(rows)==1:
            grid.deleteRow(rows[0])
            grid.calcTotal()
        else:
            fetch.msg('select one row only')

        
    def OnSave(self, evt):
        print
        #rint'OnSave--------------'
        
        division_id  = fetch.cmbID(self.choice_divisioan)
        date         = self.datepicker_ctrl_1.GetDbReadyValue()
        description  = self.text_ctrl_description.GetValue()
        ckRef        = self.text_ctrl_ckrefno.GetValue()
        supplierRef  = self.text_ctrl_supplierrefno.GetValue()
        
        supplier_id = fetch.cmbID(self.choice_supplier)
        
        pettycash = self.checkbox_pettycash.GetValue()
        
        debit_items_count  = self.grid_debits.getItemCount()
        credit_items_count = self.grid_credits.getItemCount()
        msg = ''
        
        if not division_id:
            msg += '- division\n'
            
        if not tran_description:
            msg += '-transaction description\n'
            
        if not supplier_id:
             msg += '-supplier\n'
        
        if not date:
            msg += '-transaction date\n'
        
        if not ckRef:
            msg += '-ck ref missing\n'
        
        if debit_items_count + credit_items_count == 0:
            msg += '-credit or debit entries\n'
            
        if msg:
            msg = 'Missing Items:\n' + msg
            fetch.msg(msg)
            return
        
        if self.debit_total != self.credit_total:
            fetch.msg('transaction totals do not match')
        
        data = (supplier_id, date, description,  ckRef, supplier_id, supplierRef, pettycash)
        if self.journal_id:
            self.updateEntries(data)
        else:
            self.newEntry(data)
          
          
          
            
    def newEntry(self, data):
        supplier_id, date, description, ckRef, supplier_id, supplierRef, pettycash = data
        print
        
        #rint'new entry'
        
        
        self.journal_id = fetch.nextID('acc_journal')
        #rint ( supplier_id, date, tran_description,
                                    ckRef, supplierRef, pettycash,
                                    self.journal_id)
        sql = "INSERT INTO  acc_journal \
                        SET supplier_id = %d, date='%s', name='%s', \
                            details = '%s', ck_ref = '%s', supplier_ref = '%s, petty_cash=%s" % (
                            supplier_id, date, tran_description,
                            tran_description[255:], ckRef, supplierRef, pettycash)
        #rint'insert into journal'
        #rintsql
        
        
        debit_items  = self.grid_debits.getItemCount()
        credit_items = self.grid_credits.getItemCount()
        
        if debit_items:
            #rint'add debit items to acc_journal_items '
            self.insertDebitItems(debit_items)
            
        if credit_items:
            #rint'add credit items to acc_journal_items '
            self.insertCreditItems(credit_items)
            
    def insertDebitItems(self, debit_items):
        if debit_items: #rint'add debit_items to acc_journal_items '
        for x in range(0, debit_items):
            account_id = int(self.grid_debits.GetCellValue(x, 0))
            amount = self.grid_debits.GetCellValue(x, 2)
            amount = float(amount.replace(',',''))
            sql = "INSERT INTO acc_journal_items \
                      SET (journal_id, account_id, debit, amount) \
                   VALUES (%d, %d, %d, %d)" % (self.journal_id, account_id, True, amount)
            #rintsql
        
    def insertCreditItems(self, credit_items):
        if credit_items: #rint'add credit items to acc_journal_items '
        for x in range(0, credit_items):
            account_id = int(self.grid_credits.GetCellValue(x, 0))
            amount = self.grid_credits.GetCellValue(x, 2)
            amount = float(amount.replace(',',''))
            sql = "INSERT INTO acc_journal_items \
                      SET (journal_id, account_id, debit, amount)) \
                   VALUES (%d, %d, %d, %d)" % (self.journal_id, account_id, False, amount)
            #rintsql
        
        
    def updateEntries(self, data):
        supplier_id, date, tran_description, ckRef, supplier_id, supplierRef, pettycash = data
        
        debit_items  = self.grid_debits.getItemCount()
        credit_items = self.grid_credits.getItemCount()
        
        print
        #rint'updateEntries'
        
        print
        #rint'remove existing entries'
        sql = "DELETE FROM acc_journal_items \
                     WHERE journal_id = %d" % self.journal_id
        #rintsql
            
        sql = "DELETE FROM acc_journal_items \
                     WHERE journal_id = %d" % self.journal_id
        #rint"remove all credit & debit items", sql
        
        if not (debit_items + credit_items)> 0:
            sql1 = "DELETE FROM acc_journal \
                          WHERE id = %d" % self.journal_id
            msg =  'No debit items or credit items. Please edit'
            fetch.msg(msg)
            return
            
        else:
            # update jurnal details
            sql = "UPDATE acc_journal \
                      SET supplier_id = %d, date = '%s', name = '%s', \
                          details='%s', ck_ref='%s', supplier_ref = '%s', petty_cash = %s \
                    WHERE id = %d" % (
                          supplier_id, date, tran_description,
                          tran_description[255:], ckRef, supplierRef, pettycash, 
                          self.journal_id)
            #rint'\nUpdate jurnal details'
            #rintsql
            
            # 'insert each debit item'
            if debit_items: #rint'insert each debit item'
            for x in range(0, debit_items):
                account_id = int(self.grid_debits.GetCellValue(x, 0))
                amount = self.grid_debits.GetCellValue(x, 2)
                amount = float(amount.replace(',',''))
                sql = "INSERT INTO acc_journal_items \
                          SET (journal_id, account_id, debit, amount) \
                       VALUES (%d, %d, %d, %d)" % (self.journal_id, account_id, True, amount)
                
                #rintsql
            
            # 'insert each debit item'
            if credit_items: #rint'insert each debit item'
            for x in range(0, credit_items):
                account_id = int(self.grid_credits.GetCellValue(x, 0))
                amount = self.grid_credits.GetCellValue(x, 2)
                amount = float(amount.replace(',',''))
                sql = "INSERT INTO acc_journal_items \
                          SET (journal_id, account_id, debit, amount) \
                       VALUES (%d, %d, %d, %d)" % (self.journal_id, account_id, False, amount)
                
                #rintsql
        
        self.EndModal(wx.ID_OK)
        
    def getDebitItems(self, ):
        pass
    
         
    def OnClose(self, evt):
        self.EndModal(0) 

if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgTransaction(None)
    try:
        dlg.displayData()
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
