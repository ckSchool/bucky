import wx, math, time, images

import wx.lib.mixins.listctrl as listmix

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
        
        for i in range(0, self.GetColumnCount()): # Possible extra columns
            txt = self.GetItemText(idx, i)
            txt = str(txt)
            l.append(txt)
            
        print '\n returning:', l
        return l
    
    def GetCurrentItem(self): return self.currentItem # callbacks for implementing virtualness
        
    def GetListCtrl(self):# Used by the ColumnSorterMixin,
        return self

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
        self.tlp.text_ctrl_drag.SetValue(data)
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
        self.tlp.text_ctrl_drag.SetValue('')
        self.tlp.update_monitor()
    
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

    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object
        if self.GetData():
            # " convert it back to a list and give it to the viewer "
            ldata = self.data.GetData()[0:-1].split(',')
            student_id, name, form = ldata
            itemlist = list((int(student_id), name, form))
            #itemlist = []
            #for item in ldata:
            #    itemlist.append(item)
            #student_id, name, form = ldata
            
        idx = len(self.dv.itemDataMap)
        self.dv.AppendItem(itemlist)
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d

def create(parent):
    return DlgExculEditor(parent) 
        
class DlgExculEditor(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.SetTitle("excul shuffler")
        self.SetSize((1200, 450))
        
        self.panel_left = wx.Panel(self, -1)
        self.text_ctrl_pool = wx.TextCtrl(self.panel_left, -1,'', style = wx.TE_MULTILINE)
        self.text_ctrl_g1   = wx.TextCtrl(self.panel_left, -1,'', style = wx.TE_MULTILINE)
        self.text_ctrl_g2   = wx.TextCtrl(self.panel_left, -1,'', style = wx.TE_MULTILINE)
        self.text_ctrl_g3   = wx.TextCtrl(self.panel_left, -1,'', style = wx.TE_MULTILINE)
        self.text_ctrl_g4   = wx.TextCtrl(self.panel_left, -1,'', style = wx.TE_MULTILINE)
        self.text_ctrl_drag = wx.TextCtrl(self.panel_left, -1,'')
        
        self.vList_waiting  = VirtualList(self, -1, style=wx.LC_REPORT)
        
        self.panel_clubListCtrls = wx.ScrolledWindow(self, -1)
        
        self.vList_g1 = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        self.vList_g2 = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        self.vList_g3 = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        self.vList_g4 = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        
        self.club_listCtrls = [ self.vList_g1, self.vList_g2, self.vList_g3, self.vList_g4]
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.panel_clubListCtrls.SetScrollbars(1,1,1,1)
        columns=( ('ID', 40), ('WAITING', 150), ('ADDR', 50))
        self.vList_waiting.SetColumns(columns)
        
        index = 0
        for l in self.club_listCtrls:
            club_id, club_name = clubs[index][0], clubs[index][1]
            columns=( ('ID', 40), (club_name, 150), ('ADDR', 50))
            l.SetColumns(columns)
            l.SetName(str(club_id))
            index += 1
 
    def __do_layout(self):
        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_left.Add(self.text_ctrl_pool, 1,0,0)
        sizer_left.Add(self.text_ctrl_g1, 1,0,0)
        sizer_left.Add(self.text_ctrl_g2, 1,0,0)
        sizer_left.Add(self.text_ctrl_g3, 1,0,0)
        sizer_left.Add(self.text_ctrl_g4, 1,0,0)
        sizer_left.Add(self.text_ctrl_drag, 1,0,0)
        self.panel_left.SetSizer(sizer_left)
        
        sizer_listCtrl_holder = wx.GridSizer(2, 2, 5, 5)
        
        sizer_listCtrl_holder.Add(self.vList_g1)
        sizer_listCtrl_holder.Add(self.vList_g2)
        sizer_listCtrl_holder.Add(self.vList_g3)
        sizer_listCtrl_holder.Add(self.vList_g4)
        self.panel_clubListCtrls.SetSizer(sizer_listCtrl_holder)
        
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.panel_left, 0, wx.EXPAND, 0)
        sizer_main.Add(self.vList_waiting,    0, wx.EXPAND | wx.ALL, 5)
        sizer_main.Add(self.panel_clubListCtrls, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
       
    def __do_main(self):
        pass
     
    def update_monitor(self):
        self.text_ctrl_pool.SetValue(str(self.vList_waiting.itemDataMap))
        self.text_ctrl_g1.SetValue(str(self.vList_g1.itemDataMap))
        self.text_ctrl_g2.SetValue(str(self.vList_g2.itemDataMap))
        self.text_ctrl_g3.SetValue(str(self.vList_g3.itemDataMap))
        self.text_ctrl_g4.SetValue(str(self.vList_g4.itemDataMap))
        
    def displayData(self):
        # load data 
        self.vList_waiting.SetItemMap(non_members) 
        # data fo each club_listCtrl
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