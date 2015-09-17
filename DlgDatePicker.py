import wx, datetime, time
import wx.calendar as cal

def create(parent, date):
    return DlgDatePicker(parent, date)

class DlgDatePicker(wx.Dialog):
    def __init__(self, parent, date):
        wx.Dialog.__init__(self, parent)
        self.SetClientSize(wx.Size(273, 221))
        
        self.date = date
        
        self.calendar_ctrl = wx.calendar.CalendarCtrl(self, -1,  style = cal.CAL_SHOW_HOLIDAYS)
        self.static_line_1 = wx.StaticLine(self, -1)
        self.button_1 = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL)


        self.__set_properties()
        self.__do_layout()

        self.calendar_ctrl.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalendarSelected, self.calendar_ctrl) 
       
        self.__do_main(date)

    def __set_properties(self):
        self.SetTitle("Date picker")

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.calendar_ctrl, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(self.static_line_1, 0, wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_1.Add(self.button_1,      0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        
    def __do_main(self, mydate):# works with python dates datetime.date.today (2012-06-19) = 19th June 2012
        self.calendardate = mydate
        try:    self.updateCalender(mydate)
        except: self.updateCalender(datetime.date.today())
    
    def OnCalendarSelected(self, evt):
        self.calendardate = self.calendar_ctrl.Date
        self.updateCalender(self.calendardate)  

    #def set_calender(self, mydate):
    #    #self.date = mydate
    #    self.updateCalender(mydate)
    
    def updateCalender(self, mydate):
        try:
            wxDate = self.db_to_wxDateTime(mydate)
            self.calendar_ctrl.Date = wxDate
        except:
            pass
        
    def db_to_wxDateTime(self, db_date): 
        day   = db_date.day 
        month = db_date.month-1 
        year  = db_date.year 
        return wx.DateTimeFromDMY(day=day, month=month, year=year) 
 
    def PySetDate(self, date): 
        """takes datetime.datetime or datetime.date object""" 
        try:
            #rint isinstance(date, (datetime.datetime, datetime.date))
            tt = date.timetuple() 
            dmy = (tt[2], tt[1]-1, tt[0]) 
            self.calendar_ctrl.SetDate(wx.DateTimeFromDMY(*dmy)) 
        except:
            #rint 'not a datetime object ; lets try to make it so'
            try:
                # date = datetime.date("2012-06-06") no good
                # date = datetime.date("2012/06/06") no good
                date = datetime.date()
                #rint date
                try:
                    tt = date.timetuple() 
                    dmy = (tt[2], tt[1]-1, tt[0])
                    #rint dmy
                    self.calendar_ctrl.SetDate(wx.DateTimeFromDMY(*dmy))
                except:
                    pass
                    #rint "DlgDatePricker > well that did not work either"
            except:
                pass
                #rint "DlgDatePricker > thats not good"

    def PyGetDate(self, style='dmy'): 
        """returns datetime.date object""" 
        dt = self.calendar_ctrl.GetDate() 
        year = dt.GetYear() 
        mo   = dt.GetMonth() + 1 
        day  = dt.GetDay() 
        if style =='ymd':
            ymd = (year, mo, day)
        elif style == 'mdy':
            ymd = (mo, day, year)
        else:
            ymd = (day, mo, year)
        
            
        return datetime.date(*ymd)

if __name__ == '__main__':
    app = wx.App(redirect=False)
    
    # all we have to do is send datetime the day (d) month(m) and year(Y)
    from datetime import datetime
    date = datetime.date.today()
    date_object = datetime.strptime('6 7 1999', '%d %m %Y').date()
    
    dlg = create(None, date_object)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
