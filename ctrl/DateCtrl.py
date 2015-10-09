import wx, time, datetime, base64

from dialog.DatePicker import DlgDatePicker

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
 
 
from wx.lib.embeddedimage import PyEmbeddedImage

class dateconverter():
    pass
    # date = wx.DateTime() 
    # date.ParseDate(myDate[0])
        
class DateCtrl(wx.Panel):
    def __init__(self, *args, **kwds ):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.checkbox        = wx.CheckBox(self, -1, "")
        self.ctrl_panel      = wx.Panel(self,-1)
        self.text_ctrl_date  = wx.TextCtrl(self.ctrl_panel, -1, "",
                                           style=wx.TE_READONLY | wx.TE_CENTRE)

        calendar_green = PyEmbeddedImage("R0lGODlhEgAQALMAAKy5lLfFoM3cuMXTrghTKW16Tp2rgHiFWQtqOKOzhYGPYpWld4qaawBJJABJJABJJCwAAAAAEgAQAAAEb7DJSWslOKPN+cxa11kkWZxHqihM67bSiR4r+8JNkdL24v8+ycKgSAAYgYBhMEgIBE4h0YhUMp1QgUTVGxoS4LBwofhWF9ertuErJxiAAHqwbK5nKxfQK1kVWgdDRUcAhFsHBX4MCwcGRF9FJZISEQA7")
        bmp = calendar_green.GetBitmap()
        mask = wx.Mask(bmp, wx.BLUE)

        self.bitmap_button_1 = wx.BitmapButton(self.ctrl_panel, -1,
                                               bmp, style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.checkbox)
        self.Bind(wx.EVT_BUTTON,   self.OnCalender, self.bitmap_button_1)

    def __set_properties(self):
        self.checkbox.SetMinSize((21, 21))
        self.checkbox.SetValue(1)
        self.text_ctrl_date.SetMinSize((120, 21))
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        self.lowerlimit = 0
        self.upperlimit = 0

    def __do_layout(self):
        sizer_date = wx.BoxSizer(wx.HORIZONTAL)
        sizer_date.Add(self.ctrl_panel, 0, 0, 0)
        sizer_date.Add(self.checkbox, 0, wx.ALIGN_RIGHT | wx.LEFT, 10)
        
        sizer_ctrls = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ctrls.Add(self.text_ctrl_date,  1, wx.EXPAND, 0)
        sizer_ctrls.Add(self.bitmap_button_1, 0, wx.LEFT, 3)
        
        self.ctrl_panel.SetSizer(sizer_ctrls)
        
        self.SetSizer(sizer_date)
        sizer_date.Fit(self)
        self.Layout()
        
        self.date = wx.DateTime()
        
    def setDate(self, date):
        #rintdate
        date = wx.DateTime()
        
    def SetValue(self, date):
        try:
            if date == 'None':
                self.date = wx.DateTime()
                return
        except:
            pass
        #rint'SetValue date:', date
        # expects a simple date object like "21 02 2012"
        #rint "DateCtrl.SetValue expects a simple date object like '21 02 2012' . Passed date =", date
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            pass
        self.date_changed = False
        self.date = date 
        
        try:
            formated_date = self.formatDateForDisplay(date)
            self.text_ctrl_date.SetValue(formated_date)
            self.checkbox.SetValue(True)
            self.ctrl_panel.Show()
            
        except:
            self.text_ctrl_date.SetValue('')
            self.checkbox.SetValue(False)
            self.ctrl_panel.Show()
            
    def formatDateForDisplay(self, date):
        try:    txt = date.strftime("%d") + ' ' + date.strftime("%B") + ' ' + date.strftime("%Y")
        except: txt = date
        return  txt

    def OnCheckBox(self, event):  # wxGlade: DateCtrl.<event_handler>
        if    self.checkbox.Value: self.showCtrls()
        else: self.hideCtrls()
        self.date_changed = True
	
        name = self.GetName()
	#rint'DateCtrl name = ', name
	if name and name != 'panel': pub.sendMessage('DateCtrl.date_change', name=name)
	else:
	    pub.sendMessage('DateCtrl.date_change')
     
    def setDateToday(self): 
        self.date = datetime.datetime.today()
        self.text_ctrl_date.SetValue(self.formatDateForDisplay(self.date))
        
    def showCtrls(self):
        self.text_ctrl_date.Clear()
        
        self.ctrl_panel.Show()
        if self.date:
            #rint'VALID self.date:', self.date 
            self.text_ctrl_date.SetValue(self.formatDateForDisplay(self.date))
            
        else:
            #rint'INVALID self.date:', self.date , "Set to todays date"
            self.date = datetime.datetime.today()
            #rint ' after checkbox', self.date
            # do we need to convert
            # self.date = self.convert_calDate_to_datetimeDate(newdate)
            self.text_ctrl_date.SetValue(self.formatDateForDisplay(self.date))

    def hideCtrls(self):
        self.text_ctrl_date.Clear()
        self.ctrl_panel.Hide()
        
    def hideCheckbox(self):
        self.checkbox.Hide()
        
    def db_to_wxDateTime(self, db_date): 
        day   = db_date.day 
        month = db_date.month-1 
        year  = db_date.year 
        return wx.DateTimeFromDMY(day=day, month=month, year=year) 
        
    def setDateRange(self, lower=0, upper=0):
        if lower:
            self.lowerlimit = self.db_to_wxDateTime(lower)
        if upper:
            self.upperlimit = self.db_to_wxDateTime(upper)
        
        #rint'date range', lower, ' > ', upper
        	
    def OnCalender(self, event):
        #rint'OnCalender'
        #rint'limit:', self.lowerlimit, " > ", self.upperlimit
        newdate = False
        #rint'self.date:',self.date
        dlg = DlgDatePicker(None, self.date)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dlgdate = dlg.calendardate
                
                if self.lowerlimit:
                    #rintdlgdate
                    if dlgdate < self.lowerlimit:
                        dlg.Destroy()
                        return 
                if self.upperlimit:
                    if dlgdate > self.upperlimit:
                        dlg.Destroy()
                        return
                
                self.caldate = dlgdate
                #rint'self.caldate = ', self.caldate
                newdate = self.convert_calDate_to_datetimeDate(self.caldate)
                try:
                    if self.date!= newdate:
                        
                        ##rint'newdate:',newdate
                        self.date = newdate # self.convert_calDate_to_datetimeDate(newdate)
                        
                        ##rint'converted_calendar Date_to datetimeDate    self.date:',self.date
                        
                        self.text_ctrl_date.SetValue(self.formatDateForDisplay(self.date))
                        self.checkbox.SetValue(True)
                        self.date_changed = True
                except:
                    #rint'help'
                    self.date = newdate
                    self.text_ctrl_date.SetValue(self.formatDateForDisplay(self.date))
                    self.checkbox.SetValue(True)
                    self.date_changed = True
		    
		name = self.GetName()
		#rint'DateCtrl name = ', name
		if name and name != 'panel': pub.sendMessage('DateCtrl.date_change', name=name)
		else:
		    pub.sendMessage('DateCtrl.date_change')
        finally:   
            dlg.Destroy()
            
        event.Skip()
            
    def GetDbReadyValue(self):
	if self.checkbox.Value:
	    if type(self.date) is datetime.date:
		return self.date
	return '0000-00-00'
    

    def GetDatetimeDateValue(self):
        if self.checkbox.Value:
            return self.date
        else:
            return None
        
    def convert_calDate_to_datetimeDate(self, date):
        convertedDate = date
        try:
            yr = date.Year
            mn = date.Month
            dy = date.Day
            convertedDate = datetime.date(yr, mn+1, dy)
        finally:    
            #rint ' convertedDate', convertedDate
            return convertedDate
        
    def get_calendar_date(self):
        try:
            return self.caldate.FormatDate()
        except:
            #rint'no caldate yet'
            return ''
