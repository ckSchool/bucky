import wx, gVar, fetch, loadCmb

deletedDebits  = []
addedDebits    = []
deletedCredits = []
addedCredits   = []

import  wx.lib.mixins.listctrl  as  listmix

listctrldata = {}
from my_ctrls import Validator
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub



class CustomNumValidator(wx.PyValidator):  
    """ Validator for entering custom low and high limits """
    def __init__(self):
        super(CustomNumValidator, self).__init__()

    def Clone(self):
        """ """
        return CustomNumValidator()

    def Validate(self, win):
        """ """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if text.isdigit():
            return True
        else:
            wx.MessageBox("Please enter numbers only", "Invalid Input",
            wx.OK | wx.ICON_ERROR)
        return False

    """def TransferToWindow(self):
        return True
    
    def TransferFromWindow(self):
        return True"""








class TestListCtrl(wx.ListCtrl, 
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin):
    
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
     
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        h = (("id", 0, 0), ("Description", 200, wx.LIST_AUTOSIZE),("Value", 100, wx.LIST_FORMAT_RIGHT))
        self.setHeadings(h)
        
        listmix.TextEditMixin.__init__(self)
        # Event Handlers
        self.Bind(wx.EVT_LIST_CACHE_HINT, self.OnleaveList) 
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEditListLabel)
         
    
    def OnEditListLabel(self,event):
        if not event.IsEditCancelled():
            wx.CallAfter(self.calcTotal)
            
        else:
            print "edit was cancelled"
        #event.Skip()
            
    def OnleaveList(self, evt):
        print 'OnleaveList'
        self.calcTotal()
        evt.Skip()
    
    def calcTotal(self):
        print 'calcTotal'
        count = self.GetItemCount()
        totals = []
        total = 0
        
        for row in range(count):
            x  =  self.GetItemText(row, 2)
            print row, x
            total += int(x)
        gVar.dayNo = total
        gVar.listCtrl = self.GetName()
        pub.sendMessage('values.totaled')    
        
    def OnChar(self, event):
        print 'OnChar'
        key_code = event.GetKeyCode()
        if chr(key_code) in "1234567890":
            event.Skip()
        
    def OnListCtrlValue(self, evt):
        print 'OnListCtrlValue'
        col = evt.GetColumn()
        print col
        evt.Skip()
        
    def setHeadings(self, h):
        idx = 0
        for heading in h:
            txt, colwidth, listformat = heading[0],heading[1],heading[2]
            self.InsertColumn(idx, txt, listformat, width = colwidth)
            idx +=1
            
    def Populate(self, items):
        for key, data in items:
            index = self.InsertStringItem(sys.maxint, str(data[0]))
            self.SetStringItem(index, 1, data[1])
            self.SetStringItem(index, 2, str(data[2]))
            self.SetItemData(index, key)

        self.currentItem = 0


    def SetStringItem(self, index, col, data):
        if col in range(3):
            wx.ListCtrl.SetStringItem(self, index, col, data)
        else:
            try:    datalen = int(2)
            except: return
            wx.ListCtrl.SetStringItem(self, index, col, 's')
            data = 'a'





def create(parent):
    return DlgTransaction(parent)
    
class DlgTransaction(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.panel_top                 = wx.Panel(self, -1)
    
        self.panel_debits              = wx.Panel(self.panel_top, -1)
        self.label_debits              = wx.StaticText(self.panel_debits, -1, "Debits")
        self.list_ctrl_debits          = TestListCtrl(self.panel_debits, -1,
                                                      style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.panel_debits_edit         = wx.Panel(self.panel_debits, -1)
        self.text_ctrl_debit_records   = wx.TextCtrl(self.panel_debits_edit, -1, "")
        self.text_ctrl_debit_total     = wx.TextCtrl(self.panel_debits_edit, -1, "")
        self.panel_spc_debit           = wx.Panel(self.panel_debits, -1)
        self.choice_debits             = wx.Choice(self.panel_spc_debit, -1, choices=[])
        self.button_debits_add         = wx.Button(self.panel_spc_debit, -1, "Add")
        self.button_debits_delete      = wx.Button(self.panel_spc_debit, -1, "Delete")
        
        self.panel_bottom              = wx.Panel(self, -1)
        self.panel_spc_bottom_l        = wx.Panel(self.panel_bottom, -1)
        self.button_save               = wx.Button(self.panel_bottom, -1, "Save")
        self.button_cancel             = wx.Button(self.panel_bottom, -1, "Cancel")
        self.panel_spc_bottom_r        = wx.Panel(self.panel_bottom, -1)
        
        self.Bind(wx.EVT_BUTTON, self.OnAddDebit,     self.button_debits_add)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteDebit,  self.button_debits_delete)
        
        self.Bind(wx.EVT_BUTTON, self.OnSave,         self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnClose,        self.button_cancel)
        
        self.Bind(wx.EVT_CLOSE,  self.OnClose, self)
        
        wx.EVT_LIST_BEGIN_LABEL_EDIT(self.list_ctrl_debits, self.list_ctrl_debits.GetId(), self.OnListCtrlValue)
 
        pub.subscribe(self.TransTotal, 'values.totaled') 
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.SetTitle("New Transaction")
        
        self.button_save.SetMinSize((100, -1))
        self.button_cancel.SetMinSize((100, -1))

    def __do_layout(self):
        sizer_main            = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom          = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top             = wx.BoxSizer(wx.VERTICAL)
        
        sizer_debits          = wx.BoxSizer(wx.VERTICAL)
        sizer_debits_buttons  = wx.BoxSizer(wx.HORIZONTAL)
        sizer_debits_totals   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_debits_totals.Add(self.text_ctrl_debit_records, 1, wx.EXPAND, 0)
        sizer_debits_totals.Add(self.text_ctrl_debit_total,   0, 0, 0)
        self.panel_debits_edit.SetSizer(sizer_debits_totals)
        
        sizer_debits_buttons.Add(self.choice_debits,        1, wx.RIGHT, 5)
        sizer_debits_buttons.Add(self.button_debits_add,    0, wx.RIGHT, 5)
        sizer_debits_buttons.Add(self.button_debits_delete, 0, 0, 0)
        self.panel_spc_debit.SetSizer(sizer_debits_buttons)
        
        sizer_debits.Add(self.label_debits,     0, 0, 0)
        sizer_debits.Add(self.list_ctrl_debits,  1, wx.EXPAND, 0)
        sizer_debits.Add(self.panel_debits_edit, 0, wx.EXPAND, 0)
        sizer_debits.Add(self.panel_spc_debit,   0, wx.TOP | wx.EXPAND, 5)
        self.panel_debits.SetSizer(sizer_debits)
        
        sizer_top.Add(self.panel_debits,        1, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 10)
        
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
        pass
        
    def displayData(self, tid=1):
        self.debit_list = {1 : (1010101, "PLN",  350),
                           2 : (1010102, "CASE", 320)}

        self.iid = gVar.user_id
        if self.iid:
            sql = "SELECT FROM WHERE = %d" % self.iid
         
        self.loadAccounts()
        
        if tid:
            self.SetTitle('Edit Transaction')
            self.list_ctrl_debits.Populate(self.debit_list.items())
            
            
    def TransTotal(self):
        print 'TransTotal'
        self.text_ctrl_debit_total.SetValue(str(gVar.dayNo))
        
    def OnListCtrlValue(self, evt):
        print 'OnListCtrlValue' 
        if evt.GetColumn() != 2: evt.Veto()
        #evt.Skip()
 
    def loadAccounts(self):
        sql = "SELECT id, name FROM acc_accounts ORDER BY name"
        loadCmb.gen(self.choice_debits, sql)
        

    def OnAddDebit(self, evt):
        print 'OnAddDebit'
        account_id = fetch.cmbID(self.choice_debits)
        print account_id
        if self.id_inListCtrl(account_id, self.list_ctrl_debits): return
        
        account    = fetch.cmbValue(self.choice_debits)
        print   account
        addedDebits.append((account_id, 0))
        self.list_ctrl_debits.Append((account_id, account, '0'))
        # if valitade_debit_entry:
        #     append to debit.list
        #self.updateDebitTotal()   
    
    def OnDeleteDebit(self, evt):
        print 'OnDeleteDebit' # contacts = [(name, ip) for name, ip in contacts if ip != removable_ip]
        idx = self.list_ctrl_debits.GetFirstSelected()
        self.list_ctrl_debits.DeleteItem(idx)
        
        
        deletedDebits.append('ref')
        # remove from bebdit list
        self.updateDebitTotal()
        
    def id_inListCtrl(self, test_id, listctrl):
        print 'id_inListCtrl'
        z = listctrl.GetItemCount()
        for x in range(0, z) :
            print x
            iid = listctrl.GetItemText(x, 0)
            print 'list ctrl id = ', iid
            if int(iid) == int(test_id) : return True
        return False
        
        
    
    def updateDebitTotal(self):
        print'updateDebitTotal'
        pass

        
        
        
        
    def OnSave(self, evt):
        print 'save then destroy'

            
        for item in deletedDebits:
            sql = "DELETE FROM WHERE id = %d" % item
            print sql
   
        for item in addedDebits:
            iid, val = item
            sql = "INSERT INTO VALUES ('%s', %d)" % (iid, val)
            print sql
            
        # fem

        
        # how to signal update or cancel
 
        saved = True
        
        if saved:
            self.Destroy()
        else:
            fetch.msg('file not saved - please check ')
    
        self.EndModal(wx.ID_OK)
         
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
