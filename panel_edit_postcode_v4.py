import wx, gVar, fetch, loadCmb
from  wx.lib import masked

from my_ctrls import Validator
import DlgAddrItemEditor

nextItem_id = 0
        
class panel_edit_postcode(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        #self.spc1 = wx.Panel(self, -1)
        #self.panel_base = wx.Panel(self, -1)
        #self.spc2 = wx.Panel(self, -1)
        
        self.panel_top   = wx.Panel(self, -1)
        self.button_back = wx.Button(self.panel_top, -1, "< Back")
        self.panel_spct1 = wx.Panel( self.panel_top,  -1)
        self.button_save = wx.Button(self.panel_top, -1, "Save")
        self.button_edit = wx.Button(self.panel_top, -1, "Cancel")
        
        self.text_ctrl_full_address = wx.TextCtrl(self, -1)
        
        self.panel_house            = wx.Panel(self, -1)
        
        self.label_house            = wx.StaticText(self.panel_house, -1, "House Name/\nNumber")
        self.text_ctrl_house        = wx.TextCtrl(self.panel_house,   -1, "No.", validator = Validator())
        
        self.label_street           = wx.StaticText(self.panel_house, -1, "Street")
        self.text_ctrl_street       = wx.TextCtrl(self.panel_house,   -1, "", validator = Validator())
        
        self.label_within_estate    = wx.StaticText(self.panel_house, -1, "In Estate")
        
        self.panel_x = wx.Panel(self.panel_house, -1)
        
        self.checkbox_within_estate = wx.CheckBox(self.panel_x,   -1, "")
        self.label_in_cemara        = wx.StaticText(self.panel_x,   -1, "      ")
        self.button_cemara          = wx.Button(self.panel_x,   -1, "Cemara Asri")
        
        
        self.label_estate           = wx.StaticText(self.panel_house, -1, "Estate")
        self.combo_box_estate       = wx.ComboBox(self.panel_house,   -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
    
        self.label_block            = wx.StaticText(self.panel_house, -1, "Block")
        self.text_ctrl_block        = wx.TextCtrl(self.panel_house,   -1, "Blok ", validator = Validator())
    
        self.label_road             = wx.StaticText(self.panel_house, -1, "Road")
        self.text_ctrl_road         = wx.TextCtrl(self.panel_house,   -1, "Jl. ", validator = Validator())

        self.panel_post        = wx.Panel(self, -1)
        
        self.label_postcode    = wx.StaticText(self.panel_post, -1, "Postcode")
        self.num_ctrl_postcode = masked.NumCtrl(self.panel_post, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        self.pcs1              = wx.Panel(self.panel_post, -1)
        
        self.label_kelurahan   = wx.StaticText(self.panel_post, -1, "Kelurahan")
        self.combo_kelurahan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kel   = wx.Button(    self.panel_post, -1, 'Edit')
        
        self.label_kecamatan   = wx.StaticText(self.panel_post, -1, "Kecamatan")
        self.combo_kecamatan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kec   = wx.Button(    self.panel_post, -1, 'Edit')
        
        self.label_kabupaten   = wx.StaticText(self.panel_post, -1, "Kabupaten")
        self.combo_kabupaten   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kab   = wx.Button(    self.panel_post, -1, 'Edit')
        
        self.label_province     = wx.StaticText(self.panel_post, -1, "Province")
        self.combo_province     = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_prov   = wx.Button(    self.panel_post, -1, 'Edit')
        
        self.label_country         = wx.StaticText(self.panel_post, -1, "Country")
        self.combo_country         = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_country   = wx.Button(    self.panel_post, -1, 'Edit')
        
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
        
        self.Bind(wx.EVT_BUTTON,   self.InCemaraAsri,      self.button_cemara)
        self.Bind(wx.EVT_BUTTON,   self.OnBack,            self.button_back)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,            self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnEdit,            self.button_edit)
                
        self.Bind(wx.EVT_CHECKBOX, self.InEstate,     self.checkbox_within_estate)
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
        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")

        for b in self.btns_edit:
            b.SetMinSize((55,19))
            b.SetFont(font)
	    b.SetToolTipString('To create new item\nempty combo first')
	    b.SetLabelText('New/Edit')
            
        self.button_back.SetBackgroundColour('grey')
        self.button_save.SetBackgroundColour('grey')
        self.button_edit.SetBackgroundColour('grey')
        self.label_house.SetMinSize((80,-1))
        self.label_country.SetMinSize((80,-1))
        self.button_cemara.SetMinSize((85,18))
        self.SetMinSize((420,500))
	
	self.text_ctrl_full_address.SetEditable(False)
	self.selectResidesPanel()
	
    def __do_layout(self):
        sizer_top   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_house = wx.FlexGridSizer(11, 2, 5, 5)
        sizer_auto  = wx.FlexGridSizer(6, 3, 5, 5)
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
	
	sizer_house.AddGrowableCol(1)
        
        sizer_top.Add(self.button_back, 0, 0, 0)
        sizer_top.Add(self.panel_spct1, 1, 0, 0)
        sizer_top.Add(self.button_save, 0, 0, 0)
        sizer_top.Add(self.button_edit, 0, 0, 0)
        self.panel_top.SetSizer(sizer_top)
        
        sizer_house.Add(self.label_street,     0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_street, 0, wx.EXPAND, 0)
	
	sizer_house.Add(self.label_house,      0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_house,  0, 0, 0)

        gs = wx.BoxSizer(wx.HORIZONTAL)
        gs.Add(self.checkbox_within_estate, 0, 0, 0)
        gs.Add(self.label_in_cemara,        0, wx.LEFT | wx.RIGHT, 5)
        gs.Add(self.button_cemara,          0, 0, 0)
        self.panel_x.SetSizer(gs)
        
        sizer_house.Add(self.label_within_estate, 0, wx.TOP | wx.EXPAND, 14)
        sizer_house.Add(self.panel_x, 0, wx.TOP , 15)
        
        sizer_house.Add(self.label_estate,      0, wx.EXPAND, 0)
        sizer_house.Add(self.combo_box_estate,  1, wx.EXPAND, 0)
        
        sizer_house.Add(self.label_block,       0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_block,   0, 0, 0)
        
        sizer_house.Add(self.label_road,        0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_road,    1, wx.EXPAND, 0)
        
        self.panel_house.SetSizer(sizer_house)
        
        sizer_auto.Add(self.label_kelurahan,   0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kelurahan,   1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kel,   0, 0, 0)
        
        sizer_auto.Add(self.label_kecamatan,   0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kecamatan,   1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kec,   0, 0, 0)
        
        sizer_auto.Add(self.label_kabupaten,   0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kabupaten,   1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kab,   0, 0, 0)
	
	sizer_auto.Add(self.label_postcode,    0, wx.EXPAND, 0)
        sizer_auto.Add(self.num_ctrl_postcode, 0, 0, 0)
        sizer_auto.Add(self.pcs1,              0, 0, 0)
        
        sizer_auto.Add(self.label_province,     0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_province,     1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_prov,   0, 0, 0)
                       
        sizer_auto.Add(self.label_country,         0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_country,         1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_country,   0, 0, 0)
        
        sizer_auto.AddGrowableCol(1)
        
        self.panel_post.SetSizer(sizer_auto)
        
        # ----------- main  sizer --------------------------
        sizer_main.Add(self.panel_top,    0, wx.EXPAND, 10)
        sizer_main.Add(self.text_ctrl_full_address, 0 , wx.EXPAND | wx.ALL, 20) 
        sizer_main.Add(self.panel_house,  0, wx.EXPAND | wx.TOP, 10)
        sizer_main.Add(self.panel_post,   1, wx.EXPAND | wx.TOP,  5)
        self.SetSizer(sizer_main)
        
        self.Layout()

    def displayData(self, kode=2):
        self.kode = kode
        self.numCtrlActive = False
        self.loadAllCombos()
        self.enableCombos()
        self.num_ctrl_postcode.SetValue(0)
        
        if self.kode:
            self.loadAddress(self.kode)
        else:
            self.loadAllCombos()
	    

    def loadAddress(self, guardian_id):
	# change kode tothe selected address
        sql = "SELECT address \
	         FROM guardians \
		WHERE id = %d" % guardian_id
        address = fetch.getStr(sql)
	

        self.text_ctrl_full_address.SetValue(address)
        items = self.splitAddress(address)
	if not len(items)==11:
	    return
	
	street,house,estate,block,road,kelurahan,kecamatan,kabupaten,postcode,province,country = self.splitAddress(address)
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
	    self.checkbox_within_estate.SetValue(1)
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
		print 'postcode ', postcode, ' is not digit'
		print postcode,province,country
		print kecamatan,kabupaten
		
		
		loadCmb.restore_str(self.combo_country, country)
		loadCmb.restore_str(self.combo_country, province)
		loadCmb.restore_str(self.combo_country, kabupaten)
		loadCmb.restore_str(self.combo_country, kecamatan)
		loadCmb.restore_str(self.combo_country, kelurahan)
	except:
	    print 'oh no'
        
    
    def loadCmbsUnderKecID(self, kecamatanID):
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
        
        loadCmb.addressItems(self.combo_kelurahan, 'kelurahan', kecamatanID)
            
    def loadAllCombos(self):
        self.combo_kelurahan.SetName('c_kelurahan')
        self.combo_kecamatan.SetName('c_kecamatan')
        self.combo_kabupaten.SetName('c_kabupaten')
        self.combo_province.SetName( 'c_province')
        self.combo_country.SetName(  'c_country')
        
        loadCmb.estates(self.combo_box_estate)
        #loadCmb.addressItems(self.combo_kelurahan, 'kelurahan', 0)
        loadCmb.addressItems(self.combo_kecamatan, 'kecamatan', 0)
        loadCmb.addressItems(self.combo_kabupaten, 'kabupaten', 0)
        loadCmb.addressItems(self.combo_province,  'province',  0)
        loadCmb.addressItems(self.combo_country,   'country',   0)
        
    def enableCombos(self):
        for c in self.combos:
            c.Enable()
            c.SetEditable(False)
        #for b in self.btns_cancel: b.Hide()
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
            sql = "SELECT id, name \
                     FROM address_items \
                    WHERE postcode = %d" % postcode
            res = fetch.getOneDict(sql)
            if res:
                iid  = res['id']
                kecamatan = res['name']
                if kecamatan:
                    loadCmb.restore(self.combo_kecamatan, iid)
                    #fetch.msg('postcode')
                    self.loadCmbsUnderKecID(iid)
    
    def resetCmb(self, cmb):
        cmb.Freeze()
        cmb.SetSelection(0)
        cmb.Thaw()
          
    def selectResidesPanel(self):
        if self.checkbox_within_estate.Value:
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
        self.checkbox_within_estate.SetValue(1)
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
        selectedProvinceID, province = fetch.cmbID_and_Value(self.combo_province)
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
        selectedKabupatenID, kabupaten = fetch.cmbID_and_Value(self.combo_kabupaten)
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
        selectedKecamatanID, kecamatan = fetch.cmbID_and_Value(self.combo_kecamatan)
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


    def splitAddress(self, address):
	return address.split(',')
    
    def getValues(self):
        return (
		str(self.text_ctrl_street.GetValue()),
		str(self.text_ctrl_house.GetValue()),
		str(fetch.cmbValue(self.combo_box_estate)),
		str(self.text_ctrl_block.GetValue()),
		str(self.text_ctrl_road.GetValue()),
                str(fetch.cmbValue(self.combo_kelurahan)),
                str(fetch.cmbValue(self.combo_kecamatan)),
                str(fetch.cmbValue(self.combo_kabupaten)),
		str(self.num_ctrl_postcode.GetValue()),
                str(fetch.cmbValue(self.combo_province)),
		str(fetch.cmbValue(self.combo_country)))
        
    def OnSave(self, evt):
	table = 'OrangTua' # or Wali or Staff'
	column = 'AlamatA'# or Alamat or AlamatI'
	
	street    = str(self.text_ctrl_street.GetValue())
	house     = str(self.text_ctrl_house.GetValue())
	estate    = str(fetch.cmbValue(self.combo_box_estate))
	block     = str(self.text_ctrl_block.GetValue())
	road      = str(self.text_ctrl_road.GetValue())
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
        sql = "UPDATE %s \
                  SET %s= '%s' \
                WHERE Kode =%d" %(table, column, address, self.kode)
        print sql
        #fetch.updateDB(sql)

    def OnEdit(self, evt):
        self.OnBack(wx.Event)
        
    def edit(self, cmb1, cmb2, itemType):
        #rint 'editing type:',itemType
        nextItem = ''
        self.restore_id, restoreString = fetch.cmbID_and_Value(cmb1)
        if not self.restore_id:
            # prepare data for new entry
            if itemType=='country':
                self.nextItemID = 0
            else:
                #rint itemType
                nextItemID, nextItem = fetch.cmbID_and_Value(cmb2)
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
                                  SET name ='%s' \
                                WHERE %id = %d" % (itemName, self.restore_id)
                        #rint sql
                        cmb1.SetValue(itemName)
                        
                else: # insert a new item
                    #  
                    sql = "INSERT INTO address_items \
                                  (name, type, next_item_id) \
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