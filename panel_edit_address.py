import wx, gVar, fetch, loadCmb

from wx.lib         import masked
from wx.lib.buttons import GenButton
from my_ctrls       import Validator

import DlgAddrItemEditor

nextItem_id = 0
        
class panel_edit_address(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.spc1 = wx.Panel(self, -1)
        self.panel_base = wx.Panel(self, -1)
        self.spc2 = wx.Panel(self, -1)
        
        self.panel_buttons = wx.Panel(self.panel_base, -1)
        self.button_save   = wx.Button(self.panel_buttons, -1, "Save")
        self.button_edit   = wx.Button(self.panel_buttons, -1, "Cancel")
        
        self.panel_house            = wx.Panel(self.panel_base, -1)
	
	self.label_spc_addr         = wx.StaticText(self.panel_house, -1, "")
	self.text_ctrl_address      = wx.TextCtrl(self.panel_house, -1, style = wx.TE_MULTILINE|wx.TE_READONLY)
	self.text_ctrl_address.SetLabelText('dfdsfsdf') 
        
        self.label_house            = wx.StaticText(self.panel_house, -1, "House Name/\nNumber")
        self.text_ctrl_house        = wx.TextCtrl(self.panel_house,   -1, "No.", validator = Validator())
        
        self.label_street           = wx.StaticText(self.panel_house, -1, "Street")
        self.text_ctrl_street       = wx.TextCtrl(self.panel_house,   -1, "", validator = Validator())
        
        self.label_in_estate        = wx.StaticText(self.panel_house, -1, "In Estate")
        
        self.panel_estate           = wx.Panel(self.panel_house, -1)
        
        self.checkbox_in_estate     = wx.CheckBox(self.panel_estate,   -1, "")
        self.label_in_cemara        = wx.StaticText(self.panel_estate,   -1, "      ")
        self.button_cemara          = GenButton(self.panel_estate,   -1, "Cemara Asri")
        
        self.label_estate           = wx.StaticText(self.panel_house, -1, "Estate")
        self.combo_box_estate       = wx.ComboBox(self.panel_house,   -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
    
        self.label_block            = wx.StaticText(self.panel_house, -1, "Block")
        self.text_ctrl_block        = wx.TextCtrl(self.panel_house,   -1, "Blok ", validator = Validator())
    
        self.label_road             = wx.StaticText(self.panel_house, -1, "Road")
        self.text_ctrl_road         = wx.TextCtrl(self.panel_house,   -1, "Jl. ", validator = Validator())

        self.panel_post        = wx.Panel(self.panel_base, -1)
        
        self.label_postcode    = wx.StaticText(self.panel_post, -1, "Postcode")
        self.num_ctrl_postcode = masked.NumCtrl(self.panel_post, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        self.pcs1              = wx.Panel(self.panel_post, -1)
        self.panel_spc_post1   = wx.Panel(self.panel_post, -1)
        
        self.label_kelurahan   = wx.StaticText(self.panel_post, -1, "Kelurahan")
        self.combo_kelurahan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.label_kecamatan   = wx.StaticText(self.panel_post, -1, "Kecamatan")
        self.combo_kecamatan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
 
        self.label_kabupaten   = wx.StaticText(self.panel_post, -1, "Kabupaten")
        self.combo_kabupaten   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.label_province    = wx.StaticText(self.panel_post, -1, "Province")
        self.combo_province    = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.label_country     = wx.StaticText(self.panel_post, -1, "Country")
        self.combo_country     = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
       
	self.button_edit_kel       = GenButton(self.panel_post, -1, 'Edit')
        self.button_edit_kec       = GenButton(self.panel_post, -1, 'Edit')
	self.button_edit_kab       = GenButton(self.panel_post, -1, 'Edit')
	self.button_edit_prov      = GenButton(self.panel_post, -1, 'Edit')
	self.button_edit_country   = GenButton(self.panel_post, -1, 'Edit')
	
	self.button_kel_cancel     = wx.Button(self.panel_post, -1, 'Cancel')
        self.button_kec_cancel     = wx.Button(self.panel_post, -1, 'Cancel')
        self.button_kab_cancel     = wx.Button(self.panel_post, -1, 'Cancel')
        self.button_prov_cancel    = wx.Button(self.panel_post, -1, 'Cancel')
        self.button_country_cancel = wx.Button(self.panel_post, -1, 'Cancel')
        
        self.estate_ctrls =(self.label_estate,
                            self.combo_box_estate,
                            self.label_block,
                            self.text_ctrl_block,
                            self.label_in_cemara,
                            self.button_cemara)
        
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
        
        self.Bind(wx.EVT_BUTTON,   self.EditKel,           self.button_edit_kel)
        self.Bind(wx.EVT_BUTTON,   self.EditKec,           self.button_edit_kec)
        self.Bind(wx.EVT_BUTTON,   self.EditKab,           self.button_edit_kab)
        self.Bind(wx.EVT_BUTTON,   self.EditProv,          self.button_edit_prov)
        self.Bind(wx.EVT_BUTTON,   self.EditCountry,       self.button_edit_country)
        
        self.Bind(wx.EVT_BUTTON,   self.OnCancelKelurahan, self.button_kel_cancel)
        self.Bind(wx.EVT_BUTTON,   self.OnCancelKecamatan, self.button_kec_cancel)
        self.Bind(wx.EVT_BUTTON,   self.OnCancelKabupaten, self.button_kab_cancel)
        self.Bind(wx.EVT_BUTTON,   self.OnCancelProvince,  self.button_prov_cancel)
        self.Bind(wx.EVT_BUTTON,   self.OnCancelCountry,   self.button_country_cancel)
        
        self.Bind(wx.EVT_BUTTON,   self.InCemaraAsri,      self.button_cemara)
        #self.Bind(wx.EVT_BUTTON,   self.OnBack,            self.button_back)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,            self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnEdit,            self.button_edit)
                
        self.Bind(wx.EVT_CHECKBOX, self.InEstate,     self.checkbox_in_estate)
        self.Bind(wx.EVT_TEXT,     self.OnPostcode,   self.num_ctrl_postcode)
        
        self.Bind(wx.EVT_COMBOBOX, self.OnEstate,     self.combo_box_estate)
        self.Bind(wx.EVT_COMBOBOX, self.OnKel,        self.combo_kelurahan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKec,        self.combo_kecamatan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKab,        self.combo_kabupaten)
        self.Bind(wx.EVT_COMBOBOX, self.OnProvince,   self.combo_province)
        self.Bind(wx.EVT_COMBOBOX, self.OnCountry,    self.combo_country)
        
        self.__set_properties()
        self.__do_layout()
	
        self.displayData()
        
    def __set_properties(self):
	self.button_cemara.SetBezelWidth(1)
        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")

        for b in self.btns_edit:
	    b.SetBezelWidth(1)
            b.SetMinSize((55,23))
            b.SetFont(font)
	    b.SetToolTipString('To create new item\nempty combo first')
	    b.SetLabelText('New/Edit')

        self.label_house.SetMinSize((80,-1))
        self.label_country.SetMinSize((80,-1))
        self.panel_spc_post1.SetMinSize((45,-1))
        self.button_cemara.SetMinSize((85,18))
        self.SetMinSize((420,500))
	
	self.text_ctrl_address.SetEditable(False)
	self.selectResidesPanel()
	
    def __do_layout(self):
	sizer_base       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top        = wx.BoxSizer(wx.HORIZONTAL)
	grid_sizer_est   = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_house = wx.FlexGridSizer( 7, 2, 5, 5)
        grid_sizer_post  = wx.FlexGridSizer( 6, 4, 5, 5)
        sizer_main       = wx.BoxSizer(wx.VERTICAL)
        
	grid_sizer_house.AddGrowableCol(1)
	grid_sizer_post.AddGrowableCol(1)
	
        #sizer_top.Add(self.button_back,            0, 0, 0)
        #sizer_top.Add(self.panel_spct1,            1, 0, 0)
	sizer_top.Add(self.button_edit,            0, 0, 0)
        sizer_top.Add(self.button_save,            0, 0, 0)
        self.panel_buttons.SetSizer(sizer_top)
        
	grid_sizer_est.Add(self.checkbox_in_estate,0, 0, 0)
        grid_sizer_est.Add(self.label_in_cemara,   0, wx.LEFT | wx.RIGHT, 5)
        grid_sizer_est.Add(self.button_cemara,     0, 0, 0)
        self.panel_estate.SetSizer(grid_sizer_est)
	
	
	grid_sizer_house.Add(self.label_spc_addr,    0, wx.EXPAND | wx.TOP | wx.BOTTOM , 20)
	grid_sizer_house.Add(self.text_ctrl_address, 0, wx.EXPAND | wx.TOP | wx.BOTTOM , 20)
	
        grid_sizer_house.Add(self.label_street,    0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_street,0, wx.EXPAND, 0)
	
	grid_sizer_house.Add(self.label_house,     0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_house, 0, 0, 0)
        
        grid_sizer_house.Add(self.label_in_estate, 0, wx.TOP | wx.EXPAND, 14)
        grid_sizer_house.Add(self.panel_estate,    0, wx.TOP , 15)
        
        grid_sizer_house.Add(self.label_estate,    0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_box_estate,1, wx.EXPAND, 0)
        
        grid_sizer_house.Add(self.label_block,     0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_block, 0, 0, 0)
        
        grid_sizer_house.Add(self.label_road,      0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_road,  1, wx.EXPAND, 0)
        
        self.panel_house.SetSizer(grid_sizer_house)
        
        grid_sizer_post.Add(self.label_kelurahan,       0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.combo_kelurahan,       1, wx.EXPAND, 0)
        grid_sizer_post.Add(self.button_edit_kel,       0, 0, 0)
        grid_sizer_post.Add(self.button_kel_cancel,     0, wx.EXPAND, 0)
        
        grid_sizer_post.Add(self.label_kecamatan,       0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.combo_kecamatan,       1, wx.EXPAND, 0)
        grid_sizer_post.Add(self.button_edit_kec,       0, 0, 0)
        grid_sizer_post.Add(self.button_kec_cancel,     0, wx.EXPAND, 0)
        
        grid_sizer_post.Add(self.label_kabupaten,       0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.combo_kabupaten,       1, wx.EXPAND, 0)
        grid_sizer_post.Add(self.button_edit_kab,       0, 0, 0)
        grid_sizer_post.Add(self.button_kab_cancel,     0, wx.EXPAND, 0)
	
	grid_sizer_post.Add(self.label_postcode,        0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.num_ctrl_postcode,     0, 0, 0)
        grid_sizer_post.Add(self.pcs1,                  0, 0, 0)
        grid_sizer_post.Add(self.panel_spc_post1,       0, wx.EXPAND, 0)
        
        grid_sizer_post.Add(self.label_province,        0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.combo_province,        1, wx.EXPAND, 0)
        grid_sizer_post.Add(self.button_edit_prov,      0, 0, 0)
        grid_sizer_post.Add(self.button_prov_cancel,    0, wx.EXPAND, 0)
                       
        grid_sizer_post.Add(self.label_country,         0, wx.EXPAND, 0)
        grid_sizer_post.Add(self.combo_country,         1, wx.EXPAND, 0)
        grid_sizer_post.Add(self.button_edit_country,   0, 0, 0)
        grid_sizer_post.Add(self.button_country_cancel, 0, wx.EXPAND, 0)
	
        self.panel_post.SetSizer(grid_sizer_post)
        
        # ----------- main  sizer --------------------------
        
        sizer_main.Add(self.panel_house,   0, wx.EXPAND | wx.TOP, 10)
        sizer_main.Add(self.panel_post,    1, wx.EXPAND | wx.TOP,  5)
	sizer_main.Add(self.panel_buttons, 0, wx.EXPAND, 10)
        self.panel_base.SetSizer(sizer_main)
        
	sizer_base.Add(self.spc1,       0, 0, 0)
	sizer_base.Add(self.panel_base, 0, wx.LEFT, 15)
	sizer_base.Add(self.spc2,       1, 0, 0)
	self.SetSizer(sizer_base)
	
        self.Layout()

    def displayData(self):
        self.address = gVar.address
        self.numCtrlActive = False
        self.loadAllCombos()
        self.enableCombos()
        self.num_ctrl_postcode.SetValue(0)
        
        if self.address:
            self.loadAddress(self.address)
        else:
            self.loadAllCombos()

    def loadAddress(self, address):
	gVar.editedFlag = False
	# change kode to the selected address
        #sql = "SELECT AlamatA FROM OrangTua WHERE Kode = %d" % kode
        

        self.text_ctrl_address.SetValue(address)
        
	itemList = self.splitAddress(address)
	addrLen = len(itemList)
	if addrLen != 11:
	    for i in range(0, 11-addrLen):
		itemList.append('')
	street,house,estate,block,road,kelurahan,kecamatan,kabupaten,postcode,province,country = itemList

	
	street    = street.strip()
	house     = house.strip()
	estate    = estate.strip()
	block     = block.strip()
	road      = road.strip()
	kelurahan = kelurahan.strip()
	kecamatan = kecamatan.strip()
	kabupaten = kabupaten.strip()
	postcode  = postcode.strip()
	province  = province.strip()
	country   = country.strip()
	
	self.text_ctrl_block.SetValue(block)
	self.text_ctrl_house.SetValue(house)
	self.text_ctrl_road.SetValue(road)
	self.text_ctrl_street.SetValue(street)
	if estate:
	    self.checkbox_in_estate.SetValue(1)
	    self.selectResidesPanel()
	    loadCmb.restore_str(self.combo_box_estate, estate)
	  
	try :
	    postcode = int(postcode)
	    postcode = postcode*1
	    if isinstance(postcode, int):
		#rint 'postcode.isdigit'
		self.num_ctrl_postcode.SetValue(int(postcode))
		kecamatanID = fetch.cmbID(self.combo_kecamatan)
		self.loadCmbsUnderKecID(kecamatanID)
		#rint 'restore_str ,',kelurahan
		loadCmb.restore_str(self.combo_kelurahan, kelurahan)
		
	    else:
		loadCmb.restore_str(self.combo_country, country)
		loadCmb.restore_str(self.combo_country, province)
		loadCmb.restore_str(self.combo_country, kabupaten)
		loadCmb.restore_str(self.combo_country, kecamatan)
		loadCmb.restore_str(self.combo_country, kelurahan)
	except:
	    pass
	    #rint'oh no'

    def loadCmbsUnderKecID(self, kecamatanID):
        loadCmb.restore(self.combo_kecamatan, kecamatanID)
        
        selectedKabupatenID = fetch.cmbID(self.combo_kabupaten)
        selectedProvinceID  = fetch.cmbID(self.combo_province)
        # step 1: working down -------------------------------
        
        # do for kabupaten --------------------------------
        kabupatenList       = fetch.kabupatenForKecamatanID(kecamatanID)
        if selectedKabupatenID in self.idList(kabupatenList):
            return

        kabupatenID = self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)              
        provinceID  = self.provincesForKabupaten(kabupatenID, selectedKabupatenID)
        
        self.countriesForProvince(provinceID, selectedProvinceID)
        
        loadCmb.address_items(self.combo_kelurahan, 'kelurahan', kecamatanID)
            
    def loadAllCombos(self):
        self.combo_kelurahan.SetName('c_kelurahan')
        self.combo_kecamatan.SetName('c_kecamatan')
        self.combo_kabupaten.SetName('c_kabupaten')
        self.combo_province.SetName( 'c_province')
        self.combo_country.SetName(  'c_country')
        
        loadCmb.address_items(self.combo_box_estate, 'estate', 0)
        loadCmb.address_items(self.combo_kecamatan, 'kecamatan', 0)
        loadCmb.address_items(self.combo_kabupaten, 'kabupaten', 0)
        loadCmb.address_items(self.combo_province,  'province',  0)
        loadCmb.address_items(self.combo_country,   'country',   0)
        
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
        #rint'OnPostcode'
        if self.numCtrlActive:  return
        
        postcode = self.num_ctrl_postcode.GetValue()
        if postcode:
            for c in self.combos: c.SetSelection(-1)
            sql = "SELECT id, itemName \
                     FROM address_items \
                    WHERE itemType= 'kecamatan' \
		      AND postcode = %d" % postcode
            res = fetch.getOneDict(sql)
            if res:
                iid  = res['id']
                kecamatan = res['itemName']
                loadCmb.restore(self.combo_kecamatan, iid)
                #fetch.msg('postcode')
                self.loadCmbsUnderKecID(iid)
    
    def resetCmb(self, cmb):
        cmb.Freeze()
        cmb.SetSelection(0)
        cmb.Thaw()
          
    def selectResidesPanel(self):
        if self.checkbox_in_estate.Value:
            for c in self.estate_ctrls:
                c.Show()
        else:
            for c in self.estate_ctrls:
                c.Hide()   
        self.Layout()  
          
    def InEstate(self, event):
        self.selectResidesPanel()
        
    def OnEstate(self, evt):
        #rint 'OnEstate'
        if fetch.cmbValue(self.combo_box_estate)=="Perum. Cemara Asri":
            #rint 'Perum. Cemara Asri'
            self.InCemaraAsri(wx.Event)
          
    def InCemaraAsri(self, event):
        self.checkbox_in_estate.SetValue(1)
        self.num_ctrl_postcode.SetValue(20371)
        self.text_ctrl_road.SetValue('Jl. Cemara')
        loadCmb.restore_str(self.combo_box_estate, 'Perum. Cemara Asri')
        loadCmb.restore_str(self.combo_kelurahan,  'Sampali')
          
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
        self.GetTopLevelParent().goBack()

    def splitAddress(self, address):
	return address.split(',')
    
    def getValues(self):
        return (self.text_ctrl_street.GetValue().strip(),
		self.text_ctrl_house.GetValue().strip(),
		str(fetch.cmbValue(self.combo_box_estate)),
		self.text_ctrl_block.GetValue().strip(),
		self.text_ctrl_road.GetValue().strip(),
                str(fetch.cmbValue(self.combo_kelurahan)),
                str(fetch.cmbValue(self.combo_kecamatan)),
                str(fetch.cmbValue(self.combo_kabupaten)),
		str(self.num_ctrl_postcode.GetValue()),
                str(fetch.cmbValue(self.combo_province)),
		str(fetch.cmbValue(self.combo_country)))
        
    def OnSave(self, evt):
	street    = str(self.text_ctrl_street.GetValue()).strip()
	house     = str(self.text_ctrl_house.GetValue()).strip()
	estate    = str(fetch.cmbValue(self.combo_box_estate))
	block     = str(self.text_ctrl_block.GetValue()).strip()
	road      = str(self.text_ctrl_road.GetValue()).strip()
	kelurahan = str(fetch.cmbValue(self.combo_kelurahan))
	kecamatan = str(fetch.cmbValue(self.combo_kecamatan))
	kabupaten = str(fetch.cmbValue(self.combo_kabupaten))
	postcode  = str(self.num_ctrl_postcode.GetValue())
	province  = str(fetch.cmbValue(self.combo_province))
	country   = str(fetch.cmbValue(self.combo_country))
			    
	if not street or not house or not province:
	    fetch.msg('At least houseNo, street & province are needed')
	    return
	
	address =','.join((street,house,estate,block,road,kelurahan,kecamatan,kabupaten,postcode,province,country))
        #rintgVar.table, gVar.column, address, gVar.guardian_id
	sql = "UPDATE %s \
                  SET %s= '%s' \
                WHERE id = %d" %(gVar.table, gVar.column, address, gVar.guardian_id)
        #rintsql
        fetch.updateDB(sql)
	gVar.editedFlag = True
	#rint'set gVar.editedFlag to True'
	self.GetTopLevelParent().goBack()
	

    def OnEdit(self, evt):
        self.OnBack(wx.Event)
        
    def edit(self, cmb1, cmb2, itemType):
        #rint 'editing type:',itemType
        nextItem = ''
        self.restore_id, restoreString = fetch.cmbIDV(cmb1)
        if not self.restore_id:
            # prepare data for new entry
            if itemType=='country':
                self.nextItemID = 0
            else:
                #rint itemType
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
                        sql = "UPDATE address_items \
                                  SET itemName ='%s' \
                                WHERE %id = %d" % (itemName, self.restore_id)
                        #rint sql
                        cmb1.SetValue(itemName)
                        
                else: # insert a new item
                    #  
                    sql = "INSERT INTO address_items \
                                  (itemName, itemType, nextItemID) \
                           VALUES ('%s', '%s', '%s')" % (
                                   itemName, itemType, self.nextItemID)
                    #rint sql
                      
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

