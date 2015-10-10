import wx

from ctrl.myListCtrl    import VirtualList

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import wx.grid as gridlib

import data.fetch   as fetch
import data.gVar    as gVar

#---------------------------------------------------------------------------

class panel_bookings(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
           
        tempheading = ((" ",10), (" ",15), (" ",10))
        self.vListBookings   = VirtualList(self, tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
          
        # for wxMSW
        self.vListBookings.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        # for wxGTK
        self.vListBookings.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
        self.__set_properties()
        self.__do_layout()
        
    def __set_properties(self):
        headingBookings = (('id',100), ('Course',100), ('name',100), ('Status',100))#, ('name',100), ('name',100))
        self.vListBookings.SetColumns(headingBookings)

    def __do_layout(self):
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_main.Add(self.vListBookings, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        
    def displayData(self):
        #rint'panel_student_bookings : displayData'
        sql = "SELECT s.id , c.name, s.name , name.reg_status \
                 FROM students s \
                 JOIN courses c ON s.register_course_id = c.id \
                WHERE s.register_schYr = %d" % gVar.schYr
        
        school_id = 0
        if gVar.school == "CG":            school_id = 1
        if gVar.school == "SD":            school_id = 2    
        if gVar.school == "SMP":           school_id = 3    
        if gVar.school == "SMA":           school_id = 4     
  
        if school_id:
            #rint"School"
            sqlSch = " AND c.school_id = %d" % school_id
            sql = "%s%s" % (sql, sqlSch)
            
        #sql = "%s%s" % (sql, " ORDER BY cSiswa.Kelas, cSiswa.Nama"  )
  
        results = fetch.DATA(sql)
        
        gVar.msg = " %d records found" % len(results)
        pub.sendMessage("change.statusbar")    
    
        self.vListBookings.SetItemMap(results)
        self.Layout()
        
    def OnViewDetails(self, event):# View Test Results
        self.GetTopLevelParent().goTo('student_details')
     
    def OnEditBookingDetails(self, event): # Receive Payment
        self.GetTopLevelParent().goTo('edit_booking')
        
    def OnDblClick(self,evt):
        self.OnRightClick(event)
        
    def OnRightClick(self, event):
        gVar.student_id = self.student_id  = self.vListBookings.get_selected_id()

        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnViewDetails, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnEditBookingDetails, id=self.popupID2)

        menu = wx.Menu()
        menu.Append(self.popupID1, "Student Details")
        menu.Append(self.popupID2, "Booking Details")

        self.PopupMenu(menu)
        menu.Destroy()
        
"""
    Status          :OK/PENDING/NO
    No. Reg         :15/001
    Name            :Student Name
    Gender          :Male
    Date Of Birth   :01/04/1999
    Prev. School    :
    Booking Fee     :Y :1 March 2014   :Receipt No.
    
    Tested          :Y : 6 April 2014
    Test Result     :Y : Results        :FAIL
    Test Retake	    :Y : 16 April 2014
    Retake Result   :Y : Results        :OK
    Offering Letter :Y : 8 May 2014     :Ref.No.
    Offer Accepted  :Y : 12 May 2014    :Receipt No.
    
    OBV/ET          :
    Notes           :' '
    
    Parents
    """    
