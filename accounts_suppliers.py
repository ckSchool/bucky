import wx, fetch

from myListCtrl   import VirtualList as vList
from panel_buttons import panel_buttons   
from my_ctrls      import Validator
        
class panel_suppliers(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_heading = wx.StaticText(self, -1, "SUPPLIERS")
        
        self.panel_bottom  = wx.Panel(self, -1)
        
	self.vList         = vList(self.panel_bottom, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.panel_right   = wx.Panel(self.panel_bottom, -1)
        self.panel_details = wx.Panel(self.panel_right, -1)
        self.label_sply_name            = wx.StaticText(self.panel_details, -1, "Name")
        self.text_ctrl_supplier_name    = wx.TextCtrl(self.panel_details, -1, "")
        self.label_supplier_address     = wx.StaticText(self.panel_details, -1, "Address")
        self.text_ctrl_supplier_address = wx.TextCtrl(self.panel_details, -1, "", style=wx.TE_MULTILINE)
        self.label_supplier_telp        = wx.StaticText(self.panel_details, -1, "Tel.")
        self.text_ctrl_supplier_telp    = wx.TextCtrl(self.panel_details, -1, "", validator = Validator(2))
        self.panel_buttons   = self.pb  = pb = panel_buttons(self.panel_right, -1)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.vList)
        
        self.Bind(wx.EVT_BUTTON, self.OnNew,     pb.new)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,    pb.edit)
        self.Bind(wx.EVT_BUTTON, self.OnDelete,  pb.delete)
        self.Bind(wx.EVT_BUTTON, self.OnSave,    pb.save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,  pb.cancel)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, pb.refresh)
        
        self.tc = (self.text_ctrl_supplier_name, self.text_ctrl_supplier_address, self.text_ctrl_supplier_telp)

        self.__set_properties()
        self.__do_layout()
        
        self.displayData()

    def __set_properties(self):
	self.label_heading.SetMinSize((-1, 45))
        self.label_heading.SetMaxSize((-1, 45))
	
        self.vList.SetColumns((('',00),('Name',270),('Telp',70)))
        self.panel_details.Enable(False)
            
        self.text_ctrl_supplier_address.SetMinSize((300,-1))
	
	self.pb.cancel.Enable(False)
        self.pb.save.Enable(False)

    def __do_layout(self):
        sizer_main      = wx.BoxSizer(wx.VERTICAL)
        sizer_suppliers = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details   = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_supplier_details = wx.FlexGridSizer(3, 2, 10, 5)
        
        grid_sizer_supplier_details.Add(self.label_sply_name,            0, 0, 0)
        grid_sizer_supplier_details.Add(self.text_ctrl_supplier_name,    0, wx.EXPAND, 0)
        grid_sizer_supplier_details.Add(self.label_supplier_address,     0, 0, 0)
        grid_sizer_supplier_details.Add(self.text_ctrl_supplier_address, 0, wx.EXPAND, 0)
        grid_sizer_supplier_details.Add(self.label_supplier_telp,        0, 0, 0)
        grid_sizer_supplier_details.Add(self.text_ctrl_supplier_telp,    0, wx.EXPAND, 0)
        self.panel_details.SetSizer(grid_sizer_supplier_details)
        
        sizer_details.Add(self.panel_details, 0, wx.EXPAND, 0)
        sizer_details.Add(self.panel_buttons, 0, wx.EXPAND | wx.TOP, 10)
        self.panel_right.SetSizer(sizer_details)
        
        sizer_suppliers.Add(self.vList,       1, wx.EXPAND, 0)
        sizer_suppliers.Add(self.panel_right, 1, wx.EXPAND, 0)
        self.panel_bottom.SetSizer(sizer_suppliers)
        
        sizer_main.Add(self.label_heading,    0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.panel_bottom,     1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def displayData(self):
        self.editing = False
        sql = "SELECT id, name, telp FROM suppliers ORDER BY name"
        
        res = fetch.DATA(sql)
        self.vList.SetItemMap(res)
        
        if res:
            self.vList.selectItem(0)
    
    def OnItemSelected(self, evt):
        self.sid = sid = int(self.vList.GetSelectedID())
        self.index = self.vList.GetFirstSelected()
        
        self.displaySelected()
        
    def lockOut(self):
        self.pb.LockOut()
        self.vList.Enable(False)
        self.panel_details.Enable()
        self.GetTopLevelParent().panel_tree.Enable(False)
            
    def OnNew(self, evt):
        #rint'new'
        self.lockOut()
        for tc in self.tc:
            tc.SetValue('')
        self.editing = False
        
    def OnEdit(self, evt):
        #rint'OnEdit'
        self.editing = True
        self.lockOut()
    
    def OnDelete(self, evt):
	pass
        #rint'OnDelete'
        
    def OnSave(self, evt):
        #rint'OnSave'
        name =    self.text_ctrl_supplier_name.GetValue().strip()
        address = self.text_ctrl_supplier_address.GetValue()
        telp =    self.text_ctrl_supplier_telp.GetValue()
        if not name:
            fetch.msg('Name required')
            return
        
        if self.editing == True:
            sql = "UPDATE acc_suppliers \
                      SET name='%s', address = '%s', telp='%s' \
                    WHERE id = %d" % (name, address, telp, self.sid)
            # update list
            
        else:
            sql = "INSERT INTO acc_suppliers \
                          (name, address, telp) \
                   VALUES ('%s', '%s' ,'%s')" % (name, address, telp)
            
        fetch.updateDB(sql)
        self.displayData()
        self.OnCancel(wx.Event)
        
    def OnCancel(self, evt):
        #rint'OnCancel'
        self.pb.OnCancel()
        self.panel_details.Enable(False)
        self.editing = False
        self.vList.Enable()
        self.GetTopLevelParent().panel_tree.Enable()
        self.displaySelected()
        
    def displaySelected(self):
        self.text_ctrl_supplier_name.SetValue('')
        self.text_ctrl_supplier_address.SetValue('')
        self.text_ctrl_supplier_telp.SetValue('')
             
        sql = "SELECT name, address, telp FROM suppliers WHERE id = %d" % self.sid
        supplier = fetch.getOneDict(sql)
        
        if supplier:
            name = supplier['name']
            address = supplier['address']
            telp = supplier['telp']
            
            if not name    : name =''
            if not address : address = ''
            if not telp    : telp   = ''
            
            self.text_ctrl_supplier_name.SetValue(name)
            self.text_ctrl_supplier_address.SetValue(str(address))
            self.text_ctrl_supplier_telp.SetValue(str(telp))
    
    def OnRefresh(self, evt):
	pass
        #rint'OnRefresh'

