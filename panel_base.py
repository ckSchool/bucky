import wx, gVar

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import fetch, loadCmb

from panel_bookingsReportGrid import panel_bookingsReportGrid
from panel_student_bookings         import panel_bookings        

class panel_base(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        
        self.SetName('panel_base')
        
        self.panel_header       = wx.Panel(self, -1) 
        
        self.panel_year_sch     = wx.Panel(self.panel_header, -1)
        
        #self.label_1            = wx.StaticText(self.panel_header, -1, "BOOKINGS FOR > ")
        self.choice_year        = wx.Choice(self.panel_year_sch, -1, choices=[])
        self.choice_school      = wx.Choice(self.panel_year_sch, -1, choices=["All", "CG", "SD", "SMP", "SMA"])
        
        self.panel_spc2         = wx.Panel(self.panel_year_sch, -1)
        self.button_settings    = wx.Button(self.panel_year_sch, -1, "...",  style=wx.NO_BORDER)
        
        self.panel_tabs         = wx.Panel(self.panel_header, -1)
        self.button_booking     = wx.Button(self.panel_tabs,  -1, "Bookings", style=wx.NO_BORDER)
        self.button_report      = wx.Button(self.panel_tabs,  -1, "Report",   style=wx.NO_BORDER)
        
        self.panel_panels       = wx.Panel(self, -1)
        self.panel_panels.SetName("panel_panels")
        
        self.panel_bookings     = panel_bookings(self.panel_panels, -1)
        self.panel_reportGrid   = panel_bookingsReportGrid(self.panel_panels, -1)   
          
        self.Bind(wx.EVT_CHOICE, self.yearChange,       self.choice_year)
        self.Bind(wx.EVT_CHOICE, self.schoolChange,     self.choice_school)
        self.Bind(wx.EVT_BUTTON, self.OnSettings,       self.button_settings)
        self.Bind(wx.EVT_BUTTON, self.changeToBookings, self.button_booking)
        self.Bind(wx.EVT_BUTTON, self.changeToReport,   self.button_report)  
        
        self.__set_properties()
        self.__do_layout()
        
    def __set_properties(self):
        #self.choice_year.SetMinSize((60, -1))
        self.choice_year.SetSelection(0)
        self.choice_school.SetSelection(0)
        self.button_booking.SetMinSize((120,24))
        self.button_report.SetMinSize((120,24))
        self.button_settings.SetMinSize((80, -1))
        self.panel_bookings.Hide()
        self.buttonColour(self.button_report,self.button_booking)

    def __do_layout(self):
        sizer_header  = wx.BoxSizer(wx.VERTICAL)
        sizer_header.Add(self.panel_year_sch, 0, wx.EXPAND, 0)
        sizer_header.Add(self.panel_tabs,     0, wx.EXPAND, 0)
        self.panel_header.SetSizer(sizer_header)

        sizer_sch_yr = wx.BoxSizer(wx.HORIZONTAL)
        #sizer_sch_yr.Add(self.label_1,         0, 0, 0)
        sizer_sch_yr.Add(self.choice_year,     0, 0, 0)
        sizer_sch_yr.Add(self.choice_school,   0, 0, 0)
        sizer_sch_yr.Add(self.panel_spc2,      1, 0, 0)
        sizer_sch_yr.Add(self.button_settings, 0, 0, 0)
        self.panel_year_sch.SetSizer(sizer_sch_yr)
        
        sizer_tabs = wx.BoxSizer(wx.HORIZONTAL)
        sizer_tabs.Add(self.button_report,     1, 0, 0)
        sizer_tabs.Add(self.button_booking,    1, 0, 0)
        
        self.panel_tabs.SetSizer(sizer_tabs)
        
        sizer_panels = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panels.Add(self.panel_bookings,   1, wx.EXPAND | wx.ALL, 0)
        sizer_panels.Add(self.panel_reportGrid, 1, wx.EXPAND | wx.ALL, 0)
        self.panel_panels.SetSizer(sizer_panels)
        
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_main.Add(self.panel_header, 0, wx.EXPAND | wx.ALL, 0)
        sizer_main.Add(self.panel_panels, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)
        
        #self.changeToBookings(wx.Event)
        
        self.Layout()

    def displayData(self):
        print 'panel base : displayData'
        loadCmb.schYrs(self.choice_year)
        self.choice_year.SetSelection(0)
        self.yearChange(wx.Event)
        
    def updateData(self):
        #gVar.schYr = int(self.choice_year.GetStringSelection())
        self.panel_bookings.displayData()
        self.panel_reportGrid.displayData()
        
    def yearChange(self, evt):
        x = self.choice_year.GetStringSelection()
        if x != gVar.schYr:
            gVar.schYr = int(x)
            self.GetTopLevelParent().setTitle()
            self.updateData()
            
    def changeToBookings(self, evt):
        self.changeView(1)
        
    def changeToReport(self, evt):
        self.changeView(2)
        
    def buttonColour(self, bOn, bOff):
        off = (200,200,200)
        on  = (200,100,200)
        bOn.SetBackgroundColour(on)
        bOff.SetBackgroundColour(off)
        
    def changeView(self, v):
        if v==1:
            self.panel_bookings.Show()
            self.panel_reportGrid.Hide()
            self.buttonColour(self.button_booking, self.button_report)
            
        else:
            self.panel_bookings.Hide()
            self.panel_reportGrid.Show()
            self.buttonColour(self.button_report, self.button_booking)
               
        self.Layout()
        
    def restore_str(self, choice, myStr = ''):
        choice.Freeze
        myStr = str(myStr) 
        myStr = myStr.strip()
        idx   = choice.FindString(myStr)
        if idx: # select first item
            choice.Select(idx) 
        else:
            choice.Select(0)
        choice.Thaw           
                
    def schoolChange(self, evt):
        x = fetch.choice(self.choice_school)
        if x != gVar.school:
            gVar.school = x
            self.updateData()
            

    def OnNewBooking(self, event):
        gVar.student_id = 0
        self.GetTopLevelParent().goTo('edit_booking')
        #p = self.GetTopLevelParent().panes('edit_booking')
        #p.dispalyData()
    
    def OnEditCourseList(self, event):
        print 'OnEditCourseList'
        self.GetTopLevelParent().goTo('edit_courses')
    
    def OnSettings(self, evt):
        if not hasattr(self, "popupID10"):
            self.popupID10 = wx.NewId()
            self.popupID20 = wx.NewId()
            self.popupID30 = wx.NewId()
            self.popupID40 = wx.NewId()
            self.popupID50 = wx.NewId()
            self.popupID60 = wx.NewId()
            self.popupID70 = wx.NewId()
            self.popupID80 = wx.NewId()
            self.popupID90 = wx.NewId()


            self.Bind(wx.EVT_MENU, self.OnNewBooking, id=self.popupID10)
            self.Bind(wx.EVT_MENU, self.OnEditCourseList, id=self.popupID20)
            self.Bind(wx.EVT_MENU, self.OnEditProfile, id=self.popupID30)
            self.Bind(wx.EVT_MENU, self.OnExit, id=self.popupID70)
            self.Bind(wx.EVT_MENU, self.OnRefresh, id=self.popupID90)

        menu = wx.Menu()
        menu.Append(self.popupID10, "Add New Student")
        menu.Append(self.popupID20, "Edit Course List")
        menu.Append(self.popupID30, "Edit User Profile")
        if gVar.userIsAdmin:
            
            menu.Append(self.popupID40, "Edit Users")
            self.Bind(wx.EVT_MENU, self.OnEditUsers, id=self.popupID40)
            
            
            menu.Append(self.popupID50, "Edit School List")
            self.Bind(wx.EVT_MENU, self.OnSchools, id=self.popupID50)
            
            menu.Append(self.popupID60, "Edit Fees")
            self.Bind(wx.EVT_MENU, self.OnFees, id=self.popupID60)
            
            menu.Append(self.popupID80, "Edit Address Items")
            self.Bind(wx.EVT_MENU, self.OnAddress, id=self.popupID80)
            
            menu.Append(self.popupID90, "Refresh link")
            self.Bind(wx.EVT_MENU, self.OnRefresh, id=self.popupID90)
            
        menu.Append(self.popupID70, "Exit")
        self.Bind(wx.EVT_MENU, self.OnExit, id=self.popupID70)
        self.PopupMenu(menu)
        menu.Destroy()
        
    def OnRefresh(self,evt):
        fetch.db.connect()
        
    def OnAddress(self, evt):
        dlg=DlgAddrItemEditor.create(None)
        try:
            dlg.displayData(batch_id)
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
        self.displayData()
        #self.GetTopLevelParent().goTo('address_items')
    
    def OnExit(self, evt):
        self.GetTopLevelParent().OnClose(wx.Event)
        
    def OnFees(self, evt):
        self.GetTopLevelParent().goTo('course_fees')
    
    def OnEditProfile(self, evt):
        print 'OnEditProfile'
    
    def OnEditUsers(self, evt):
        print 'OnEditUsers'
    
    def OnSchools(self, evt):
        self.GetTopLevelParent().goTo('edit_schools')