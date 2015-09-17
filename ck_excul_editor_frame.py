import wx, fetch, loadCmb, math, images, gVar

import wx.lib.mixins.listctrl as listmix

gVar.schYr = 2014
symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}

class VirtualList(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=id, columns=(('',50),('',50),('',50)), style=0):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT | wx.LC_VIRTUAL | style)
        
        self.tlp = self.GetTopLevelParent()
        
        listmix.ColumnSorterMixin.__init__(self, len(columns))
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        self.itemDataMap={}
        
        self.il = wx.ImageList(16, 16)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.il_symbols={}
    
        self.SetSymbols(symbols)
        self.SetColumns(columns) # why does this need to be called twice to kick in
    
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,   self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK,       self.OnColClick)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,      self._startDrag)

        self.SetDropTarget(ListDrop(self))
        
        self.currentItem = 0

    def AppendItem(self, ldata):
        print 'AppendItem', ldata
        idx = len(self.itemDataMap)
        self.itemDataMap[idx]=ldata
        self.SetItemCount(idx+1)
        self.SortItems()
        
    def remove_selected_item(self):
        print 'remove_selected_item ', self.GetItemInfo(self.currentItem)
        idx, what, student_id, name, form = self.GetItemInfo(self.currentItem)
        if not student_id: return 0
        
        student_id = int(student_id)
        selected_item = (student_id, name, form)
        print selected_item
        
        key = self.find_key_for_student_id(student_id)
        if not key == None :
            del self.itemDataMap[key]
            self.regen_dict()
            self.loadMap()
        
        self.Refresh()
        
        return selected_item
        
    def setName(self, name='vlistCtrl'):  self.SetName(name)
        
    def OnGetItemText(self, item, col=0): # callbacks for implementing virtualness
        index = self.itemIndexMap[item]
        textItem = self.itemDataMap[index][col]
        return textItem
    
    def OnGetItemImage(self, item): return -1# callbacks for implementing virtualness
        
    def OnGetItemAttr(self, item): return None# callbacks for implementing virtualness
                
    def OnColClick(self,event):  event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.currentID   = self.GetSelectedID()
        event.Skip()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()

    def OnItemDeselected(self, evt): self.currentItem = 0
    
    def OnGetItemAttr(self, item): # callbacks for implementing virtualness
        index=self.itemIndexMap[item]
        try:
            flag=self.itemDataMap[index][2]
            return self.flag_attr_dict[flag]
        except:
            pass
            return None
        
    def SortItems(self, sorter=None):
        col = self._col
        sf  = self._colSortFlag[col]
        
        items=[]#creating pairs [column item defined by col, key]
        for k,v in self.itemDataMap.items(): items.append([v[col], k])
        
        items.sort()                    #sort the pairs by value (first element), then by key (second element).
        k=[key for value, key in items] #getting the keys associated with each sorted item in a list
        if sf==False:    k.reverse()    #False is descending (starting from last)
        self.itemIndexMap=k             #storing the keys as self.itemIndexMap (is used in OnGetItemText,Image,ItemAttr
        self.Refresh()

    # These methods should be used to interact with the controler
    def SetItemMap(self, itemMap):
        self.DeleteAllItems()
        self.Refresh()
        if not itemMap:  return

        first_row  = itemMap[0]
        item_count = len(first_row)
        col_count  = self.GetColumnCount()
        
        if item_count > col_count:
            return  # how to insert extra columns
        elif item_count < col_count:
            while item_count < self.GetColumnCount():
                self.DeleteColumn(self.GetColumnCount()-1)
        
        self.itemDataMap=itemMap        
        self.loadMap()
        
    def loadMap(self, ):
        l=len(self.itemDataMap)
        self.SetItemCount(l)
        self.SortItems()
        
    def SetColumns(self, columns = (('',50),('',50))):
        self.DeleteAllColumns()
        i=0
        for coldef in columns:
            if len(coldef)==3: # coldef includes format
                name, s, col_format = col
                self.InsertColumn(i, name, col_format)
                self.SetColumnWidth(i, s)
                i+=1
            else:
                name, s = coldef
                self.InsertColumn(i, name)
                self.SetColumnWidth(i, s)
                i+=1
                
        listmix.ColumnSorterMixin.__init__(self, len(columns))

    def SetSymbols(self, symbols, provider=wx.ART_TOOLBAR):
        for k, v in symbols.items():
            self.il_symbols[k] = self.il.Add(wx.ArtProvider_GetBitmap(v, provider, (16,16))) 
    
    def selectItem(self,idx):
        self.SetItemState(idx, wx.LIST_STATE_SELECTED,wx.LIST_STATE_SELECTED)
        
    def GetItemInfo(self, idx):
        print 'GetItemInfo'
        """Collect all relevant data of a listitem, and put it in a list"""
        l = []
        l.append(idx) # We need the original index, so it is easier to eventualy delete it
        l.append(self.GetItemData(idx)) # Itemdata
        #
        for i in range(0, self.GetColumnCount()): # Possible extra columns
            txt = self.GetItemText(idx, i)
            txt = str(txt)
            l.append(txt)
            
        return l
    
    def GetCurrentItem(self): return self.currentItem # callbacks for implementing virtualness
        
    def GetListCtrl(self): return self# Used by the ColumnSorterMixin,
        
    def GetSortImages(self):# Used by the ColumnSorterMixin,
        return self.il_symbols["sm_dn"],self.il_symbols["sm_up"]
    
    def GetSelectedID(self):
        selected_id = self.GetColumnText(self.currentItem, 0)
        try:    return int(selected_id)
        except: return 0
    
    def GetColumnText(self, index, col):
        item = self.GetItemText(index, col)
        return item
        
    def _onStripe(self):
        if self.GetItemCount()>0:
            for x in range(self.GetItemCount()):
                if x % 2==0:
                    self.SetItemBackgroundColour(x,wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DLIGHT))
                else:
                    self.SetItemBackgroundColour(x,wx.WHITE)

    def _startDrag(self, evt):
        """ Put together a data object for drag-and-drop _from_ this list. """
        
        idx, what, student_id, name, form = self.GetItemInfo(self.currentItem)
        student_id = int(student_id)
        data = "%d,%s,%s" % (student_id, name, form)
        
        ldata = wx.CustomDataObject("ListCtrlItems")
        ldata.SetData(data)
        
        # Now make a data object for the  item list.
        dropDataObj = wx.DataObjectComposite()
        dropDataObj.Add(ldata)

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(dropDataObj)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            key = self.find_key_for_student_id(student_id)
            if not key == None :
                del self.itemDataMap[key]
                self.regen_dict()
                self.loadMap()
            
            self.Refresh()
        
    def regen_dict(self):
        itemMap = {}
        index = 0
        for key in self.itemDataMap:
            itemMap[index]= self.itemDataMap[key]
            index += 1
        self.itemDataMap = itemMap
                
    def find_key_for_student_id(self, student_id):
        for key in self.itemDataMap:
            sid, name, form = self.itemDataMap[key]
            if int(sid) == student_id: return key
        return None


    def _insert(self, x, y, seq):
        print '_insert', seq
        """ Insert text at given x, y coordinates --- used with drag-and-drop. """
        self.itemDataMap[seq[0]] = seq

        # Find insertion point.
        index, flags = self.HitTest((x, y))

        if index == wx.NOT_FOUND: # not clicked on an item
            if flags & (wx.LIST_HITTEST_NOWHERE|wx.LIST_HITTEST_ABOVE|wx.LIST_HITTEST_BELOW): # empty list or below last item
                index = self.GetItemCount() # append to end of list
            elif self.GetItemCount() > 0:
                if y <= self.GetItemRect(0).y: # clicked just above first item
                    index = 0 # append to top of list
                else:
                    index = self.GetItemCount() + 1 # append to end of list
                    
        else: # clicked on an item
            # Get bounding rectangle for the item the user is dropping over.
            rect = self.GetItemRect(index)

            # If the user is dropping into the lower half of the rect, we want to insert _after_ this item.
            # Correct for the fact that there may be a heading involved
            if y > rect.y - self.GetItemRect(0).y + rect.height/2:
                index += 1
                
        for i in seq: # insert the item data
            idx = self.InsertStringItem(index, i[2])
            self.SetItemData(idx, i[1])
            for j in range(1, self.GetColumnCount()):
                try: # Target list can have more columns than source
                    self.SetStringItem(idx, j, i[2+j])
                except:
                    pass # ignore the extra columns
            index += 1
            
        self._onStripe()
        
class ListDrop(wx.PyDropTarget):
    """ Drop target for simple lists. """
    def __init__(self, source):
        """ Arguments:
         - source: source listctrl.
        """
        wx.PyDropTarget.__init__(self)
        self.dv = source

        # specify the type of data we will accept
        self.data = wx.CustomDataObject("ListCtrlItems")
        self.SetDataObject(self.data)

    # Called when OnDrop returns True.
    # We need to get the data and do something with it.
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object
        if self.GetData():
            # " convert draged string back to a list and give it to the viewer "
            ldata = self.data.GetData().split(',')
            student_id, name, form = ldata
            itemlist = list((int(student_id), name, form))
            
        idx = len(self.dv.itemDataMap)
        self.dv.AppendItem(itemlist)
        # what is returned signals the source what to do with the original data (move, copy, etc.)
        # In this case we just return the suggested value given to us.
        return d

def create(parent):
    return DlgExculEditor(parent) 
        
class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(3)
        
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-1, -2, -2])
        self.sizeChanged = False
        
        # Field 0 ... just text
        self.SetStatusText("A Custom StatusBar...", 0)
        # We're going to use a timer to drive a 'clock' in the last
        # field.
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
        self.SetStatusText(st, 2)
        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.SetTitle("Club Shuffler")
        self.SetSize((1200, 450))
        
        menubar  = wx.MenuBar()
        fileMenu = wx.Menu()
        mnuitem_save = fileMenu.Append(-1, 'Save',  'Save')
        mnuitem_print = fileMenu.Append(-1, 'Print', 'Print')
        menubar.Append(fileMenu, '&File')
        clubMenu = wx.Menu()
        mnuitem_addClub = clubMenu.Append(-1, 'Add Club',  'Add Club')
        mnuitem_editDays = clubMenu.Append(-1, 'Edit Days', 'Edit Days')
        menubar.Append(clubMenu, '&Clubs')
        
        self.SetMenuBar(menubar)
        
        
        self.Bind(wx.EVT_MENU, self.OnSave,  mnuitem_save)
        self.Bind(wx.EVT_MENU, self.OnPrint, mnuitem_print)
        
        self.Bind(wx.EVT_MENU, self.OnAddClub,  mnuitem_addClub)
        self.Bind(wx.EVT_MENU, self.OnEditDays, mnuitem_editDays)
        
        self.panel_filter = wx.Panel(self, -1)
        self.panel_main   = wx.Panel(self, -1)
        
        self.label_sch       = wx.StaticText(self.panel_filter, -1, 'School:')
        self.choice_school   = wx.Choice(self.panel_filter,     -1, choices=[])
        self.label_sem       = wx.StaticText(self.panel_filter, -1, 'Semester:')
        self.choice_semester = wx.Choice(self.panel_filter,     -1, choices=[])
        
        self.rb_mon = wx.RadioButton(self.panel_filter, -1, 'Mon')
        self.rb_tue = wx.RadioButton(self.panel_filter, -1, 'Tue')
        self.rb_wed = wx.RadioButton(self.panel_filter, -1, 'Wed')
        self.rb_thr = wx.RadioButton(self.panel_filter, -1, 'Thur')
        self.rb_fri = wx.RadioButton(self.panel_filter, -1, 'Fri')
        self.rb_xxx = wx.RadioButton(self.panel_filter, -1, 'x')
        
        self.rbtns = [self.rb_mon, self.rb_tue, self.rb_wed,
                      self.rb_thr, self.rb_fri, self.rb_xxx ]
        
        self.vList_waiting       = VirtualList(self.panel_main, -1, style=wx.LC_REPORT)
        self.panel_clubListCtrls = wx.ScrolledWindow(self.panel_main, -1)
        
        self.sizer_clubs = wx.GridSizer(2, 2, 5, 5)
        self.panel_clubListCtrls.SetSizer( self.sizer_clubs)
        
        for btn in self.rbtns:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnDayChange, btn)
            btn.Hide()
            
        values = [1,2,3,4,5] 
        self.rb_dict = dict(zip(self.rbtns, values))
        self.rb_rev_dict = dict(zip(values, self.rbtns))
        
        self.Bind(wx.EVT_CHOICE, self.OnFilterChange, self.choice_school)
        self.Bind(wx.EVT_CHOICE, self.OnFilterChange, self.choice_semester)
        #self.Bind(wx.EVT)
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.panel_clubListCtrls.SetScrollbars(1, 1, 1, 1)
        columns=( ('ID', 0), ('Unallocated', 150), ('Form', 50))
        self.vList_waiting.SetColumns(columns)
        self.vList_waiting.SetMinSize((300, -1))
        
        self.choice_school.Append('Primary',   2)
        self.choice_school.Append('Secondary', 3)
       
        self.choice_semester.Append('Semester 1', 1)
        self.choice_semester.Append('Semester 2', 2)

    def __do_layout(self):
        sizer_base   = wx.BoxSizer(wx.VERTICAL)
        sizer_filter = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_filter.Add(self.label_sem,       0, wx.ALL, 5)
        sizer_filter.Add(self.choice_semester, 0, wx.ALL, 5)
        sizer_filter.Add(self.label_sch,       0, wx.ALL, 5)
        sizer_filter.Add(self.choice_school,   0, wx.ALL, 5)
        
        for btn in self.rbtns:
            sizer_filter.Add(btn,      0, wx.ALL, 5)
        self.panel_filter.SetSizer(sizer_filter)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.vList_waiting,       0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        sizer_main.Add(self.panel_clubListCtrls, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_filter, 0, wx.EXPAND , 10)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND ,  10)
        self.SetSizer(sizer_base)
       
    def __do_main(self):
        self.choice_semester.SetSelection(0)
        self.choice_school.SetSelection(0)
        self.OnFilterChange(wx.Event)
        
    def OnDayChange(self, evt):
        self.displayData()
        
    def OnPrint(self, evt):
        print 'print'
        
    def OnFilterChange(self, evt):
        semester  = fetch.cmbID(self.choice_semester)
        school_id = fetch.cmbID(self.choice_school)
        for btn in self.rb_dict:
            btn.Hide()
        self.rb_xxx.Freeze()    
        self.rb_xxx.SetValue(1)    
        self.rb_xxx.Thaw()
        
        schedule = fetch.exculSchedule_forSchSemYr(school_id, semester, gVar.schYr)
        
        for row in schedule:
            day = row['day']
            rb  = self.rb_rev_dict[day]
            rb.SetValue(1)
            rb.Show()
            
        try:
            self.Layout()
        except:
            print "-"# can't set size of uninitialized sizer item"
        self.displayData()
        
    def displayData(self):
        day = 0
        for btn in self.rb_dict:
            if btn.GetValue():
                day = self.rb_dict[btn]
                btn.Show()
        
        semester  = fetch.cmbID(self.choice_semester)
        school_id = fetch.cmbID(self.choice_school)
        print '\n.........................\n'
        schedule_id = fetch.excul_schedule_id(day, semester, school_id, gVar.schYr)
  
        self.vList_waiting.DeleteAllItems()
        non_members = fetch.excul_unallocatedDATA(schedule_id)
        print 'non_members'
        print non_members
        self.vList_waiting.SetItemMap(non_members)
        
        self.init_club_lists(schedule_id)
        
        self.Layout()
        
    def OnResize(self, evt):
        self.Layout()
    
        
    def init_club_lists(self, schedule_id):
        club_dict = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        club_count = len(club_dict)
        rows = math.ceil(club_count/3 + .5)
        
        if club_count > 0:
            try:
                self.sizer_clubs.DeleteWindows()
                self.sizer_clubs.Destroy()
                self.panel_clubListCtrls.DestroyChildren()
                self.AddNewSizerAndCtrls(schedule_id)
                 
            except:
                self.AddNewSizerAndCtrls(schedule_id)
        
        else:
            if self.sizer_clubs:
                self.sizer_clubs.DeleteWindows()
        
        return
    

    def AddClubList(self, key, club_dict):
        club_id   = int(key)
        club_info = club_dict[club_id]
        club_name = club_info[2]
        members   = fetch.excul_studentList(club_id)
        vList     = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        columns   = (('ID', 0), (club_name, 150),('Form', 50))
        
        vList.SetColumns(columns)
        vList.SetName(str(club_id))
        vList.SetItemMap(members)
        
        self.club_listCtrls.append(vList)
        self.sizer_clubs.Add(vList, 1, wx.EXPAND | wx.ALL, 5)
        
        # make list ctrl visable modual wide
        self.vClubListCtrls[key] = vList
        
        # add bindings
        # for wxMSW
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick, vList)

        # for wxGTK
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick, vList)
        
        self.Bind(wx.EVT_COMMAND_LEFT_DCLICK, self.OnDblClick, vList)
        
    def OnRightClick(self, event):
        vList =  event.GetEventObject()
        club_id = int(vList.GetName())
        
        groupInfo = fetch.excul_groupInfo(club_id)
        print 'groupInfo ', groupInfo
        subject_name = groupInfo['subject_name']
        
        self.currentItem = vList.currentItem
        student_id       = vList.GetSelectedID()
        gVar.student_id  = student_id
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne,   id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo,   id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            
        # make a menu
        menu = wx.Menu()
        # add some items
        title = "%s, %s, %s" % (subject_name, "Teacher", "Population")
        menu.SetTitle(title)
        menu.Append(self.popupID1, "Edit Club")
        menu.Append(self.popupID2, "Delete Club")
        menu.AppendSeparator()
        
        self.currentItem = vList.currentItem
        
        student_id = vList.GetSelectedID()
        item_has_focus = vList.GetFirstSelected()
        if item_has_focus > -1:
            print item_has_focus
            menu.Append(self.popupID3, "View Student Details")
        
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        position = self.ScreenToClient(wx.GetMousePosition())
        self.PopupMenu(menu, position)
        menu.Destroy()
    
    def OnPopupOne(self, event):
        print "OnPopupOne Edit Club"
        item = event.GetEventObject().GetName()

    def OnPopupTwo(self, event):
        print "OnPopupTwo Delete Club"
        item = event.GetEventObject().GetName()

    def OnPopupThree(self, event):
        print 'OnPopup 3 - Student Details'
        print  'gVar.student_id', gVar.student_id

  
    def OnDblClick(self, evt):
        vList = evt.GetEventObject()
        selected_item = vList.remove_selected_item()
        self.vList_waiting.AppendItem(selected_item)
        print 'OnDblClick'
        
    def AddNewSizerAndCtrls(self, schedule_id):
        club_dict = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        number_of_ctrls = len(club_dict)
 
        rows = math.ceil(number_of_ctrls/3 + .5)
        if rows >0:
            self.sizer_clubs = wx.GridSizer(rows, 3, 5, 5)
            self.panel_clubListCtrls.SetSizer(self.sizer_clubs)
     
            self.club_listCtrls = []
            self.vClubListCtrls = {}
            for key in club_dict:
                self.AddClubList(key, club_dict)
            self.Layout() 
        
    def OnSave(self, evt):
        print 'OnSave'
        if not self.vClubListCtrls: return
        for key in self.vClubListCtrls:
            print 'key', key
            vList = self.vClubListCtrls[key]
            excul_id = int(vList.GetName())
            members = vList.itemDataMap
            
            if members:
                self.updateDB(excul_id, members)
                
    def updateDB(self, excul_group_id, members):
        sql = "DELETE FROM excul_students \
                WHERE excul_group_id =%d " % excul_group_id
        fetch.updateDB(sql)
        for key in members:
            student_id, name, form = members[key]
            sql = "INSERT INTO excul_students \
                               (student_id, excul_group_id) \
                        VALUES (%d, %d)" % (student_id, excul_group_id) 
            fetch.updateDB(sql)
            
    def OnAddClub(self, ):
        pass
        print 'OnAddClub'
    
    
    def OnEditDays(self, ):
        pass
        print 'OnEditDays'
        
if __name__ == "__main__":
    schYr = 2014
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()