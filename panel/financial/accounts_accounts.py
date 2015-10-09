import wx, fetch, loadCmb
import wx.lib.masked as masked

from myListCtrl    import VirtualList as vList
from my_ctrls      import Validator
import panel._buttons.panel_buttons   

    
## --------------------------------------------------------    
class panel_accounts(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        
        self.panel_top     = wx.Panel(self, -1)
        self.panel_bottom  = wx.Panel(self, -1)
        
        self.label_heading = wx.StaticText(self.panel_top, -1, "PURCHASE ACCOUNTS")
        
        self.vList         = vList(self.panel_bottom, style = wx.LC_HRULES | wx.LC_VRULES |wx.LC_SINGLE_SEL)
        self.panel_right   = wx.Panel(self.panel_bottom, -1)
        
        self.panel_details           = wx.Panel(self.panel_right, -1)
        self.label_section_catagory    = wx.StaticText(self.panel_details, -1, "Catagory")
        self.choice_account_catagory = wx.Choice(self.panel_details,     -1, choices=[])
        self.label_section_code        = wx.StaticText(self.panel_details, -1, "Code")
        self.panel_section_code        = wx.Panel(self.panel_details, -1)
        
        self.text_ctrl_acc_code_1  = self.create_code_ctrl(self.panel_section_code)
        self.text_ctrl_acc_code_2  = self.create_code_ctrl(self.panel_section_code)
        self.text_ctrl_acc_code_3  = self.create_code_ctrl(self.panel_section_code)
        self.text_ctrl_acc_code_4  = self.create_code_ctrl(self.panel_section_code)
        
        self.label_account_name     = wx.StaticText(self.panel_details,  -1, "Section")
        self.text_ctrl_section_name = wx.TextCtrl(self.panel_details,    -1, "")
        self.label_account_balance  = wx.StaticText(self.panel_details,  -1, "Opening Ballance")
        
        self.text_ctrl_balance = masked.NumCtrl(self.panel_details, -1, name="text_ctrl_opening_balance" )
    
        self.panel_buttons = self.pb = panel_buttons(self.panel_right, -1)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
        self.Bind(wx.EVT_CHOICE, self.OnSelectAccount, self.choice_account_catagory)
        
        self.Bind(wx.EVT_BUTTON, self.OnNew,     self.pb.new)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,    self.pb.edit)
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  self.pb.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.pb.save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,  self.pb.cancel)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.pb.refresh)
        
        self.tc = ( self.text_ctrl_acc_code_1,
                    self.text_ctrl_acc_code_2,
                    self.text_ctrl_acc_code_3,
                    self.text_ctrl_acc_code_4,
                    self.text_ctrl_section_name,
                    self.text_ctrl_balance)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def create_code_ctrl(self, panel):
        ctrl = masked.TextCtrl( panel, -1, "",
                mask         = "##",
                excludeChars = "",
                formatcodes  = "F^-",
                includeChars = "",
                validRegex   = "^\(\d{3}\) \d{3}-\d{4}",
                validRange   = (0,99),
                choices      = "",
                choiceRequired = True,
                defaultValue = "",
                demo         = True,
                name         = "")
        return ctrl
        
    def __set_properties(self):
        self.panel_top.SetMinSize((-1, 50))
        self.panel_top.SetMaxSize((-1, 60))
        self.vList.SetColumns(( ('',00),
                                ('Code',70),
                                ('Section',170),
                                ('?',10)))
        
        loadCmb.acc_catagories(self.choice_account_catagory)
        
        self.text_ctrl_acc_code_1.SetMinSize((32, -1))
        self.text_ctrl_acc_code_2.SetMinSize((32, -1))
        self.text_ctrl_acc_code_3.SetMinSize((32, -1))
        self.text_ctrl_acc_code_4.SetMinSize((32, -1))
        
        self.choice_account_catagory.SetMinSize((200, 21))
        self.choice_account_catagory.SetSelection(0)
        
        self.text_ctrl_balance.SetGroupChar( ',' )
        self.text_ctrl_acc_code_1.Enable(False)
        
        self.pb.cancel.Enable(False)
        self.pb.save.Enable(False)
        
        self.panel_details.Enable(False)
        
    def __do_layout(self):
        sizer_main                 = wx.BoxSizer(wx.VERTICAL)
        sizer_account_sections     = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_section_details = wx.FlexGridSizer(4, 2, 10, 5)
        sizer_pkrn_code = wx.BoxSizer(wx.HORIZONTAL)
        sizer_right     = wx.BoxSizer(wx.VERTICAL)
        
        sizer_pkrn_code.Add(self.text_ctrl_acc_code_1, 0, 0, 0)
        sizer_pkrn_code.Add(self.text_ctrl_acc_code_2, 0, wx.LEFT, 5)
        sizer_pkrn_code.Add(self.text_ctrl_acc_code_3, 0, wx.LEFT, 5)
        sizer_pkrn_code.Add(self.text_ctrl_acc_code_4, 0, wx.LEFT, 5)
        self.panel_section_code.SetSizer(sizer_pkrn_code)
        
        grid_sizer_section_details.Add(self.label_section_catagory,  0, 0, 0)
        grid_sizer_section_details.Add(self.choice_account_catagory, 0, 0, 0)
        grid_sizer_section_details.Add(self.label_section_code,      0, 0, 0)
        
        grid_sizer_section_details.Add(self.panel_section_code,     0, wx.LEFT, 0)
        grid_sizer_section_details.Add(self.label_account_name,     0, 0, 0)
        grid_sizer_section_details.Add(self.text_ctrl_section_name, 0, 0, 0)
        grid_sizer_section_details.Add(self.label_account_balance,  0, 0, 0)
        grid_sizer_section_details.Add(self.text_ctrl_balance,      0, 0, 0)
        self.panel_details.SetSizer(grid_sizer_section_details)
        
        grid_sizer_section_details.AddGrowableRow(1)
        grid_sizer_section_details.AddGrowableCol(1)
        
        sizer_right.Add(self.panel_details,   0, wx.EXPAND | wx.ALL, 10)
        sizer_right.Add(self.panel_buttons,   0, wx.EXPAND, 0)
        self.panel_right.SetSizer(sizer_right)
        
        sizer_account_sections.Add(self.vList,       1, wx.EXPAND, 0)
        sizer_account_sections.Add(self.panel_right, 1, wx.EXPAND, 0)
        self.panel_bottom.SetSizer(sizer_account_sections)
        
        sizer_heading = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_heading.Add(self.label_heading,    0, wx.EXPAND,0)
        self.panel_top.SetSizer(sizer_heading)
        
        sizer_main.Add(self.panel_top,    0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.panel_bottom, 1, wx.EXPAND | wx.LEFT, 5)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)

    def __do_main(self):
        self.displayDetails()
        
    def displayDetails(self):
        sql = "SELECT code, code AS code, name FROM acc_accounts"
        DATA = fetch.DATA(sql)
        #rint sql, DATA
        for key in DATA:
            data = DATA[key]
            self.acc_code = str(data[1])
            a, b, c, d = (self.acc_code[:1], self.acc_code[1:3], self.acc_code[3:5], self.acc_code[5:])
            k = '%s.%s.%s.%s' % (a, b, c, d)
            DATA[key] = (data[0], k, data[2])
        
        self.vList.SetItemMap(DATA)
        acc_catagory_id = fetch.acc_catagory_id(self.acc_code)
        loadCmb.restore(self.choice_account_catagory, acc_catagory_id)

    def OnSelectAccount(self,evt):
        self.text_ctrl_acc_code_1.SetValue(str(fetch.cmbID(self.choice_account_catagory)))
            
    def OnItemSelected(self, evt):
        self.index    = self.vList.GetFirstSelected()
        self.acc_code = int(self.vList.GetSelectedID())
        self.displaySelected()
        
    def displaySelected(self):
        #rint'displaySelected : self.acc_code=', self.acc_code
        codeStr = str(self.acc_code)
        a = codeStr[ :1]
        b = codeStr[1:3]
        c = codeStr[3:5]
        d = codeStr[5: ]
        
        self.text_ctrl_acc_code_1.SetValue(a)
        self.text_ctrl_acc_code_2.SetValue(b)
        self.text_ctrl_acc_code_3.SetValue(c)
        self.text_ctrl_acc_code_4.SetValue(d)
        
        name = fetch.acc_name(self.acc_code)
        self.text_ctrl_section_name.SetValue(name)
        
        acc_catagory_id = fetch.acc_catagory_id(self.acc_code)
        loadCmb.restore(self.choice_account_catagory, acc_catagory_id)
        
        bal = fetch.acc_balance(self.acc_code)
        bal = "{:,}".format(bal)
        self.text_ctrl_balance.SetValue(bal)

    def lockOut(self):
        self.pb.LockOut()
        self.vList.Enable(False)
        self.panel_details.Enable()
        self.GetTopLevelParent().panel_tree.Enable(False)
        
    def OnNew(self, evt):
        #rint'accounts_accounts > new'
        self.editing = False
        self.lockOut()
        for tc in self.tc: tc.Clear()
        self.text_ctrl_acc_code_1.SetValue(str(fetch.cmbID(self.choice_account_catagory)))
        
    def OnEdit(self, evt):
        self.editing = True
        self.lockOut()
        
    def OnDelete(self, evt):
        pass
        #rint'OnDelete'
        
    def OnSave(self, evt):
        pass
        #rint'OnSave'
               
        acc_catagory_id = fetch.cmbID(self.choice_account_catagory)
        code_2 = self.text_ctrl_acc_code_2.GetValue()
        code_3 = self.text_ctrl_acc_code_3.GetValue()
        code_4 = self.text_ctrl_acc_code_4.GetValue()
        
        acc_code = "%s%s%s%s" % (acc_catagory_id, code_2, code_3, code_4)
        acc_code = acc_code.strip()
  
        if len(acc_code)<7:
            fetch.msg('Account code incomplete')
            return
        
        account_name = self.text_ctrl_section_name.GetValue()
        if not account_name:
            fetch.msg('Name required') 
            return
        
        if not self.editing: 
            if fetch.acc_code_exists(acc_code):
                fetch.msg('Account code already in use')
                return

            if fetch.acc_name_exists(account_name):
                fetch.msg('Account name in use - please try another')
                return
            
        start_ballance = self.text_ctrl_balance.GetValue()

        if self.editing:
            sql = "UPDATE acc_accounts \
                      SET name, balance=%d ='%s', acc_catagory_id = %d \
                    WHERE code = %d" % (account_name, start_ballance, acc_code, acc_catagory_id)
                
        else:
            sql = "INSERT INTO acc_accounts \
                              (name, balance, code, acc_catagory_id) \
                       VALUES('%s', %d, %d)" % ( 
                               account_name, int(start_ballance), int(acc_code), acc_catagory_id)
        #rintsql
        #fetch.updateDB(sql)
        
        self.OnCancel(wx.Event)
        self.displayDetails()
        
    def OnCancel(self, evt):
        #rint'OnCancel'
        self.pb.OnCancel()
        self.GetTopLevelParent().panel_tree.Enable()
        self.unlockdown()
    
    def unlockdown(self):
        self.panel_details.Enable(False)
        self.vList.Enable()
        self.displaySelected()
        
    def OnRefresh(self, evt):
        pass
        #rint'OnRefresh'
        
        
