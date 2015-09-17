import wx, gVar

import fetchodbc as fetch
import loadCmbODBC as loadCmb

from datetime          import date

from DateCtrl          import DateCtrl
#from PanelStudentFees  import PanelStudentFees
from PanelRegAssesment import PanelRegAssesment
from PanelRegProcess   import PanelRegProcess
#from bio import student

class PanelStudentEditor(wx.Panel):
    def __init__(self, *args, **kwds):
        _custom_classes = {'wx.Panel': ['PanelStudentFees']}
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.SetBackgroundColour((240,240,255))
        
        self.nb_studentData      = wx.Notebook(self, -1, style=0)
        
        self.pane_biodata   = wx.Panel(self.nb_studentData, -1)
        self.pane_education = wx.Panel(self.nb_studentData, -1)
        self.pane_medical   = wx.Panel(self.nb_studentData, -1)
        self.pane_fees      = wx.Panel(self.nb_studentData, -1)#PanelStudentFees(self.nb_studentData, -1)
        
        self.panel_bio      = wx.Panel(self.pane_biodata, -1)
        self.panel_siblings = wx.Panel(self.pane_biodata, -1)
        self.panel_address  = wx.Panel(self.pane_biodata, -1)
        self.panel_telp     = wx.Panel(self.pane_biodata, -1)
        
        self.panel_sib_base  = wx.Panel(self.panel_siblings, -1)
        self.panel_education = wx.Panel(self.pane_education, -1)

        self.panel_bio2        = wx.Panel(self.panel_bio,  -1)
        
        self.label_name        = wx.StaticText(self.panel_bio2, -1, "Name")
        self.text_ctrl_name    = wx.TextCtrl(self.panel_bio2,   -1, "")
        
        self.labelbirthplace   = wx.StaticText(self.panel_bio2, -1, "Birthplace")
        self.panel_pob         = wx.Panel(self.panel_bio2, -1)
        self.choice_pob        = wx.Choice(self.panel_pob,    -1, choices=[])
        self.button_edit_pob   = wx.Button(self.panel_pob,      -1, "...")
        
        self.label_faith       = wx.StaticText(self.panel_bio2, -1, "Faith")
        self.choice_faith      = wx.Choice(self.panel_bio2,   -1, choices=[])
        
        self.label_gender      = wx.StaticText(self.panel_bio2, -1, "Gender")
        self.choice_gender     = wx.Choice(self.panel_bio2,   -1, choices=['Male','Female'])
        
        self.label_dob         = wx.StaticText(self.panel_bio2, -1, "Date of birth")
        self.panel_dob         = wx.Panel(self.panel_bio2, -1)
        self.date_ctrl_dob     = DateCtrl(self.panel_bio2, -1)
        
        self.label_residence   = wx.StaticText(self.panel_bio2, -1, "Residence")
        self.combo_residence   = wx.Choice(self.panel_bio2,   -1, choices=['Father','Mother','Guargian'])
        
        self.label_sib_birth       = wx.StaticText(self.panel_sib_base , -1, "birth")
        self.spin_sibling_by_birth = wx.SpinCtrl(self.panel_sib_base , -1, "", min=0, max=100)
        
        
        self.label_sib_step    = wx.StaticText(self.panel_sib_base , -1, "step")
        self.spin_sibling_step = wx.SpinCtrl(self.panel_sib_base , -1, "", min=0, max=100)
        
        self.label_sib_adopted = wx.StaticText(self.panel_sib_base , -1, "adopted")
        self.spin_sib_adopted  = wx.SpinCtrl(self.panel_sib_base , -1, "", min=0, max=100)
        
        self.label_childNo     = wx.StaticText(self.panel_sib_base , -1, "Child #")
        self.spin_birth_order  = wx.SpinCtrl(self.panel_sib_base , -1, "", min=0, max=100)
        
        self.label_status      = wx.StaticText(self.panel_sib_base , -1, "Status")
        self.choice_status     = wx.Choice(self.panel_sib_base ,         -1, choices=[])
        
        self.label_previous_school = wx.StaticText(self.panel_education, -1, "Previous school")
        self.choice_schools        = wx.Choice(self.panel_education,   -1, choices=[])
        
        self.label_Current_status         = wx.StaticText(self.panel_education, -1, "Current status")
        self.text_ctrl_current_edu_status = wx.TextCtrl(self.panel_education, -1, "")
        
        self.label_edu_notes     = wx.StaticText(self.pane_education,  -1, "Notes:")
        self.text_ctrl_edu_notes = wx.TextCtrl(self.pane_education, - 1, "")
        
        self.panel_blood         = wx.Panel(self.pane_medical,  -1)
        self.label_blood_group   = wx.StaticText(self.panel_blood,  -1, "Blood group")
        self.choice_blood_group  = wx.Choice(self.panel_blood, -1, choices=[])
        
        self.label_medical_notes     = wx.StaticText(self.pane_medical,  -1, "Notes:")
        self.text_ctrl_medical_notes = wx.TextCtrl(self.pane_medical,    -1, "")
        
        #self.text_ctrl_address     = wx.TextCtrl(self.panel_address, -1, "")
  
        #self.text_ctrl_telephone   = wx.TextCtrl(self.panel_telp, -1, "", style=wx.TE_PROCESS_TAB)

        #self.button_edit_telephone = wx.Button(self.panel_telp,    -1, "...")
        #self.button_edit_address   = wx.Button(self.panel_address, -1, "...")
        
        self.static_line_1 = wx.StaticLine(self.panel_sib_base, -1)
        self.static_line_2 = wx.StaticLine(self.panel_sib_base, -1)

        self.sizer_bio_static_staticbox    = wx.StaticBox(self.panel_bio,      -1, " ")
        self.sizer_student_sibs_staticbox  = wx.StaticBox(self.panel_siblings, -1, "Siblings")
        #self.sizer__student_addr_staticbox = wx.StaticBox(self.panel_address,  -1, "Address")
        #self.sizer_student_telp_staticbox  = wx.StaticBox(self.panel_telp,     -1, "Telephone")

        self.text_ctrls = [ self.text_ctrl_name, self.text_ctrl_edu_notes,  self.text_ctrl_medical_notes,
                            self.text_ctrl_current_edu_status]
        
        self.spin_ctrls  = [self.spin_sibling_by_birth, self.spin_sibling_step,              
                            self.spin_sib_adopted,      self.spin_birth_order]
        
        self.combo_ctrls = [self.choice_blood_group, self.choice_status,
                            self.choice_schools,     self.choice_pob,
                            self.choice_faith,       self.choice_gender,
                            self.combo_residence]
        
        self.button_ctrls =[self.button_edit_pob,       self.button_edit_pob ]
        
        self.__set_properties()
        self.__set_bindings()
        self.__do_layout()
        self.__do_main()
        
    def __set_bindings(self):
        #self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNbChanging)
        #self.nb_studentData.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNB_changePage) 
        #self.nb_studentData.Bind(wx.EVT_PAGE_CHANGING, self.OnNB_changePage, self.nb_studentData)
        #self.Bind(wx.EVT_BUTTON, self.OnEditAddress,   self.button_edit_address)
        #self.Bind(wx.EVT_BUTTON, self.OnEditTelp,      self.button_edit_telephone)
        
        #self.text_ctrl_first_name.Bind(wx.EVT_TEXT,    self.OnFirstName , id=wx.ID_ANY)
        #self.text_ctrl_middle_name.Bind(wx.EVT_BUTTON, self.OnMiddleName, id=wx.ID_ANY)
        #self.text_ctrl_last_name.Bind(wx.EVT_BUTTON,   self.OnLastName  , id=wx.ID_ANY)
        pass
    
    def OnNB_changePage(self, evt):
        print 'OnNB_changePage'
        if self.editmode:
            evt.Veto()
        #rint 'OnNB_changePage ', x
        
        
    def __set_properties(self):
        self.date_ctrl_dob.checkbox.Hide()
        self.text_ctrl_name.SetMinSize((200, -1))
        self.spin_sibling_by_birth.SetMinSize(  (41, -1))
        self.spin_sibling_step.SetMinSize((41, -1))
        self.spin_sib_adopted.SetMinSize((41, -1))
        self.spin_birth_order.SetMinSize((41, -1))
        self.choice_blood_group.SetMinSize((61, -1))
        #self.choice_status.SetMinSize((70, 21))
        #self.choice_faith.SetMinSize((110, 21))
        #self.choice_pob.SetMinSize(  (110, 21))
        #self.text_ctrl_address.SetMinSize(    (-1, 90))
        #self.button_edit_address.SetMinSize(  (30, 16))
        self.button_edit_pob.SetMinSize(      (30, 16))
        #self.button_edit_telephone.SetMinSize((30, 16))

    def __do_layout(self):
        sizer_ownData = wx.BoxSizer(wx.VERTICAL)
        sizer_medical = wx.BoxSizer(wx.VERTICAL)
        sizer_edu     = wx.BoxSizer(wx.VERTICAL)
        sizer_dob     = wx.BoxSizer(wx.HORIZONTAL)
        sizer_pob     = wx.BoxSizer(wx.HORIZONTAL)
        sizer_blood   = wx.BoxSizer(wx.HORIZONTAL)
        
        grid_sizer_edu         = wx.FlexGridSizer(2, 2, 5, 5)
        grid_sizer_student     = wx.FlexGridSizer(3, 2, 5, 5)
        grid_sizer_student_bio = wx.FlexGridSizer(8, 2, 5, 5)
        
        #self.sizer_student_telp_staticbox.Lower()
        #sizer_student_telp     = wx.StaticBoxSizer(self.sizer_student_telp_staticbox, wx.VERTICAL)
        
        #self.sizer__student_addr_staticbox.Lower()
        #sizer__student_addr    = wx.StaticBoxSizer(self.sizer__student_addr_staticbox, wx.VERTICAL)
        
        self.sizer_student_sibs_staticbox.Lower()
        sizer_student_sibs_static = wx.StaticBoxSizer(self.sizer_student_sibs_staticbox, wx.VERTICAL)
        sizer_student_siblings    = wx.FlexGridSizer(6, 2, 2, 0)
        
        self.sizer_bio_static_staticbox.Lower()
        sizer_bio_static          = wx.StaticBoxSizer(self.sizer_bio_static_staticbox, wx.VERTICAL)
        
        sizer_pob.Add(self.choice_pob,   1, wx.EXPAND, 0)
        sizer_pob.Add(self.button_edit_pob, 0, wx.EXPAND, 0)
        self.panel_pob.SetSizer(sizer_pob)

        grid_sizer_student_bio.Add(self.label_name,     0, 0, 0)
        grid_sizer_student_bio.Add(self.text_ctrl_name, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_dob,     0, 0, 0)
        grid_sizer_student_bio.Add(self.date_ctrl_dob, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_faith, 0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_faith,  0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_gender, 0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_gender, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.labelbirthplace, 0, 0, 0)
        grid_sizer_student_bio.Add(self.panel_pob, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_residence, 0, 0, 0)
        grid_sizer_student_bio.Add(self.combo_residence, 0, wx.EXPAND, 0)
        
        self.panel_bio2.SetSizer(grid_sizer_student_bio)
        
        sizer_bio_static.Add(self.panel_bio2, 1, wx.EXPAND, 0)
        self.panel_bio.SetSizer(sizer_bio_static)
        
        grid_sizer_student.Add(self.panel_bio, 0, wx.EXPAND, 0)
        
        
        sizer_student_siblings.Add(self.label_sib_birth,       0, 0, 0)
        sizer_student_siblings.Add(self.spin_sibling_by_birth, 0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_step,        0, 0, 0)
        sizer_student_siblings.Add(self.spin_sibling_step,     0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_adopted,     0, 0, 0)
        sizer_student_siblings.Add(self.spin_sib_adopted,      0, 0, 0)
        sizer_student_siblings.Add(self.static_line_1,    0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.static_line_2,    0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.label_childNo,    0, 0, 0)
        sizer_student_siblings.Add(self.spin_birth_order, 0, 0, 0)
        sizer_student_siblings.Add(self.label_status,     0, 0, 0)
        sizer_student_siblings.Add(self.choice_status, 0, 0, 0)
        self.panel_sib_base .SetSizer(sizer_student_siblings)
        
        sizer_student_sibs_static.Add(self.panel_sib_base , 1, wx.EXPAND, 0)
        self.panel_siblings.SetSizer(sizer_student_sibs_static)
        
        grid_sizer_student.Add(self.panel_siblings,        0, wx.EXPAND, 0)
        #sizer__student_addr.Add(self.text_ctrl_address,    1, wx.EXPAND, 1)
        #sizer__student_addr.Add(self.button_edit_address,  0, wx.ALIGN_RIGHT, 0)
        #self.panel_address.SetSizer(sizer__student_addr)
        
        #grid_sizer_student.Add(self.panel_address,         1, wx.EXPAND, 0)
        #sizer_student_telp.Add(self.text_ctrl_telephone,   0, wx.EXPAND, 1)
        #sizer_student_telp.Add(self.button_edit_telephone, 0, wx.ALIGN_RIGHT, 0)
        #self.panel_telp.SetSizer(sizer_student_telp)
        
        #grid_sizer_student.Add(self.panel_telp, 1, wx.EXPAND, 0)
        self.pane_biodata.SetSizer(grid_sizer_student)
        
        grid_sizer_edu.Add(self.label_previous_school,        0, 0, 0)
        grid_sizer_edu.Add(self.choice_schools,            0, 0, 0)
        grid_sizer_edu.Add(self.label_Current_status,         0, 0, 0)
        grid_sizer_edu.Add(self.text_ctrl_current_edu_status, 0, 0, 0)
        
        self.panel_education.SetSizer(grid_sizer_edu)
        
        sizer_edu.Add(self.panel_education, 0, wx.ALL | wx.EXPAND, 2)
        sizer_edu.Add(self.label_edu_notes, 0, wx.TOP, 8)
        sizer_edu.Add(self.text_ctrl_edu_notes, 1, wx.EXPAND, 0)
        
        self.pane_education.SetSizer(sizer_edu)
        
        sizer_blood.Add(self.label_blood_group,  0, 0, 0)
        sizer_blood.Add(self.choice_blood_group, 0, 0, 0)
        self.panel_blood.SetSizer(sizer_blood)
        
        sizer_medical.Add(self.panel_blood,             0, wx.TOP, 6)
        sizer_medical.Add(self.label_medical_notes,     0, wx.TOP, 6)
        sizer_medical.Add(self.text_ctrl_medical_notes, 1, wx.EXPAND, 0)
        
        self.pane_medical.SetSizer(sizer_medical)
        
        self.nb_studentData.AddPage(self.pane_biodata,   "Biodata")
        self.nb_studentData.AddPage(self.pane_education, "Previous Education")
        self.nb_studentData.AddPage(self.pane_medical,   "Medical")
        self.nb_studentData.AddPage(self.pane_fees,      "Fees")
                                                                 
        sizer_ownData.Add(self.nb_studentData, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_ownData)
        sizer_ownData.Fit(self)
        self.Layout()
        
    def __do_main(self):
        loadCmb.pob(    self.choice_pob)
        loadCmb.faiths( self.choice_faith)
        loadCmb.schools(self.choice_schools)
        loadCmb.blood(  self.choice_blood_group)
    
    def displayData(self, student_id):
        print self.GetName(), "make student id open to class   student_id=", student_id
        self.clearCtrls()
        
        self.student_id = student_id
        if not student_id:  return
        
        student_details = fetch.studentDetails_id(student_id)
        #rint student_details
        if not student_details: return
        name = student_details['Nama']
        x  = str(student_details['TgLahir'])
        dob              = x.split(' ')[0]
        
        ailment          = ''#str(student_details['student_ailment'])
        faith_id         = student_details['Agama']
        
        previous_school_id = student_details['KSekolahAsal']
        
        birth_place      = str(student_details['TempatLahir'])
        edu_status       = ''     # ??? is this still needed
        edu_notes        = ''    # ??? seperate quiry on  table "edu_notes"
        #address          = ''#str(student_details['address_line1']) + "\n" + str(student_details['address_line2'])
        #address         += str(student_details['city'])          + "\n" + str(student_details['state'])
        #address         += str(student_details['pin_code'])      + "\n" + str(student_details['country_id'])
        #telephone        = ''# str(student_details['phone1'])        + "\n" + str(student_details['phone2'])
        
        blood_group_id   = str(student_details['GolDarah'])
        blood_group      = ''#fetch.bloodGroup(blood_group_id)
        
        siblings_birth    = student_details['SaudaraKandung']
        siblings_step     = student_details['SaudaraTiri']
        siblings_adopted  = student_details['SaudaraAngkat']
        if not siblings_step: siblings_step=0
        if not siblings_adopted: siblings_adopted =0
        birth_order      = student_details['AnakKe']
        if not birth_order:   birth_order = 1
        
        if student_details['Pria']:
            gender_index = 1
        else:
            gender_index = 2 

        self.text_ctrl_name.SetValue(name)
        
        self.text_ctrl_current_edu_status.SetValue(edu_status)
        self.text_ctrl_edu_notes.SetValue(edu_notes)
        self.text_ctrl_medical_notes.SetValue(ailment)

        #self.text_ctrl_address.SetValue('')
        #self.text_ctrl_telephone.SetValue('') 
        
        if dob: # "should be of format : 2012-06-26"                
            self.date_ctrl_dob.SetValue(dob)
            
        self.spin_sibling_by_birth.SetValue(siblings_birth)
        self.spin_sibling_step.SetValue(siblings_step)
        self.spin_sib_adopted.SetValue(siblings_adopted)
        self.spin_birth_order.SetValue(birth_order)
        
        self.choice_gender.SetSelection(gender_index)
        
        loadCmb.restore(self.choice_faith,  faith_id)
        loadCmb.restore_str(self.choice_pob,  birth_place)
        loadCmb.restore(self.choice_schools,     previous_school_id)
        loadCmb.restore_str(self.choice_status,    edu_status)
        loadCmb.restore_str(self.choice_blood_group, blood_group)
                
    def clearCtrls(self):     
        for ctrl in self.text_ctrls:  ctrl.SetValue('')
        for ctrl in self.spin_ctrls:  ctrl.SetValue(0)
        for ctrl in self.combo_ctrls: ctrl.SetSelection(0)
        
    def enableCtrls(self, state = True):
        self.editmode = state
        self.date_ctrl_dob.Enable(state)
        for ctrl in self.button_ctrls:ctrl.Enable(state)
        #for ctrl in self.text_ctrls:  ctrl.SetEditable(state)
        for ctrl in self.spin_ctrls:  ctrl.Enable(state)
        for ctrl in self.combo_ctrls: ctrl.Enable(state)
        #self.pane_fees.enableCtrls(state)
        
         
    def disable_ctrls(self):
        self.enableCtrls(False)
        
    def OnDOB(self, event):  # wxGlade: aSsOwnData.<event_handler>
        event.Skip()

    def OnEditAddress(self, event):  # wxGlade: aSsOwnData.<event_handler>
        event.Skip()

    def OnEditTelp(self, event):  # wxGlade: aSsOwnData.<event_handler>
        event.Skip()
    
    def OnFirstName(self,id):
        pass
    
    def OnLastName(self,id):
        pass
    
    def OnMiddleName(self,id):
        pass

    def saveData(self):
        birth_date   = self.date_ctrl_dob.GetDbReadyValue()
        
        first_name         = self.text_ctrl_name.GetValue()
        address            = self.text_ctrl_address.GetValue()
        telephone          = self.text_ctrl_telephone.GetValue()
        previous_school_id = self.choice_schools.GetValue()
        try:
            previous_school_id = int(previous_school_id)
        except :
            previous_school_id = 0
        
        edu_status         = self.text_ctrl_current_edu_status.GetValue()
        try:
            edu_status = int(edu_status)
        except:
            edu_status = 0
        
        edu_notes          = self.text_ctrl_edu_notes.GetValue()
        medical_notes      = self.text_ctrl_medical_notes.GetValue()
        
        pob          = self.choice_pob.GetValue()
        faith_id     = fetch.cmbID(self.choice_faith)
        birth_status = self.choice_status.GetValue()
        blood_group  = self.choice_blood_group.GetValue()
        
        idx = self.choice_gender.GetSelection()
        
        if   idx == 1: gender = 'm'
        elif idx == 2: gender = 'f'
        else:          gender = '?'
        
        siblings_by_birth    = self.spin_sibling_by_birth.GetValue()
        siblings_by_marrige  = self.spin_sibling_step.GetValue()
        siblings_by_adoption = self.spin_sib_adopted.GetValue()
        
        if  not siblings_by_birth:    siblings_by_birth=0
        if  not siblings_by_marrige:  siblings_by_marrige=0
        if  not siblings_by_adoption: siblings_by_adoption=0
        
        no_of_siblings = "%d,%d,%d" % (siblings_by_birth, siblings_by_marrige, siblings_by_adoption)
        
        birth_order = self.spin_birth_order.GetValue()

        sql = "UPDATE CSiswa SET (Nama, TglLahir, TempatLahir, Agama, GolDarah, Pria, \
                                  SaudaraKandung, SaudaraTiri, SaudaraAngkat, AnakKe,  KSekolahAsal) \
                          VALUES ('%s',    '%s',     '%s',       %d,     '%s',    %d, \
                                        %d,          %d,            %d,          %d,     %d) \
                WHERE Kode = %d" % (name, dob, pob, faith,  blood_group,  gender,
                                    siblings_by_birth, siblings_by_marrige, siblings_by_adoption, birth_order, iprevious_school_id,
                                    self.student_id)
        print sql
        #fetch.updateDB(sql)
        
    def addRegpanels(self):
        self.nb_boidata_pane_assesment = PanelRegAssesment(self.nb_studentData, -1)
        self.nb_boidata_pane_regstatus = PanelRegProcess(self.nb_studentData, -1)
        self.nb_studentData.AddPage(self.nb_boidata_pane_regstatus, "Reg status")
        self.nb_studentData.AddPage(self.nb_boidata_pane_assesment, "Reg assesment")