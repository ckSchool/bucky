import wx, gVar, fetch, loadCmb

from panel_edit_address import panel_edit_address

#from wx.lib.pubsub import setupkwargs
#from wx.lib.pubsub import pub

from wx.lib         import masked
#from wx.lib.buttons import GenButton
from my_ctrls       import Validator

import DlgAddrItemEditor

nextItem_id = 0

def create(parent):
    return DlgEditAddress(parent)
    
class DlgEditAddress(wx.Dialog):
    _custom_classes = {'wx.Panel': ['NB']}
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base = wx.Panel(self, -1)
        
        self.panel_buttons = wx.Panel(self.panel_base, -1)
        #self.panel_buttons = wx.Panel(self, -1)
        self.button_save   = wx.Button(self.panel_buttons, -1, "Save")
        self.button_edit   = wx.Button(self.panel_buttons, -1, "Cancel")
        
        #self.panel_house            = wx.Panel(self.panel_base, -1)
        
        self.text_ctrl_full_address = wx.TextCtrl(self.panel_base, -1)
        
        self.panel_house            = wx.Panel(self.panel_base, -1)
        
        self.label_house            = wx.StaticText(self.panel_house, -1, "House Name/\nNumber")
        self.text_ctrl_house        = wx.TextCtrl(self.panel_house,   -1, "No.", validator = Validator())
        
        self.label_street           = wx.StaticText(self.panel_house, -1, "Street")
        self.text_ctrl_street       = wx.TextCtrl(self.panel_house,   -1, "", validator = Validator())
        
        self.label_within_estate    = wx.StaticText(self.panel_house, -1, "In Estate")
        
        self.panel_in_estate        = wx.Panel(self.panel_house, -1)
        self.checkbox_within_estate = wx.CheckBox(self.panel_in_estate,   -1, "")
        self.label_in_cemara        = wx.StaticText(self.panel_in_estate,   -1, "      ")
        self.button_cemara          = wx.Button(self.panel_in_estate,   -1, "Cemara Asri")
        
        
        self.label_estate           = wx.StaticText(self.panel_house, -1, "Estate")
        self.panel_estates          = wx.Panel(self.panel_house, -1)
        self.combo_estate           = wx.ComboBox(self.panel_estates,   -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_estate     = wx.Button(self.panel_estates, -1, 'New/Edit')
    
        self.label_block            = wx.StaticText(self.panel_house, -1, "Block")
        self.text_ctrl_block        = wx.TextCtrl(self.panel_house,   -1, "Blok ", validator = Validator())
    
        self.label_road             = wx.StaticText(self.panel_house, -1, "Road")
        self.text_ctrl_road         = wx.TextCtrl(self.panel_house,   -1, "Jl. ", validator = Validator())

        self.panel_post        = wx.Panel(self.panel_base, -1)
        
        self.label_postcode    = wx.StaticText(self.panel_post, -1, "Postcode")
        self.num_ctrl_postcode = masked.NumCtrl(self.panel_post, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        self.pcs1              = wx.Panel(self.panel_post, -1)
        
        self.label_kelurahan   = wx.StaticText(self.panel_post, -1, "Kelurahan")
        self.combo_kelurahan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kel   = wx.Button(    self.panel_post, -1, 'New/Edit')
        
        self.label_kecamatan   = wx.StaticText(self.panel_post, -1, "Kecamatan")
        self.combo_kecamatan   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kec   = wx.Button(    self.panel_post, -1, 'New/Edit')
        
        self.label_kabupaten   = wx.StaticText(self.panel_post, -1, "Kabupaten")
        self.combo_kabupaten   = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_kab   = wx.Button(    self.panel_post, -1, 'New/Edit')
        
        self.label_province     = wx.StaticText(self.panel_post, -1, "Province")
        self.combo_province     = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_prov   = wx.Button(    self.panel_post, -1, 'New/Edit')
        
        self.label_country         = wx.StaticText(self.panel_post, -1, "Country")
        self.combo_country         = wx.ComboBox(  self.panel_post, -1, choices=[], style=wx.CB_DROPDOWN, validator = Validator())
        self.button_edit_country   = wx.Button(    self.panel_post, -1, 'New/Edit')
        
        self.estate_ctrls =(self.label_estate,
                            self.label_block,
                            self.text_ctrl_block,
                            self.label_in_cemara,
                            self.button_cemara,
                            self.panel_estates)
        
        self.btns_edit   =(self.button_edit_kel,
                           self.button_edit_kec,
                           self.button_edit_kab,
                           self.button_edit_prov,
                           self.button_edit_country,
                           self.button_edit_estate)
        
        self.combos = (    self.combo_kabupaten,
                           self.combo_kecamatan,
                           self.combo_kelurahan,
                           self.combo_province,
                           self.combo_country)
        
        self.Bind(wx.EVT_BUTTON,   self.EditEstate,        self.button_edit_estate)
        self.Bind(wx.EVT_BUTTON,   self.EditKel,           self.button_edit_kel)
        self.Bind(wx.EVT_BUTTON,   self.EditKec,           self.button_edit_kec)
        self.Bind(wx.EVT_BUTTON,   self.EditKab,           self.button_edit_kab)
        self.Bind(wx.EVT_BUTTON,   self.EditProv,          self.button_edit_prov)
        self.Bind(wx.EVT_BUTTON,   self.EditCountry,       self.button_edit_country)
        
        self.Bind(wx.EVT_BUTTON,   self.InCemaraAsri,      self.button_cemara)
        self.Bind(wx.EVT_BUTTON,   self.OnSave,            self.button_save)
        self.Bind(wx.EVT_BUTTON,   self.OnEdit,            self.button_edit)
                
        self.Bind(wx.EVT_CHECKBOX, self.InEstate,     self.checkbox_within_estate)
        self.Bind(wx.EVT_TEXT,     self.OnPostcode,   self.num_ctrl_postcode)
        
        self.Bind(wx.EVT_COMBOBOX, self.OnEstate,     self.combo_estate)
        self.Bind(wx.EVT_COMBOBOX, self.OnKel,        self.combo_kelurahan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKec,        self.combo_kecamatan)
        self.Bind(wx.EVT_COMBOBOX, self.OnKab,        self.combo_kabupaten)
        self.Bind(wx.EVT_COMBOBOX, self.OnProvince,   self.combo_province)
        self.Bind(wx.EVT_COMBOBOX, self.OnCountry,    self.combo_country)
        

        self.__set_properties()
        self.__do_layout()
        self.displayData()
        
    def __set_properties(self):
        
        self.text_ctrl_full_address.SetMinSize((-1, 150))
        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")

        for b in self.btns_edit:
            b.SetMinSize((55,19))
            b.SetFont(font)
	    b.SetToolTipString('To create new item\nempty combo first')
	    b.SetLabelText('New/Edit')
            
        # self.button_save.SetBackgroundColour('grey')
        # self.button_edit.SetBackgroundColour('grey')
        self.label_house.SetMinSize((80,-1))
        self.label_country.SetMinSize((80,-1))
        self.button_cemara.SetMinSize((85,18))
        self.SetMinSize((420,500))
	
	self.text_ctrl_full_address.SetEditable(False)
	self.selectResidesPanel()
	
    def __do_layout(self):
        sizer_base   = wx.BoxSizer(wx.VERTICAL)
        sizer_top    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_house  = wx.FlexGridSizer(11, 2, 5, 5)
        sizer_auto   = wx.FlexGridSizer(6, 3, 5, 5)
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_estate = wx.BoxSizer(wx.HORIZONTAL)
	
	sizer_house.AddGrowableCol(1)
        sizer_auto.AddGrowableCol(1)
        
        sizer_top.Add(self.button_save, 0, 0, 0)
        sizer_top.Add(self.button_edit, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_top)
        
        sizer_house.Add(self.label_street,     0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_street, 0, wx.EXPAND, 0)
	
	sizer_house.Add(self.label_house,      0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_house,  0, 0, 0)

        gs = wx.BoxSizer(wx.HORIZONTAL)
        gs.Add(self.checkbox_within_estate, 0, 0, 0)
        gs.Add(self.label_in_cemara,        0, wx.LEFT | wx.RIGHT, 5)
        gs.Add(self.button_cemara,          0, 0, 0)
        self.panel_in_estate.SetSizer(gs)
        
        sizer_house.Add(self.label_within_estate, 0, wx.TOP | wx.EXPAND, 14)
        sizer_house.Add(self.panel_in_estate, 0, wx.TOP , 15)
        
        sizer_estate.Add(self.combo_estate,       1, wx.EXPAND, 0)
        sizer_estate.Add(self.button_edit_estate, 0, 0, 0)
        self.panel_estates.SetSizer(sizer_estate)
        
        sizer_house.Add(self.label_estate,      0, wx.EXPAND, 0)
        sizer_house.Add(self.panel_estates,     1, wx.EXPAND, 0)
        
        sizer_house.Add(self.label_block,       0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_block,   0, 0, 0)
        
        sizer_house.Add(self.label_road,        0, wx.EXPAND, 0)
        sizer_house.Add(self.text_ctrl_road,    1, wx.EXPAND, 0)
        
        self.panel_house.SetSizer(sizer_house)
        
        sizer_auto.Add(self.label_kelurahan,    0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kelurahan,    1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kel,    0, 0, 0)
        
        sizer_auto.Add(self.label_kecamatan,    0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kecamatan,    1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kec,    0, 0, 0)
        
        sizer_auto.Add(self.label_kabupaten,    0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_kabupaten,    1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_kab,    0, 0, 0)
	
	sizer_auto.Add(self.label_postcode,     0, wx.EXPAND, 0)
        sizer_auto.Add(self.num_ctrl_postcode,  0, 0, 0)
        sizer_auto.Add(self.pcs1,               0, 0, 0)
        
        sizer_auto.Add(self.label_province,     0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_province,     1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_prov,   0, 0, 0)
                       
        sizer_auto.Add(self.label_country,       0, wx.EXPAND, 0)
        sizer_auto.Add(self.combo_country,       1, wx.EXPAND, 0)
        sizer_auto.Add(self.button_edit_country, 0, 0, 0)
        
        self.panel_post.SetSizer(sizer_auto)
        
        # ----------- main  sizer --------------------------
        sizer_main.Add(self.text_ctrl_full_address, 0 , wx.EXPAND, 0) 
        sizer_main.Add(self.panel_house,  0, wx.EXPAND | wx.TOP, 10)
        sizer_main.Add(self.panel_post,   1, wx.EXPAND | wx.TOP,  5)
        line = wx.StaticLine(self.panel_base, -1)
        sizer_main.Add(line,    0, wx.EXPAND | wx.TOP, 10)
        sizer_main.Add(self.panel_buttons,    0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base,   1, wx.EXPAND | wx.ALL,  15)
        self.SetSizer(sizer_base)
        
        self.Layout()
        self.Fit()
        self.Centre()

    def displayData(self):
        self.next_item_id = 0
        self.guardian_id = gVar.guardian_id
        self.numCtrlActive = False
        self.loadAllCombos()
        self.enableCombos()
        self.num_ctrl_postcode.SetValue(0)
        
        if self.guardian_id:
            self.loadAddress(self.guardian_id)
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
	    self.restore_str(self.combo_estate, estate)
	  
	try :
	    postcode = int(postcode)
	    postcode = postcode*1
	    if isinstance(postcode, int):
		self.num_ctrl_postcode.SetValue(int(postcode))
		kecamatanID = self.cmbID(self.combo_kecamatan)
		self.loadCmbsUnderKecID(kecamatanID)
		self.restore_str(self.combo_kelurahan, kelurahan)
		
	    else:
		self.restore_str(self.combo_country, country)
		self.restore_str(self.combo_country, province)
		self.restore_str(self.combo_country, kabupaten)
		self.restore_str(self.combo_country, kecamatan)
		self.restore_str(self.combo_country, kelurahan)
	except:
	    print 'oh no'
        
    
    def loadCmbsUnderKecID(self, kecamatanID):
        self.restore(self.combo_kecamatan, kecamatanID)
        
        selectedKabupatenID = self.cmbID(self.combo_kabupaten)
        selectedProvinceID  = self.cmbID(self.combo_province)
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
        self.combo_kelurahan.SetName('kelurahan')
        self.combo_kecamatan.SetName('kecamatan')
        self.combo_kabupaten.SetName('kabupaten')
        self.combo_province.SetName( 'province')
        self.combo_country.SetName(  'country')
        self.combo_estate.SetName(   'estate')
        
        loadCmb.addressItems(self.combo_estate, 0)
        #loadCmb.addressItems(self.combo_kelurahan, 'kelurahan', 0)
        loadCmb.addressItems(self.combo_kecamatan, 0)
        loadCmb.addressItems(self.combo_kabupaten, 0)
        loadCmb.addressItems(self.combo_province,  0)
        loadCmb.addressItems(self.combo_country,   0)
        
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
        if not self.restore(self.combo_province, self.restoreID):
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
                    self.restore(self.combo_kecamatan, iid)
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
        self.Layout()
        self.Fit()
        
    def OnEstate(self, evt):
        #rint 'OnEstate'
        if fetch.cmbValue(self.combo_estate)=="Perum. Cemara Asri":
            #rint 'Perum. Cemara Asri'
            self.InCemaraAsri(wx.Event)
          
    def InCemaraAsri(self, event):
        self.checkbox_within_estate.SetValue(1)
        self.num_ctrl_postcode.SetValue(20371)
        self.text_ctrl_road.SetValue('Jl. Cemara')
        loadCmb.restore_str(self.combo_estate, 'Cemara Asri')
        loadCmb.restore_str(self.combo_kelurahan,  'Sampali')
          
    def OnCountry(self, evt):
        print 'OnCountry'
        print
        countryID = self.cmbID(self.combo_country)
        if countryID:
            print ' List provinces For Country'
            provinceList        = fetch.provincesForCountryID(countryID)
            selectedProvinceID  = self.cmbID(self.combo_province)
            provinceID          = self.setComboItems(self.combo_province, provinceList)
            provinceIDlist      = self.idList(provinceList)
            if provinceID:
                if provinceID != selectedProvinceID:
                    kabupatenID = self.kabupatenForProvinces(provinceIDlist)
            else:
                
                # combo_province may have been loaded with a list of provinces
                # or none
                if provinceList:
                    kabupatenID = self.kabupatenForProvinces(provinceIDlist)
        else:
            print 'No country load all provinces '
            provinceList        = fetch.provincesForCountryID()
            selectedProvinceID  = self.cmbID(self.combo_province)
            provinceID          = self.setComboItems(self.combo_province, provinceList)
            print ' List All Provinces'

    def kabupatenForProvinces(self, provinceIDlist):
        print ' List All Kabupaten For All Provinces In Province List'
        kabupatenList   = fetch.kabupatenForProvinceList(provinceIDlist)
        if kabupatenList:# load combo_kabupaten up with kabupaten for provinceID
            return self.setComboItems(self.combo_kabupaten, kabupatenList)
        else:
            return 0
    
    def OnProvince(self, event):
        print 'OnProvince '
        print
        selectedProvinceID = self.cmbID(self.combo_province)
        province           = fetch.cmbValue(self.combo_province)
        
        if selectedProvinceID:
            print 'Selected province ', selectedProvinceID , ':', province
            print 'work down'
            
            print 'Get country for selected province (there should only be one)', selectedProvinceID
            countryList = fetch.countriesForProvinceID(selectedProvinceID)
            print 'countryList ',countryList
            if countryList:
                selectedCountryID = self.cmbID(self.combo_country)
                print ' this should select the country if there is one'
                self.setGen(selectedCountryID, countryList, self.combo_country)
            
            # work up ---------------------
            print ' work up'
            kabupatenList       = fetch.kabupatenForProvinceID(selectedProvinceID)
            selectedKabupatenID = self.cmbID(self.combo_kabupaten)
            print 'kabupatenList, ',kabupatenList , ',    SelectedKabupatenID', selectedKabupatenID
            if selectedKabupatenID in self.idList(kabupatenList):
                return
            self.clearPostcodeCtrls((self.combo_kecamatan,
                                     self.combo_kabupaten,
                                     self.combo_kelurahan))
            #  kabupaten --------------------------
            if kabupatenList:
                print 'Has kabupatenList'
                kabupatenID = self.setComboItems(self.combo_kabupaten, kabupatenList)
                if selectedKabupatenID != kabupatenID:
                    pass
                    # select kecamatan for all kabupaten in list
                    
        else:
            print 'No province selected'
            # if country :
            # select all kab for country
            # else:
            # select all kab
            
            # if not kab-id:
            # select all kec for all kab
            
            

    def OnKab(self, event):
        print 'OnKab  get cmbID(self.combo_kabupaten)'
        print
        selectedKabupatenID = self.cmbID(self.combo_kabupaten)
        #print 'selectedKabupatenID =', selectedKabupatenID
        if not selectedKabupatenID:
            #print 'selectedKabupatenID = None ?????', selectedKabupatenID 
            return
        
        kabupaten           = fetch.cmbValue(self.combo_kabupaten)
        
        provinceList        = fetch.provincesForKabupaten(kabupaten)
        selectedProvinceID  = self.cmbID(self.combo_province)
        provinceID          = self.setGen(selectedProvinceID, provinceList, self.combo_province)
        if selectedProvinceID != provinceID:
            self.countriesForProvince(provinceID, selectedProvinceID)
        
        # step 2: work upward -----------------------
        kecamatenList = fetch.kecamatanForKabupatenID(selectedKabupatenID)
        if kecamatenList:
            selectedKecamatenID = self.cmbID(self.combo_kecamatan)
            kecamatenID = self.setComboItems(self.combo_kecamatan, kecamatenList)
            if kecamatenID != selectedKecamatenID:
                self.resetCmb(self.combo_kelurahan)

    def OnKec(self, event):
        print 'OnKec'
        selectedKecamatanID = self.cmbID(self.combo_kecamatan)
        kecamatan           = fetch.cmbValue(self.combo_kecamatan)
        selectedKabupatenID = self.cmbID(self.combo_kabupaten)
        selectedProvinceID  = self.cmbID(self.combo_province)
        
        if selectedKecamatanID:
            self.postcodeForKecamatan(selectedKecamatanID)
            #  working down ----------------
            kabupatenList = fetch.kabupatenForKecamatanID(selectedKecamatanID)
            if kabupatenList:
                kabupatenID  = self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)
                if selectedKabupatenID != kabupatenID:
                    provinceList       = fetch.provincesForKabupatenID(kabupatenID)
                    selectedProvinceID = self.cmbID(self.combo_province)
                    provinceID         = self.setGen(selectedProvinceID, provinceList, self.combo_province)
                    if selectedProvinceID != provinceID:
                        self.countriesForProvince(provinceID, provinceID)
            # step 2 - work up
            self.resetCmb(self.combo_kelurahan)
            alist = fetch.kelurahanForKecamatanID(selectedKecamatanID)
            self.setComboItems(self.combo_kelurahan, alist)
    
    def OnKel(self, event):
        print 'OnKel'
        selectedKecamatanID = self.cmbID(self.combo_kecamatan)
        selectedKabupatenID = self.cmbID(self.combo_kabupaten)
        selectedProvinceID  = self.cmbID(self.combo_province)
        
        if selectedKecamatanID:    return

        # kecamatan -----------------------------
        kecamatanList = fetch.kecamatanForKelurahanID(kelurahanID)
        kecamatanID   = self.setKecamatan(selectedKecamatanID, kecamatanList) 
        kabupatenID   = self.doForKabupaten(kecamatanID, selectedKecamatanID)
        provinceID    = self.provincesForKabupaten(kabupatenID, selectedKabupatenID)
        
        self.countriesForProvince(provinceID, selectedProvinceID)

    def clearPostcodeCtrls(self, ctrls):
        print 'clearPostcodeCtrls'
        for cmb in ctrls:
            cmb.Freeze()
            cmb.Clear()
            
            cmb.SetSelection(0)
            cmb.Thaw()
        self.num_ctrl_postcode.Freeze()
        self.num_ctrl_postcode.Clear()
        self.num_ctrl_postcode.Thaw()
        
    def setComboItems(self, cmb, itemsList):
        print 'setComboItems'
        selectedID = self.cmbID(cmb)
        cmb.Freeze()
        cmb.Clear()
        for row in itemsList:
            cmb.Append(str(row[1]), int(row[0]))
        cmb.Insert(' ', 0)
        cmb.Thaw()
        
        selectedID = self.restore(cmb, selectedID)
        if not selectedID:
            if len(itemsList) == 1:
                selectedID = itemsList[0][0]
                self.restore(cmb, selectedID)
        return selectedID
    
    def restore(self, cmb, origional_id=0):
        print 'restore id:', cmb.GetName()
        cmb.Freeze()
        try:
            if origional_id:
                #print ' try to find origional_id', origional_id
                #print 'cmb.GetCount()',cmb.GetCount()
                for y in range(cmb.GetCount()):
                    
                    cmb.Select(y) # select first item
                    itemId = self.cmbID(cmb)
                    #print 'y=', y, 'itemId=', itemId
                    if itemId == origional_id:
                        #print 'itemId == origional_id'
                        
                        cmb.Thaw()
                        return True
        except:
            pass
        
        cmb.Select(0)
        cmb.Thaw()
        return False
        
    
    def postcodeForKecamatan(self, kecamatanID):
        print 'postcodeForKecamatan'
        self.numCtrlActive = True
        try:     self.num_ctrl_postcode.SetValue(fetch.postcodeForKecID(kecamatanID))
        except:  self.num_ctrl_postcode.Clear()
        self.numCtrlActive = False
    
    def idList(self, data):
        myl = []
        if data: 
            for r in data:
                myl.append(r[0])
        return myl

    def countriesForProvince(self, setID, selectedID):
        print 'countriesForProvince'
        cmb = self.combo_country
        cmbID = self.cmbID(cmb)
        if selectedID: aList = fetch.countriesForProvinceID(selectedID)
        else:          aList = fetch.countriesForProvinceID(setID)
        return self.setGen(cmbID, aList, cmb)
        
    def provincesForKabupaten(self, setID, selectedID):
        print 'provincesForKabupaten'
        cmb = self.combo_province
        cmbID = self.cmbID(cmb)
        if selectedID: aList = fetch.provinceForKabupatenID(selectedKabupatenID)
        else:          aList = fetch.provinceForKabupatenID(setID)
        return self.setGen(cmbID, aList, cmb)
    
    def kabupatenForKecamatan(self,  setID, selectedID):
        print 'kabupatenForKecamatan'
        cmb = self.combo_kabupaten
        cmbID = self.cmbID(cmb)
        if selectedID: aList = fetch.kabForKacID(selectedID)
        else:          aList = fetch.kabForKacID(setID)
        return self.setGen(cmbID, aList, cmb)
    
    def kecForKel(self, kelID, selectedKelID):
        print 'kecForKel'
        cmb = self.combo_kecamatan
        cmbID = self.cmbID(cmb)
        if selectedID: aList = fetch.kecForKelID(selectedKelID)
        else:          aList = fetch.kecForKelID(kelID)
        return self.setGen(cmbID, aList, cmb)
    
    def bForA(self, AID, selectedID, cmb, call):
        print 'bForA'
        cmbID = self.cmbID(cmb)
        if selectedAID: aList = call(selecteID)
        else:           aList = call(AID)
        return self.setGen(cmbID, aList, cmb)
    
    def doForKabupaten(self, kecamatanID, selectedKecamatanID):
        print 'doForKabupaten'
        selectedKabupatenID = self.cmbID(self.combo_kabupaten)
        if kecamatanID: kabupatenList = fetch.provinceForKabupaten(selectedKecamatanID)
        else:           kabupatenList = fetch.proviceForKecamatan(selectedKecamatanID)
        return self.setGen(selectedKabupatenID, kabupatenList, self.combo_kabupaten)
            
    def upFillKel(self, kelurahanList):
        print 'upFillKel'
        self.setComboItems(self.combo_kelurahan, kelurahanList)
        """if kelurahanList:
            self.setComboItems(self.combo_kelurahan, kelurahanList)
            selectedKelurahanID = self.setComboItems(self.combo_kelurahan, kelurahanList)
            if selectedKelurahanID in self.idList(kelurahanList): return
            elif len(kelurahanList) == 1:
                kelurahanID = kelurahanList[0][0]
                self.restore(self.combo_box_kel, kelurahanID)"""

    def setKecamatan(self, selectedKecamatanID, kecamatanList):
        print 'setKecamatan'
        self.setGen(selectedKecamatanID, kecamatanList, self.combo_kecamatan)
        self.postcodeClear()
        return 0

    def setGen(self, selectedItemID, aList, cmb):
        print 'set gen'
        if aList:
            print ' we have a list'
            r = aList[0]
            if len(r) != 2:
                fetch.msg('list error')
            
            if len(aList)  > 1:
                selectedItemID = self.setComboItems(cmb, aList)
                
            elif len(aList)==1:
                #print 'aList on one: ', aList
                selectedItemID =  int(aList[0][0])
                #print 'selectedItem>ID>', selectedItemID, cmb, cmb.GetName()
                if selectedItemID:
                    self.restore(cmb, selectedItemID)
                    
            else:
                self.clearPostcodeCtrls((cmb,))
        #print 'setCmn return id', selectedItemID
        return selectedItemID
   
    def postcodeClear(self):
        self.numCtrlActive = True
        self.num_ctrl_postcode.Clear()
        self.numCtrlActive = False

    def splitAddress(self, address):
	return address.split(',')
    
    def getValues(self):
        return (
		str(self.text_ctrl_street.GetValue()),
		str(self.text_ctrl_house.GetValue()),
		str(fetch.cmbValue(self.combo_estate)),
		str(self.text_ctrl_block.GetValue()),
		str(self.text_ctrl_road.GetValue()),
                str(fetch.cmbValue(self.combo_kelurahan)),
                str(fetch.cmbValue(self.combo_kecamatan)),
                str(fetch.cmbValue(self.combo_kabupaten)),
		str(self.num_ctrl_postcode.GetValue()),
                str(fetch.cmbValue(self.combo_province)),
		str(fetch.cmbValue(self.combo_country)))
        
    def OnSave(self, evt):
        # aim to make this generic
        
	table  = 'guardians' 
	column = 'address'
	
	street    = str(self.text_ctrl_street.GetValue())
	house     = str(self.text_ctrl_house.GetValue())
	estate    = str(fetch.cmbValue(self.combo_estate))
	block     = str(self.text_ctrl_block.GetValue())
	road      = str(self.text_ctrl_road.GetValue())
	kelurahan = str(fetch.cmbValue(self.combo_kelurahan))
	kecamatan = self.combo_kecamatan.GetStringSelection()
	kabupaten = str(fetch.cmbValue(self.combo_kabupaten))
	postcode  = str(self.num_ctrl_postcode.GetValue())
	province  = str(fetch.cmbValue(self.combo_province))
	country   = str(fetch.cmbValue(self.combo_country))
			    
	if not street or not house or not province:
	    fetch.msg('At least houseNo, street & province are needed')
	    return
	
	address =','.join((street,house,estate,block,road,kelurahan,kecamatan,kabupaten,postcode,province,country))
        sql = "UPDATE %s \
                  SET address = '%s' \
                WHERE id =%d" %(table, address, self.guardian_id)
        print sql
        fetch.updateDB(sql)

    def OnEdit(self, evt):
        self.Close()
        
    def cmbID(self, cmb):
        print 'cmbID ', cmb.GetName()
        index = cmb.GetSelection()
        print 'index', index
        if index > 0:
            print ' has index', index
            #print 'CurrentSelection=', index
            selected_id = cmb.GetClientData(index)
            #print 'selected_id', selected_id
        else:
            selected_id = 0
        return selected_id
        
        
    def edit(self, cmb1, cmb2, itemType):
        print 'edit   type:',itemType
        
        nextItem = ''
        
        self.restore_id = self.cmbID(cmb1)
        restoreString = fetch.cmbValue(cmb1)
        if not self.restore_id:
            # prepare data for new entry
            if itemType=='country':
                self.next_item_id = 0
            else:
                if cmb2:
                    next_item_id = self.cmbID(cmb2)
                    print cmb2.GetName(), 'next_item_id', next_item_id
                    nextItem   = fetch.cmbValue(cmb2)
                    if not next_item_id:
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
                    if self.next_item_id: 
                        sql = "INSERT INTO address_items \
                                      (name, type, next_item_id) \
                               VALUES ('%s', '%s', '%s')" % (
                                       itemName, itemType, self.next_item_id)
                    else:
                        sql = "INSERT INTO address_items \
                                      (name, type) \
                               VALUES ('%s', '%s')" % (
                                       itemName, itemType)
                    print sql
                    fetch.updateDB(sql)
                      
        finally:    
            dlg.Destroy()
            
    def EditEstate(self, event):
        self.edit(self.combo_estate, None, 'estate')     
        
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

if __name__ == '__main__':
    app = wx.App(None)
    dlg = create(None)
    try:
        gVar.address = 'new address'
        dlg.displayData()
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
    
    