import wx


class MyPanel1(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.panel_11 = wx.Panel(self, -1)
        self.button_back = wx.Button(self.panel_11, -1, "< Back")
        self.panel_12 = wx.Panel(self.panel_11, -1)
        self.button_save = wx.Button(self.panel_11, -1, "Save")
        self.button_edit = wx.Button(self.panel_11, -1, "Edit")
        self.panel_house = wx.Panel(self, -1)
        self.label_house = wx.StaticText(self.panel_house, -1, "House ")
        self.text_ctrl_house = wx.TextCtrl(self.panel_house, -1, "")
        self.label_street = wx.StaticText(self.panel_house, -1, "Street")
        self.text_ctrl_street = wx.TextCtrl(self.panel_house, -1, "")
        self.label_within_estate = wx.StaticText(self.panel_house, -1, "Within Estate")
        self.checkbox_within_estate = wx.CheckBox(self.panel_house, -1, "")
        self.panel_estate = wx.Panel(self, -1)
        self.label_estate = wx.StaticText(self.panel_estate, -1, "Estate")
        self.combo_box_estate = wx.ComboBox(self.panel_estate, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_block = wx.StaticText(self.panel_estate, -1, "Block")
        self.text_ctrl_block = wx.TextCtrl(self.panel_estate, -1, "")
        self.panel_road = wx.Panel(self, -1)
        self.label_road = wx.StaticText(self.panel_road, -1, "Road")
        self.text_ctrl_road = wx.TextCtrl(self.panel_road, -1, "")
        self.panel_15 = wx.Panel(self, -1)
        self.label_country = wx.StaticText(self.panel_15, -1, "Country")
        self.combo_box_country = wx.ComboBox(self.panel_15, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_province = wx.StaticText(self.panel_15, -1, "Province")
        self.combo_box_province = wx.ComboBox(self.panel_15, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_postcode = wx.StaticText(self.panel_15, -1, "Postcode")
        self.text_ctrl_postcode = wx.TextCtrl(self.panel_15, -1, "")
        self.label_kabupaten = wx.StaticText(self.panel_15, -1, "Kabupaten")
        self.combo_box_kab = wx.ComboBox(self.panel_15, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_kecamatan = wx.StaticText(self.panel_15, -1, "Kecamatan")
        self.combo_box_kec = wx.ComboBox(self.panel_15, -1, choices=[], style=wx.CB_DROPDOWN)
        self.lable_kelurahan = wx.StaticText(self.panel_15, -1, "Kelurahan")
        self.combo_box_kel = wx.ComboBox(self.panel_15, -1, choices=[], style=wx.CB_DROPDOWN)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.label_street.SetMinSize((70, 13))
        self.label_within_estate.SetMinSize((70, 24))
        self.label_estate.SetMinSize((070, 21))
        self.label_road.SetMinSize((070, 21))
        self.label_country.SetMinSize((70, 21))

    def __do_layout(self):
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_5 = wx.FlexGridSizer(6, 2, 1, 1)
        grid_sizer_road = wx.FlexGridSizer(1, 2, 1, 1)
        grid_sizer_estate = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_house = wx.FlexGridSizer(3, 2, 1, 1)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add(self.button_back, 0, 0, 0)
        sizer_8.Add(self.panel_12, 1, wx.EXPAND, 0)
        sizer_8.Add(self.button_save, 0, 0, 0)
        sizer_8.Add(self.button_edit, 0, 0, 0)
        self.panel_11.SetSizer(sizer_8)
        sizer_7.Add(self.panel_11, 0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.label_house, 0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_house, 0, 0, 0)
        grid_sizer_house.Add(self.label_street, 0, wx.EXPAND, 0)
        grid_sizer_house.Add(self.text_ctrl_street, 0, 0, 0)
        grid_sizer_house.Add(self.label_within_estate, 0, wx.TOP | wx.EXPAND, 14)
        grid_sizer_house.Add(self.checkbox_within_estate, 0, wx.TOP | wx.BOTTOM, 15)
        self.panel_house.SetSizer(grid_sizer_house)
        grid_sizer_house.AddGrowableCol(1)
        sizer_7.Add(self.panel_house, 0, wx.TOP | wx.EXPAND, 10)
        grid_sizer_estate.Add(self.label_estate, 0, wx.EXPAND, 0)
        grid_sizer_estate.Add(self.combo_box_estate, 0, 0, 0)
        grid_sizer_estate.Add(self.label_block, 0, wx.EXPAND, 0)
        grid_sizer_estate.Add(self.text_ctrl_block, 0, 0, 0)
        self.panel_estate.SetSizer(grid_sizer_estate)
        sizer_7.Add(self.panel_estate, 0, wx.BOTTOM | wx.EXPAND, 10)
        grid_sizer_road.Add(self.label_road, 0, wx.EXPAND, 0)
        grid_sizer_road.Add(self.text_ctrl_road, 0, 0, 0)
        self.panel_road.SetSizer(grid_sizer_road)
        grid_sizer_road.AddGrowableCol(1)
        sizer_7.Add(self.panel_road, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        grid_sizer_5.Add(self.label_country, 1, wx.EXPAND, 0)
        grid_sizer_5.Add(self.combo_box_country, 0, 0, 0)
        grid_sizer_5.Add(self.label_province, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.combo_box_province, 0, 0, 0)
        grid_sizer_5.Add(self.label_postcode, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.text_ctrl_postcode, 0, 0, 0)
        grid_sizer_5.Add(self.label_kabupaten, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.combo_box_kab, 0, 0, 0)
        grid_sizer_5.Add(self.label_kecamatan, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.combo_box_kec, 0, 0, 0)
        grid_sizer_5.Add(self.lable_kelurahan, 0, wx.EXPAND, 0)
        grid_sizer_5.Add(self.combo_box_kel, 0, 0, 0)
        self.panel_15.SetSizer(grid_sizer_5)
        grid_sizer_5.AddGrowableCol(1)
        sizer_7.Add(self.panel_15, 0, wx.TOP | wx.EXPAND, 10)
        self.SetSizer(sizer_7)
        sizer_7.Fit(self)