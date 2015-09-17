import wx, gVar, fetch, loadCmb

from datetime  import date
from DateCtrl  import DateCtrl

import panel_student_list

class panel_bio(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.text_ctrls   = []
        self.choice_ctrls = []
        
        self.panel_top = wx.Panel(self, -1)

        self.panel_bio        = wx.Panel(self.panel_top, -1)
        self.panel_siblings   = wx.Panel(self.panel_top, -1)
        self.panel_address    = wx.Panel(self.panel_top, -1)
        self.panel_telp       = wx.Panel(self.panel_top, -1)
        
        self.panel_sib_base   = wx.Panel(self.panel_siblings, -1)
        
        self.panel_bio2       = wx.Panel(self.panel_bio,  -1)
        
        self.label_name      = wx.StaticText(self.panel_bio2, -1, "Name")
        self.text_ctrl_name  = wx.TextCtrl(self.panel_bio2,   -1, "")
        self.text_ctrls .append(self.text_ctrl_name)
        
        self.labelbirthplace         = wx.StaticText(self.panel_bio2, -1, "Birthplace")
        self.choice_pob              = wx.Choice(self.panel_bio2,     -1, choices=[])
        
        self.label_faith             = wx.StaticText(self.panel_bio2, -1, "Faith")
        self.choice_faith            = wx.Choice(self.panel_bio2,     -1, choices=["Buddhist", "Muslim", "Christian", "Hindu", "Other"])
         
        self.label_gender            = wx.StaticText(self.panel_bio2, -1, "Gender")
        self.choice_gender           = wx.Choice(self.panel_bio2,     -1, choices=[])
        
        self.label_dob               = wx.StaticText(self.panel_bio2, -1, "Date of birth")
        self.datectrl_dob                = DateCtrl(self.panel_bio2, -1)
        
        self.label_residence         = wx.StaticText(self.panel_bio2, -1, "Residence")
        self.choice_residence        = wx.Choice(self.panel_bio2,     -1, choices=["Parents", "Father", "Mother", "Guardian", "Other"])
        
        self.label_sib_birth         = wx.StaticText(self.panel_sib_base , -1, "birth")
        self.choice_siblings_by_birth = wx.Choice(self.panel_sib_base,     -1, choices=['1','2','3','4','5'])
        
        self.label_sib_step          = wx.StaticText(self.panel_sib_base , -1, "step")
        self.choice_siblings_step    = wx.Choice(self.panel_sib_base,      -1, choices=['1','2','3','4','5'])
        
        self.label_sib_adopted       = wx.StaticText(self.panel_sib_base,  -1, "adopted")
        self.choice_siblings_adopted      = wx.Choice(self.panel_sib_base, -1, choices=['1','2','3','4','5'])
        
        self.label_childNo           = wx.StaticText(self.panel_sib_base , -1, "Child #")
        self.choice_birth_order      = wx.Choice(self.panel_sib_base ,     -1, choices=['1','2','3','4','5'])
        
        self.label_status            = wx.StaticText(self.panel_sib_base , -1, "Status")
        self.choice_status           = wx.Choice(self.panel_sib_base ,     -1, choices=['Natural', 'Adopted'])

        self.static_line_1 = wx.StaticLine(self.panel_sib_base, -1)
        self.static_line_2 = wx.StaticLine(self.panel_sib_base, -1)

        self.sizer_bio_static_staticbox   = wx.StaticBox(self.panel_bio,      -1, " ")
        self.sizer_siblings_staticbox = wx.StaticBox(self.panel_siblings, -1, "Siblings")

        self.choice_ctrls = [self.choice_pob,   self.choice_birth_order,
                            self.choice_faith,  self.choice_gender,
                            self.choice_residence,
                            self.choice_siblings_by_birth, self.choice_siblings_step,
                            self.choice_siblings_adopted, self.choice_status]
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        self.datectrl_dob.checkbox.Hide()
        self.text_ctrl_name.SetMinSize((200, -1))
        self.choice_siblings_by_birth.SetMinSize((50, -1))
        for txtctrl in self.text_ctrls:
            pass# txtctrl.SetEditable(False)
        self.Refresh()

    def __do_layout(self):
        grid_sizer_student     = wx.FlexGridSizer(1, 2, 5, 5)
        grid_sizer_student_bio = wx.FlexGridSizer(8, 2, 5, 5)
        
        self.sizer_siblings_staticbox.Lower()
        sizer_siblings_static  = wx.StaticBoxSizer(self.sizer_siblings_staticbox, wx.VERTICAL)
        sizer_student_siblings = wx.FlexGridSizer(6, 2, 2, 0)
         
        self.sizer_bio_static_staticbox.Lower()
        sizer_bio_static       = wx.StaticBoxSizer(self.sizer_bio_static_staticbox, wx.VERTICAL)
        
        grid_sizer_student_bio.Add(self.label_name,       0, 0, 0)
        grid_sizer_student_bio.Add(self.text_ctrl_name,   0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_dob,        0, 0, 0)
        grid_sizer_student_bio.Add(self.datectrl_dob,         0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_faith,      0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_faith,     0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_gender,     0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_gender,    0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.labelbirthplace,  0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_pob,       0, wx.EXPAND, 0)
        
        grid_sizer_student_bio.Add(self.label_residence,  0, 0, 0)
        grid_sizer_student_bio.Add(self.choice_residence, 0, wx.EXPAND, 0)
        
        self.panel_bio2.SetSizer(grid_sizer_student_bio)
        
        sizer_bio_static.Add(self.panel_bio2, 1, wx.EXPAND, 0)
        self.panel_bio.SetSizer(sizer_bio_static)
        
        sizer_student_siblings.Add(self.label_sib_birth,          0, 0, 0)
        sizer_student_siblings.Add(self.choice_siblings_by_birth, 0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_step,           0, 0, 0)
        sizer_student_siblings.Add(self.choice_siblings_step,     0, 0, 0)
        sizer_student_siblings.Add(self.label_sib_adopted,        0, 0, 0)
        sizer_student_siblings.Add(self.choice_siblings_adopted,  0, 0, 0)
        sizer_student_siblings.Add(self.static_line_1,      0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.static_line_2,      0, wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_student_siblings.Add(self.label_childNo,      0, 0, 0)
        sizer_student_siblings.Add(self.choice_birth_order, 0, 0, 0)
        sizer_student_siblings.Add(self.label_status,       0, 0, 0)
        sizer_student_siblings.Add(self.choice_status,      0, 0, 0)
        self.panel_sib_base .SetSizer(sizer_student_siblings)
        
        sizer_siblings_static.Add(self.panel_sib_base , 1, wx.EXPAND, 0)
        self.panel_siblings.SetSizer(sizer_siblings_static)
        
        grid_sizer_student.Add(self.panel_bio,           0, wx.EXPAND, 0)
        grid_sizer_student.Add(self.panel_siblings,      0, wx.EXPAND, 0)
        
        self.panel_top.SetSizer(grid_sizer_student)
        
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.panel_top)
        #sizer_main.Add(self.button_edit)
        self.SetSizer(sizer_main)
        
    def __do_main(self):
        loadCmb.gender(self.choice_gender)
        loadCmb.faiths(self.choice_faith)
   
    def NewData(self):
        self.choice_faith.SetSelection(min_level)
        
    def displayData(self, student_id):
        self.student_details = student_details = fetch.studentDetails_id(student_id)
        if not student_details:
               print 'not details found'
               return
        else:  print 'student_details : ', student_details
        
        name = student_details['name']
        self.text_ctrl_name.SetValue(name)
        
        dob  = student_details['dob']
        self.datectrl_dob.SetValue(dob)
   
        faith_id = student_details['faith_id']
        loadCmb.restore(self.choice_faith,   faith_id)
        
        pob = str(student_details['pob'])
        loadCmb.restore_str(self.choice_pob, pob)
        
        blood_group_id   = str(student_details['blood_type_id'])
        
        if student_details['gender']:
            self.choice_gender.SetSelection(1)
        else:
            self.choice_gender.SetSelection(2)
        
        self.setCmb(self.choice_siblings_by_birth, student_details['siblings_by_birth'])
        self.setCmb(self.choice_siblings_step,     student_details['siblings_step'])
        self.setCmb(self.choice_siblings_adopted,  student_details['siblings_adopted'])
        
        if student_details['child_no']:
              child_no = student_details['child_no']
        else: child_no = 1
        self.choice_birth_order.SetSelection(child_no-1)
        
    def enableCtrls(self):
        print 'panel_bio enableCtrls'
        for ctrl in self.text_ctrls:   ctrl.SetEditable(True)
        for ctrl in self.choice_ctrls: ctrl.Enable()
        self.datectrl_dob.Enable()
        
    def disableCtrls(self):
        print 'panel_bio disableCtrls'
        for ctrl in self.text_ctrls:   ctrl.SetEditable(False)
        for ctrl in self.choice_ctrls: ctrl.Enable(False)
        self.datectrl_dob.Enable(False)
        
    def clearCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetLabel('')
        for ctrl in self.choice_ctrls: ctrl.SetSelection(0)
        
        loadCmb.faiths(self.choice_faith)
        loadCmb.pob(self.choice_pob)
        self.disableCtrls()
        
    def setCmb(self, cmb, val):
        if val: cmb.SetSelection(val)
        
    def Save(self):
        print ' save bio '
        name     = self.text_ctrl_name.GetValue()
        dob      = self.datectrl_dob.GetDbReadyValue()
        pob      = fetch.cmbValue(self.choice_pob)
        faith_id = fetch.cmbID(self.choice_faith)
        gender   = (fetch.cmbID(self.choice_gender) == 1)
        
        siblings_by_birth = int(fetch.cmbValue(self.choice_siblings_by_birth))
        siblings_step     = int(fetch.cmbValue(self.choice_siblings_step))
        siblings_adopted  = int(fetch.cmbValue(self.choice_siblings_adopted))
        child_no          = int(fetch.cmbValue(self.choice_birth_order))
        
        sql = "UPDATE students \
                  SET name='%s', dob ='%s',  pob ='%s', faith_id =%d, gender=%d, \
                      siblings_by_birth =%d, siblings_step = %d,      siblings_adopted = %d, child_no =%d \
                WHERE id =%d" % (
                       name, dob, pob, faith_id, gender,
                       siblings_by_birth, siblings_step, siblings_adopted, child_no, gVar.student_id)
        print sql
        fetch.updateDB(sql)
        
        