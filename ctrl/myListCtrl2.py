import wx, gVar

import wx.lib.mixins.listctrl as listmix
import cPickle

class VirtualList(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, columns=(('',50),('',50),('',50)), style=0):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT | wx.LC_VIRTUAL | style)
        
        listmix.ColumnSorterMixin.__init__(self, len(columns))
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        
        self.itemDataMap={}
        
        self.il = wx.ImageList(16, 16)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.il_symbols={}
        
        #adding some art (sm_up and sm_dn are used by ColumnSorterMixin
        #symbols can be added to self.il using SetSymbols
        symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}
        self.SetSymbols(symbols)
        
        #building the columns
        self.SetColumns(columns)
        
        #adding some attributes (colourful background for each item rows)
        self.attr1 = self.attr2 = self.attr3 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")
        self.attr2.SetBackgroundColour("light blue")
        self.attr3.SetBackgroundColour("purple")
        
        # set up a dictionary to map attr
        self.flag_attr_dict={}
        self.flag_attr_dict['Rock']    = self.attr2
        self.flag_attr_dict['Roll']    = self.attr1
        self.flag_attr_dict['New Age'] = self.attr1
        
        #events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,   self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK,       self.OnColClick)
        
        self.currentItem = 0

    # for ctrl identification
    def setName(self, name='vlistCtrl'):
        self.SetName(name)

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...
    
    def GetCurrentItem(self):
        gVar.vListCurrentID = self.currentItem
        return self.currentItem

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s
    
    def decorateBanding(self):
        c = self.GetItemCount()
        
        if not c: return
        
        #rint ' self.GetItemCount()', self.GetItemCount()
        
        for index in range(c): 
            if (index%2)==0:
                #rint 'wx.Colour(215, 215, 235)'
                self.SetItemBackgroundColour(index,wx.Colour(215, 215, 235))
            else:
                #rint 'wx.Colour(255, 255, 255)'
                self.SetItemBackgroundColour(index,wx.Colour(255, 255, 255))

    def OnGetItemImage(self, item): return -1

    def OnGetItemAttr(self, item): return None

    #---------------------------------------------------
    # These methods are Used by the ColumnSorterMixin,
    # see wx/lib/mixins/listctrl.py

    def GetListCtrl(self):   return self

    def GetSortImages(self): return self.il_symbols["sm_dn"],self.il_symbols["sm_up"]
    
    def sort(self, col):
        self._col = col
        self.SortItems(col)

    def SortItems(self, sorter=None):
        #rint 'sort by col', self._col
        """
        Brief: A SortItem which works with virtual lists
        The sorter is not actually used (should it be?) """
        
        # These are actually defined in ColumnSorterMixin
        # col is the column which was clicked on and
        # sf, the sort flag is False for descending (Z->A)
        # and True for ascending (A->Z).
        
        col =self._col
        sf  =self._colSortFlag[col]
        
        items=[]#creating pairs [column item defined by col, key]
        for k,v in self.itemDataMap.items(): items.append([v[col], k])
        
        items.sort()                    #sort the pairs by value (first element), then by key (second element).
                                        #Multiple same values are okay, because the keys are unique.
        k=[key for value, key in items] #getting the keys associated with each sorted item in a list
        if sf==False:    k.reverse()    #False is descending (starting from last)
        self.itemIndexMap=k             #storing the keys as self.itemIndexMap (is used in OnGetItemText,Image,ItemAttr)
        
        self.decorateBanding()
        
        self.Refresh()                  #redrawing the list

    #---------------------------------------------------
    # These methods should be used to interact with the
    # controler
    
    def SetItemMap(self, itemMap):
        print'vList > SetItemMap > ', itemMap
        self.DeleteAllItems()
        self.Refresh()
        if not itemMap:
            #rintitemMap, 'is not an itemMap'
            return
        
        first_row  = itemMap[0]
        txt = 'session %d' % first_row[0]
        x = 8
        #self.SetColumns(((txt, 50), (str(x), 50), (str(x), 50), (str(x), 50), (str(x), 50)))
        
        
                
        item_count = len(first_row)
        col_count  = self.GetColumnCount()
        
        # reduces number of columns in the ListCtrl to match the data set size
        if item_count > col_count:
            print 'too many items for columns'
            return 
              
        elif item_count < col_count:
            while item_count < self.GetColumnCount():
                self.DeleteColumn(self.GetColumnCount()-1)
                
        """
        Brief: sets the items to be displayed in the control
        Param itemMap: a dictionary {id1:("item1","item2",...), 
        id2:("item1","item2",...), ...} and ids are unique  """
        
        l=len(itemMap)
        self.itemDataMap=itemMap
        self.SetItemCount(l)
        print "map set:", itemMap
        
        # This where the real work gets done
        # SortItems regenerates self.itemIndexMap and redraws the ListCtrl
        self.SortItems()
        
    def SelectAll(self):
        self.Freeze()
        for i in range(self.GetItemCount()):
            self.SetItemState(i, wx.LIST_STATE_SELECTED,wx.LIST_STATE_SELECTED)
        self.Thaw() 
        
    def SelectNone(self):
        self.Freeze()
        for i in range(self.GetItemCount()):
            self.Select(i,0)
        self.Thaw()
        
    def SetColumns(self, columns = (('',50),('',50))):
        """Brief: adds columns to the control
           Param. columns: a list of columns (("name1", width1), ("name2", width2),...)
        """
        self.DeleteAllColumns()
        i=0
        for col in columns:
            ##rintcol
            if len(col)==3: # ie col_format has been sent
                ##rint'Formating Column'
                name, s, col_format = col
                #rint name, s
                self.InsertColumn(i, name, col_format)
                self.SetColumnWidth(i, s)
                i+=1
            else:
                ##rint'Just Labeling Column'
                name, s = col
                self.InsertColumn(i, name)
                self.SetColumnWidth(i, s)
                i+=1
                
        listmix.ColumnSorterMixin.__init__(self, len(columns))

    def SetSymbols(self, symbols, provider=wx.ART_TOOLBAR):
        """Brief: adds symbols to self.ImageList
           Symbols are provided by the ArtProvider
           Param symbols: a dictionary of the form:
           {"name1":wx.ART_ADD_BOOKMARK,"name2":wx.ART_DEL_BOOKMARK,...}
           Param provider: an optional provider
        """
        for k, v in symbols.items():
            self.il_symbols[k] = self.il.Add(wx.ArtProvider_GetBitmap(v, provider, (16,16))) 
                
    def OnColClick(self,event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        gVar.vListCurrentID = self.currentItem

        event.Skip()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()

    def OnItemDeselected(self, evt):
        self.currentItem = 0
    
    def OnGetItemImage(self, item):
        # how to make this definable?
        index =self.itemIndexMap[item]
        status=self.itemDataMap[index][1]
        if   status=="paid":   return self.il_symbols["paid_idx"]
        elif status=="leave":  return self.il_symbols["leave_idx"]
        elif status=="stay":   return self.il_symbols["stay_idx"]
        elif status=="retake": return self.il_symbols["retake_idx"]
        else:                  return -1

    def OnGetItemAttr(self, item):
        # how to make this definable?
        index=self.itemIndexMap[item]
        try:
            flag=self.itemDataMap[index][2]
            return self.flag_attr_dict[flag]
        except:
            return None

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()
        
    def get_selected_id(self):
        selected_id = self.getColumnText(self.currentItem, 0)
        try:    return int(selected_id)
        except: return 0
    
    def getSelectedFlag(self):
        selected_flag = self.getColumnText(self.currentItem, 1)
        if selected_flag: return selected_flag
        else: return ''
    
    def setSelectedFlag(self, flag):
        self.SetItem(self.currentItem, 1, flag)

    def GetSelectedID(self):
        """
        Gets current selected item id.
        """
        index = self.GetFirstSelected()
        try:
            myid = self.getColumnText(index, 0)
            return int(myid)
        except:
            return None
    
    def GetSelectedIDs(self):
        """
        Gets a list if selected item ids from the list control.
        """
        selection = []
        index = self.GetFirstSelected()
        if index >- 1:
            
            #index = self.GetFirstSelected()
            selection.append(selected_id)
            while len(selection) != self.GetSelectedItemCount():
              selected_id = self.getColumnText(self.GetNextSelected(index), 0)
              selection.append(selected_id)
            
        return selection
    
            
    
    def GetSelectedItems(self):
        """
        Gets the selected items for the list control.
        Selection is returned as a list of selected indices,
        from low to high.
        """
        selection = []
        index = self.GetFirstSelected()
        if index>-1:
            # index = self.GetFirstSelected()
            selection.append(index)
            while len(selection) != self.GetSelectedItemCount():
              index = self.GetNextSelected(index)
              selection.append(index)
            
        return selection
    
    def GetId_firstSelected(self):
        return self.GetFirstSelected()
    
    def GetAllIds(self):
        """
        Gets the selected items for the list control.
        returned as a list of selected indices,
        low to high.
        """
        item_ids = []
        items = self.GetItemCount()
        for index in range(items):
            item_ids.append(int(self.GetItemText(index,0)))
      
        return item_ids
    
    def GetIds_ofSelectedItems(self):
        """
        Gets the selected items for the list control.
        Selection is returned as a list of selected indices,
        fro  low to high.
        """
        selection = []
        index = self.GetFirstSelected()
        if index>-1:
            selection.append(int(self.GetItemText(index,0)))
            while len(selection) != self.GetSelectedItemCount():
              index = self.GetNextSelected(index)
              selection.append(int(self.GetItemText(index, 0)))
      
        return selection
    
    def GetIds_ofSelectedItems_withNoBatches(self):
        """
        Gets the selected items that have zero batch count 
        Selection is returned as a list of selected indices,
        from low to high.
        """
        item_count = self.GetSelectedItemCount()
        selection = []
        index = self.GetFirstSelected()
        c = 0 
        if c <= item_count:
            c +=1
            batch_count = self.GetItemText(index, 5)
            if batch_count =='0' or batch_count =='' :
                selection.append(int(self.GetItemText(index, 0)))
            else:
                pass
                #rint "this course can't be be removed because it has batch"
            index = self.GetNextSelected(index)
            #selection.append(int(self.GetItemText(index, 0)))
        return selection  
    
    def selectItem(self,idx):
        self.SetItemState(idx, wx.LIST_STATE_SELECTED,wx.LIST_STATE_SELECTED)

    def render(self, bak, front):
        self.SetBackgroundColour(bak)
        self.SetForegroundColour(front)
 
    def initList(self, symbols, heading):
        self.SetSymbols(symbols)
        self.SetColumns(heading)
        self.SortListItems(1, 1)
