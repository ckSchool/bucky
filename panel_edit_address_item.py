import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb

#import DlgAddrItemEdit, re


next_id = 0
dicStreetInEst = {}
dicEst = {}
dicRd = {}
dicKel = {}
dicKec = {}
dicKab = {}
dicProv = {}
dicCountry = {}

class edit_address_item(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
	self.button_back         = wx.Button(self,     -1, '< Back')
	self.label_spc1          = wx.StaticText(self, -1, '')
	
        self.label_addressItem   = wx.StaticText(self, -1, 'Name')
	self.txtCtrl_addressItem = wx.TextCtrl(self,   -1, '')
	
	self.label_item_type     = wx.StaticText(self, -1, 'Item Type')
        self.choice_item_type    = wx.ComboBox(self,   -1, choices=[])
	
        self.label_spc2          = wx.StaticText(self, -1, '')
        self.button_save         = wx.Button(self.p_kelToCountry,-1, 'Save' )
	
	self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)
	self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)
        
        self.__do_layout()
        self.__do_main()

    def __do_layout(self):
        sizer_1 = wx.FlexGridSizer(cols=2, hgap=5, rows=4, vgap=3)

	sizer_1.Add(self.button_back ,0,0,0)
	sizer_1.Add(self.label_spc1 ,0,0,0)

        sizer_1.Add(self.label_addressItem ,0,0,0)
	sizer_1.Add(self.txtCtrl_addressItem ,0,0,0)
	
	sizer_1.Add(self.label_item_type ,0,0,0)
	sizer_1.Add(self.choice_item_type ,0,0,0)
	
	sizer_1.Add(self.label_spc2 ,0,0,0)
	sizer_1.Add(self.button_save ,0,0,0)
	
        self.SetSizer(sizer_1)



    def __do_main(self):	
        pass
    
    def OnBack(self, evt):
	pass
    
    def OnSave(self, evt):
	pass
        

        
    def displayData(self, item_id = 0):
	#rint'panel_edit_address_item : displayData'
        self.item_id = int(item_id)

            
