import wx

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

from ctrl.DateCtrl import DateCtrl
import dialog.EditAddress

class panel_guardian_data(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_top_left         = wx.Panel(self, -1)
        self.panel_name             = wx.Panel(self.panel_top_left, -1)
        
	self.label_first_name       = wx.StaticText(self.panel_name, -1, "Name")
        self.text_ctrl_name         = wx.TextCtrl(self.panel_name,   -1, "")
	
        self.label_email            = wx.StaticText(self.panel_name, -1, "Email")
        self.text_ctrl_email        = wx.TextCtrl(self.panel_name,   -1, "")
	
        self.label_blood_group      = wx.StaticText(self.panel_name, -1, "Blood group")
        self.combo_box_blood_group  = wx.ComboBox(self.panel_name,   -1, choices=[], style=wx.CB_DROPDOWN)
        
	self.label_dob              = wx.StaticText(self.panel_name, -1, "Date of birth")
        self.panel_blood_dob        = wx.Panel(self.panel_name,      -1)
        self.date_ctrl_dob          = DateCtrl(self.panel_blood_dob, -1)
	
        self.label_relationship     = wx.StaticText(self.panel_name, -1, "Relationship")
        self.combo_box_relationship = wx.ComboBox(self.panel_name,   -1, choices=[], style=wx.CB_DROPDOWN)
        
	self.label_faith            = wx.StaticText(self.panel_name, -1, "Faith")
        self.combo_box_faith        = wx.ComboBox(self.panel_name,   -1, choices=[], style=wx.CB_DROPDOWN)
        
        self.sizer_name_static_staticbox = wx.StaticBox(self.panel_top_left, -1, "Name ")
        
        self.panel_top_right            = wx.Panel(self, -1)
        self.label_main_occupation      = wx.StaticText(self.panel_top_right, -1, "Main")
        self.combo_occupation_main      = wx.ComboBox(self.panel_top_right,   -1, choices=[])
        self.label_2nd_occupation       = wx.StaticText(self.panel_top_right, -1, "2nd")
        self.text_ctrl_occupation_other = wx.TextCtrl(self.panel_top_right,   -1, "")
        self.label_income               = wx.StaticText(self.panel_top_right, -1, "Income")
        self.text_ctrl_income           = wx.TextCtrl(self.panel_top_right,   -1, "")
        self.label_qualification        = wx.StaticText(self.panel_top_right, -1, "Qualification")
        self.combo_box_qualification    = wx.ComboBox(self.panel_top_right,   -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_english              = wx.StaticText(self.panel_top_right, -1, "Engllish")
        self.combo_box_english_level    = wx.ComboBox(self.panel_top_right,   -1, choices=["Weak", "Average", "Good", "Native"], style=wx.CB_DROPDOWN)
        
        self.sizer_occupation_staticbox = wx.StaticBox(self.panel_top_right, -1, "Occupation")
        
        self.panel_bottom_left          = wx.Panel(self, -1)
        self.text_ctrl_address          = wx.TextCtrl(self.panel_bottom_left, -1, style = wx.TE_MULTILINE)
        self.button_edit_address        = wx.Button(self.panel_bottom_left,   -1, "...")
        
        self.sizer_address_staticbox    = wx.StaticBox(self.panel_bottom_left, -1, "Address")
        
        self.panel_bottom_right         = wx.Panel(self, -1)
        self.text_ctrl_telp           = wx.TextCtrl(self.panel_bottom_right,  -1, "")
        self.text_ctrl_hp           = wx.TextCtrl(self.panel_bottom_right,  -1, "")
        self.button_edit_telp           = wx.Button(self.panel_bottom_right,    -1, "...")
        
        self.sizer_telp_staticbox       = wx.StaticBox(self.panel_bottom_right, -1, "Telephone")

	self.Bind(wx.EVT_BUTTON, self.OnEditAddress,  self.button_edit_address)
        self.Bind(wx.EVT_BUTTON, self.OnBtnEditGtelp, self.button_edit_telp)
	
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.SetSize((384, 424))
        self.text_ctrl_name.SetMinSize((200, 21))
        self.text_ctrl_email.SetMinSize((200, 21))
        self.combo_box_blood_group.SetMinSize((120, 21))
        self.combo_box_qualification.SetMinSize((100, 21))
        self.combo_box_english_level.SetMinSize((40, 21))
        self.combo_box_english_level.SetSelection(-1)
        self.panel_top_right.SetMinSize((140, -1))
        self.text_ctrl_address.SetMinSize((262, 90))
        self.text_ctrl_address.Enable(False)
        self.button_edit_address.SetMinSize((41, 16))
        self.button_edit_telp.SetMinSize((41, 16))
        self.button_edit_telp.Hide()
        
    def __do_layout(self):
        grid_sizer_guardian = wx.FlexGridSizer(4, 2, 0, 0)
        self.sizer_telp_staticbox.Lower()
        sizer_telp          = wx.StaticBoxSizer(self.sizer_telp_staticbox, wx.VERTICAL)
        self.sizer_address_staticbox.Lower()
        sizer_address       = wx.StaticBoxSizer(self.sizer_address_staticbox, wx.VERTICAL)
        self.sizer_occupation_staticbox.Lower()
        sizer_occupation    = wx.StaticBoxSizer(self.sizer_occupation_staticbox, wx.VERTICAL)
        self.sizer_name_static_staticbox.Lower()
        sizer_name_static   = wx.StaticBoxSizer(self.sizer_name_static_staticbox, wx.VERTICAL)
        grid_sizer_name     = wx.FlexGridSizer(8, 2, 2, 1)
        sizer_blood_dob     = wx.BoxSizer(wx.HORIZONTAL)
        
        grid_sizer_name.Add(self.label_first_name,      0, wx.TOP, 15)
        grid_sizer_name.Add(self.text_ctrl_name,        0, wx.TOP, 15)
        grid_sizer_name.Add(self.label_email,           0, 0, 0)
        grid_sizer_name.Add(self.text_ctrl_email,       0, 0, 0)
        grid_sizer_name.Add(self.label_blood_group,     0, 0, 0)
        grid_sizer_name.Add(self.combo_box_blood_group, 0, 0, 2)
        grid_sizer_name.Add(self.label_dob,             0, 0, 0)
        
        sizer_blood_dob.Add(self.date_ctrl_dob, 0, 0, 0)
        
        self.panel_blood_dob.SetSizer(sizer_blood_dob)
        grid_sizer_name.Add(self.panel_blood_dob,        1, wx.EXPAND, 0)
        
        grid_sizer_name.Add(self.label_faith,            0, wx.TOP | wx.BOTTOM, 0)
        grid_sizer_name.Add(self.combo_box_faith,        0, wx.TOP | wx.BOTTOM | wx.EXPAND, 0)
        
        grid_sizer_name.Add(self.label_relationship,     0, wx.TOP | wx.BOTTOM, 2)
        grid_sizer_name.Add(self.combo_box_relationship, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 2)
        
        self.panel_name.SetSizer(grid_sizer_name)
        
        sizer_name_static.Add(self.panel_name,           1, wx.EXPAND, 0)
        self.panel_top_left.SetSizer(sizer_name_static)
        
        grid_sizer_guardian.Add(self.panel_top_left,     1, wx.TOP | wx.EXPAND, 0)
        
        sizer_occupation.Add(self.label_main_occupation,      0, 0, 0)
        sizer_occupation.Add(self.combo_occupation_main,      0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_2nd_occupation,       0, 0, 0)
        sizer_occupation.Add(self.text_ctrl_occupation_other, 0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_income,               0, 0, 0)
        sizer_occupation.Add(self.text_ctrl_income,           0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_qualification,        0, 0, 0)
        sizer_occupation.Add(self.combo_box_qualification,    0, wx.EXPAND, 0)
        sizer_occupation.Add(self.label_english,              0, wx.EXPAND, 0)
        sizer_occupation.Add(self.combo_box_english_level,    0, wx.EXPAND, 0)
        
        self.panel_top_right.SetSizer(sizer_occupation)
        grid_sizer_guardian.Add(self.panel_top_right,    1, wx.EXPAND, 0)
        sizer_address.Add(self.text_ctrl_address,        0, wx.EXPAND, 0)
        sizer_address.Add(self.button_edit_address,      0, wx.ALIGN_RIGHT, 0)
        self.panel_bottom_left.SetSizer(sizer_address)
        grid_sizer_guardian.Add(self.panel_bottom_left,  1, wx.EXPAND, 0)
        sizer_telp.Add(self.text_ctrl_telp,              0, wx.EXPAND, 0)
        sizer_telp.Add(self.text_ctrl_hp,                0, wx.EXPAND, 0)
        sizer_telp.Add(self.button_edit_telp,            0, wx.ALIGN_RIGHT, 0)
        self.panel_bottom_right.SetSizer(sizer_telp)
        grid_sizer_guardian.Add(self.panel_bottom_right, 1, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_guardian)
       
    def __do_main(self):
        self.editMode=False
	self.address = ''
	
    def student_has_other_guardian(self, student_id):
	sql = "SELECT father_id, mother_id, guardian_id FROM students WHERE id = %d" % student_id
	res = fetch.getOneDict(sql)
	father_id   = res['father_id']
	mother_id   = res['mother_id']
	guardian_id = res['guardian_id']
	
    
	if father_id or mother_id or guardian_id:
	    return True
	else:
	    return False
    
    def displayData(self, guardian_type, guardian_id, student_id):
	if guardian_id:
	    self.editMode = True
	else:
	    if self.student_has_other_guardian(student_id):
		self.editMode = True
	    else:
		self.editMode = False
		
        # #rint'Guardian displayData', guardian_type, guardian_id, student_id
        self.guardian_type = guardian_type
        self.guardian_id   = guardian_id
        self.student_id    = student_id
        
        self.clearCtrls()
  
        if not guardian_id: return
	
	data = self.loadData(guardian_id)
  

	# unpack data (name, address, faith_id, dob, HP, telp, wilayah,
	#	       pob, occupation_main, occupation_other, nationality)
	
	
		
	name, address, faith_id, dob, telp, hp, wilayah, pob, occupation_main_id, occupation_other, nationality_id = data
	    
	self.text_ctrl_name.SetValue(name)
	self.address = address
	self.text_ctrl_address.SetValue(address)
	loadCmb.restore(self.combo_box_faith, faith_id)
	self.date_ctrl_dob.SetValue(dob)
	self.text_ctrl_telp.SetValue(hp)
        self.text_ctrl_hp.SetValue(telp)
	# wilayah
	# pob
        loadCmb.restore(self.combo_occupation_main, occupation_main_id)
        self.text_ctrl_occupation_other.SetValue(str(occupation_other))
	# nationality

        if guardian_type == 'guardian':
	    try:
		relationship = fetch.guardianRelationship(student_id)
                index = self.combo_box_relationship.FindString(relationship)
                self.combo_box_relationship.SetSelection(index)
		self.label_relationship.Show()
		self.combo_box_relationship.Show()
            except:  pass
        else:
            self.label_relationship.Hide()
            self.combo_box_relationship.Hide()
        
    def loadData(self, guardian_id):
	sql = "SELECT * \
                 FROM guardians \
		WHERE id = %d" % guardian_id
	
        res = fetch.getOneDict(sql)
	if not res: return

	name     = res['name']
	address  = res['address']
	faith_id = res['faith_id']
	dob      = res['dob']
	telp     = res['telp']
	hp       = res['hp']
	wilayah  = res['wilayah']
	pob      = res['pob']
	occupation_main_id = res['occupation_main_id']
	occupation_other   = res['occupation_other']
	nationality        = res['nationality']

	return (name, address, faith_id, dob, telp, hp, wilayah, 
		pob, occupation_main_id, occupation_other, nationality)
    
        
    def saveData(self):
	name          = self.text_ctrl_name.GetValue()
        dob       = self.date_ctrl_dob.GetDbReadyValue()
	if not dob:
	    dob =  '1800-01-01'
    
        occupation_main   = fetch.cmbID(self.combo_occupation_main)
        occupation_other = self.text_ctrl_occupation_other.GetValue()
        
        #english_level = self.combo_box_english_level.GetValue()
        #qualification = self.combo_box_qualification.GetValue()
        
        #relationship  = fetch.cmbID(self.combo_box_relationship)
        #blood_group   = fetch.cmbID(self.combo_box_blood_group)
        
        address        = self.text_ctrl_address.GetValue()
        HP            = self.text_ctrl_telp.GetValue()
        telp       = self.text_ctrl_hp.GetValue()
        #income        = self.text_ctrl_income.GetValue()
        
        #email         = self.text_ctrl_email.GetValue()
        faith_id       = fetch.cmbID(self.combo_box_faith)
	
	wilayah = ''
	pob = ''
	nationality = 0
        
        nb_name = self.GetName()
	
	
	data = (name, address, faith_id, \
		dob, HP, telp, \
		wilayah, pob, occupation_main, \
		occupation_other, nationality)

	if self.editMode:
	    self.updateGuardian(data)
	
	else:
	    self.insertGuardian(data)
	    
    def insertGuardian(self, data):
	data = list(data)
	nb_name = self.GetName()
	if nb_name =='g':   relationship = 'guardian'
	elif nb_name =='f': relationship = 'father'
	else:               relationship = 'mother'
	data.append(relationship)
	
	sql = "INSERT INTO guardians (name, address, faith_id, \
				    dob, telp1, telp2,\
				    wilayah, pob, occ_main_id, \
				    occ_other, nationality, relationship) \
			    VALUES ('%s', '%s', %d, \
				    '%s', '%s', '%s', \
				    '%s', '%s', %d, \
				    '%s', %d, %d)" % tuple(data)
	#rintsql
	guardian_id = fetch.updateDB(sql)
	
	sql = "UPDATE students SET "
	if nb_name =='g':   sql += " guardian_id "
	elif nb_name =='f': sql += " father_id "
	else:               sql == " mother_id "
	sql += "= %d WHERE id = %d" % (guardian_id, self.student_id)
	    
	fetch.updateDB(sql)

    def updateGuardian(self, data):
	data = list(data)
	
	nb_name = self.GetName()
	if nb_name =='g':   relationship = 'guardian'
	elif nb_name =='f': relationship = 'father'
	else:               relationship = 'mother'
	data.append(relationship)
	
	##rint'DATA Update Guardian >>', data
		
	sql = "UPDATE guardians \
	          SET (name='%s', address='%s', faith_id=%d, \
			dob = '%s', telp1='%s', telp2='%s',\
			wilayah  = '%s', pob='%s', occ_main_id=%d, \
			occ_other = '%s', nationality_id = %d, relationship='s') \
		WHERE id = %d" % (tuple(data), self.guardian_id)
	#rintsql
	fetch.updateDB(sql)
	
    def OnEditAddress(self, evt):
	#rint'panel_guardian_data    OnEditAddress'
	if not self.guardian_id:
	    fetch.msg('can not enter address before guardian has been created')
	    return
	
	gVar.guardian_id = self.guardian_id
	gVar.address     = self.address
	
	#self.GetTopLevelParent().goTo('edit_address')
	dlg = DlgEditAddress.create(None)
        try:
            dlg.ShowModal()
            gVar.address = dlg.getEditedAddress()
	    if address == gVar.address:
		pass
	    else:
		pass
		#rint'update g'
        finally:
            dlg.Destroy()
            
    def updateStudentRecord(self, guardian_id):
        #rint'updateStudentRecord id '

	sql = " UPDATE students SET "
        if self.guardian_type == 'guardian': sql += " guardian_id "
	if self.guardian_type == 'mother':   sql += "  mother_id "
	else:                                sql += "  father_id  "  
        sql += " = %d  WHERE id = %d" % ( guardian_id, self.student_id)
        #rintsql
        #fetch.updateDB(sql)
  
    def OnBtnG_dob(self, event):  #
        #rint "Event handler `OnBtnG_dob' not implemented!"
        event.Skip()

    def OnEditGAddress(self, event): 
        self.GetTopLevelParent().goTo('panel_edit_address')

    def OnBtnEditGtelp(self, event):  
        #rint "Event handler `OnBtnEditGtelp' not implemented!"
        event.Skip()
        
    def clearCtrls(self):
        self.text_ctrl_name.Value      = ''
        self.text_ctrl_email.Value           = ''
        self.date_ctrl_dob.Value             = ''
        self.combo_occupation_main.Value = ''
        self.text_ctrl_occupation_other.Value  = ''
        self.text_ctrl_income.Value          = ''
        self.text_ctrl_address.Value         = ''
        self.text_ctrl_telp.Value          = ''
        self.text_ctrl_hp.Value          = ''
        
        self.combo_box_blood_group.SetSelection(0)
        self.combo_box_relationship.SetSelection(0)
        self.combo_box_faith.SetSelection(0)
        self.combo_box_qualification.SetSelection(0)
        self.combo_box_english_level.SetSelection(0)

    def enableCtrls(self, state = True):
	
        self.text_ctrls = [
            self.text_ctrl_name,    self.text_ctrl_email,
            self.date_ctrl_dob,     self.combo_occupation_main,
            self.text_ctrl_income,  self.text_ctrl_occupation_other,
            self.text_ctrl_address, self.text_ctrl_telp,
            self.text_ctrl_hp]
        
        for ctrl in self.text_ctrls:
            try:    ctrl.SetEditable(state)
            except: pass
        
        self.combo_box_blood_group.Enable(  state)
        self.combo_box_relationship.Enable( state)
        self.combo_box_faith.Enable(state)
        self.combo_box_qualification.Enable(state)
        self.combo_box_english_level.Enable(state)
 
    def setCmb(self, cmb, str):
        try:     cmb.SetSelection(cmb.FindString(str))
        except:  pass

    def makeStr(self, x = ''):
        try:    return str(x)
        except: return ''
"""        
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
            event.Skip()"""