import wx, gVar,  pyodbc

from myListCtrl import VirtualList as vListCtrl
#from BetterListCtr import vListCtrl 
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import fetchodbc as fetch


class roundup(wx.Panel):
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
        
        #self.__set_properties()
        self.__do_layout()
        #self.__do_main()
        
    """ self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.listCtrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.listCtrl)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.listCtrl)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.listCtrl)
        
        self.listCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.listCtrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)"""
               
    def OnRightClick(self, event):
        #self.listCtrl.GetCurrentItem()
        self.currentItem =  gVar.course_id
        print 'self.currentItem', self.currentItem
        
        print 'lodilo... have result, publishing it via pubsub'
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
        print "Popup one\n"
        index = self.listCtrl.GetFirstSelected()
        print 'item data=', self.listCtrl.GetItemData(index)
        #print "FindItem:", self.listCtrl.FindItem(-1, "Roxette")
        #print "FindItemData:", self.listCtrl.FindItemData(-1, 0)

    def OnPopupTwo(self, event): # Receive Payment
        print "Selected items:\n"
        index = self.listCtrl.GetFirstSelected()
        
        while index != -1:
            print "      %s: %s\n" % (self.listCtrl.GetItemText(index), self.listCtrl.GetColumnText(index, 0))
            index = self.listCtrl.GetNextSelected(index)

    def OnPopupThree(self, event): # Update Status
        print "Popup three\n"
        #self.listCtrl.ClearAll()
        #wx.CallAfter(self.listCtrl.PopulateList)

    def OnPopupFour(self, event): # View Student Details
        item = self.listCtrl.GetItem(self.currentItem)
        print item.m_text, item.m_itemId, self.listCtrl.GetItemData(self.currentItem)
  
    def OnPopupFive(self, event): # Withdraw Application
        pass # self.listCtrl.DeleteAllItems()
  
    def OnPopupSix(self, event):
        self.listCtrl.EditLabel(self.currentItem)    
    
    def ShowData(self):
        """          CURRENT_POPULATION LEAVING  RETAKE  CONTINUE   
        CLASSNAME    CurrentPopulation  Leaving  Retake  Continue
        CLASSNAME    CurrentPopulation  Leaving  Retake  Continue
        Totals       CurrentPopulation  Leaving  Retake  Continue
                                         NEW_BOOKINGS     CONTINUE    TOTAL  CLASS_SIZE CLASSES     PENDING_BOOKINGS
                     NEXTCLASSNAME       NewBookings      Continue                                  Pending_Bookings
                     NEXTCLASSNAME       NewBookings      Continue                                  Pending_Bookings 
        
        
        """
        mylist = []
        mylist.append(("","CURRENT_POPULATION",  "CONT.",  "REDO", "OUT") )
        
        
        sql ="SELECT courses FROM courses_by_year WHERE schYr = %s" % gVar.schYr
        course_ids = fetch.getOne_dict(sql)[0].split(',')
        print sql, course_ids
        
        sql ="SELECT course_level FROM courses_levels ORDER BY course_level"
        course_levels = fetch.getList(sql)
        
        for level in course_levels:
            for course_id in course_ids:
                sql ="SELECT id, course_name, school_id FROM courses WHERE course_level=%d AND id =%d" % (int(level), int(course_id))
                res = fetch.getAll_dict(sql)
                print sql, res
                for row in res:
                    mylist.append(row)
        print mylist

        

        for level in range(3,20):
            # show last years classes & student
            sql ="SELECT Kode, Nama, Sekolah FROM Kelas WHERE course_level=%d AND TahunAjaran =%d" % (level,gVar.schYr-1)
            print sql
            classes = fetch.getAll_dict(sql)
            
            level_totals =[0,0,0,0,0]
            for myClass in classes:
                class_id = myClass[0]
                now  = fetch.batchPopulation(class_id) #GetClassPopulation
                level_totals[0]+=now
                cont = 4 #GetRereg
                level_totals[1]+=cont
                out  = 2#GetStudentsLeaving
                level_totals[2]+=out
                redo = 1#GetStudentsRetaking
                level_totals[3]+=redo
                subtot = cont-out+redo
                level_totals[4]+=subtot
                
                index = self.listCtrl.Append((myClass[1], now, cont, out, redo, subtot))
                self.listCtrl.SetItemData(index, class_id)
            self.listCtrl.Append(('Totals', str(level_totals[0]), str(level_totals[1]), str(level_totals[2]), str(level_totals[3]), str(level_totals[4])))
            
            # list of Kelas for sch yr
            sql ="SELECT classes_id, classes.name FROM classes INNER JOIN cSiswa ON (cSiswa.Kelas = classes.id) WHERE cSiswa.TahunAjaran = %d AND classes.course_level=%d" % (gVar.schYr, level )
            res2 = fetch.getAll_dict(sql)
            print sql, res2
            
            for row in res2:
                self.listCtrl.Append(('New reg','','',''))
                #sql ="SELECT * FROM cSiswa WHERE TahunAjaran = %d AND Kelas =%d" % (gVar.schYr, )
            
        return   
        for course_id in results:
            sql ="SELECT id, school_id, course_level, course_name FROM courses WHERE id =%d" % int(course_id)
            course = fetch.getOne_dict(sql)
            mylist.append(course)
        
         
        mylist.sort(key=lambda tup: tup[1])
        
        mylist = [(tup[1], tup) for tup in mylist]
        print 'mylist ',mylist 
        school_ids = list(set(mylist))
        print 'school_ids', school_ids
        #[(tup[1], tup) for tup in data]
        print mylist
        
        sql ="SELECT course_level, course_name FROM courses ORDER BY course_level, course_name"
        results = fetch.getAll_dict(sql)
        #print 'courses', results
        """
        #for 
        
        
        sql = "SELECT cSiswa.Kode , courses.course_name, cSiswa.Nama , cSiswa.Status \
                FROM cSiswa INNER JOIN courses ON cSiswa.Kelas = courses.id \
               WHERE cSiswa.TahunAjaran = %s" % gVar.schYr

        schoolKode = 0
        if gVar.school == "CG":            schoolKode = 1
        if gVar.school == "SD":            schoolKode = 2    
        if gVar.school == "SMP":           schoolKode = 3    
        if gVar.school == "SMA":           schoolKode = 4     
  
        print gVar.school, schoolKode
        if schoolKode:
            print "School"
            #sqlSch = " AND courses.school_id = %d" % schoolKode
            #sql = "%s%s" % (sql, sqlSch)
  
        sql = "%s%s" % (sql, " ORDER BY courses.course_level, cSiswa.Nama"  )

        #sql = "SELECT Kode, Nama, Status FROM cSiswa \
        #      WHERE TahunAjaran = %s" % gVar.schYr
        
        #sql = "SELECT course_name \
        #        FROM courses "
        
        print sql
        results = fetch.getAll_dict(sql)
        print len(results), "Results "
        print

        results = fetch.DATA(sql)
        #print "DATA = " , results
        self.listCtrl.SetItemMap(results)"""

    def __do_layout(self):
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_main.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)