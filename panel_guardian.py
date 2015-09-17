import wx,  gVar
import fetchodbc as fetch

import loadCmbODBC as loadCmb

from DateCtrl import DateCtrl
# from TextCtrlAutoComplete import TextCtrlAutoComplete

class guardian_data(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.labelHead     = wx.StaticText(self, -1, "?")
        self.panel_main    = wx.Panel(self, -1)
        
        self.panel_top_left = wx.Panel(self.panel_main, -1)
        self.staticbox_name = wx.StaticBox(self.panel_top_left,         -1, "Name")
        
        self.panel_top_right      = wx.Panel(self.panel_main, -1)
        self.staticbox_occupation = wx.StaticBox(self.panel_top_right,  -1, "Occupation")
        
        self.panel_bottom_left = wx.Panel(self.panel_main, -1)
        self.staticbox_address = wx.StaticBox(self.panel_bottom_left,   -1, "Address")
        
        self.panel_bottom_right = wx.Panel(self.panel_main, -1)
        self.staticbox_telp     = wx.StaticBox(self.panel_bottom_right, -1, "Telephone")
        
        self.panel_name          = wx.Panel(self.panel_top_left, -1)
        
        self.label_name          = wx.StaticText(self.panel_name, -1, "First name")
        self.text_ctrl_name      = wx.TextCtrl(self.panel_name,   -1, "")
        self.label_email         = wx.StaticText(self.panel_name, -1, "Email")
        self.text_ctrl_email     = wx.TextCtrl(self.panel_name,   -1, "")
        self.label_blood_group   = wx.StaticText(self.panel_name, -1, "Blood group")
        self.choice_blood_group  = wx.Choice(self.panel_name,     -1, choices=[])
        self.label_dob           = wx.StaticText(self.panel_name, -1, "Date of birth")
        self.panel_blood_dob     = wx.Panel(self.panel_name,      -1)
        self.date_ctrl_dob       = DateCtrl(self.panel_blood_dob, -1)
        self.label_relationship  = wx.StaticText(self.panel_name, -1, "Relationship")
        self.choice_relationship = wx.Choice(self.panel_name,     -1, choices=[])
        self.label_faith         = wx.StaticText(self.panel_name, -1, "Faith")
        self.choice_faith        = wx.Choice(self.panel_name,     -1, choices=["Buddhist", "Muslim", "Christian", "Hindu", "Other"])
        
        self.panel_occupation    = wx.Panel(self.panel_top_right, -1)
        
        self.label_occupation_main  = wx.StaticText(self.panel_occupation, -1, "Main")
        self.choice_occupation_main = wx.Choice(self.panel_occupation,     -1, choices=[])
        
        self.label_occupation_2nd   = wx.StaticText(self.panel_occupation, -1, "2nd")
        self.choice_occupation_2nd  = wx.Choice(self.panel_occupation,     -1, choices=[])
        
        self.label_income           = wx.StaticText(self.panel_occupation, -1, "Income")
        self.spin_income            = wx.SpinCtrl(self.panel_occupation,   -1, "", min=0, max=100)
        self.label_qualification    = wx.StaticText(self.panel_occupation, -1, "Qualification")
        self.choice_qualification   = wx.Choice(self.panel_occupation,     -1, choices=[])
        self.label_english          = wx.StaticText(self.panel_occupation, -1, "Engllish")
        self.choice_english_level   = wx.Choice(self.panel_occupation,     -1, choices=["Weak", "Average", "Good", "Native"])
        
        self.text_ctrl_address   = wx.TextCtrl(self.panel_bottom_left, -1, value="", style= wx.TE_MULTILINE )
        self.button_edit_address = wx.Button(self.panel_bottom_left,   -1, "...")
        
        self.text_ctrl_phone1    = wx.TextCtrl(self.panel_bottom_right, -1, "")
        self.text_ctrl_phone2    = wx.TextCtrl(self.panel_bottom_right, -1, "")
        self.button_edit_telp    = wx.Button(self.panel_bottom_right,   -1, "...")
        
        self.Bind(wx.EVT_BUTTON, self.OnEditAddress, self.button_edit_address)
        self.Bind(wx.EVT_BUTTON, self.OnEditTelp, self.button_edit_telp)
        
        self.text_ctrls = [ self.text_ctrl_name,   self.text_ctrl_email,
                            self.date_ctrl_dob,    self.text_ctrl_address,
                            self.text_ctrl_phone1, self.text_ctrl_phone2]
        
        self.choice_ctrls = (self.choice_occupation_main, self.choice_occupation_2nd,
                             self.choice_blood_group,     self.choice_faith,
                             self.choice_qualification,   self.choice_english_level,
                             self.choice_relationship)
                             
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def derivedRelatives(self, relative):
        return [relative, 'step' + relative, relative + '-in-law']
    
    def head(self, txt=''):
        self.labelHead.SetLabel(txt)
        
    def __set_properties(self):
        self.date_ctrl_dob.checkbox_1.Hide()
        myfont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.labelHead.SetFont(myfont)
        
        self.SetSize((384, 424))
        self.text_ctrl_name.SetMinSize((200, 21))
        self.text_ctrl_email.SetMinSize((200, 21))
        self.choice_blood_group.SetMinSize((120, 21))
        self.choice_qualification.SetMinSize((100, 21))
        self.choice_english_level.SetMinSize((40, 21))
        self.choice_english_level.SetSelection(-1)
        self.panel_top_right.SetMinSize((140, -1))
        self.text_ctrl_address.SetMinSize((262, 90))
        self.text_ctrl_address.Enable(False)
        self.button_edit_address.SetMinSize((41, 16))
        self.button_edit_telp.SetMinSize((41, 16))
        self.button_edit_telp.Hide()
        
    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        
        grid_sizer_guardian = wx.FlexGridSizer(4, 2, 0, 0)
        
        self.staticbox_telp.Lower()
        self.staticbox_address.Lower()
        self.staticbox_occupation.Lower()
        self.staticbox_name.Lower()
        
        grid_sizer_name  = wx.FlexGridSizer(6, 2, 2, 1)
        sizer_occupation = wx.FlexGridSizer(5, 2, 2, 1)
        
        sizer_blood_dob  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_name_static  = wx.StaticBoxSizer(self.staticbox_name, wx.VERTICAL)
        sizer_name_static.Add(self.panel_name, 1, wx.EXPAND, 0)
        self.panel_top_left.SetSizer(sizer_name_static)
                                     
        sizer_occupation_static = wx.StaticBoxSizer(self.staticbox_occupation, wx.VERTICAL)
        sizer_occupation_static.Add(self.panel_occupation, 1, wx.EXPAND, 0)
        self.panel_top_right.SetSizer(sizer_occupation_static)
        
        sizer_telp_static       = wx.StaticBoxSizer(self.staticbox_telp, wx.VERTICAL)
        sizer_address_static    = wx.StaticBoxSizer(self.staticbox_address, wx.VERTICAL)
        
        sizer_blood_dob.Add(self.date_ctrl_dob, 0, 0, 0)
        self.panel_blood_dob.SetSizer(sizer_blood_dob)
        
        grid_sizer_name.Add(self.label_name, 0, 0, 0)
        grid_sizer_name.Add(self.text_ctrl_name, 0, wx.EXPAND, 0)
        grid_sizer_name.Add(self.label_dob, 0, 0, 0)
        grid_sizer_name.Add(self.panel_blood_dob, 1, wx.EXPAND, 0)
        grid_sizer_name.Add(self.label_faith, 0, wx.TOP | wx.BOTTOM, 0)
        grid_sizer_name.Add(self.choice_faith, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 0)
        grid_sizer_name.Add(self.label_blood_group, 0, 0, 0)
        grid_sizer_name.Add(self.choice_blood_group, 0, 0, 2)
        grid_sizer_name.Add(self.label_relationship, 0, wx.TOP | wx.BOTTOM, 2)
        grid_sizer_name.Add(self.choice_relationship, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 2)
        grid_sizer_name.Add(self.label_email, 0, 0, 0)
        grid_sizer_name.Add(self.text_ctrl_email, 0, 0, 0)
        self.panel_name.SetSizer(grid_sizer_name)
        
        sizer_occupation.Add(self.label_occupation_main,  0, 0, 0)
        sizer_occupation.Add(self.choice_occupation_main, 0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_occupation_2nd,   0, 0, 0)
        sizer_occupation.Add(self.choice_occupation_2nd,  0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_income,           0, 0, 0)
        sizer_occupation.Add(self.spin_income,            0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_qualification,    0, 0, 0)
        sizer_occupation.Add(self.choice_qualification,   0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_english,          0, wx.EXPAND, 0)
        sizer_occupation.Add(self.choice_english_level,   0, wx.EXPAND, 0)
        self.panel_occupation.SetSizer(sizer_occupation)
        
        sizer_address_static.Add(self.text_ctrl_address,        0, wx.EXPAND, 0)
        sizer_address_static.Add(self.button_edit_address,      0, wx.ALIGN_RIGHT, 0)
        
        sizer_telp_static.Add(self.text_ctrl_phone1,            0, wx.EXPAND, 0)
        sizer_telp_static.Add(self.text_ctrl_phone2,            0, wx.EXPAND, 0)
        sizer_telp_static.Add(self.button_edit_telp,            0, wx.ALIGN_RIGHT, 0)
        
        self.panel_bottom_left.SetSizer(sizer_address_static)
        self.panel_bottom_right.SetSizer(sizer_telp_static)
        
        grid_sizer_guardian.Add(self.panel_top_left,     1, wx.EXPAND, 0)
        grid_sizer_guardian.Add(self.panel_top_right,    1, wx.EXPAND, 0)
        grid_sizer_guardian.Add(self.panel_bottom_left,  1, wx.EXPAND, 0)
        grid_sizer_guardian.Add(self.panel_bottom_right, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(grid_sizer_guardian)
        
        sizer_main.Add(self.labelHead,  0, wx.TOP | wx.EXPAND, 10)
        sizer_main.Add(self.panel_main, 1, wx.EXPAND , 0)
        self.SetSizer(sizer_main)
       
    def __do_main(self):
        self.editMode=False
     
    def displayData(self, student_id, guardian_id=0, guardian_type=''):
        print 'Guardian displayData'
        self.current_address=''
        self.guardian_type = guardian_type
        self.guardian_id   = guardian_id
        self.student_id    = student_id
        
        self.clearCtrls()
        #self.editMode = False
        if not guardian_id: return
        
        self.editMode = True
            
        if guardian_type == 'father':
            self.father(guardian_id)
            self.SetBackgroundColour((145,137,210))
        elif guardian_type == 'mother':
            self.mother(guardian_id)
            self.SetBackgroundColour((210,145,137))
        elif guardian_type == 'guardian':
            self.guardian(guardian_id)
            self.SetBackgroundColour((137,210,145))
            
    def father(self, gid):
        sql = "SELECT * FROM OrangTua WHERE Kode = %d" % gid
        res = fetch.getOneDict(sql)
        if not res: return
        #print res
        makeStr = self.makeStr
        Nama = res['NamaA']
        TgLahir = makeStr(res['TgLahirA'])
        Pekerjaan = res['PekerjaanA']
        PekerjaanLain = res['PekerjaanLainA']
        Alamat = res['AlamatA']
        HP = res['HPA']
        Telepon = res['TeleponA']
        Agama = res['AgamaA']
        
        self.setData(Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama)
        self.label_relationship.Hide()
        self.choice_relationship.Hide()
    
    def mother(self, gid):
        sql = "SELECT * FROM OrangTua WHERE Kode = %d" % gid
        res = fetch.getOneDict(sql)
        if not res: return
        makeStr = self.makeStr
        Nama = res['NamaI']
        TgLahir = makeStr(res['TgLahirI'])
        Pekerjaan = res['PekerjaanI']
        PekerjaanLain = res['PekerjaanLainI']
        
        if res['SamaDenganAyah']:
            Alamat = res['AlamatA']
        else:
            Alamat = res['AlamatI']
            
        HP = res['HPI']
        Telepon = res['TeleponI']
        Agama = res['AgamaI']
        
        self.setData(Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama)
        
        self.label_relationship.Hide()
        self.choice_relationship.Hide()
    
    def guardian(self, gid):
        sql = "SELECT * FROM Wali WHERE Kode = %d" % gid
        res = fetch.getOneDict(sql)
        if not res: return
        
        makeStr = self.makeStr
        
        Nama = res['Nama']
        TgLahir = makeStr(res['TgLahir'])
        Pekerjaan = res['Pekerjaan']
        PekerjaanLain = res['PekerjaanLain']
        Alamat = res['Alamat']
        HP = res['HP']
        Telepon = res['Telepon']
        Agama = res['Agama']
        
        self.setData(Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama)
    
    def setData(self,Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama):
        print Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama
        
        self.current_address=Alamat=Alamat.replace(",", "\n")
        
        self.text_ctrl_name.SetValue(str(Nama))
        print 'TgLahir:',TgLahir

        self.date_ctrl_dob.SetValue(TgLahir)
        #self.choice_occupation_main.SetValue(str(Pekerjaan))
        #self.choice_occupation_2nd.SetValue(str(PekerjaanLain))
        self.text_ctrl_address.SetValue(str(Alamat))
        self.text_ctrl_phone1.SetValue(str(HP))
        self.text_ctrl_phone2.SetValue(str(Telepon))
        self.setCmb(self.choice_faith, Agama)
        
        #try:
        #    index = self.choice_english_level.FindString(res['english_ability'])
        #    self.choice_english_level.SetSelection(index)
        #except:  pass
        
        #try:
        #    index = self.choice_qualification.FindString(res['education'])
        #    self.choice_qualification.SetSelection(index)
        #except:  pass
        
        #try:
        #    index = self.choice_relationship.FindString(res['relation'])
        #    self.choice_relationship.SetSelection(index)

        #try:
        #    index = self.choice_blood_group.FindString(res['blood_group'])
        #    self.choice_blood_group.SetSelection(index)
        #except:  pass
        
        
        
        #self.spin_income.SetValue(makeStr(res['income']))
        #self.date_ctrl_dob.SetValue(makeStr(res['birth_date']))
        #self.text_ctrl_email.SetValue(makeStr(res['email']))

    def saveData(self):
        birth_date    = self.date_ctrl_dob.GetDbReadyValue()
        print 'birth_date:',birth_date
        name    = self.text_ctrl_name.GetValue()
        
        occupation    = self.choice_occupation_main.GetValue()
        occupation2   = self.choice_occupation_2nd.GetValue()
        
        english_ability = self.choice_english_level.GetValue()
        qualification = self.choice_qualification.GetValue()
        
        relationship  = self.choice_relationship.GetValue()
        blood_group   = self.choice_blood_group.GetValue()
        
        address       = self.text_ctrl_address.GetValue()
        phone1        = self.text_ctrl_phone1.GetValue()
        phone2        = self.text_ctrl_phone2.GetValue()
        income        = self.spin_income.GetValue()
        
        email         = self.text_ctrl_email.GetValue()
        faith         = self.choice_faith.GetCurrentSelection()
        addr=[]
        if address:
            addr = address.split('\n')
            
        try:    address_line1 = addr[0]
        except: address_line1 = ''
        
        try:    address_line2 = addr[1]
        except: address_line2 = ''
        
        try:    city = addr[2]
        except: city = ''
        
        try:    state = addr[3]
        except: state = ''
        
        country_id = 7
        
        setQl = "   SET (Nama,TgLahir,Pekerjaan,PekerjaanLain,Alamat,HP,Telepon,Agama) \
                VALUES  ('%s', '%s',    %d,      %d,           '%s', '%s','%s',  %d)" % (
                          name, dob, occupation1, occupation2, address, phone1, phone2, faith)
        #rint '.........................'
      
        l = [first_name, middle_name, last_name, occupation, occupation2,
                   english_ability, qualification, relationship, blood_group,
                    address_line1,   address_line2, city, state, country_id,
                    email,  phone1,  phone2, income, birth_date, faith]
        
        L = [str(x) for x in l]
        hasData = "".join(L)
        if hasData:
            if self.editMode:
                if hasData:
                    sql = "UPDATE guardians %s WHERE Kode = %s"  % (setQl, self.guardian_id)
                    #rint sql
                    #fetch.updateDB(sql)
                    
                else:
                    self.updateStudentRecord(self.guardian_id)
            else:
                #guid = fetch.add#NewUser(first_name, last_name)
                #sql = "INSERT INTO guardians SET %s , guid='%s'"  % (setQl, guid)
		sql = "INSERT INTO guardians SET %s "  % (setQl,)
		#rint sql
                #new_guardian_id = fetch.updateDB(sql)
                self.updateStudentRecord(new_guardian_id)
            
    def updateStudentRecord(self, guardian_id):
        #rint ' id = fetch.updateDB(', sql
        gid = guardian_id
        if self.guardian_type == 'father':
            sql = " UPDATE students SET father_id   = %d" % gid
            
        if self.guardian_type == 'mother':
            sql = " UPDATE students SET mother_id   = %d" % gid
            
        if self.guardian_type == 'guardian':
            sql = " UPDATE students SET guardian_id = %d" % gid
            
        sql += " WHERE id = %d" % self.student_id
        #rint sql
        #fetch.updateDB(sql) 
    
    def OnEditDate(self, event):  #
        import OpenDlg
        dateObject = self.date_ctrl_dob.GetDbReadyValue()
        print 'dateObject:',dateObject
        OpenDlg.DatePicker(dateObject)
        event.Skip()

    def OnEditAddress(self, event):
        self.GetTopLevelParent().goTo('edit_address')

    def OnEditTelp(self, event):  
        #rint "Event handler `OnEditTelp' not implemented!"
        event.Skip()
    
    def clearCtrls(self):
        for ctrl in self.text_ctrls:
            ctrl.Value = ''
        
        for ctrl in self.choice_ctrls:
            ctrl.SetSelection(0)
    
    def enableCtrls(self, state = True):
        for ctrl in self.text_ctrls:
            try:    ctrl.SetEditable(state)
            except: 
		    pass
        
        for ctrl in self.choice_ctrls:
            ctrl.Enable(state)

    def setCmb(self, cmb, str):
        try:     cmb.SetSelection(cmb.FindString(str))
        except:  pass
        
    def makeStr(self, x=''):
        try:    return str(x)
        except: return ''
        
class PromptingComboBox(wx.ComboBox) :
    def __init__(self, parent, value, choices=[], style=0, **par):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, style=style|wx.CB_DROPDOWN, choices=choices, **par)
        self.choices = choices
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.Bind(wx.EVT_CHAR, self.EvtChar)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox)
        self.ignoreEvtText = False

    def EvtCombobox(self, event):
        self.ignoreEvtText = True
        event.Skip()

    def EvtChar(self, event):
        if event.GetKeyCode() == 8:
            self.ignoreEvtText = True
        event.Skip()

    def EvtText(self, event):
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return
        currentText = event.GetString()
        found = False
        for choice in self.choices :
            if choice.startswith(currentText):
                self.ignoreEvtText = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(currentText))
                self.SetMark(len(currentText), len(choice))
                found = True
                break
        if not found:
            event.Skip()