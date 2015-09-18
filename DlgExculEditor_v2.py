import wx, fetch, math, images, gVar

gVar.schYr = 2014

import wx.lib.mixins.listctrl as listmix

schedule_id = 1
symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}

clubs ={0: (0, 'Chess',         'Pollung',  '0'),
        1: (1, 'Futsal',        'Pardono',  '0'),
        2: (2, 'Climbing',      'Rolita',   '0'),
        3: (3, 'Table Tennis',  'Gary',     '1')}

club_members = { 0:{0: (73, 'Arles ', '6 SD C'),
                    1: (74, 'Avid',    '5 SD B'),
                    2: (76, 'Audjana', '6 SD D')},
                 1:{0: (81, 'Bndrew',   '3 SD C'),
                    1: (32, 'Bana',     '6 SD A'),
                    2: (65, 'Bimon',    '4 SD C'),
                    3: (21, 'Bames',    '5 SD C')},
                 2:{0: (73, 'Charles ', '6 SD C'),
                    1: (74, 'Cvid',     '5 SD B'),
                    2: (76, 'Caudjana', '6 SD D')},
                 3:{0: (81, 'Dndrew',   '3 SD C'),
                    1: (32, 'Dana',     '6 SD A'),
                    2: (65, 'Dimon',    '4 SD C'),
                    3: (21, 'Dames',    '5 SD C')}
                }
                
non_members = { 0: (3, 'Jab ', '3 SD A'),
                1: (4, 'Job',  '4 SD B'),
                2: (6, 'Jill', '4 SD C')}

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
        idx = len(self.itemDataMap)
        self.itemDataMap[idx]=ldata
        self.SetItemCount(idx+1)
        self.SortItems()
        
        
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
        col =self._col
        sf  =self._colSortFlag[col]
        
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
                print self.itemDataMap
                del self.itemDataMap[key]
                print self.itemDataMap
                itemMap = {}
                index = 0
                for key in self.itemDataMap:
                    itemMap[index]= self.itemDataMap[key]
                    index += 1
                self.itemDataMap = itemMap
                self.loadMap()
            
            self.Refresh()
        
       
    
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
        
class DlgExculEditor(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME | wx.MAXIMIZE_BOX
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.SetTitle("excul shuffler")
        self.SetSize((1200, 450))
        
        self.panel_filter = wx.Panel(self, -1)
        self.panel_main   = wx.Panel(self, -1)
        
        self.choice_school   = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_semester = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_day      = wx.Choice(self.panel_filter, -1, choices=[])
        
        self.choice_school   = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_semester = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_day      = wx.Choice(self.panel_filter, -1, choices=[])
     
        self.vList_waiting       = VirtualList(self.panel_main, -1, style=wx.LC_REPORT)
        self.panel_clubListCtrls = wx.ScrolledWindow(self.panel_main, -1)
        
        self.sizer_clubs = wx.GridSizer(2, 2, 5, 5)
        self.panel_clubListCtrls.SetSizer( self.sizer_clubs)
        
        self.init_club_lists()
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def OnResize(self, evt):
        self.Layout()
    
        
    def init_club_lists(self):
        self.sizer_clubs.DeleteWindows()
        self.sizer_clubs.Destroy()
        self.Layout()
        
        club_dict = fetch.exculGroupsDATA_forScheduleID(schedule_id) 
        rows = math.ceil(len(club_dict)/3 + .5) 
        self.sizer_clubs = wx.GridSizer(rows, 3, 5, 5)
        self.panel_clubListCtrls.SetSizer(self.sizer_clubs)
        
        self.club_listCtrls = []
        self.vClubListCtrls = {}
        for key in club_dict:
            club_id = int(key)
            club_info = club_dict[club_id]
            self.vClubListCtrls[key] = vl = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
            self.club_listCtrls.append(vl)
            self.sizer_clubs.Add(vl, 1, wx.EXPAND | wx.ALL, 5)
            
             
            club_name = club_info[2]
            columns=(('ID',40), (club_name,150),('Class',50))
            vl.SetColumns(columns)
            vl.SetName(str(key))
            l = fetch.excul_studentList(club_id)
            
            vl.SetItemMap(l)
            
        
    def __set_properties(self):
        self.panel_clubListCtrls.SetScrollbars(1,1,1,1)
        columns=( ('ID', 40), ('WAITING', 150), ('ADDR', 50))
        self.vList_waiting.SetColumns(columns)
        
 
    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.vList_waiting,       0, wx.EXPAND | wx.RIGHT, 10)
        sizer_main.Add(self.panel_clubListCtrls, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_filter, 0, wx.EXPAND | wx.ALL, 10)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer_base)
       
    def __do_main(self):
        pass
     
    def update_monitor(self):
        self.text_ctrl_pool.SetValue(str(self.vList_waiting.itemDataMap))
        self.text_ctrl_g1.SetValue(str(self.vList_g1.itemDataMap))
        self.text_ctrl_g2.SetValue(str(self.vList_g2.itemDataMap))
        self.text_ctrl_g3.SetValue(str(self.vList_g3.itemDataMap))
        self.text_ctrl_g4.SetValue(str(self.vList_g4.itemDataMap))
        
    def displayData(self):
        non_members = fetch.excul_unallocatedDATA(2)
        print 'non_members'
        print non_members
        print
        self.vList_waiting.SetItemMap(non_members) 
        # data fo each club_listCtrl
        
        
        return
        for key in clubs:
            row = clubs[key]
            club_id = clubs[key][0]
            print club_id
            try:
                l = club_members[club_id] 
                self.club_listCtrls[key].SetItemMap(l)
            except:
                print 'no members'
        self.Layout()
        
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = create(None)
    try:
        dlg.displayData()
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()