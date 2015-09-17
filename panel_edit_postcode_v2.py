import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb
from  wx.lib import masked

from my_ctrls import Validator
import DlgAddrItemEditor

nextItem_id = 0
        
class panel_edit_postcode(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_top   = wx.Panel(self, -1)
        self.button_back = wx.Button(self.panel_top, -1, "< Back")
        self.panel_spct1 = wx.Panel( self.panel_top, -1)
        self.button_save = wx.Button(self.panel_top, -1, "Save")
        self.button_edit = wx.Button(self.panel_top, -1, "Cancel")

        self.button_back.SetBackgroundColour('grey')
        self.button_save.SetBackgroundColour('grey')
        self.button_edit.SetBackgroundColour('grey')

        self.panel_address     = wx.Panel(self, -1)
        
        self.label_postcode    = wx.StaticText(self.panel_address, -1, "Postcode")
        self.num_ctrl_postcode = masked.NumCtrl(self.panel_address, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        self.pcs1              = wx.Panel(self.panel_address, -1)
	self.panel_spc_post1   = wx.Panel(self.panel_address, -1)
	
        self.label_kelurahan   = wx.StaticText(self.panel_address, -1, "Kelurahan")
	self.combo_kelurahan   = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
	self.button_edit_kel   = wx.Button(    self.panel_address, -1, 'Edit')
	self.button_kel_cancel = wx.Button(    self.panel_address, -1, 'Cancel')
	
        self.label_kecamatan   = wx.StaticText(self.panel_address, -1, "Kecamatan")
	self.combo_kecamatan   = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
	self.button_edit_kec   = wx.Button(    self.panel_address, -1, 'Edit')
	self.button_kec_cancel = wx.Button(    self.panel_address, -1, 'Cancel')
	
        self.label_kabupaten   = wx.StaticText(self.panel_address, -1, "Kabupaten")
	self.combo_kabupaten   = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
	self.button_edit_kab   = wx.Button(    self.panel_address, -1, 'Edit')
	self.button_kab_cancel = wx.Button(    self.panel_address, -1, 'Cancel')
	
        self.label_province     = wx.StaticText(self.panel_address, -1, "Province")
	self.combo_province     = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
	self.button_edit_prov   = wx.Button(    self.panel_address, -1, 'Edit')
	self.button_prov_cancel = wx.Button(    self.panel_address, -1, 'Cancel')
	
	self.label_country         = wx.StaticText(self.panel_address, -1, "Country")
        self.combo_country         = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
	self.button_edit_country   = wx.Button(    self.panel_address, -1, 'Edit')
	self.button_country_cancel = wx.Button(    self.panel_address, -1, 'Cancel')
	
	self.btns_edit   =(self.button_edit_kel,
			   self.button_edit_kec,
			   self.button_edit_kab,
			   self.button_edit_prov,
			   self.button_edit_country)
	
	self.btns_cancel =(self.button_kel_cancel,
			   self.button_kec_cancel,
			   self.button_kab_cancel,
			   self.button_prov_cancel,
			   self.button_country_cancel)
	
        self.combos = (    self.combo_kabupaten,
                           self.combo_kecamatan,
                           self.combo_kelurahan,
                           self.combo_province,
			   self.combo_country)
	
	self.Bind(wx.EVT_BUTTON,   self.EditKel,     self.button_edit_kel)
	self.Bind(wx.EVT_BUTTON,   self.EditKec,     self.button_edit_kec)
	self.Bind(wx.EVT_BUTTON,   self.EditKab,     self.button_edit_kab)
	self.Bind(wx.EVT_BUTTON,   self.EditProv,    self.button_edit_prov)
	self.Bind(wx.EVT_BUTTON,   self.EditCountry, self.button_edit_country)

        self.Bind(wx.EVT_TEXT,     self.OnPostcode, self.num_ctrl_postcode)
	
	self.Bind(wx.EVT_BUTTON,   self.OnCancelKelurahan,self.button_kel_cancel)
	self.Bind(wx.EVT_BUTTON,   self.OnCancelKecamatan,self.button_kec_cancel)
	self.Bind(wx.EVT_BUTTON,   self.OnCancelKabupaten,self.button_kab_cancel)
	self.Bind(wx.EVT_BUTTON,   self.OnCancelProvince, self.button_prov_cancel)
	self.Bind(wx.EVT_BUTTON,   self.OnCancelCountry,  self.button_country_cancel)
	
        self.Bind(wx.EVT_BUTTON,   self.OnBack,     self.button_back)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,     self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnEdit,     self.button_edit)
	
	self.Bind(wx.EVT_COMBOBOX, self.OnKel,      self.combo_kelurahan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKec,      self.combo_kecamatan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKab,      self.combo_kabupaten)
	self.Bind(wx.EVT_COMBOBOX, self.OnProvince, self.combo_province)
	self.Bind(wx.EVT_COMBOBOX, self.OnCountry,  self.combo_country)
	
        self.__set_properties()
        self.__do_layout()
        self.displayData()
	
    def __set_properties(self):
	font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")
	#.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
	
	for b in self.btns_edit:
	    b.SetMinSize((45,19))
	    b.SetFont(font)

	for b in self.btns_cancel:
	    b.SetMinSize((45,19))
	    b.SetFont(font)
	    b.Hide()
	    
	self.panel_spc_post1.SetMinSize((45,-1))

        self.label_province.SetMinSize((75, 21))
        self.SetMinSize((450,400))

    def __do_layout(self):
        sizer_top   = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer  = wx.FlexGridSizer(6, 4, 5, 5)
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        
	grid_sizer.Add(self.label_postcode,    0, wx.EXPAND, 0)
        grid_sizer.Add(self.num_ctrl_postcode, 0, 0, 0)
	grid_sizer.Add(self.pcs1,              0, 0, 0)
	grid_sizer.Add(self.panel_spc_post1,   0, wx.EXPAND, 0)
        
        grid_sizer.Add(self.label_kelurahan,   0, wx.EXPAND, 0)
	grid_sizer.Add(self.combo_kelurahan,   1, wx.EXPAND, 0)
	grid_sizer.Add(self.button_edit_kel,   0, 0, 0)
	grid_sizer.Add(self.button_kel_cancel, 0, wx.EXPAND, 0)
	    
        grid_sizer.Add(self.label_kecamatan,   0, wx.EXPAND, 0)
        grid_sizer.Add(self.combo_kecamatan,   1, wx.EXPAND, 0)
	grid_sizer.Add(self.button_edit_kec,   0, 0, 0)
	grid_sizer.Add(self.button_kec_cancel, 0, wx.EXPAND, 0)
	
        grid_sizer.Add(self.label_kabupaten,   0, wx.EXPAND, 0)
        grid_sizer.Add(self.combo_kabupaten,   1, wx.EXPAND, 0)
	grid_sizer.Add(self.button_edit_kab,   0, 0, 0)
	grid_sizer.Add(self.button_kab_cancel, 0, wx.EXPAND, 0)
        
        grid_sizer.Add(self.label_province,     0, wx.EXPAND, 0)
        grid_sizer.Add(self.combo_province,     1, wx.EXPAND, 0)
	grid_sizer.Add(self.button_edit_prov,   0, 0, 0)
	grid_sizer.Add(self.button_prov_cancel, 0, wx.EXPAND, 0)
		       
	grid_sizer.Add(self.label_country,         0, wx.EXPAND, 0)
        grid_sizer.Add(self.combo_country,         1, wx.EXPAND, 0)
	grid_sizer.Add(self.button_edit_country,   0, 0, 0)
	grid_sizer.Add(self.button_country_cancel, 0, wx.EXPAND, 0)
	
        grid_sizer.AddGrowableCol(1)
        
        sizer_top.Add(self.button_back, 0, 0, 0)
        sizer_top.Add(self.panel_spct1, 1, 0, 0)
        sizer_top.Add(self.button_save, 0, 0, 0)
        sizer_top.Add(self.button_edit, 0, 0, 0)
        self.panel_top.SetSizer(sizer_top)
    
        self.panel_address.SetSizer(grid_sizer)
        
        # ----------- main  sizer --------------------------
        sizer_main.Add(self.panel_top,     0, wx.EXPAND, 10)
        sizer_main.Add(self.panel_address, 1, wx.EXPAND | wx.TOP, 10)
        self.SetSizer(sizer_main)
        
        self.Layout()
    
    def displayData(self, address_id=0):
	self.address_id = address_id
	
        self.numCtrlActive = False
        self.loadAllCombos()
	self.enableCombos()
        self.num_ctrl_postcode.SetValue(0)

	if address_id:
	    sql = "SELECT poscode FROM addresses WHERE address_id = %d" % address_id
	    postcode = fetch.getStr(sql)
	    if postcode:
		sql = "SELECT * FROM postcodes WHERE postcode =%d" % postcode
		dataSet = fetch.getOneDict(sql)
		self.num_ctrl_postcode.SetValue(dataSet['postcode'])
		kelurahan, kecamatan, kabupaten, province = (dataSet('kelurahan'), dataSet('kecamatan'), dataSet('kabupaten'), dataSet('province'))
		
		if kelurahan:
		    loadCmb.restore_str(self.combo_kabupaten, kabupaten)
		    self.loadCmbsUnderKab(kabupaten)
		    
		elif kecamatan:
		    loadCmb.restore_str(self.combo_kecamatan, kecamatan)
		    self.loadCmbsUnderKec(kecamatan)
		    
		elif kelurahan:
		    loadCmb.restore_str(self.combo_kelurahan, kelurahan)
		    self.loadCmbsUnderKal(kelurahan)
        else:
	    self.loadAllCombos()
	    
    def loadAllCombos(self):
	#loadCmb.addressItems(self.combo_kabupaten, 'kabupaten', 0)
        loadCmb.kab(self.combo_kabupaten)
        loadCmb.kec(self.combo_kecamatan)
        loadCmb.kel(self.combo_kelurahan)
        loadCmb.prov(self.combo_province)
	loadCmb.countries(self.combo_country)
	
    def enableCombos(self):
	for c in self.combos:
	    c.Enable()
	    c.SetEditable(False)
	for b in self.btns_cancel: b.Hide()
	for b in self.btns_edit:   b.Show()
	    
    def disableCombos(self, cmb):
	for b in self.btns_edit:   b.Show() 
	for c in self.combos:
	    if c != cmb:
		c.Disable()
		c.SetEditable(False)
	    else:
		c.SetEditable(True)
		
    def edit(self, cmb1, cmb2, itemType):
	self.restore_str = fetch.cmbValue(cmb1)
	nextItem = fetch.cmbValue(cmb2)
	if not nextItem: return
	
	nextItemID = fetch.cmbID(cmb2)
	
	dlg = DlgAddrItemEditor.create(None)
	try:
	    dlg.displayData(self.restore_str)
	    if dlg.ShowModal() == wx.ID_OK:
		itemName = dlg.itemName
		if self.restore_str: # update an edited item
		    if itemName and itemName != self.restore_str:
			# test to make sure name is unique
			print 'save ', itemName
			print 'next item id ='
			cmb1.SetValue(itemName)
		    else: # insert a new item
			sql = "INSERT INTO addressItems (itemName, itemType, nextItemID) \
	                                         VALUES ('%s', '%s', '%s')" % (itemName, itemType, self.nextItemID)
		      
	finally:    
	    dlg.Destroy()
    
    def EditKel(self, evt): 
	self.edit(self.combo_kelurahan, self.combo_kecamatan, 'kelurahan')
    
    def EditKec(self, evt):
	self.edit(self.combo_kecamatan, self.combo_kabupaten, 'kecamatan')
	
    def EditKab(self, evt):
	self.edit(self.combo_kabupaten, self.combo_province,  'kabupaten')
    
    def EditProv(self, evt):
	self.edit(self.combo_province,self.combo_country,     'country')
    
    def EditCountry(self, evt):
	self.edit(self.combo_country, None)
    
    def OnCancelKelurahan(self, evt):
	self.restore_str(self.combo_kelurahan)

    def OnCancelKecamatan(self, evt):
	self.restore_str(self.combo_kelurahan)

    def OnCancelKabupaten(self, evt):
	self.restore_str(self.combo_kabupaten)
    
    def OnCancelProvince(self, evt):
	self.restore_str(self.combo_province)
	
    def restore_str(self, cmb):
	if not loadCmb.restore_str(self.combo_province, self.restoreStr):
	    self.combo_province.SetSelection(-1)
	self.enableCombos()
	
    def OnCancelCountry(self, evt):
	if not loadCmb.restore_str(self.combo_country, self.restoreStr):
	    self.combo_country.SetSelection(-1)
	self.enableCombos()
	
    def OnPostcode(self,evt):
	if self.numCtrlActive:  return
	
        postcode = self.num_ctrl_postcode.GetValue()
        if postcode:
            for c in self.combos: c.SetSelection(-1)
            sql = "SELECT kecamatan, kabupaten, province \
                     FROM postcodes \
                    WHERE postcode = %d" % postcode
            res = fetch.getOneDict(sql)
            if res:
                province  = res['province']
                kecamatan = res['kecamatan']
                kabupaten = res['kabupaten']
                if kecamatan:
                    loadCmb.restore_str(self.combo_kecamatan, kecamatan)
                    self.loadCmbsUnderKec(kecamatan)
                    
                elif kabupaten:
		    loadCmb.restore_str(self.combo_kabupaten, kabupaten)
                    self.loadCmbsUnderKab(kabupaten)
                    
                elif province:
		    loadCmb.restore_str(self.province, province)
                    self.loadCmbsUnderProv(province)
    
    def resetCmb(self, cmb, msg):
	fetch.msg(msg)
	cmb.Freeze()
	cmb.SetSelection(-1)
	cmb.Thaw()
	
    def gen(self, cmbA, cmbB, btnA, msg, x):
	self.restoreStr = itemA = fetch.cmbValue(cmbA)
	itemB = fetch.cmbValue(cmbB)
	if itemA == '-new-':
	    if itemB and itemB != '-new-':
		btnA.Show()
		self.disableCombos(cmbA)
	    else: 
		self.resetCmb(cmbA, msg)
	else:
	    self.enableCombos()
	    x(itemA)
	    
    def OnCountry(self, evt):
	self.restoreStr = country = fetch.cmbValue(self.combo_country)
	if country == '-new-':
	    button_country_cancel.Show()
	    self.disableCombos(self.combo_country)
	else:
	    self.enableCombos()
	    self.loadCmbsUnderCountry(country)
	
    def OnProvince(self, event):
	self.gen(self.combo_province,
		 self.combo_country,
		 self.button_prov_cancel,
		 'select a country',
		 self.loadCmbsUnderProv)

    def OnKab(self, event):
	self.gen(self.combo_kabupaten,
		 self.combo_province,
		 self.button_kab_cancel,
		 'select a province',
		 self.loadCmbsUnderKab)
        
    def OnKec(self, event):
	self.gen(self.combo_kecamatan,
		 self.combo_kabupaten,
		 self.button_kec_cancel,
		 'select a kabupaten',
		 self.loadCmbsUnderKec)
        
    def OnKel(self, event):
	self.gen(self.combo_kelurahan,
		 self.combo_kecamatan,
		 self.button_kel_cancel,
		 'select a kecamtan',
		 self.loadCmbsUnderKel)
    
    def clearPostcodeCtrls(self, ctrls):
        for cmb in ctrls:
            cmb.Freeze()
            cmb.SetSelection(-1)
            cmb.Thaw()
            
        self.num_ctrl_postcode.Freeze()
        self.num_ctrl_postcode.Clear()
        self.num_ctrl_postcode.Thaw()
        
    def setComboItems(self, cmb, items):
        selected = fetch.cmbValue(cmb)
        cmb.Freeze()
        cmb.SetItems(items)
	cmb.Insert('-new-', 0)
        cmb.Thaw()
        selected = loadCmb.restore_str(cmb, selected)
	print ' restored item',selected 
	if not selected:
	    print ' nothing selected'
	    if len(items)==1:
		selected = items[0]
		print 'only one in the list', selected
		loadCmb.restore_str(cmb, selected)
        return selected
    
    def postcodeForKecamatan(self, kecamatan):
        self.num_ctrl_postcode.Freeze()
        try:
            self.num_ctrl_postcode.SetValue(fetch.postcodeForKec(kecamatan))
	except:
	    self.num_ctrl_postcode.SetValue()
        finally:
            self.num_ctrl_postcode.Thaw()
    
	
    # main auto fill code --------------------------------
    def loadCmbsUnderCountry(self, country):
	provinceList  = fetch.provincesForCountry(country)
	kabupatenList = fetch.kabupatenForCountry(country)
	
	selectedProvince  = fetch.cmbValue(self.combo_province)
	selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	selectedKecamatan = fetch.cmbValue(self.combo_kecamatan) 
        selectedKelurahan = fetch.cmbValue(self.combo_kelurahan)
	
	if selectedProvince in provinceList:  return
	
	
    def loadCmbsUnderProv(self, province):
        kabupatenList = fetch.kabupatenForProvince(province)
	kecamatanList = fetch.kecamatanForProvince(province)
	
        selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	selectedKecamatan = fetch.cmbValue(self.combo_kecamatan) 
        selectedKelurahan = fetch.cmbValue(self.combo_kelurahan)

        if selectedKabupaten in kabupatenList:  return
        
        #  kabupaten --------------------------
	self.clearPostcodeCtrls((self.combo_kabupaten, ))
        self.clearPostcodeCtrls((self.combo_kecamatan, self.combo_kabupaten, self.combo_kelurahan))
        
        if kabupatenList:
            kabupaten = self.setComboItems(self.combo_kabupaten, kabupatenList)
            if kabupaten in kabupatenList:  return
                
	#  kecamaten --------------------------
	if selectedKecamatan in kecamatanList: return
	
	self.clearPostcodeCtrls((self.combo_kecamatan, ))
	if kecamatanList:  
	    kecamatan = self.setComboItems(self.combo_kecamatan, kecamatanList)
	    if kecamatan in kecamatanList:
		self.postcodeForKecamatan(kecamatan)
		return
	    
	self.loadKelurahanProvince(province)

    def loadKelurahanProvince(self, province):
	print 'loadKelurahanProvince'
	selectedKelurahan = fetch.cmbValue(self.combo_kelurahan)
	kelurahanList     = fetch.kelurahanForProvince(province)	    
	if kelurahanList:
	    if selectedKelurahan in kelurahanList: return
	    
	    kelurahan = self.setComboItems(self.combo_kelurahan, kelurahanList)
	    if not (kelurahan in kelurahanList) and len(kelurahanList)==1:
		loadCmb.restore_str(self.combo_box_kel, kelurahan)

    def loadCmbsUnderKab(self, kabupaten):
        print 'loadCmbsUnderKab',kabupaten
	
	# step 1: work down -------------------------------
        provinceList = fetch.provinceForKabupaten(kabupaten)
        selectedProvince = fetch.cmbValue(self.combo_province)
	self.setComboItems(self.combo_province, provinceList)
   
        # step 2: work upward -----------------------
        kecamatenList = fetch.kecamatanForKabupaten(kabupaten)
        if kecamatenList:  
            selectedKecamaten = self.setComboItems(self.combo_kecamatan, kecamatenList)
  
            if selectedKecamaten in kecamatenList:
                pass
            elif len(kecamatenList)==1:
                kecamaten = kecamatenList[0]
                loadCmb.restore_str(self.combo_kecamatan, kecamatenList)
                self.postcodeForKecamatan(kecamaten)
                return
        
            else: #  ----------------- check / load :  kelurahan  --------------------------
                kelurahanList = fetch.kelurahanForKabupaten(kabupaten)
		self.upFillKel(kelurahanList)

    def loadCmbsUnderKec(self, kecamatan):
        self.postcodeForKecamatan(kecamatan)
	print 'loadCmbsUnderKec', kecamatan
        
	# step 1: working down -------------------------------
        
        # do for kabupaten --------------------------------
        kabupatenList     = fetch.kabupatenForKecamatan(kecamatan)
        selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	
	if selectedKabupaten in kabupatenList: return
	
        kabupaten = self.setGen(selectedKabupaten, kabupatenList, self.combo_kabupaten)              
        
        #  do for province -------------------------------
	selectedProvince = fetch.cmbValue(self.combo_province)
        if kabupaten: provinceList = fetch.provinceForKabupaten(selectedKabupaten)
        else:         provinceList = fetch.proviceForKecamatan(kecamatan)
        self.setGen( selectedProvince, provinceList, self.combo_province)

        # step 2 - work up
        kelurahanList = fetch.kelurahanForKecamatan(kecamatan)
        self.upFillKel(kelurahanList)
        
    def loadCmbsUnderKel(self, kelurahan):
	print 'loadCmbsUnderKel'
	
        selectedKecamatan = fetch.cmbValue(self.combo_kecamatan)
        if selectedKecamatan:    return

        # kecamatan -----------------------------
        kecamatanList     = fetch.kecamatanForKelurahan(kelurahan)
        selectedKecamatan = self.setKecamatan(selectedKecamatan, kecamatanList) 

        # kabupaten ------------------------------
	kabupatenList     = fetch.kabupatenForKecamatan(selectedKecamatan)
	selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	
        if selectedKabupaten in kabupatenList:     return
	
	kabupaten = self.setGen( selectedKabupaten, kabupatenList, self.combo_kabupaten)

        # province -------------------------------
	selectedProvince = fetch.cmbValue(self.combo_province)
        if kabupaten:   provinceList = fetch.provinceForKabupaten(selectedKabupaten)
        else:           provinceList = fetch.proviceForKecamatan(selectedKecamatan)
        self.setGen( selectedProvince, provinceList, self.combo_province)
	    
    def upFillKel(self, kelurahanList):
	if kelurahanList:  
	    selectedKelurahan = self.setComboItems(self.combo_kelurahan, kelurahanList)
	    if selectedKelurahan in kelurahanList: return
	    elif len(kelurahanList) == 1:          loadCmb.restore_str(self.combo_box_kel, kelurahanList[0])

    def setKecamatan(self, selectedKecamatan, kecamatanList):
	print 'setKecamatan'
	self.SetGen(selectedKecamatan, kecamatanList, self.combo_kecamatan)
	if kecamatanList:
	    return self.SetGen(selectedKecamatan, kecamatanList, self.combo_kecamatan)
	else:
	    self.postcodeClear()
	    return ''

    def setGen(self, selectedItem, aList, cmb):
	if aList:
	    if len(aList)>1:    selectedItem = self.setComboItems(cmb, aList)
	    elif len(aList)==1: loadCmb.restore_str(cmb, aList[0])
	    else:       	self.clearPostcodeCtrls((cmb,))
	return selectedItem
    # -------------------------------------------------------------------
    def postcodeClear(self):
        self.numCtrlActive = True
        self.num_ctrl_postcode.Clear()
        self.numCtrlActive = False

    def OnBack(self, evt):
        pass
        
    def OnSave(self, evt):
        if self.postcode: self.updatePostcode(self.getValues())
        else:             self.insertPostcode(self.getValues())

    def getValues(self):
        return (self.num_ctrl_postcode.GetValue(),
		fetch.cmbValue(self.combo_kelurahan),
		fetch.cmbValue(self.combo_kecamatan),
		fetch.cmbValue(self.combo_kabupaten),
		fetch.cmbValue(self.combo_province))
	
    def updatePostcode(self, post, kal, kec, kab, prov): 
        sql = "UPDATE postcodes \
		      (kelurahan, kecamatan, kabupaten, province) \
	       VALUES (?, ?, ?, ?) \
		WHERE postcode =%d" % post
	data = [kal, kec, kab, prov]
	print 'updatePostcode' , sql, data; return
	fetch.updateDB_data(sql, data)
    
    def insertPostcode(self, post, kal, kec, kab, prov): 
	sql = "INSERT INTO postcodes \
		      (kelurahan, kecamatan, kabupaten, province, postcode) \
	       VALUES (?, ?, ?, ?, ?)"
	data =  [kal, kec, kab, prov, post]
	print 'insertPostcode ', sql, data; return
	fetch.updateDB_data(sql, data)

    def OnEdit(self, evt):
        self.OnBack(wx.Event)
        
# --------------------------------------------------------------------------    
        
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1)
        
        self.SetBackgroundColour('grey')
        p = self.panel_edit_address = panel_edit_postcode(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(p, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Center()
        self.Fit()
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
app = MyApp(redirect=False)
app.MainLoop()