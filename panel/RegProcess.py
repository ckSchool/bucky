import wx, datetime


import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

from ctrl.DateCtrl import DateCtrl

class PanelRegProcess(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PanelRegProcess.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.label_blank = wx.StaticText(self, -1, "")
        self.label_date_format = wx.StaticText(self, -1, "dd mm yyyy", size=(120,21))
        self.label_notes = wx.StaticText(self, -1, "Notes")
        
        self.label_booking = wx.StaticText(self, -1, "Booking fee paid", size=(-1,21))
        #self.datectrl_Booking_Fee = wx.DatePickerCtrl(self, -1,  style=wx.DP_DROPDOWN | wx.DP_ALLOWNONE, size=(40,25))
        self.datectrl_Booking_Fee = DateCtrl(self, -1)
        
        self.text_ctrl_booking = wx.TextCtrl(self, -1, "", size=(-1,21))
        
        self.label_assesment_fee = wx.StaticText(self, -1, "Fee & observation date", size=(-1,21))
        #self.datectrl_Observation = wx.DatePickerCtrl(self, -1,  style=wx.DP_DROPDOWN | wx.DP_ALLOWNONE, size=(40,25))
        self.datectrl_Observation = DateCtrl(self, -1)
        
        self.text_ctrl_observation_note = wx.TextCtrl(self, -1, "")
        
        self.label_offer_letter = wx.StaticText(self, -1, "Offer letter sent", size=(-1,21))
        self.datectrl_Offer_Letter = DateCtrl(self, -1)
        self.datectrl_Offer_Letter.SetSize((40,25))
        
        self.label_8 = wx.StaticText(self, -1, "")
        
        self.label_admission_fee = wx.StaticText(self, -1, "Admission fee paid", size=(-1,21))
        #self.datectrl_Admission_Fee = wx.DatePickerCtrl(self, -1, style=wx.DP_DROPDOWN | wx.DP_ALLOWNONE, size=(40,25))
        self.datectrl_Admission_Fee = DateCtrl(self, -1)
        
        self.text_ctrl_admission = wx.TextCtrl(self, -1, "", size=(-1,21))
        
        self.Layout()

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        self.__do_main()
        

    def __set_properties(self):
        pass

    def __do_layout(self):
        grid_sizer_main = wx.FlexGridSizer(5, 3, 0, 0)
        
        grid_sizer_main.Add(self.label_blank, 0, 0, 0)
        grid_sizer_main.Add(self.label_date_format, 0, 0, 0)
        grid_sizer_main.Add(self.label_notes, 0, 0, 0)
        
        grid_sizer_main.Add(self.label_booking, 0, 0, 0)
        grid_sizer_main.Add(self.datectrl_Booking_Fee, 0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_booking, 0, wx.EXPAND, 0)
        
        grid_sizer_main.Add(self.label_assesment_fee, 0, 0, 0)
        grid_sizer_main.Add(self.datectrl_Observation, 0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_observation_note, 0, wx.EXPAND, 0)
        
        grid_sizer_main.Add(self.label_offer_letter, 0, 0, 0)
        grid_sizer_main.Add(self.datectrl_Offer_Letter, 0, 0, 0)
        grid_sizer_main.Add(self.label_8, 0, 0, 0)
        
        grid_sizer_main.Add(self.label_admission_fee, 0, 0, 0)
        grid_sizer_main.Add(self.datectrl_Admission_Fee, 0, 0, 0)
        grid_sizer_main.Add(self.text_ctrl_admission, 0, wx.EXPAND, 0)
        
        self.SetSizer(grid_sizer_main)
        
        self.gsm = grid_sizer_main
        grid_sizer_main.Fit(self)
        grid_sizer_main.AddGrowableCol(2)
        # end wxGlade
        
    def __do_main(self):
        self.clear_ctrls() 

    def clear_ctrls(self):
        ###rint'PanelRegProcess clear_ctrls'
        ctrl_list =  [self.datectrl_Admission_Fee, self.datectrl_Offer_Letter,
                      self.datectrl_Booking_Fee, self.datectrl_Observation]
        for ctrl in ctrl_list:
            invalidDate = wx.DateTime()
            # ##rintstr(invalidDate)
            ctrl.SetValue(invalidDate)
            
        self.text_ctrl_booking.SetValue('')
        self.text_ctrl_observation_note.SetValue('')
        self.text_ctrl_admission.SetValue('')
    
    def db_to_wxDateTime(self, d):
        try:
            x = fetch.convert_fromDBdate(d)
            # ##rintx
            return x
        except:
            return None

        ###rintd
        '''try:
            day=d.day 
            month=d.month-1 
            year=d.year 
            c = wx.DateTimeFromDMY(day=day, month=month, year=year)
            ##rintc
            return c
        except:
            pass'''
        
    def setTxtCrl(self,TxtCrl,dt):
        if dt:  TxtCrl.SetValue(dt)
        
    def displayData(self, student_id):
        self.clear_ctrls()
        if not student_id:  return
        student_details = fetch.registation_details(student_id)
        ###rintstudent_details
        # booking
        self.setTxtCrl(self.datectrl_Booking_Fee, student_details['booking_date'])
        # observation  / assesment
        self.setTxtCrl(self.datectrl_Observation, student_details['observation_date'])
        # offer 
        self.setTxtCrl(self.datectrl_Offer_Letter, student_details['offering_letter_date'])
        # admission
        self.setTxtCrl(self.datectrl_Admission_Fee, student_details['admission_fee_date'])

        #self.Layout()   
            
        self.text_ctrl_booking.SetValue(str(student_details['booking_fee']))               
        self.text_ctrl_observation_note.SetValue(str(student_details['observation_note']) )         
        self.text_ctrl_admission.SetValue(str(student_details['admission_fee']))
        
        ad = str(student_details['admission_date'])

    
    def OnMoreNotes(self, evt):
        pass
        
    def wxDateTime_to_db(self, my_date):
        isodate = my_date.FormatISODate() 
        return isodate
    
    def save(self, student_id):
        try: booking_date = self.datectrl_Booking_Fee.GetDbReadyValue()
        except: booking_date = 'Null'
                 
        try: observation_date = self.datectrl_Observation.GetDbReadyValue()
        except: observation_date = 'Null'
        
        try: offering_letter_date = self.datectrl_Offer_Letter.GetDbReadyValue()
        except: offering_letter_date = 'Null'
            
        try: admission_fee_date = self.datectrl_Admission_Fee.GetDbReadyValue()
        except: admission_fee_date = 'Null'
              
        try: admission_fee = int(self.text_ctrl_admission.GetValue())
        except: admission_fee = 0
        
        try:booking_fee = int(self.text_ctrl_booking.GetValue())
        except: booking_fee = 0
        
        observation_note = self.text_ctrl_observation_note.GetValue()
       
        ###rintbooking_date, observation_date, offering_letter_date, admission_fee_date
        a = " booking_date = '%s'"         % booking_date        
        b = " observation_date = '%s'"     % observation_date
        c = " offering_letter_date = '%s'" % offering_letter_date
        d = " admission_fee_date = '%s'"   % admission_fee_date
        e = " admission_fee = %d"          % int(admission_fee)
        f = " booking_fee = %d"            % int(booking_fee)
        g = " observation_note = '%s'"     % observation_note
        ###rint ' a,b,c,d, student_id', a,b,c,d, student_id
        sql = "UPDATE students SET \
                      %s, %s, %s,%s, %s, %s, %s \
                WHERE id = %d" % (
                      a,b,c,d,e,f,g,
                      student_id)
        ###rintsql
        fetch.updateDB(sql)