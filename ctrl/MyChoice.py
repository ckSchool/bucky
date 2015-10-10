import wx, gVar
import loadCmbODBC as loadCmb
import fetchodbc as fetch


class MyChoice(wx.Choice): 
    def __init__(self, parent, id=-1): 
        wx.Choice.__init__(self, parent, id) 
        self.Bind(wx.EVT_CHOICE, self.OnSelect)
        self.new_id=0
        #operator_control = MyChoice (panel,-1)
        
    def initChoices(self, sql, first_item, dlg=None):
        self.dlg=dlg
        self.Clear()
        loadCmb.genAdd(self, sql, first_item)
        
    def OnSelect(self, event):
        self.new_id = fetch.cmbID(self)
        if self.new_id == -1:
            self.new_id=0
            self.Freeze()
            self.Select(1)
            
            # new something 
            dlg = self.dlg.create(None)
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    self.new_id = dlg.getNewID()
                    self.GetParent().ComboChanged(self.GetId())
            finally:
                dlg.Destroy()
                
            self.Thaw()
        
        else:
            try:
                self.GetParent().ComboChanged('school')  
            except:
                try:
                    self.GetGrandparent().ComboChanged('school')
                except:
                    pass
                
                
    def GetID(self):
        return self.new_id
 