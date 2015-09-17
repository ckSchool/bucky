import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb
from  wx.lib import masked

from my_ctrls import Validator
       
class panel_edit_address(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
	
	self.spc1 = wx.Panel(self, -1)
	self.panel_base = wx.Panel(self, -1)
	self.spc2 = wx.Panel(self, -1)
        
        self.panel_top   = wx.Panel(self.panel_base, -1)
        self.button_back = wx.Button(self.panel_top, -1, "< Back")
        self.panel_spct1 = wx.Panel( self.panel_top,  -1)
        self.button_save = wx.Button(self.panel_top, -1, "Save")
        self.button_edit = wx.Button(self.panel_top, -1, "Cancel")

        self.button_back.SetBackgroundColour('grey')
        self.button_save.SetBackgroundColour('grey')
        self.button_edit.SetBackgroundColour('grey')

        self.panel_address          = wx.Panel(self.panel_base, -1)
        
        self.label_house            = wx.StaticText(self.panel_address, -1, "House Name/\nNumber")
        
        self.text_ctrl_house        = wx.TextCtrl(self.panel_address,   -1, "", validator = Validator())
        
        self.label_street           = wx.StaticText(self.panel_address, -1, "Street")
        self.text_ctrl_street       = wx.TextCtrl(self.panel_address,   -1, "", validator = Validator())
        
        self.label_within_estate    = wx.StaticText(self.panel_address, -1, "In Estate")
        
        self.panel_x = wx.Panel(self.panel_address, -1)
        
        self.checkbox_within_estate = wx.CheckBox(self.panel_x,   -1, "")
        self.label_in_cemara        = wx.StaticText(self.panel_x,   -1, "Cemara Asri")
        self.button_cemara          = wx.Button(self.panel_x,   -1, "")
        
        
        self.label_estate           = wx.StaticText(self.panel_address, -1, "Estate")
        self.combo_box_estate       = wx.ComboBox(self.panel_address,   -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
    
        self.label_block            = wx.StaticText(self.panel_address, -1, "Block")
        self.text_ctrl_block        = wx.TextCtrl(self.panel_address,   -1, "", validator = Validator())
    
        self.label_road             = wx.StaticText(self.panel_address, -1, "Road")
        self.text_ctrl_road         = wx.TextCtrl(self.panel_address,   -1, "", validator = Validator())

        
        self.label_postcode         = wx.StaticText(self.panel_address, -1, "Postcode")
        self.num_ctrl_postcode      = masked.NumCtrl(self.panel_address, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        
        self.label_kabupaten        = wx.StaticText(self.panel_address, -1, "Kabupaten")
        self.combo_kabupaten          = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.label_kecamatan        = wx.StaticText(self.panel_address, -1, "Kecamatan")
        self.combo_kecamatan        = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.lable_kelurahan        = wx.StaticText(self.panel_address, -1, "Kelurahan")
        self.combo_kelurahan        = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.label_province         = wx.StaticText(self.panel_address, -1, "Province")
        self.combo_province         = wx.ComboBox(  self.panel_address, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        
        self.estate_ctrls =(self.label_estate,
                            self.combo_box_estate,
                            self.label_block,
                            self.text_ctrl_block,
			    self.label_in_cemara,
			    self.button_cemara)
        
        self.combos = (     self.combo_kabupaten,
                            self.combo_kecamatan,
                            self.combo_kelurahan,
                            self.combo_province)

        self.Bind(wx.EVT_TEXT,     self.OnPostcode, self.num_ctrl_postcode)

        
        self.Bind(wx.EVT_BUTTON,   self.OnBack,     self.button_back)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,     self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnEdit,     self.button_edit)
    
        self.Bind(wx.EVT_COMBOBOX, self.OnProvince, self.combo_province)
        self.Bind(wx.EVT_COMBOBOX, self.OnKab,      self.combo_kabupaten)
        self.Bind(wx.EVT_COMBOBOX, self.OnKec,      self.combo_kecamatan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKel,      self.combo_kelurahan)
	
	
        self.Bind(wx.EVT_CHECKBOX, self.InEstate,   self.checkbox_within_estate)
        self.Bind(wx.EVT_BUTTON,   self.InCemaraAsri,  self.button_cemara)
	self.Bind(wx.EVT_COMBOBOX, self.OnEstate,   self.combo_box_estate)
        
        self.__set_properties()
        self.__do_layout()
        self.displayData()

    def __set_properties(self):
	self.panel_base.SetMinSize((300, 400))
        font = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.label_within_estate.SetFont(font)
        self.label_province.SetMinSize((75, 21))
        self.checkbox_within_estate.SetValue(1)
        self.SetMinSize((300,400))
	self.combo_kabupaten.SetEditable(False)
        self.combo_kecamatan.SetEditable(False)
        self.combo_kelurahan.SetEditable(False)
        self.combo_province.SetEditable(False)
	self.button_cemara.SetMaxSize((35,15))

        
    def __do_layout(self):
	sizer_base = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top         = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_house  = wx.FlexGridSizer(11, 2, 5, 5)
        sizer_main        = wx.BoxSizer(wx.VERTICAL)
	
        grid_sizer_house.AddGrowableCol(1)
        
        sizer_top.Add(self.button_back, 0, 0, 0)
        sizer_top.Add(self.panel_spct1, 1, 0, 0)
        sizer_top.Add(self.button_save, 0, 0, 0)
        sizer_top.Add(self.button_edit, 0, 0, 0)
        self.panel_top.SetSizer(sizer_top)
        
        grid_sizer_house.Add(self.label_house,      0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_house,  0, 0, 0)
        
        grid_sizer_house.Add(self.label_street,     0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_street, 0, wx.EXPAND, 0)

        gs = wx.BoxSizer(wx.HORIZONTAL)
        gs.Add(self.checkbox_within_estate, 0, 0, 0)
        gs.Add(self.label_in_cemara,        0, wx.LEFT | wx.RIGHT, 5)
        gs.Add(self.button_cemara,          0, 0, 0)
        self.panel_x.SetSizer(gs)
        
	grid_sizer_house.Add(self.label_within_estate, 0, wx.TOP | wx.EXPAND, 14)
        grid_sizer_house.Add(self.panel_x, 0, wx.TOP , 15)
        
        grid_sizer_house.Add(self.label_estate,      0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_box_estate,  1, wx.EXPAND, 0)
        
        grid_sizer_house.Add(self.label_block,       0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_block,   0, 0, 0)
        
        grid_sizer_house.Add(self.label_road,        0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_road,    1, wx.EXPAND, 0)
        
        grid_sizer_house.Add(self.label_postcode,    0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.num_ctrl_postcode, 0, 0, 0)
        
        grid_sizer_house.Add(self.lable_kelurahan,   0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_kelurahan,   1, wx.EXPAND, 0)
    
        grid_sizer_house.Add(self.label_kecamatan,   0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_kecamatan,   1, wx.EXPAND, 0)
        
        grid_sizer_house.Add(self.label_kabupaten,   0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_kabupaten,   1, wx.EXPAND, 0)
        
        grid_sizer_house.Add(self.label_province,    0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.combo_province,    1, wx.EXPAND, 0)
        
        self.panel_address.SetSizer(grid_sizer_house)
        
        # ----------- main  sizer --------------------------
        sizer_main.Add(self.panel_top,     0, wx.EXPAND, 10)
        sizer_main.Add(self.panel_address, 1, wx.EXPAND | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_main)
        
	sizer_base.Add(self.spc1,1,0,0)
	sizer_base.Add(self.panel_base, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
	sizer_base.Add(self.spc2,1,0,0)
	self.SetSizer(sizer_base)
        self.Layout()
    
    def displayData(self, address_id=0):
        self.numCtrlActive = False
        self.address_id = address_id
        self.loadAllCombos()
        self.num_ctrl_postcode.SetValue(0)
        
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
                
    def loadAllCombos(self):
        loadCmb.kab(self.combo_kabupaten)
        loadCmb.kec(self.combo_kecamatan)
        loadCmb.kel(self.combo_kelurahan)
        loadCmb.prov(self.combo_province)
        
        loadCmb.estates(self.combo_box_estate)
	
        print 'loaded all'      
    
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
	print 'OnEstate'
	if fetch.cmbValue(self.combo_box_estate)=="Perum. Cemara Asri":
	    print 'Perum. Cemara Asri'
	    self.InCemaraAsri(wx.Event)
          
    def InCemaraAsri(self, event):
        self.checkbox_within_estate.SetValue(1)
        self.num_ctrl_postcode.SetValue(20371)
        self.text_ctrl_road.SetValue('Cemara')
        loadCmb.restore_str(self.combo_box_estate, 'Perum. Cemara Asri')
        loadCmb.restore_str(self.combo_kelurahan,  'Sampali')
        
    def OnPostcode(self, event):
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
                    
    def OnProvince(self, event):
	print 'on province'
	return
        province = fetch.cmbValue(self.combo_province)
        self.loadCmbsUnderProv(province)

    def OnKab(self, event):
        kabupaten = fetch.cmbValue(self.combo_kabupaten)
        self.loadCmbsUnderKab(kabupaten)
        
    def OnKec(self, event):
        kecamatan = fetch.cmbValue(self.combo_kecamatan)
        self.loadCmbsUnderKec(kecamatan)
        
    def OnKel(self, event):
        kelurahan = fetch.cmbValue(self.combo_kelurahan)
        self.loadCmbsUnderKel(kelurahan)
    
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
	
    def loadCmbsUnderProv(self, province):
        kabupatenList = fetch.kabupatenForProvince(province)
	kecamatenList = fetch.kecamatanForProvince(province)
	
        selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	selectedKecamtan  = fetch.cmbValue(self.combo_kecamatan) 
        selectedKelurahan = fetch.cmbValue(self.combo_kelurahan)

        if selectedKabupaten in kabupatenList:  return
        
        #  kabupaten --------------------------
	self.clearPostcodeCtrls((self.combo_kabupaten, ))
        self.clearPostcodeCtrls((self.combo_kecamatan, self.combo_kabupaten, self.combo_kelurahan))
        
        if kabupatenList:
            kabupaten = self.setComboItems(self.combo_kabupaten, kabupatenList)
            if kabupaten in kabupatenList:  return
                
	#  kecamaten --------------------------
	if selectedKecamaten in kecamatenList: return
	
	self.clearPostcodeCtrls((self.combo_kecamatan, ))
	if kecamatenList:  
	    kecamaten = self.setComboItems(self.combo_kacamatan, kecamatenList)
	    if kecamaten in kecamatenList:
		self.postcodeForKecamatan(kecamaten)
		return
	    
	self.loadKelurahanProvince(province)


    def loadKelurahanProvince(self, province):
	#self.postcodeClear()
	print 'loadKelurahanProvince'
	selectedKelurahan = fetch.cmbValue(self.combo_kelurahan)
	kelurahanList     = fetch.kelurahanForProvince(province)	    
	if kelurahanList:
	    if selectedKelurahan in kelurahanList: return
	    kelurahan = self.setComboItems(self.combo_kelurahan, kelurahanList)
	    if not (kelurahan in kelurahanList) and len(kelurahanList)==1:
		loadCmb.restore_str(self.combo_box_kel, kelurahan)

    def loadCmbsUnderKab(self, kabupaten):
        #self.postcodeClear()
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
        #self.postcodeClear()
        self.postcodeForKecamatan(kecamatan)
	print 'loadCmbsUnderKec', kecamatan
        
	# step 1: working down -------------------------------
        
        # do for kabupaten --------------------------------
        kabupatenList     = fetch.kabupatenForKecamatan(kecamatan)
        selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	
	if selectedKabupaten in kabupatenList: return
	
        kabupaten = self.setKabupaten(selectedKabupaten, kabupatenList )               
        
        #  do for province -------------------------------
	selectedProvince = fetch.cmbValue(self.combo_province)
        if kabupaten:
            provinceList = fetch.provinceForKabupaten(selectedKabupaten)
	    self.setProvinces(selectedProvince, provinceList)
	    
        else:
            provinceList = fetch.proviceForKecamatan(kecamatan)
            self.setProvinces(selectedProvince, provinceList)

        # step 2 - work up
        kelurahanList = fetch.kelurahanForKecamatan(kecamatan)
        self.upFillKel(kelurahanList)
        
    def loadCmbsUnderKel(self, kelurahan):
        #self.postcodeClear()
	print 'loadCmbsUnderKel'
	
        selectedKecamatan = fetch.cmbValue(self.combo_kecamatan)
        if selectedKecamatan:    return

        # kecamatan -----------------------------
        kecamatanList     = fetch.kecamatanForKelurahan(kelurahan)
	print kelurahan, ' kelurahan > kecamatan', kecamatanList
        selectedKecamatan = self.setKecamatan(selectedKecamatan, kecamatanList) 

        # kabupaten ------------------------------
	kabupatenList     = fetch.kabupatenForKecamatan(selectedKecamatan)
	
	selectedKabupaten = fetch.cmbValue(self.combo_kabupaten)
	
        if selectedKabupaten in kabupatenList:     return
	
	kabupaten = self.setKabupaten(selectedKabupaten, kabupatenList)  

        # province -------------------------------
	selectedProvince = fetch.cmbValue(self.combo_province)
        if kabupaten:
            provinceList = fetch.provinceForKabupaten(selectedKabupaten)
	    self.setProvinces(selectedProvince, provinceList)
                
        else:
            provinceList = fetch.proviceForKecamatan(selectedKecamatan)
            self.setProvinces(selectedProvince, provinceList)

    def upFillKel(self, kelurahanList):
	if kelurahanList:  
	    selectedKelurahan = self.setComboItems(self.combo_kelurahan, kelurahanList)
	    if selectedKelurahan in kelurahanList:
		return
	    elif len(kelurahanList) == 1:
		loadCmb.restore_str(self.combo_box_kel, kelurahanList[0])
		
		
    def setKelurahan(self, selectedKelurahan, kelurahanList):
	print 'setKelurahan'
	if kelurahanList:
	    if len(kecamatanList) == 1:
		kelurahan = kelurahanList[0]
		loadCmb.restore_str(self.combo_kelurahan, kelurahan)
	    else:
		kelurahan = self.setComboItems(self.combo_kecamatan, kelurahanList)
	    return kelurahan
	    
	else:
	    return ''

    def setKecamatan(self, selectedKecamatan, kecamatanList):
	print 'setKecamatan'
	if kecamatanList:
	    if len(kecamatanList) == 1:
		kecamatan = kecamatanList[0]
		loadCmb.restore_str(self.combo_kecamatan, kecamatan)
	    else:
		kecamatan = self.setComboItems(self.combo_kecamatan, kecamatanList)
	     
	    print ' set postcode for ', kecamatan
	    self.postcodeForKecamatan(kecamatan)
	    return kecamatan

	else:
	    print 'postcodeClear'
	    self.postcodeClear()
	    return ''
    
    def setKabupaten(self, selectedKabupaten, kabupatenList):
	print 'setKabupaten'
	if kabupatenList:
	    if len(kabupatenList)>1:
		selectedKabupaten = self.setComboItems(self.combo_kabupaten, kabupatenList)
	    
	    elif len(kabupatenList)==1:
		    loadCmb.restore_str(self.combo_kabupaten, kabupatenList[0])
	    
	    else:
		self.setComboItems(self.combo_kabupaten, kabupatenList)
	return selectedKabupaten
    
    def setProvinces(self, selectedProvince, provinceList):
	print 'setProvinces'
	if provinceList:
	    if len(provinceList)>1:
		selectedProvince = self.setComboItems(self.combo_province, provinceList)
		
	    elif len(provinceList)==1:
		loadCmb.restore_str(self.combo_province, provinceList[0])
		
	    else: 
		self.clearPostcodeCtrls((self.combo_province,))
	return selectedProvince
    # -------------------------------------------------------------------
		
    def postcodeClear(self):
        self.numCtrlActive = True
        self.num_ctrl_postcode.Clear()
        self.numCtrlActive = False

    def OnBack(self, evt):
        self.GetTopLevelParent().goBack()
        
    def OnSave(self, evt):
        if self.address_id: self.updateAddress()
        else:               self.insertAddress()

    def getValues(self):
        house  = self.text_ctrl_house.GetValue()
        street = self.text_ctrl_street.GetValue()
        estate = fetch.cmbValue(self.combo_box_estate)
        block  = self.text_ctrl_block.GetValue()
        road   = self.text_ctrl_road.GetValue()
        post   = self.num_ctrl_postcode.GetValue()
        kal    = fetch.cmbValue(self.combo_kelurahan)
        kec    = fetch.cmbValue(self.combo_kecamatan)
        kab    = fetch.cmbValue(self.combo_kabupaten)
        prov   = fetch.cmbValue(self.combo_province)
	
	#if not estate in listEstates:

        return (house, street, estate, block, road, post, kal, kec, kab, prov)

 
    def updateAddress(self):
        house, street, estate, block, road, post, kal, kec, kab, prov = self.getValues()
        sql = "UPDATE addresses \
                  SET number, street, estate, block, road, postcode \
               VALUES (%,     %,      %,      %,     %,    %) \
                WHERE self.addr_id=%d" 
        data = (house, street, estate, block, road, post, self.addr_id)
        print sql, data; return
        fetch.updateDB_data(sql, data)
        
        if self.postcodeExists(postcode):  self.updatePostcode()
        else:                              self.insertPostcode()
    
    def insertAddress(self):
        house, street, estate, block, road, post, kal, kec, kab, prov = self.getValues()
	if house and (street or road) and post :
	    sql = '''INSERT INTO addresses \
			  (house, street, estate, block, road, postcode) \
		   VALUES (?,  ?,   ?,   ?,  ?,  ?) '''
	    data = [house, street, estate, block, road, post]
	    #print sql, data; return
	    fetch.updateDB_data(sql, data)
	else:
	    fetch.msg('house, post code street or road missing')
        
    def updatePostcode(self):
        house, street, estate, block, road, post, kal, kec, kab, prov = self.getValues()
	if post:
	    sql = "UPDATE postcodes \
		      (kelurahan, kecamatan, kabupaten, province) \
		   VALUES (?, ?, ?, ?) \
		    WHERE postcode =%d" % post
	    data = [kal, kec, kab, prov]
	    print 'updatePostcode' , sql, data; return
	    fetch.updateDB_data(sql, data)
	    
        else:
	    fetch.msg('house, post code street or road missing')
	    
    def insertPostcode(self):
        house, street, estate, block, road, post, kal, kec, kab, prov = self.getValues()
	if post:
	    sql = "INSERT INTO postcodes \
		      SET kelurahan, kecamatan, kabupaten, province \
		   VALUES (?, ?, ?, ?, ?)\
		    WHERE postcode = %d" %post
	    data =  [kal, kec, kab, prov]
	    print 'insertPostcode ', sql, data; return
	    fetch.updateDB_data(sql, data)

    def OnEdit(self, evt):
        self.OnBack(wx.Event)
        
# --------------------------------------------------------------------------    
        
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1)
        
        self.SetBackgroundColour('grey')
        p = self.panel_edit_address = panel_edit_address(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(p, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Center()
        self.Fit()
"""        
class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
app = MyApp(redirect=False)
app.MainLoop()"""