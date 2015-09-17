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

        for b in self.btns_edit:
            b.SetMinSize((45,19))
            b.SetFont(font)

        for b in self.btns_cancel:
            b.SetMinSize((45,19))
            b.SetFont(font)
            b.Hide()
            
        self.panel_spc_post1.SetMinSize((45,-1))
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

    def displayData(self, address_id=1):
        self.address_id = address_id
	self.numCtrlActive = False
        self.loadAllCombos()
        self.enableCombos()
        self.num_ctrl_postcode.SetValue(0)
	
        if address_id:
            self.loadAddress(address_id)
        else:
            self.loadAllCombos()
	    
    
    def loadAddress(self, address_id):
	print 'loadAddress'
	
	sql = "SELECT postcode \
		 FROM addresses \
		WHERE id = %d" % address_id
	print sql
        postcode = fetch.getDig(sql)
	#if postcode:
	self.num_ctrl_postcode.SetValue(str(postcode))
	sql = "SELECT id, itemName \
		 FROM addressItems \
		WHERE itemType = 'kecamatan' \
		  AND postcode = %d " % postcode
	dataSet = fetch.getAllCol(sql)
	if len(dataSet)!=1: # as it should

	    print ' what to do ?'
	    return
	kecamatanID = dataSet[0][0]
	loadCmb.restore(self.combo_kecamatan, kecamatanID)
	
	selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
	selectedProvinceID  = fetch.cmbID(self.combo_province)
        # step 1: working down -------------------------------
        
	#kecamatan = 
        # do for kabupaten --------------------------------
        kabupatenList       = fetch.kabupatenForKecamatanID(kecamatanID)
        if selectedKabupatenID in self.idList(kabupatenList):
	    return

        kabupatenID = self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)              
	provinceID  = self.provincesForKabupaten(kabupatenID, selectedKabupatenID)
	
        self.countriesForProvince(provinceID, selectedProvinceID)
	
	return
        # step 2 - work up
        kelurahanList = fetch.kelurahanForKecamatanID(kecamatanID)
	#rint 'upFillKel   kelurahanList', kelurahanList
        self.upFillKel(kelurahanList)    
            
    def loadAllCombos(self):
	self.combo_kabupaten.SetName('c_kabupaten')
	self.combo_kecamatan.SetName('c_kecamatan')
	self.combo_kelurahan.SetName('c_kelurahan')
	self.combo_province.SetName('c_province')
	self.combo_country.SetName('c_country')
	
        loadCmb.addressItems(self.combo_kabupaten, 'kabupaten', 0)
        loadCmb.addressItems(self.combo_kecamatan, 'kecamatan', 0)
        #loadCmb.addressItems(self.combo_kelurahan, 'kelurahan', 0)
        loadCmb.addressItems(self.combo_province,  'province',  0)
        loadCmb.addressItems(self.combo_country,   'country',   0)
        
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
     
    def restore_id(self, cmb):
        if not loadCmb.restore(self.combo_province, self.restoreID):
            self.combo_province.SetSelection(0)
        self.enableCombos()
        
    def OnPostcode(self, evt):
        #rint 'OnPostcode'
        if self.numCtrlActive:  return
        
        postcode = self.num_ctrl_postcode.GetValue()
        if postcode:
            for c in self.combos: c.SetSelection(-1)
            sql = "SELECT id, itemName \
                     FROM addressItems \
                    WHERE postcode = %d" % postcode
            res = fetch.getOneDict(sql)
            if res:
                iid  = res['id']
                kecamatan = res['itemName']
                if kecamatan:
                    loadCmb.restore(self.combo_kecamatan, iid)
		    fetch.msg('postcode')
                    self.loadCmbsUnderKecID(iid)
    
    def resetCmb(self, cmb):
        cmb.Freeze()
        cmb.SetSelection(0)
        cmb.Thaw()
            
    def OnCountry(self, evt):
        countryID = fetch.cmbID(self.combo_country)
	if countryID:
	    provinceList        = fetch.provincesForCountryID(countryID)
	    selectedProvinceID  = fetch.cmbID(self.combo_province)
	    provinceID          = self.setComboItems(self.combo_province, provinceList)
	    provinceIDlist      = self.idList(provinceList)
	    if provinceID:
		if provinceID != selectedProvinceID:
		    kabupatenID = self.kabupatenForProvince(provinceIDlist)
	    else:
		# combo_province may have been loaded with a list of provinces
		# or none
		if provinceList:
		    kabupatenID = self.kabupatenForProvince(provinceIDlist)

    def kabupatenForProvince(self, provinceIDlist):
	kabupatenList   = fetch.kabupatenForProvinceList(provinceIDlist)
	if kabupatenList:# load combo_kabupaten up with kabupaten for provinceID
	    return self.setComboItems(self.combo_kabupaten, kabupatenList)
	else:
	    return 0
    
    def OnProvince(self, event):
	selectedProvinceID, province = fetch.cmbIDV(self.combo_province)
	if selectedProvinceID:
	    countryList = fetch.countriesForProvinceID(selectedProvinceID)
	    if countryList:
		selectedCountryID = fetch.cmbID(self.combo_country)
		self.setGen(selectedCountryID, countryList, self.combo_country)
	# work up ---------------------
	kabupatenList       = fetch.kabupatenForProvinceID(selectedProvinceID)
	selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
	if selectedKabupatenID in self.idList(kabupatenList):
	    return
	self.clearPostcodeCtrls((self.combo_kecamatan,
				 self.combo_kabupaten,
				 self.combo_kelurahan))
        #  kabupaten --------------------------
        if kabupatenList:
            kabupatenID = self.setComboItems(self.combo_kabupaten, kabupatenList)
            if selectedKabupatenID != kabupatenID:
		pass
		# select kecamatan for all kabupaten in list 

    def OnKab(self, event):
	selectedKabupatenID, kabupaten = fetch.cmbIDV(self.combo_kabupaten)
        provinceList       = fetch.provincesForKabupaten(kabupaten)
	selectedProvinceID = fetch.cmbID(self.combo_province)
	provinceID         = self.setGen(selectedProvinceID, provinceList, self.combo_province)
	if selectedProvinceID != provinceID:
	    self.countriesForProvince(provinceID, selectedProvinceID)
	
        # step 2: work upward -----------------------
        kecamatenList = fetch.kecamatanForKabupatenID(selectedKabupatenID)
        if kecamatenList:
	    selectedKecamatenID = fetch.cmbID(self.combo_kecamatan)
            kecamatenID = self.setComboItems(self.combo_kecamatan, kecamatenList)
            if kecamatenID != selectedKecamatenID:
                self.resetCmb(self.combo_kelurahan)

    def OnKec(self, event):
        selectedKecamatanID, kecamatan = fetch.cmbIDV(self.combo_kecamatan)
	selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
	selectedProvinceID  = fetch.cmbID(self.combo_province)
	
	if selectedKecamatanID:
	    self.postcodeForKecamatan(selectedKecamatanID)
	    #  working down ----------------
	    kabupatenList = fetch.kabupatenForKecamatanID(selectedKecamatanID)
	    if kabupatenList:
		kabupatenID  = self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)
		if selectedKabupatenID != kabupatenID:
		    provinceList       = fetch.provincesForKabupatenID(kabupatenID)
		    selectedProvinceID = fetch.cmbID(self.combo_province)
		    provinceID         = self.setGen(selectedProvinceID, provinceList, self.combo_province)
		    if selectedProvinceID != provinceID:
			self.countriesForProvince(provinceID, provinceID)
	    # step 2 - work up
	    self.resetCmb(self.combo_kelurahan)
	    alist = fetch.kelurahanForKecamatanID(selectedKecamatanID)
	    self.setComboItems(self.combo_kelurahan, alist)

    

    def OnKel(self, event):
        selectedKecamatanID = fetch.cmbID(self.combo_kecamatan)
	selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
	selectedProvinceID  = fetch.cmbID(self.combo_province)
	
        if selectedKecamatanID:    return

        # kecamatan -----------------------------
        kecamatanList = fetch.kecamatanForKelurahanID(kelurahanID)
        kecamatanID   = self.setKecamatan(selectedKecamatanID, kecamatanList) 
        kabupatenID   = self.doForKabupaten(kecamatanID, selectedKecamatanID)
        provinceID    = self.provincesForKabupaten(kabupatenID, selectedKabupatenID)
	
        self.countriesForProvince(provinceID, selectedProvinceID)

    def clearPostcodeCtrls(self, ctrls):
        for cmb in ctrls:
            cmb.Freeze()
            cmb.SetSelection(0)
            cmb.Thaw()
        self.num_ctrl_postcode.Freeze()
        self.num_ctrl_postcode.Clear()
        self.num_ctrl_postcode.Thaw()
        
    def setComboItems(self, cmb, itemsList):
        selectedID = fetch.cmbID(cmb)
        cmb.Freeze()
	cmb.Clear()
        for row in itemsList:
            cmb.Append(str(row[1]), row[0])
        cmb.Insert(' ', 0)
        cmb.Thaw()
        
        selectedID = loadCmb.restore(cmb, selectedID)
        if not selectedID:
            if len(itemsList) == 1:
                selectedID = itemsList[0][0]
                loadCmb.restore(cmb, selectedID)
        return selectedID
    
    def postcodeForKecamatan(self, kecamatanID):
        self.numCtrlActive = True
        try:     self.num_ctrl_postcode.SetValue(fetch.postcodeForKecID(kecamatanID))
        except:  self.num_ctrl_postcode.Clear()
        self.numCtrlActive = False
    
    def idList(self, data):
        myl = []
        for r in data:    myl.append(r[0])
        return myl

    def countriesForProvince(self, setID, selectedID):
	cmb = self.combo_country
	cmbID = fetch.cmbID(cmb)
        if selectedID: aList = fetch.countriesForProvinceID(selectedID)
        else:          aList = fetch.countriesForProvinceID(setID)
	return self.setGen(cmbID, aList, cmb)
	
    def provincesForKabupaten(self, setID, selectedID):
	cmb = self.combo_province
	cmbID = fetch.cmbID(cmb)
        if selectedID: aList = fetch.provinceForKabupatenID(selectedKabupatenID)
        else:          aList = fetch.provinceForKabupatenID(setID)
        return self.setGen(cmbID, aList, cmb)
    
    def kabupatenForKecamatan(self,  setID, selectedID):
	cmb = self.combo_kabupaten
	cmbID = fetch.cmbID(cmb)
        if selectedID: aList = fetch.kabForKacID(selectedID)
        else:          aList = fetch.kabForKacID(setID)
        return self.setGen(cmbID, aList, cmb)
    
    def kecForKel(self, kelID, selectedKelID):
	cmb = self.combo_kecamatan
	cmbID = fetch.cmbID(cmb)
        if selectedID: aList = fetch.kecForKelID(selectedKelID)
        else:          aList = fetch.kecForKelID(kelID)
        return self.setGen(cmbID, aList, cmb)
    
    def bForA(self, AID, selectedID, cmb, call):
	cmbID = fetch.cmbID(cmb)
        if selectedAID: aList = call(selecteID)
        else:           aList = call(AID)
        return self.setGen(cmbID, aList, cmb)
    
    def doForKabupaten(self, kecamatanID, selectedKecamatanID):
	selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
        if kecamatanID: kabupatenList = fetch.provinceForKabupaten(selectedKecamatanID)
        else:           kabupatenList = fetch.proviceForKecamatan(selectedKecamatanID)
        return self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)
            
    def upFillKel(self, kelurahanList):
	self.setComboItems(self.combo_kelurahan, kelurahanList)
        """if kelurahanList:
            self.setComboItems(self.combo_kelurahan, kelurahanList)
	    selectedKelurahanID = self.setComboItems(self.combo_kelurahan, kelurahanList)
	    if selectedKelurahanID in self.idList(kelurahanList): return
            elif len(kelurahanList) == 1:
		kelurahanID = kelurahanList[0][0]
		loadCmb.restore(self.combo_box_kel, kelurahanID)"""

    def setKecamatan(self, selectedKecamatanID, kecamatanList):
        self.setGen(selectedKecamatanID, kecamatanList, self.combo_kecamatan)
        self.postcodeClear()
        return 0

    def setGen(self, selectedItemID, aList, cmb):
        if aList:
	    r = aList[0]
	    if len(r) != 2:
		fetch.msg('list error')
	    
            if len(aList)  > 1: selectedItemID = self.setComboItems(cmb, aList)
            elif len(aList)==1:
		selectedItemID =  aList[0][0]
		loadCmb.restore(cmb, selectedItemID)
            else:               self.clearPostcodeCtrls((cmb,))
        return selectedItemID
   
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
                fetch.cmbID(self.combo_kelurahan),
                fetch.cmbID(self.combo_kecamatan),
                fetch.cmbID(self.combo_kabupaten),
                fetch.cmbID(self.combo_province))
        
    def updatePostcode(self, post, kal, kec, kab, prov): 
        sql = "UPDATE postcodes \
                      (kelurahan, kecamatan, kabupaten, province) \
               VALUES (?, ?, ?, ?) \
                WHERE postcode =%d" % post
        data = [kal, kec, kab, prov]
        #rint 'updatePostcode' , sql, data; return
        fetch.updateDB_data(sql, data)
    
    def insertPostcode(self, post, kal, kec, kab, prov): 
        sql = "INSERT INTO postcodes \
                      (kelurahan, kecamatan, kabupaten, province, postcode) \
               VALUES (?, ?, ?, ?, ?)"
        data =  [kal, kec, kab, prov, post]
        #rint 'insertPostcode ', sql, data; return
        fetch.updateDB_data(sql, data)

    def OnEdit(self, evt):
        self.OnBack(wx.Event)
	
    def edit(self, cmb1, cmb2, itemType):
	print 'editing type:',itemType
	nextItem = ''
        self.restore_id, restoreString = fetch.cmbIDV(cmb1)
	if not self.restore_id:
	    # prepare data for new entry
	    if itemType=='country':
		self.nextItemID = 0
	    else:
		print itemType
		nextItemID, nextItem = fetch.cmbIDV(cmb2)
		if not nextItemID:
		    fetch.msg('Please Select A Follow On Item')
		    return
        
        dlg = DlgAddrItemEditor.create(None)
        try:
            dlg.displayData(self.restore_id, itemType, nextItem)
            if dlg.ShowModal() == wx.ID_OK:
                itemName = dlg.itemName
		if not itemName: return
		
		# prevent duplicate name if country
		# prevent duplicate name where next item same
		# warning of other duplicate names -if not kelurahan
		
                if self.restore_id: # editing an item
		    if itemName == restoreString:
			return
                    else:
			sql = "UPDATE addressItems \
				  SET itemName ='%s' \
				WHERE %id = %d" % (itemName, self.restore_id)
			print sql
			cmb1.SetValue(itemName)
			
                else: # insert a new item
		    #  
                    sql = "INSERT INTO addressItems \
		                  (itemName, itemType, nextItemID) \
                           VALUES ('%s', '%s', '%s')" % (
			           itemName, itemType, self.nextItemID)
		    print sql
                      
        finally:    
            dlg.Destroy()
	
    def EditKel(self, evt):
        self.edit(self.combo_kelurahan, self.combo_kecamatan, 'kelurahan')
    
    def EditKec(self, evt):
        self.edit(self.combo_kecamatan, self.combo_kabupaten, 'kecamatan')
        
    def EditKab(self, evt):
        self.edit(self.combo_kabupaten, self.combo_province,  'kabupaten')
    
    def EditProv(self, evt):
        self.edit(self.combo_province, self.combo_country,     'province')
    
    def EditCountry(self, evt):
        self.edit(self.combo_country, None, 'country')
    
    def OnCancelKelurahan(self, evt):
        self.restore_id(self.combo_kelurahan)

    def OnCancelKecamatan(self, evt):
        self.restore_id(self.combo_kelurahan)

    def OnCancelKabupaten(self, evt):
        self.restore_id(self.combo_kabupaten)
    
    def OnCancelProvince(self, evt):
        self.restore_id(self.combo_province)
	
    def OnCancelCountry(self, evt):
	self.restore_id(self.combo_country)
        #if not loadCmb.restore(self.combo_country, self.restoreID):
        #    self.combo_country.SetSelection(0)
        #self.enableCombos()
        
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