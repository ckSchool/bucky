import  wx, gVar, fetch

from myListCtrl import VirtualList

class panel_course_bookings(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        #self.button_back = wx.Button(self, -1,"< Back")
        self.heading     = wx.StaticText(self, -1, "Booking Status - Students Of Course ")
        
	#headings = [('',50),('',50),('',50)]
	self.vList = VirtualList(self, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
	self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemSelected, self.vList)
        
        #self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)
        
        sizer      = wx.BoxSizer(wx.VERTICAL)
        
        #sizer.Add(self.button_back)
        sizer.Add(self.heading)
        sizer.Add(self.vList, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        
        self.Layout()
        self.__do_main()
    
    def __do_main(self):
        #course_name = fetch.course_name(course_id)
        #self.heading.SetLabelText(txt)
        self.vList.SetColumns((('id',50),('Name',270),('Booking Status',70)))

        
    def displayData(self):
        print "panel_course_bookings : displayData"
        sql = "SELECT id, name, reg_status \
                 FROM students \
                WHERE register_course_id = %d \
                  AND register_schYr = %d" % (int(gVar.course_id), gVar.schYr )
        res = fetch.DATA(sql)
        self.vList.SetItemMap(res)
        
    def OnItemSelected(self, evt):
        student_id  = self.vList.GetSelectedID()
        index = self.vList.GetFirstSelected()
        
    #def OnBack(self, evt):
    #    self.GetTopLevelParent().goBack()
