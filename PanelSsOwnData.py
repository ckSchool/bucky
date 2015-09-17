import wx, gVar

import fetchodbc as fetch
import loadCmbODBC as loadCmb

from datetime          import date

from DateCtrl          import DateCtrl
#from PanelStudentFees  import PanelStudentFees
from PanelRegAssesment import PanelRegAssesment
from PanelRegProcess   import PanelRegProcess
#from bio import student

class PanelSsOwnData(wx.Panel):
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

        self.panel_bio2 = wx.Panel(self.panel_bio,  -1)
        
        self.label_name = wx.StaticText(self.panel_bio2, -1, "Name")
        self.data_name  = wx.StaticText(self.panel_bio2,   -1, "")
        
        self.labelbirthplace = wx.StaticText(self.panel_bio2, -1, "Birthplace")
        self.data_pob        = wx.StaticText(self.panel_bio2,    -1, "")
        
        self.label_faith = wx.StaticText(self.panel_bio2, -1, "Faith")
        self.data_faith  = wx.StaticText(self.panel_bio2,   -1, "")
        
        self.label_gender = wx.StaticText(self.panel_bio2, -1, "Gender")
        self.data_gender  = wx.StaticText(self.panel_bio2,   -1, "")
        
        self.label_dob = wx.StaticText(self.panel_bio2, -1, "Date of birth")
        self.data_dob  = wx.StaticText(self.panel_bio2, -1, "")
        
        self.label_residence = wx.StaticText(self.panel_bio2, -1, "Residence")
        self.data_residence  = wx.StaticText(self.panel_bio2,   -1, "")
        
        self.label_sib_birth       = wx.StaticText(self.panel_sib_base , -1, "birth")
        self.data_sibling_by_birth = wx.StaticText(self.panel_sib_base , -1, "")
        
        self.label_sib_step    = wx.StaticText(self.panel_sib_base , -1, "step")
        self.data_sibling_step = wx.StaticText(self.panel_sib_base , -1, "   ")
        
        self.label_sib_adopted = wx.StaticText(self.panel_sib_base , -1, "adopted")
        self.data_sib_adopted  = wx.StaticText(self.panel_sib_base , -1, "")
        
        self.label_childNo    = wx.StaticText(self.panel_sib_base , -1, "Child #")
        self.data_birth_order = wx.StaticText(self.panel_sib_base , -1, "")
        
        self.label_status      = wx.StaticText(self.panel_sib_base , -1, "Status")
        self.data_status       = wx.StaticText(self.panel_sib_base ,         -1, "")
        
        self.label_previous_school = wx.StaticText(self.panel_education, -1, "Previous school")
        self.data_school           = wx.StaticText(self.panel_education,   -1, "")
        
        self.label_Current_status    = wx.StaticText(self.panel_education, -1, "Current status")
        self.data_current_edu_status = wx.TextCtrl(self.panel_education, -1, "")
        
        self.label_edu_notes = wx.StaticText(self.pane_education,  -1, "Notes:")
        self.data_edu_notes  = wx.TextCtrl(self.pane_education, - 1, "")
        
        self.panel_blood       = wx.Panel(self.pane_medical,  -1)
        self.label_blood_group = wx.StaticText(self.panel_blood,  -1, "Blood group")
        self.data_blood_group  = wx.StaticText(self.panel_blood, -1, "")
        
        self.label_medical_notes = wx.StaticText(self.pane_medical,  -1, "Notes:")
        self.data_medical_notes  = wx.TextCtrl(self.pane_medical,    -1, "")

        self.static_line_1 = wx.StaticLine(self.panel_sib_base, -1)
        self.static_line_2 = wx.StaticLine(self.panel_sib_base, -1)

        self.sizer_bio_static_staticbox   = wx.StaticBox(self.panel_bio,      -1, " ")
        self.sizer_student_sibs_staticbox = wx.StaticBox(self.panel_siblings, -1, "Siblings")


        self.data_ctrls  = [self.data_name, self.data_edu_notes,  self.data_medical_notes,
                            self.data_current_edu_status, self.data_sibling_by_birth, self.data_sibling_step,              
                            self.data_sib_adopted,      self.data_birth_order,
                            self.data_blood_group, self.data_status,
                            self.data_school,     self.data_pob,
                            self.data_faith,       self.data_gender,
                            self.data_residence]
        
        for c in self.data_ctrls:
            c.SetBackgroundColour('white')
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        self.data_name.SetMinSize((200, -1))

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
        
        self.sizer_student_sibs_staticbox.Lower()
        sizer_student_sibs_static = wx.StaticBoxSizer(self.sizer_student_sibs_staticbox, wx.VERTICAL)
        sizer_student_siblings    = wx.FlexGridSizer(6, 2, 2, 0)
        
        self.sizer_bio_static_staticbox.Lower()
        sizer_bio_static          = wx.StaticBoxSizer(self.sizer_bio_static_staticbox, wx.VERTICAL)
        
        grid_sizer_student_bio.Add(self.label_name,     0, 0, 0)
        grid_sizer_student_bio.Add(self.data_name, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_dob,     0, 0, 0)
        grid_sizer_student_bio.Add(self.data_dob, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_faith, 0, 0, 0)
        grid_sizer_student_bio.Add(self.data_faith,  0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_gender, 0, 0, 0)
        grid_sizer_student_bio.Add(self.data_gender, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.labelbirthplace, 0, 0, 0)
        grid_sizer_student_bio.Add(self.data_pob, 0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_residence, 0, 0, 0)
        grid_sizer_student_bio.Add(self.data_residence, 0, wx.EXPAND, 0)
        
        self.panel_bio2.SetSizer(grid_sizer_student_bio)
        
        sizer_bio_static.Add(self.panel_bio2, 1, wx.EXPAND, 0)
        self.panel_bio.SetSizer(sizer_bio_static)
        
        grid_sizer_student.Add(self.panel_bio, 0, wx.EXPAND, 0)
        
        sizer_student_siblings.Add(self.label_sib_birth,       0, 0, 0)
        sizer_student_siblings.Add(self.data_sibling_by_birth, 0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_step,        0, 0, 0)
        sizer_student_siblings.Add(self.data_sibling_step,     0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_adopted,     0, 0, 0)
        sizer_student_siblings.Add(self.data_sib_adopted,      0, 0, 0)
        sizer_student_siblings.Add(self.static_line_1,    0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.static_line_2,    0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.label_childNo,    0, 0, 0)
        sizer_student_siblings.Add(self.data_birth_order, 0, 0, 0)
        sizer_student_siblings.Add(self.label_status,     0, 0, 0)
        sizer_student_siblings.Add(self.data_status, 0, 0, 0)
        self.panel_sib_base .SetSizer(sizer_student_siblings)
        
        sizer_student_sibs_static.Add(self.panel_sib_base , 1, wx.EXPAND, 0)
        self.panel_siblings.SetSizer(sizer_student_sibs_static)
        
        grid_sizer_student.Add(self.panel_siblings,        0, wx.EXPAND, 0)
        self.pane_biodata.SetSizer(grid_sizer_student)
        
        grid_sizer_edu.Add(self.label_previous_school,        0, 0, 0)
        grid_sizer_edu.Add(self.data_school,                  0, 0, 0)
        grid_sizer_edu.Add(self.label_Current_status,         0, 0, 0)
        grid_sizer_edu.Add(self.data_current_edu_status, 0, 0, 0)
        
        self.panel_education.SetSizer(grid_sizer_edu)
        
        sizer_edu.Add(self.panel_education, 0, wx.ALL | wx.EXPAND, 2)
        sizer_edu.Add(self.label_edu_notes, 0, wx.TOP, 8)
        sizer_edu.Add(self.data_edu_notes, 1, wx.EXPAND, 0)
        
        self.pane_education.SetSizer(sizer_edu)
        
        sizer_blood.Add(self.label_blood_group,  0, 0, 0)
        sizer_blood.Add(self.data_blood_group, 0, 0, 0)
        self.panel_blood.SetSizer(sizer_blood)
        
        sizer_medical.Add(self.panel_blood,             0, wx.TOP, 6)
        sizer_medical.Add(self.label_medical_notes,     0, wx.TOP, 6)
        sizer_medical.Add(self.data_medical_notes, 1, wx.EXPAND, 0)
        
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
        pass
    
    def displayData(self, student_id):
        print self.GetName(), "make student id open to class   student_id=", student_id
        self.clearCtrls()
        
        print 'x'
        
        self.student_id = student_id
        if not student_id:  return
        
        print 'y'
        
        student_details = fetch.studentDetails_id(student_id)
        
        print 'z', student_details
        
        if not student_details: return
        name = student_details['Nama']
        x  = str(student_details['TgLahir'])
        dob              = x.split(' ')[0]
        
        print 'x'
        
        ailment          = ''#str(student_details['student_ailment'])
        faith_id         = student_details['Agama']
        
        previous_school_id = student_details['KSekolahAsal']
        
        birth_place      = str(student_details['TempatLahir'])
        edu_status       = ''     # ??? is this still needed
        edu_notes        = ''    # ??? seperate quiry on  table "edu_notes"
 
        blood_group_id   = str(student_details['GolDarah'])
        blood_group      = ''#fetch.bloodGroup(blood_group_id)
        
        siblings_birth    = student_details['SaudaraKandung']
        siblings_step     = student_details['SaudaraTiri']
        siblings_adopted  = student_details['SaudaraAngkat']
        if not siblings_step: siblings_step=0
        if not siblings_adopted: siblings_adopted =0
        birth_order      = student_details['AnakKe']
        if not birth_order:   birth_order = 1
        
        print 'x'
        
        if student_details['Pria']:
            self.data_gender.SetLabel('male')
        else:
            self.data_gender.SetLabel('female')
        
        self.data_name.SetLabel(name)
        
        self.data_current_edu_status.SetLabel(edu_status)
        self.data_edu_notes.SetLabel(edu_notes)
        self.data_medical_notes.SetLabel(ailment)

        self.data_dob.SetLabel(dob)
            
        self.data_sibling_by_birth.SetLabel(str(siblings_birth))
        self.data_sibling_step.SetLabel(str(siblings_step))
        self.data_sib_adopted.SetLabel(str(siblings_adopted))
        self.data_birth_order.SetLabel(str(birth_order))

        previous_school = fetch.schoolName(previous_school_id)
        faith = fetch.faith(faith_id)
        
        self.data_faith.SetLabel(faith)
        self.data_pob.SetLabel(birth_place)
        self.data_school.SetLabel(previous_school)
        self.data_status.SetLabel(edu_status)
        self.data_blood_group.SetLabel(blood_group)
        
        print 'fghdfhgfdh'
        
        
    def clearCtrls(self):     
        for ctrl in self.data_ctrls:  ctrl.SetLabel('')
        
    def enableCtrls(self, state = True):
        pass
        
         
    def disable_ctrls(self):
        pass
        
