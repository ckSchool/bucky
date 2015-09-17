import wx, gVar, fetch, loadCmb

class panel_edit_school(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        #self.button_back  = wx.Button(self, -1, "< Back")
        
        
        self.panel_top             = wx.Panel(self,  -1)
        self.panel_bottom          = wx.Panel(self,  -1)
        self.button_save           = wx.Button(self, -1, "Save")
        
        #self.bitmap_course        = wx.StaticBitmap(self.panel_top, -1, wx.Bitmap(".\\images\\48\\subject_48.png", wx.BITMAP_TYPE_ANY))
        self.panel_main            = wx.Panel(self.panel_top,        -1)
        
        self.label_school_name     = wx.StaticText(self.panel_main, -1, "School Name")
        self.text_ctrl_school_name = wx.TextCtrl(self.panel_main,   -1, "")
        
        self.label_type            = wx.StaticText(self.panel_main, -1, "Catagory")
        self.choice_type           = wx.Choice(self.panel_main,    -1, choices=['Other','TK', 'SD','SMP','SMA'])

        self.label_address         = wx.StaticText(self.panel_main, -1, "Top Level")
        self.text_ctrls_address    = wx.SpinCtrl(self.panel_main,    -1, initial=18, min=1,  max=18)
        
        self.label_is_ck           = wx.StaticText(self.panel_main, -1, "Chandra Kusuma")
        self.checkbox_is_ck        = wx.CheckBox(self.panel_main, -1, '')

        self.sizer_main_staticbox  = wx.StaticBox(self.panel_top,    -1, "")
        
        self.button_save.Bind(wx.EVT_BUTTON,      self.OnSave)
        #self.Bind(wx.EVT_BUTTON, self.OnBack,     self.button_back)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.label_school_name.SetMinSize((100, 13))
        

    def __do_layout(self):
        sizer_base      = wx.BoxSizer(wx.VERTICAL)
               
        grid_sizer_main = wx.FlexGridSizer(4, 2, 10, 3)
        
        self.sizer_main_staticbox.Lower()
        sizer_main     = wx.StaticBoxSizer(self.sizer_main_staticbox, wx.HORIZONTAL)

        grid_sizer_main.Add(self.label_school_name,     0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_school_name, 0, wx.EXPAND, 0)
        
        grid_sizer_main.Add(self.label_type,            0, 0, 0)
        grid_sizer_main.Add(self.choice_type,           0, wx.EXPAND, 0)
        
        grid_sizer_main.Add(self.label_address,         0, 0, 0)
        grid_sizer_main.Add(self.text_ctrls_address,    0, wx.EXPAND, 0)
        
        grid_sizer_main.Add(self.label_is_ck,           0, 0, 0)
        grid_sizer_main.Add(self.checkbox_is_ck,        0, wx.EXPAND, 0)
        
        self.panel_main.SetSizer(grid_sizer_main)
        
        #sizer_main.Add(self.bitmap_course, 0, wx.RIGHT, 15)
        sizer_main.Add(self.panel_main, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)
        self.panel_top.SetSizer(sizer_main)

        #sizer_base.Add(self.button_back, 0, wx.ALL | wx.EXPAND, 10)
        sizer_base.Add(self.panel_top,   0, wx.ALL | wx.EXPAND, 10)
        sizer_base.Add(self.button_save, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 20)
        self.SetSizer(sizer_base)
        
        sizer_base.Fit(self)
        self.Layout()
        self.Center()

    def __do_main(self):
        pass
        
    def displayData(self):
        print 'panel_edit_school : displayData'

        if gVar.school_id:
            self.editMode = True
            self.displaySchoolDetails()
            
        else:
            self.editMode = False
    
    def displaySchoolDetails(self):
        sql = "SELECT * FROM schools \
                WHERE is = %d" % gVar.school_id
        
        res = fetch.getAllDict(sql)
        #rint 'displaySchoolDetails' , res
        if not res:return
        
        address     = res['address']
        school_name = res['name']
        school_type = res['type']
        isCK        = res['isCK']
        
        self.text_ctrl_school_name.SetValue(school_name)
        self.choice_type.SetSelection(min_level)
        #self.text_ctrls_address.SetValue(max_level)
        
        self.checkbox_is_ck.SetValue(isCK)

    def OnBack(self, evt):
        #self.panel_contact.enableCtrls(False)
        self.GetTopLevelParent().goBack()    
        
    def OnCancel(self, event):
        self.id = 0
        self.EndModal(-1)
        
    def schoolNameAvailable(self, school_name):
        sql = 'SELECT id FROM schools \
                WHERE name = %s ' % (school_name)
        
        if self.editMode:
            sql += " AND NOT id = %d" % gVar.school_id
        
        #rint sql
        if fetch.getDig(sql):
            fetch.msg("Duplicate name, please try another")
            return False
            
        else:       
            return True
        
    def OnSave(self, event):
        self.school_name  = '"%s"' % self.text_ctrl_school_name.GetValue()

        
        if not self.school_name:
            txt = "Data not sufficient: must have school name"
            return
        
 
    def insertNewSchool(self):
        sql = "INSERT INTO schools \
                  SET name = '%s', type =%d, address ='%s', isCK=%d " % (
                      self.school_name, self.type, self.address, self.isCK)
        #rint sql
        #fetch.updateDBtransaction(sql)

    def updateSchool(self):
        if not self.school_name == self.origional_name:
            sql = " UPDATE schools \
                       SET name = '%s',  type =%d, address ='%s', isCK=%d \
                     WHERE id = %d"  % (self.school_name, self.type, self.address, self.isCK, gVar.school_id)
            #rint sql
            #fetch.updateDB(sql)

