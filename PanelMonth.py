import  wx, gVar, datetime, calendar

from wx.lib.pubsub import pub

class PanelMonth(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.statusbar         = self.GetTopLevelParent().statusbar
	
        self.button_last_month = wx.Button(self,   -1, "<", style=wx.NO_BORDER)
        self.text_ctrl_month   = wx.TextCtrl(self, -1, "",  style=wx.BORDER_NONE | wx.TE_CENTER)
        self.button_next_month = wx.Button(self,   -1, ">", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnLastMonth, self.button_last_month)
        self.Bind(wx.EVT_BUTTON, self.OnNextMonth, self.button_next_month)
	
        self.__do_main()
	
    def __set_properties(self):
        self.button_last_month.SetMinSize((21, -1))
        self.button_last_month.SetBackgroundColour(gVar.darkGrey)
        self.button_last_month.SetForegroundColour(wx.WHITE)
        self.button_last_month.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.text_ctrl_month.SetMinSize((80, 16))
	self.text_ctrl_month.SetBackgroundColour(gVar.darkGrey)
        self.text_ctrl_month.SetForegroundColour(wx.WHITE)
        self.text_ctrl_month.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.button_next_month.SetMinSize((21, -1))
        self.button_next_month.SetBackgroundColour(gVar.darkGrey)
        self.button_next_month.SetForegroundColour(wx.WHITE)
        self.button_next_month.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_main.Add(self.button_last_month, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 2)
        sizer_main.Add(self.text_ctrl_month,   0, wx.ALIGN_CENTER_VERTICAL , 0)
        sizer_main.Add(self.button_next_month, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 2)
        
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)

    def __do_main(self):
	self.schYr             = gVar.schYr
        self.schMonthNumber    = 1
        self.dayNames          ={0:'M',1:'T',2:'W',3:'T',4:'F',5:'s',6:'s'}
        self.month_sch_to_real ={1:7, 2:8, 3:9, 4:10, 5:11, 6:12, 7:1, 8:2, 9:3, 10:4, 11:5, 12:6} 
        self.schoolMonths_dict ={1:'July',      2:'August',   3:'September', 4:'October',
                                 5:'November',  6:'December', 7:'January',   8:'Feburary',
                                 9:'March',    10:'April',   11:'May',      12:'June'}
        self.daysInMonth    = calendar.monthrange(self.schYr, self.schMonthNumber)[1]
        self.text_ctrl_month.Value = self.schoolMonths_dict[self.schMonthNumber]
	
    def OnLastMonth(self, event):
        if self.schMonthNumber > 1: self.changeMonth(-1)

    def OnNextMonth(self, event):
        if self.schMonthNumber < 12: self.changeMonth(+1)
              
    def changeMonth(self, x):
        self.schMonthNumber += x
        m = self.schMonthNumber
	gVar.monthNo = m
        realMonth = self.schoolMonths_dict[self.schMonthNumber]
        self.text_ctrl_month.SetValue(realMonth)
        pub.sendMessage('change.month')
	
	
	
	
	
	
	
	
	
	
	
	
	
# --------------  PanelSemester  ------------------
	
class PanelSemester(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        #self.statusbar         = self.GetTopLevelParent().statusbar
	
	#self.label_semester   = wx.StaticText(self, -1, "Semester:")
        self.button_semester1 = wx.Button(self, -1, "Semester 1", style=wx.NO_BORDER)
        self.button_semester2 = wx.Button(self, -1, "Semester 2", style=wx.NO_BORDER)
	
	self.button_semester1.Bind(wx.EVT_BUTTON, self.OnSemester)
        self.button_semester2.Bind(wx.EVT_BUTTON, self.OnSemester)
	
        self.__set_properties()
        self.__do_layout()
	self.__do_main()

    def __set_properties(self):
	self.button_semester1.SetSize((120,21))
	self.button_semester2.SetSize((120,21))
	self.button_semester1.SetBackgroundColour(gVar.darkerGrey)
	self.button_semester2.SetBackgroundColour(gVar.darkerGrey)
	self.SetBackgroundColour(gVar.darkerGrey)
	
	self.button_semester1.SetMinSize((120, -1))
	self.button_semester2.SetMinSize((120, -1))
	
	self.highlightBtn(self.button_semester1)

    def __do_layout(self):
        sizer_semester = wx.BoxSizer(wx.HORIZONTAL)
 
        sizer_semester.Add(self.button_semester1, 1, wx.ALL, 3)
        sizer_semester.Add(self.button_semester2, 1, wx.ALL, 3)

        self.SetSizer(sizer_semester)
	self.SetMinSize((200,21))
        sizer_semester.Fit(self)
	self.Layout()

    def __do_main(self):
	pass
	
    def OnSemester(self, event):
	#rint
	#rint 'OnSemester > gVar.semester ',gVar.semester 
	
        if gVar.semester == 1:
	      gVar.semester = 2
	      self.highlightBtn(self.button_semester2)    
	else:
	    gVar.semester = 1
	    self.highlightBtn(self.button_semester1)    
	pub.sendMessage('change.semester')
	self.Refresh()
	
    def highlightBtn(self, btn_to_glow):
        self.button_semester1.SetForegroundColour(gVar.mediumGrey)
	self.button_semester2.SetForegroundColour(gVar.mediumGrey)
	btn_to_glow.SetForegroundColour(gVar.barkleys)
	    
