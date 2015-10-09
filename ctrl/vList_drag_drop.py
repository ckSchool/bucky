# dragDrop_vListCtrl

import wx, math

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

import data.images  as images

import wx.lib.mixins.listctrl as listmix

symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}
draglist = []

class VirtualList(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=id, columns=(('',50),('',50),('',50)), style=0):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT | wx.LC_VIRTUAL | style)
        
        listmix.ColumnSorterMixin.__init__(self, len(columns))
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        self.itemDataMap = {}
        self.il = wx.ImageList(16, 16)
        self.il_symbols  = {}
        self.dropFlag = True
        
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.SetSymbols(symbols)
        self.SetColumns(columns) # this need to be called twice to kick in, why?
    
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

    def OnItemDeselected(self, event): self.currentItem = 0
    
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
        
        items.sort()                      #sort the pairs by value (first element), then by key (second element).
        k = [key for value, key in items] #getting the keys associated with each sorted item in a list
        if sf == False:    k.reverse()    #False is descending (starting from last)
        self.itemIndexMap = k             #storing the keys as self.itemIndexMap (is used in OnGetItemText,Image,ItemAttr
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

    def GetSelectedItems(self):
        """  Gets the selected items for the list control.
        Selection is returned as a list of selected indices, low to high.
        """
        selection = []
        index = self.GetFirstSelected()
        selection.append(index)
        while len(selection) != self.GetSelectedItemCount():
            index = self.GetNextSelected(index)
            selection.append(index)
        return selection
    
    def _startDrag(self, event):
        global draglist
        self.dropFlag = False

        """ Put together a data object for drag-and-drop _from_ this list. """
        # we want to support multi item drag - how?
        selectedItemsList = self.GetSelectedItems()
        removelist = []
        draglist   = []
        for key in selectedItemsList:
            idx, what, student_id, name, form = self.GetItemInfo(key)
            student_id = int(student_id)
            removelist.append(student_id)
            
            data = (student_id, name, form)
            draglist.append(data)
            
        # Now make a signaling flag item list.
        ldata = wx.CustomDataObject("ListCtrlItems")
        ldata.SetData('True')
        
        # Now make a data object for the  item list.
        dropDataObj = wx.DataObjectComposite()
        dropDataObj.Add(ldata)
        
        dropSource = wx.DropSource(self)
        dropSource.SetData(dropDataObj)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)
        
        # If move, we want to remove the item from this list.
        newdixt = {}
        if res == wx.DragMove:
            mydict = self.itemDataMap
            for key in removelist:
                mydict = { k : v for k, v in mydict.iteritems() if mydict[k][0] != key }
            self.itemDataMap = mydict
            self.regen_dict()
            self.loadMap()
        self.Refresh()
        self.dropFlag = True
            
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
        if not self.dv.dropFlag: return 0
        if self.GetData(): # boolian flage
            for item in draglist:
                self.dv.AppendItem(item)
        return d