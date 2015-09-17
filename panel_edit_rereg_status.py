import  wx, gVar, loadCmb, fetch

class panel_edit_rereg_status(wx.Panel):
    def __init__(self, parent, pid):
        wx.Panel.__init__(self, parent, pid)
        self.parent = parent
        
        self.button_back     = wx.Button(self, -1, "< Back < ReregStatus")
        
        self.panel_details   = wx.Panel(self, -1)
         
        self.label_name      = wx.StaticText(self.panel_details, -1, 'Name')
        self.text_ctrl_name  = wx.TextCtrl(self.panel_details, -1)
        
        self.label_status    = wx.StaticText(self.panel_details, -1, 'Status')
        self.choice_status   = wx.Choice(self.panel_details, -1, choices=['?', 'continue', 'retake', 'exit',])
        
        self.label_refNo     = wx.StaticText(self.panel_details, -1, 'Rereg receipt No.\nNo.Surat Pindah')
        self.text_ctrl_refNo = wx.TextCtrl(self.panel_details, -1)
        
        self.label_course    = wx.StaticText(self.panel_details, -1, 'Next Course')
        self.choice_course   = wx.Choice(self.panel_details, -1, choices=[])
        
        self.button_save     = wx.Button(self, -1, "Save")
        
        self.text_ctrl_name.SetEditable(False)
        self.text_ctrl_name.SetMinSize(( 200, 23))
        self.choice_course.SetMinSize((  200, -1))
        self.choice_status.SetMinSize((  200, -1))
        self.text_ctrl_refNo.SetMinSize((200, -1))
        
        self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)
        
        self.Bind(wx.EVT_CHOICE, self.OnChoiceStatusChange, self.choice_status )
        
        self.__do_layout()
        
    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        
        sizer_details = wx.BoxSizer(wx.VERTICAL)
        
        sizer_details.Add(self.label_name,      0, 0, 0)
        sizer_details.Add(self.text_ctrl_name,  0, 0, 0)
        
        sizer_details.Add(self.label_status,    0, 0, 0)
        sizer_details.Add(self.choice_status,   0, 0, 0)
        
        sizer_details.Add(self.label_course,    0, 0, 0)
        sizer_details.Add(self.choice_course,   0, 0, 0)
        
        sizer_details.Add(self.label_refNo,     0, 0, 0)
        sizer_details.Add(self.text_ctrl_refNo, 0, 0, 0)
        
        self.panel_details.SetSizer(sizer_details)
        
        sizer_base.Add(self.button_back,   0,0,0)
        sizer_base.Add(self.panel_details, 1, wx.EXPAND | wx.ALL, 10)
        sizer_base.Add(self.button_save,   0,0,0)
        self.SetSizer(sizer_base)
        self.Layout()
        
    def displayData(self, student_id, NoInduk, KKelas):
        print "panel_edit_rereg_status : displayData"
        # query for bookings
        #sql = "SELECT Kode, Nama, Status FROM CSiswa WHERE Kode%d" % student_id
        loadCmb.courses_forYear(self.choice_course, gVar.schYr+1)
        self.KKelas  = KKelas
        self.NoInduk = NoInduk
        # query for rereg
        sql = "SELECT s.id, s.NoInduk, s.name, sbf.rereg_status, sbf.next_course_id \
                 FROM students_by_form \
                 JOIN students ON sbf.student_id = Siswa.id \
                WHERE sbf.student_id = '%s' \
                  AND f.id = %d" % (student_id, form_id)
        res = fetch.getOneDict(sql)
        
        self.next_level = fetch.form_level(KKelas)+1
        
        print sql, res
        if res:
            name = res['Nama']
            self.text_ctrl_name.SetValue(name)
            
            rereg_status = res['ReregStatus']
            course_id    = res['NextCourseID']
            
            if rereg_status =='?':
                self.choice_status.Select(0) # ?
                        
            elif rereg_status == "continue":
                print  "continue"
                loadCmb.courses_forLevel_forYear(self.choice_course, gVar.schYr+1, self.next_level)
                loadCmb.restore(self.choice_course, course_id)
                    
            elif rereg_status == "retake":
                    self.choice_status.Select(2)    
            
            elif rereg_status == "exit":
                    self.choice_status.Select(3)
                    
            self.showHideCourses(rereg_status =='continue' or rereg_status =='retake')

            self.text_ctrl_refNo.SetValue('')
            self.Layout()
        
    def showHideCourses(self, show):
        if show:
            self.choice_course.Show()
            self.label_course.Show()
        else:
            self.choice_course.Hide()
            self.label_course.Hide()
        
    def OnChoiceStatusChange(self, evt):
        rereg_status = fetch.cmbValue(self.choice_status)
        self.showHideCourses(rereg_status =='continue')# or rereg_status =='retake')

        loadCmb
        rereg_status = fetch.cmbValue(self.choice_status)
        if rereg_status =='continue':
            print "gVar.schYr+1, self.next_level", gVar.schYr+1, self.next_level
            loadCmb.courses_forLevel_forYear(self.choice_course, gVar.schYr+1, self.next_level)
            
        if rereg_status =='retake':
            # load choices - same level courses
            pass
        
        self.Layout()    

    def OnBack(self, evt):
        gVar.previousPanel = gVar.lastPanel
        gVar.lastPanel=self
        self.Hide()
        self.GetTopLevelParent().OnBack()
        return
        #self.GetTopLevelParent().OnBackFrom_report_studentsOfClass_editBooking(self)
        
    def OnSave(self, evt):
        status = fetch.cmbValue(self.choice_status)
        refNo  = self.text_ctrl_refNo.GetValue()
        course_id = fetch.cmbID(self.choice_course)
        
        if status == "?": 
            ReregStatus = "?"
            
        elif status =="exit":
            ReregStatus = "exit,%s" % (refNo, )
            
        else:
            ReregStatus = "%s, %d, %s" % (status, course_id, refNo)
        
        
        sql = "UPDATE SiswaPerKelas SET ReregStatus = '%s' WHERE KKelas =%d AND NoInduk ='%s' " % (ReregStatus, self.KKelas, self.NoInduk)
        print sql
        fetch.updateDB(sql)
"""  
class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Student For Course, Booking Status", size=(640,480))

        p = panel_edit_rereg_status(self, -1)
        
        
        bs = wx.BoxSizer(wx.VERTICAL)
        bs.Add(p, 1, wx.EXPAND, 0)
        self.SetSizer(bs)
        self.Layout()
        
        student_id, NoInduk, KKelas = (0, 'D0676', 10)
        p.displayData(student_id, NoInduk, KKelas)
        
               

    




#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App()
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()


#---------------------------------------------------------------------------
"""