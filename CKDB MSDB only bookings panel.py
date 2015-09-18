import wx, gVar,  pyodbc

from BetterListCtr import vListCtrl 

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import fetchodbc as fetch


class bookingPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self.list = vListCtrl(self, style=wx.LC_HRULES)
          
        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    """ self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        
        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)"""
               
    def OnRightClick(self, event):
        self.currentItem = self.list.currentItem
        #rint'self.currentItem', self.currentItem
        
        #rint'lahdida... have result, publishing it via pubsub'
        pub.sendMessage('change_statusbar', arg1=123, arg2=dict(a='abc', b='def'))
        
        #self.index = self.list.GetFirstSelected()

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
        menu.Append(self.popupID1, "View Test Results")
        menu.Append(self.popupID2, "Receive Payment")
        menu.Append(self.popupID3, "Update Status")
        menu.Append(self.popupID4, "View Student Details")
        menu.Append(self.popupID4, "Withdraw Application")
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    
    def OnPopupOne(self, event):# View Test Results
        #rint"Popup one\n"
        #rint"FindItem:", self.list.FindItem(-1, "Roxette")
        #rint"FindItemData:", self.list.FindItemData(-1, 11)

    def OnPopupTwo(self, event): # Receive Payment
        #rint"Selected items:\n"
        index = self.list.GetFirstSelected()
        
        while index != -1:
            #rint"      %s: %s\n" % (self.list.GetItemText(index), self.list.GetColumnText(index, 0))
            index = self.list.GetNextSelected(index)

    def OnPopupThree(self, event): # Update Status
        #rint"Popup three\n"
        #self.list.ClearAll()
        #wx.CallAfter(self.list.PopulateList)

    def OnPopupFour(self, event): # View Student Details
        item = self.list.GetItem(self.currentItem)
        #rintitem.m_text, item.m_itemId, self.list.GetItemData(self.currentItem)
  
    def OnPopupFive(self, event): # Withdraw Application
        pass # self.list.DeleteAllItems()
  
    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)    
    
    def updateData(self):
        sql = "SELECT cSiswa.Kode , courses.course_name, cSiswa.Nama , cSiswa.Status \
                FROM cSiswa INNER JOIN courses ON cSiswa.Kelas = courses.id \
               WHERE cSiswa.TahunAjaran = %s" % gVar.schYr

        schoolKode = 0
        if gVar.school == "CG":            schoolKode = 1
        if gVar.school == "SD":            schoolKode = 2    
        if gVar.school == "SMP":           schoolKode = 3    
        if gVar.school == "SMA":           schoolKode = 4     
  
        #rintgVar.school, schoolKode
        if schoolKode:
            #rint"School"
            #sqlSch = " AND courses.school_id = %d" % schoolKode
            #sql = "%s%s" % (sql, sqlSch)
  
        sql = "%s%s" % (sql, " ORDER BY cSiswa.Kelas, cSiswa.Nama"  )

        #sql = "SELECT Kode, Nama, Status FROM cSiswa \
        #      WHERE TahunAjaran = %s" % gVar.schYr
        
        #sql = "SELECT course_name \
        #        FROM courses "
        
        #rintsql
        results = fetch.getAll_dict(sql)
        #rintlen(results), "Results "
        print

        results = fetch.DATA(sql)
        ##rint"DATA = " , results
        self.list.PopulateList(results)

    def __do_layout(self):
        sizer_main = wx.BoxSizer( wx.VERTICAL)
        sizer_main.Add(self.list, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer_main)