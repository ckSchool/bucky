import wx, gVar, fetch

from myListCtrl import VirtualList as vListCtrl

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub



class bookings_report(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        tempheading = (("Course Name", 20),("NOW", 30), ("CONT.", 30), ("REDO", 30), ("OUT", 30), ("TOTAL",35), ("NEW",30), ("TOTAL",35), ("CLASS SIZE",50), ("CLASSES",55), (" ",10), (" ",10))
        self.listCtrl = wx.ListCtrl(self,  size=(-1,100), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        idx=0
        for h in tempheading:
            self.listCtrl.InsertColumn(idx, h[0], h[1])
            idx +=1
          
        # for wxMSW
        self.listCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.listCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
        self.__do_layout()
               
    def OnRightClick(self, event):
        #
        index = self.listCtrl.GetFirstSelected()
        #rint'item data=', self.listCtrl.GetItemData(index)
        
        #rint'lodilo... have result, publishing it via pubsub'
        pub.sendMessage('change_statusbar', arg1=123, arg2=dict(a='abc', b='def'))
        
        #self.index = self.listCtrl.GetFirstSelected()

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            
        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "?")
        menu.Append(self.popupID2, "?")
        menu.Append(self.popupID3, "?")
        menu.Append(self.popupID4, "?")
        menu.Append(self.popupID4, "?")
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    
    def OnPopupOne(self, event):# View Test Results
        #rint"Popup one\n"
        index = self.listCtrl.GetFirstSelected()
        #rint'item data=', self.listCtrl.GetItemData(index)
        #
        ##rint"FindItem:", self.listCtrl.FindItem(-1, "Roxette")
        ##rint"FindItemData:", self.listCtrl.FindItemData(-1, 0)

    def OnPopupTwo(self, event): # Receive Payment
        #rint"Selected items:\n"
        index = self.listCtrl.GetFirstSelected()
        
        while index != -1:
            #rint"      %s: %s\n" % (self.listCtrl.GetItemText(index), self.listCtrl.GetColumnText(index, 0))
            index = self.listCtrl.GetNextSelected(index)

    def OnPopupThree(self, event): # Update Status
        #rint"Popup three\n"
        #self.listCtrl.ClearAll()
        #wx.CallAfter(self.listCtrl.PopulateList)

    def OnPopupFour(self, event): # View Student Details
        item = self.listCtrl.GetItem(self.currentItem)
        #rintitem.m_text, item.m_itemId, self.listCtrl.GetItemData(self.currentItem)
  
    def OnPopupFive(self, event): # Withdraw Application
        pass # self.listCtrl.DeleteAllItems()
  
    def OnPopupSix(self, event):
        self.listCtrl.EditLabel(self.currentItem)    
    
    def showData(self):
        """
        TYPE    CLASSNAME CURRENT_POPULATION LEAVING  RETAKE  CONTINUE    TOTAL  CLASS_SIZE CLASSES     PENDING_BOOKINGS    notes  
        heading CLASSNAME CURRENT_POPULATION LEAVING  RETAKE  CONTINUE   
        kelas   ClassName CurrentPopulation  Leaving  Retake  Continue
        kelas   ClassName CurrentPopulation  Leaving  Retake  Continue
        tot     Totals    CurrentPopulation  Leaving  Retake  Continue
        heading NEXTCLASSNAME                         NEW     CONTINUE    TOTAL  CLASS_SIZE CLASSES     PENDING_BOOKINGS
        course  nextclassname                         New     Continue    tot                           Pending_Bookings
        course  nextclassname                         New     Continue    tot                            Pending_Bookings 
        space
        
        """
        mylist = []
        mylist.append(("TYPE", "FORM NAME", "POP.NOW", "OUT", "RETAKE", "CONT.", "TOTAL", "FORM SIZE", "FORMS", "PENDING BOOKINGS", "NOTES") )
        
        # list of course ids for year
        sql ="SELECT courses \
                FROM courses_by_year \
               WHERE schYr = %s" % gVar.schYr
        course_ids = fetch.getList(sql)
        
        sql ="SELECT level \
                FROM courses_levels \
               ORDER BY course_level"
        course_levels = fetch.getList(sql)
        
        for level in course_levels:
            for course_id in course_ids:
                sql ="SELECT id, name, school_id \
                        FROM courses \
                       WHERE level=%d AND id =%d" % (int(level), int(course_id))
                res = fetch.getAllDict(sql)
                for row in res:
                    mylist.append(row)
        #rintmylist

        for level in range(3,20):
            # show last years classes & students
            sql ="SELECT id, name, school_id \
                    FROM forms \
                   WHERE level=%d AND schYr =%d" % (level, gVar.schYr-1)
            forms = fetch.getAllDict(sql)
            
            level_totals =[0,0,0,0,0]
            for myForm in forms:
                form_id = myForm[0]
                now  = fetch.formPopulation(form_id) #GetClassPopulation
                level_totals[0]+=now
                cont = 4 #GetRereg
                level_totals[1]+=cont
                out  = 2 #GetStudentsLeaving
                level_totals[2]+=out
                redo = 1 #GetStudentsRetaking
                level_totals[3]+=redo
                subtot = cont-out+redo
                level_totals[4]+=subtot
                
                index = self.listCtrl.Append((myForm[1], now, cont, out, redo, subtot))
                self.listCtrl.SetItemData(index, form_id)
            self.listCtrl.Append(('Totals', str(level_totals[0]), str(level_totals[1]), str(level_totals[2]), str(level_totals[3]), str(level_totals[4])))
            
            # list of Kelas for this sch yr
            sql ="SELECT c.id, c.name \
                    FROM courses c \
                    JOIN students ON s.join_course_id = c.id) \
                   WHERE s.register_schYr = %d AND c.level=%d" % (gVar.schYr, level )
            res2 = fetch.getAllDict(sql)
            
            for row in res2:
                self.listCtrl.Append(('New reg','','',''))
                #sql ="SELECT * FROM cSiswa WHERE TahunAjaran = %d AND Kelas =%d" % (gVar.schYr, )
            
        return   
        for course_id in results:
            sql ="SELECT id, school_id, level, name \
                    FROM courses \
                   WHERE id =%d" % int(course_id)
            course = fetch.getOneDict(sql)
            mylist.append(course)
        
         
        mylist.sort(key=lambda tup: tup[1])
        
        mylist = [(tup[1], tup) for tup in mylist]
        school_ids = list(set(mylist))
        
        sql ="SELECT level, name \
                FROM courses \
               ORDER BY level, name"
        results = fetch.getAllDict(sql)
        ##rint'courses', results
    

    def __do_layout(self):
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_main.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)
