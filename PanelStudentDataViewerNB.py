import wx, datetime, gVar, loadCmb, fetch

import DlgSelectContact

from PanelSsOwnData     import PanelSsOwnData
from PanelDetailsEditor import PanelStudentEditor

from panel_guardian_data  import panel_guardian_data

import DlgSelectContact

class PanelStudentDataViewerNB(wx.Panel):
    def __init__(self, *args, **kwds):
        
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.scrolled_window  = wx.ScrolledWindow(self, -1)
        
        self.panel_student     = wx.Panel(self.scrolled_window, -1)
        self.panel_studentView = PanelSsOwnData(self.panel_student, -1)
        self.panel_studentEdit = PanelStudentEditor(self.panel_student, -1)
        self.button_edit       = wx.Button(self.panel_student, -1, "Edit")
        
        self.button_add_guardian = wx.Button(self, -1, "Add Guardian")
    
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnEdit,  self.button_edit)
        self.Bind(wx.EVT_BUTTON, self.OnAddGuardian,  self.button_add_guardian)
        self.pane_g =[]
        self.__do_main()
        
    def OnEdit(self, evt):
        if self.button_edit.GetLabel()=="Edit":
            self.panel_studentView.Hide()
            self.panel_studentEdit.Show()
            self.button_edit.SetLabel("Save")
        else:
            self.panel_studentView.Show()
            self.panel_studentEdit.Hide()
            self.button_edit.SetLabel("Edit")
            
        self.Layout()

    def __set_properties(self):
        self.scrolled_window.SetScrollRate(10, 10)
        

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_student = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_scroll = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add(self.scrolled_window, 1, wx.EXPAND, 0)
        sizer_main.Add(self.button_add_guardian,0,0,0)
        
        sizer_student.Add(self.panel_studentView, 1, 0, 0)
        sizer_student.Add(self.panel_studentEdit, 1, 0, 0)
        sizer_student.Add(self.button_edit,       0, 0, 0)
        self.panel_student.SetSizer(sizer_student)
        
        self.sizer_scroll.Add(self.panel_student, 0, wx.EXPAND, 0)

        self.scrolled_window.SetSizer(self.sizer_scroll)
        
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        self.student_id = 0
        self.student_details = ''
        self.panel_studentEdit.Hide()
        
    def clearCtrls(self):
        return
        self.panel_father.clearCtrls()
        self.panel_guardian.clearCtrls()
        self.panel_mother.clearCtrls()
        #self.panel_student.clearCtrls()
              
    def displayData(self, student_id):
        #rint'displayData:',student_id
        if not student_id:  self.clearCtrls()
        
        self.panel_studentView.displayData(student_id)
        
        sql = "SELECT KOrangTua, KWali \
                 FROM Siswa \
                WHERE CKID = %d" % int(student_id)
        details = fetch.getOneDict(sql)
        #rintsql, details
        if not details: return
        KOrangTua = details['KOrangTua']
        KWali     = details['KWali']
        
        if KOrangTua:
            sql = "SELECT * FROM OrangTua \
                WHERE Kode = %d" % int(KOrangTua)
            details = fetch.getOneDict(sql)

            if details['NamaA']:
                ##rintdetails['NamaA']
                p=self.OnAddGuardian(wx.Event)
                p.head('FATHER')
                #p.labelHead.SetBackgroundColour((255, 200, 255))
                p.displayData(student_id, KOrangTua, 'father')
                
            if details['NamaI']:
                ##rintdetails['NamaI']
                p=self.OnAddGuardian(wx.Event)
                p.head('MOTHER')
                #p.labelHead.SetBackgroundColour((255, 255, 200))
                p.displayData(student_id, KOrangTua, 'mother')
                
        if KWali:
            sql = "SELECT * FROM Wali \
                WHERE Kode = %d" % int(KWali)
            details = fetch.getOneDict(sql)
            ##rintsql, details
            p = self.OnAddGuardian(wx.Event)
            p.head('GUARDIAN')
            #p.labelHead.SetBackgroundColour((200, 255, 255))
            p.displayData(student_id, KWali, 'guardian')
            
    def saveDetails(self):
        #self.panel_student.saveData()
        for p in self.pane_g:
            p.saveData()
        
    def OnStudent(self,  evt):
        self.HighlightBtn(0)
        
    def OnAddGuardian(self, evt):
        dlg = wx.SingleChoiceDialog(
                self, 'Test Single Choice', 'The Caption',
                ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'], 
                wx.CHOICEDLG_STYLE
                )
        dlg = DlgSelectContact.create(None)
        if dlg.ShowModal() == wx.ID_OK:
            pass
            #rint'You selected: %s\n' % dlg.GetStringSelection()

        dlg.Destroy()
        
        x = PanelGuardianData(self.scrolled_window, -1)
        self.pane_g.append(x)
        self.sizer_scroll.Add(x, 1, wx.EXPAND, 0)
        self.Layout()
        ##rint"OnAddGuardian"#self.HighlightBtn(1)
        return x
    
    def HighlightBtn(self, idxBtn):
        self.current_panel_idx = idxBtn
        for x in range(len(self.selected_button)):
            btn = self.selected_button[x]
            btn.Freeze()
            
            if x == idxBtn:
                btn.SetBackgroundColour(gVar.barkleys)
                btn.SetForegroundColour(gVar.darkGrey)
                self.view_panels[x].Show()
            
            else:
                btn.SetBackgroundColour(gVar.darkGrey)
                btn.SetForegroundColour(gVar.mediumGrey)
                self.view_panels[x].Hide()
                
            btn.Thaw()
             
        self.Layout()