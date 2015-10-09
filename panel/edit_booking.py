import wx, time

from ctrl.DateCtrl import DateCtrl
from datetime import datetime, date

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar


class panel_edit_booking(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_l = wx.Panel(self, -1)
        self.panel_r = wx.Panel(self, -1)
        
        self.panel_top     = wx.Panel(self.panel_l, -1)
        self.label_heading = wx.StaticText(self.panel_l, -1, " Book New Student or Edit Booking")
        self.panel_scroll  = wx.ScrolledWindow(self.panel_l, -1, style=wx.TAB_TRAVERSAL)
        
        #self.button_back   = wx.Button(    self.panel_top, -1, "< Back")
        #self.pcs1          = wx.StaticText(self.panel_top, -1, "")
        self.button_save   = wx.Button(self.panel_top, -1, "Save")
        self.button_edit   = wx.Button(    self.panel_top, -1, "Edit")
        
        self.panel_bio     = wx.Panel(self.panel_scroll, -1)
        
        self.label_student_name     = wx.StaticText(self.panel_bio, -1, "Name")
        self.text_ctrl_student_name = wx.TextCtrl(self.panel_bio, -1, "")
        
        self.label_gender           = wx.StaticText(self.panel_bio, -1, "Gender")
        self.choice_gender          = wx.Choice(self.panel_bio, -1, choices=["Male", "Female"])
        
        self.label_dob              = wx.StaticText(self.panel_bio, -1, "Date Of Birth")
        self.date_dob               = DateCtrl(self.panel_bio, -1)
        
        self.label_status         = wx.StaticText(self.panel_bio, -1, "registration_status")
        self.choice_status        = wx.Choice(self.panel_bio, -1, choices=["", "Accepted", "Rejected", "Booked: Awaiting Testing",
                                                                           "Primary Tested Passed",
                                                                           "Primary Tested Failed: Will Retest",
                                                                           "Primary Tested Failed: Won't Retest",
                                                                           "Retest Passed: ",
                                                                           "Retest Failed: ",
                                                                           "Offer Letter Sent",
                                                                           "Offer Accepted, Confirmation Fee Paid" ])
        
        self.label_booking_id     = wx.StaticText(self.panel_bio, -1, "Booking ID")
        self.label_ctrl_booking_id = wx.StaticText(self.panel_bio, -1, "")
        
        self.panel_booking         = wx.Panel(self.panel_scroll, -1)
        self.label_join_course     = wx.StaticText(self.panel_booking, -1, "Join Course")
        self.choice_joining_course = wx.Choice(self.panel_booking, -1, choices=[])
        self.spc1 = wx.StaticText(self.panel_booking, -1, "")
        self.spc2 = wx.StaticText(self.panel_booking, -1, "")
        self.label_booking_fee           = wx.StaticText(self.panel_booking, -1, "Booking Fee")
        self.date_booking_fee            = DateCtrl(self.panel_booking, -1)
        self.label_booking_receiptNo     = wx.StaticText(self.panel_booking, -1, "Receipt No.")
        self.text_ctrl_booking_receiptNo = wx.TextCtrl(self.panel_booking, -1, "")
        self.label_test                  = wx.StaticText(self.panel_booking, -1, "Test")
        self.date_test                   = DateCtrl(self.panel_booking, -1)
        self.label_test_result           = wx.StaticText(self.panel_booking, -1, "Result")
        self.choice_result_test          = wx.Choice(self.panel_booking, -1, choices=["", "A: Strong", "B: Good", "C: Medium", "D:Weak", "E:Very Weak"])
        self.label_retest                = wx.StaticText(self.panel_booking, -1, "Retest")
        self.date_retest                 = DateCtrl(self.panel_booking, -1)
        self.label_retest_result         = wx.StaticText(self.panel_booking, -1, "Result")
        self.choice_result_retest        = wx.Choice(self.panel_booking, -1, choices=["", "Acceptable", "Not Acceptable"])
        self.label_offer_letter          = wx.StaticText(self.panel_booking, -1, "Offer Letter")
        self.date_offer_letter_sent      = DateCtrl(self.panel_booking, -1)
        self.label_offer_ref             = wx.StaticText(self.panel_booking, -1, "Ref.")
        self.text_ctrl_offer_ref         = wx.TextCtrl(self.panel_booking, -1, "")
        self.label_offer_accepted        = wx.StaticText(self.panel_booking, -1, "Offer Accepted")
        self.date_offer_accepted         = DateCtrl(self.panel_booking, -1)
        self.label_receipt_accept        = wx.StaticText(self.panel_booking, -1, "Receipt No.")
        self.text_ctrl_accept_receiptNo  = wx.TextCtrl(self.panel_booking, -1, "")
        self.panel_notes                 = wx.Panel(self.panel_scroll, -1)
        self.label_notes                 = wx.StaticText(self.panel_notes, -1, "Notes:")
        self.text_ctrl_notes             = wx.TextCtrl(self.panel_notes, -1, "", style=wx.TE_MULTILINE)
        
        self.date_ctrls =[  self.date_dob,          
                            self.date_booking_fee,        
                            self.date_test,         
                            self.date_retest,          
                            self.date_offer_letter_sent,           
                            self.date_offer_accepted]
        
        
            
        self.text_ctrls = [ self.text_ctrl_student_name, 
                            self.text_ctrl_booking_receiptNo,
                            self.text_ctrl_offer_ref,        
                            self.text_ctrl_accept_receiptNo,  
                            self.text_ctrl_notes]
        
        self.text_ctrls_editable = [self.text_ctrl_student_name, 
                                    #self.text_ctrl_booking_receiptNo,
                                    #self.text_ctrl_offer_ref,        
                                    #self.text_ctrl_accept_receiptNo,  
                                    self.text_ctrl_notes]
            
        self.choice_ctlrs =[#self.choice_result_test, 
                            self.choice_status, 
                            self.choice_joining_course,
                            #self.choice_result_retest,      
                            self.choice_gender]
        
        self.choice_ctlrs2 =[self.choice_result_test, 
                            self.choice_status, 
                            self.choice_joining_course,
                            self.choice_result_retest,      
                            self.choice_gender]
        
        #self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)
        self.Bind(wx.EVT_BUTTON, self.OnEdit, self.button_edit)
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.button_save)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.label_ctrl_booking_id.SetMinSize((-1, 21))
        self.text_ctrl_student_name.SetMinSize((350, 21))
        
        self.label_booking_fee.SetMinSize((-1, -1))
        self.panel_scroll.SetScrollRate(10, 10)
        
        self.label_dob.SetMinSize(self.label_offer_accepted.GetSize())
        self.date_dob.text_ctrl_date.SetBackgroundColour('white')
        for c in self.choice_ctlrs2:
            c.Disable()
            
        for t in self.text_ctrls:
            t.SetEditable(False)

    def __do_layout(self):
        sizer_base  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_top   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main  = wx.BoxSizer(wx.VERTICAL)
        sizer_bio   = wx.BoxSizer(wx.VERTICAL)
        sizer_notes = wx.BoxSizer(wx.HORIZONTAL)
        
        grid_sizer_bio     = wx.FlexGridSizer(5, 2, 5, 5)
        grid_sizer_booking = wx.FlexGridSizer(6, 4, 5, 5)
        
        #sizer_top.Add(self.button_back,   0, 0, 0)
        #sizer_top.Add(self.pcs1, 1, 0, 0)
        sizer_top.Add(self.button_save,   0, 0, 0)
        sizer_top.Add(self.button_edit, 0, 0, 0)
        self.panel_top.SetSizer(sizer_top)

        
        grid_sizer_bio.Add(self.label_booking_id,     0, 0, 0)
        grid_sizer_bio.Add(self.label_ctrl_booking_id, 0, wx.EXPAND, 0)
        
        grid_sizer_bio.Add(self.label_student_name,     0, 0, 0)
        grid_sizer_bio.Add(self.text_ctrl_student_name, 0, wx.EXPAND, 0)
        
        grid_sizer_bio.Add(self.label_gender,  0, 0, 0)
        grid_sizer_bio.Add(self.choice_gender, 0, 0, 0)
        
        grid_sizer_bio.Add(self.label_dob, 0, 0, 0)
        grid_sizer_bio.Add(self.date_dob,  0, 0, 0)
        
        grid_sizer_bio.Add(self.label_status,  0, 0, 0)
        grid_sizer_bio.Add(self.choice_status, 0, 0, 0)
        
        
        #grid_sizer_bio.Add(self.label_previous_school,  0, 0, 0)
        #grid_sizer_bio.Add(self.choice_previous_school, 0, wx.EXPAND, 0)
        self.panel_bio.SetSizer(grid_sizer_bio)
       
        grid_sizer_booking.Add(self.label_join_course,     0, 0, 0)
        grid_sizer_booking.Add(self.choice_joining_course, 0, 0, 0)
        grid_sizer_booking.Add(self.spc1, 0, 0, 0)
        grid_sizer_booking.Add(self.spc2, 0, 0, 0)
        
        grid_sizer_booking.Add(self.label_booking_fee, 0, wx.TOP, 0)
        grid_sizer_booking.Add(self.date_booking_fee,  0, 0, 0)
        grid_sizer_booking.Add(self.label_booking_receiptNo,     0, 0, 0)
        grid_sizer_booking.Add(self.text_ctrl_booking_receiptNo, 0, 0, 0)
        
        grid_sizer_booking.Add(self.label_test, 0, 0, 0)
        grid_sizer_booking.Add(self.date_test,  0, 0, 0)
        grid_sizer_booking.Add(self.label_test_result,  0, 0, 0)
        grid_sizer_booking.Add(self.choice_result_test, 0, 0, 0)
        
        grid_sizer_booking.Add(self.label_retest, 0, 0, 0)
        grid_sizer_booking.Add(self.date_retest,  0, 0, 0)
        grid_sizer_booking.Add(self.label_retest_result,  0, 0, 0)
        grid_sizer_booking.Add(self.choice_result_retest, 0, 0, 0)
        
        grid_sizer_booking.Add(self.label_offer_letter,     0, 0, 0)
        grid_sizer_booking.Add(self.date_offer_letter_sent, 0, 0, 0)
        grid_sizer_booking.Add(self.label_offer_ref,     0, 0, 0)
        grid_sizer_booking.Add(self.text_ctrl_offer_ref, 0, 0, 0)
        
        grid_sizer_booking.Add(self.label_offer_accepted, 0, 0, 0)
        grid_sizer_booking.Add(self.date_offer_accepted,  0, 0, 0)
        grid_sizer_booking.Add(self.label_receipt_accept,       0, 0, 0)
        grid_sizer_booking.Add(self.text_ctrl_accept_receiptNo, 0, 0, 0)
        self.panel_booking.SetSizer(grid_sizer_booking)
        
        sizer_notes.Add(self.label_notes,     0, 0, 0)
        sizer_notes.Add(self.text_ctrl_notes, 1, wx.EXPAND, 0)
        self.panel_notes.SetSizer(sizer_notes)
        
        sizer_bio.Add(self.panel_bio,      0, wx.EXPAND, 0)
        sizer_bio.Add(self.panel_booking,  0, wx.TOP | wx.EXPAND, 5)
        sizer_bio.Add(self.panel_notes,    1, wx.TOP | wx.EXPAND, 5)
        self.panel_scroll.SetSizer(sizer_bio)
        
        sizer_main.Add(self.panel_top,     0, wx.EXPAND, 0)
        sizer_main.Add(self.label_heading, 0, wx.TOP | wx.BOTTOM, 10)
        sizer_main.Add(self.panel_scroll,  1, wx.EXPAND | wx.BOTTOM, 10)
        self.panel_l.SetSizer(sizer_main)
        sizer_main.Fit(self.panel_l)
        
        sizer_base.Add(self.panel_l, 1, wx.EXPAND | wx.LEFT, 15)
        sizer_base.Add(self.panel_r, 1 ,0, 0)
        self.SetSizer(sizer_base)
        
        self.Layout()

        
    def __do_main(self):
        loadCmb.gender(self.choice_gender)
        # self.choice_previous_school
        #loadCmb.retest_results(self.choice_result_retest)

    
    def displayData(self):
        self.student_id = student_id = gVar.student_id
        #return
        #rint"panel_edit_booking : displayData"
        self.clearCtrls()
        
        if student_id == 0:
            self.enableCtrls(True)
            self.button_edit.SetLabelText('Cancel')
            sql = "SELECT MAX (id) FROM students"
            student_id = fetch.getDig(sql)+1
            self.label_ctrl_booking_id.SetLabelText(str(student_id))
            
        else:
            self.button_save.Hide()
            self.button_edit.SetLabelText('Edit')
            self.enableCtrls(False)
            
        loadCmb.courses_forYear(self.choice_joining_course, gVar.schYr)

        self.text_ctrl_student_name.Enable(student_id == 0)
        if student_id:
            
            sql = "SELECT * FROM students WHERE student_id = %d" % int(student_id)
            res = fetch.getOneDict(sql)

            name                 = res['name']
            student_id           = res['student_id']
            gender               = res['gender']
            register_course_id   = res['register_course_id']
            registration_status  = res['reg_status']
            dob                  = res['dob']
            schYr                = res['register_schYr']
  
            self.label_heading.SetLabelText('Editing Booking For:')
            self.label_ctrl_booking_id.SetLabelText(str(student_id))
    
            self.text_ctrl_student_name.SetValue(name)

            if gender:
                self.choice_gender.SetSelection(0)
            else:
                self.choice_gender.SetSelection(1)
            
            self.date_dob.SetValue(dob)
            
            course_id = res['register_course_id']
            loadCmb.restore(self.choice_joining_course, course_id)
            
            #KSekolahPindah = res['KSekolahPindah']
            #loadCmb.restore(self.choice_previous_school, KSekolahPindah)

            #if not registration_status: registration_status = 0
            loadCmb.restore(self.choice_status, registration_status)
            
            sql = "SELECT * \
                     FROM acc_invoices i \
                     JOIN acc_invoice_items ii ON ii.invoice_id = i.id \
                    WHERE i.student_id = %d ORDER BY (ck_ref)" % gVar.student_id
            res = fetch.getAllDict(sql)

            mystr =""
            for r in res: 
                k = r.pop('student_id')
                
                ck_ref = r.pop('ck_ref')
                mystr += '%s : %s \n' % ('ck_ref', ck_ref)
                
                date = r.pop('Tanggal')
                mystr += '%s : %s \n' % ('Date', date)
                
                for key in r:
                    val = r[key]
                    if val: 
                        l = '%s : %s \n' % (key, r[key])
                        mystr += l
                mystr += "\n"    
   
            self.text_ctrl_notes.SetValue(mystr)
            """
            
            self.date_booking_fee            = DateCtrl(self.panel_booking, -1)
            
            self.text_ctrl_booking_receiptNo = wx.TextCtrl(self.panel_booking, -1, "")
            
            self.date_test                   = DateCtrl(self.panel_booking, -1)
            
            self.choice_result_test          = wx.Choice(self.panel_booking, -1, choices=["A: Strong", "B: Good", "C: Medium", "D:Weak", "E:Very Weak"])
            
            self.date_retest                 = DateCtrl(self.panel_booking, -1)
            
            self.choice_result_retest        = wx.Choice(self.panel_booking, -1, choices=["Acceptable", "Not Acceptable"])
            
            self.date_offer_letter_sent      = DateCtrl(self.panel_booking, -1)
            
            self.text_ctrl_offer_ref         = wx.TextCtrl(self.panel_booking, -1, "")
            
            self.date_offer_accepted         = DateCtrl(self.panel_booking, -1)
            
            self.text_ctrl_accept_receiptNo  = wx.TextCtrl(self.panel_booking, -1, "")
            
            self.text_ctrl_notes             = wx.TextCtrl(self.panel_notes, -1, "", style=wx.TE_MULTILINE)"""
            
        else:
            self.enableCtrls()
    
    def OnEdit(self, evt):
        if self.button_edit.GetLabelText()=='Cancel':
            #rint'Cancel'
            self.button_edit.SetLabelText('Edit')
            self.enableCtrls(False)
            self.button_save.Hide()
        else:
            self.enableCtrls()
            
            if gVar.student_id:
                self.date_dob.Disable()
                self.text_ctrl_student_name.SetEditable(False)
                self.choice_gender.Disable()
        
            self.button_edit.SetLabelText('Cancel')
            self.button_save.Show()
        self.Layout()

    def OnSave(self, evt):
        if gVar.student_id:
            sql, data = self.updateBooking()
        else:
            sql, data = self.insertNewStudent()
         
        if sql:
            #fetch.updateDB_data(sql,data)
            fetch.updateDB(sql)
            self.button_save.Hide()
            self.button_edit.SetLabelText('Edit')
            self.enableCtrls(False)    
            
    def insertNewStudent(self):
        name    = self.text_ctrl_student_name.GetValue()
        gender    = fetch.cmbID(self.choice_gender)
        register_course_id   = fetch.cmbID(self.choice_joining_course)
        registration_status  = self.choice_status.GetCurrentSelection()
        
        sql = "SELECT MAX (student_id) \
                 FROM students"
        student_id = fetch.getDig(sql)+1
        try:     dob = self.date_dob.caldate
        except:  dob = 0
            
        if name and register_course_id and registration_status and dob and gender <2:
            sql = "INSERT INTO students (student_id, name, dob, schYr, \
                                         registration_status, register_course_id, gender) \
                                 VALUES (%d, '%s', '%s', %d, %d, %d, %d)" % (
                                         student_id, name, dob,  gVar.schYr,
                                         registration_status, register_course_id, gender)
            return sql, []
        
            """
            sql = "INSERT INTO students (student_id, name, dob, schYr, registration_status, register_course_id, gender) \
                               VALUES (?, ?, ?, ?, ?, ?, ?)"
            return sql, (student_id, name, dob,  gVar.schYr, registration_status, register_course_id, gender)"""
            
        else:
            fetch.msg('Fields Name, Course, DOB, registration_status & Gender need to be filled')
            return 'fail', []
            
    def updateBooking(self):
        register_course_id  = fetch.cmbID(self.choice_joining_course)
        registration_status = self.choice_status.GetCurrentSelection()

        return "UPDATE students \
                   SET register_course_id, registration_status \
                VALUES (%d, %d) \
                 WHERE student_id =%d" , (
                       register_course_id, registration_status,
                       gVar.student_id)
   
    def clearCtrls(self):
        for c in self.text_ctrls:
            c.SetValue('')
            
        for c in self.choice_ctlrs:
            c.SetSelection(0)
        for c in self.date_ctrls:
            c.SetValue(0) 
            
        
    def enableCtrls(self, tf=True):
        for c in self.text_ctrls_editable:
            c.SetEditable(tf)
            
        for c in self.choice_ctlrs:
            if tf: c.Enable()
            else : c.Disable()
            
        self.date_dob
        if tf: self.date_dob.Enable()
        else : self.date_dob.Disable()
        #for c in self.date_ctrls:
        #    if tf: c.Enable()
        #    else : c.Disable()
    
    def OnBack(self, evt):
        self.GetTopLevelParent().goBack()

        
            