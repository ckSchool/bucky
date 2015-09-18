import wx

import wx.lib.mixins.listctrl as listmix

vListCurrentID = 0
group_id = 1
headings = (('item no',0),('group id',0),('subject',140),('staff id',0),('teacher',150),('pop',30),('loc',30))
        

g1 = {0:(10, "g1 andrew"), 1:(11,"andrew"), 2:(12,"andrew"), 3:(13,"andrew"), 4:(14,"andrew") }
g2 = {0:(6, "g2 andrew"), 7:(1,"andrew"), 8:(2,"andrew"), 9:(3,"andrew")}
g3 = {0:(3, "g3 andrew"), 4:(1,"andrew"), 5:(2,"andrew")}
g4 = {0:(1, "g4 andrew"), 2:(1,"andrew")}
g5 = {0:(0, "g5 andrew")}

dataset = {1:g1,2:g2,3:g3,4:g4,5:g5}

dataset_days = {1:((1, 1),),
                2:((1, 3), (2, 4)),
                3:((1, 5), (2, 4), (3, 4)),
                4:((1, 3), (2, 2), (3, 4), (4, 4)),
                5:((1, 1), (2, 4), (3, 4), (4, 4), (5, 2)) }

class VirtualList(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=id, columns=(('',50),('',50),('',50)), style=0):
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
        # why does this need to be called twice to kick in
        
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
    
    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return None

    #---------------------------------------------------
    # These methods are Used by the ColumnSorterMixin,
    # see wx/lib/mixins/listctrl.py

    def GetListCtrl(self):
        return self

    def GetSortImages(self):
        return self.il_symbols["sm_dn"],self.il_symbols["sm_up"]
    
    def sort(self, col):
        self._col = col
        self.SortItems(col)

    def SortItems(self, sorter=None):
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

        self.Refresh()                  #redrawing the list

    #---------------------------------------------------
    # These methods should be used to interact with the controler
    
    def SetItemMap(self, itemMap):
        
        self.DeleteAllItems()
        self.Refresh()
        if not itemMap:
            return

        first_row  = itemMap[0]
        item_count = len(first_row)
        col_count  = self.GetColumnCount()
        
        # --------------------------------
        if item_count > col_count:
            #rint" can't just InsertColumn"
            ''' File "C:\Users\Andrew\Documents\PyCkDbNew\myListCtrl.py", line 350, in __init__
                self.vlist_ctrl.SortListItems(2, 1)
                File "C:\Python27\lib\site-packages\wx-2.9.4-msw\wx\lib\mixins\listctrl.py", line 81, in SortListItems
                self._colSortFlag[col] = ascending
                IndexError: list assignment index out of range'''
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
        #rint"map set:"#, itemMap
        #This regenerates self.itemIndexMap and redraws the ListCtrl
        self.SortItems()
        
    def SetColumns(self, columns = (('',50),('',50))):
        """Brief: adds columns to the control
           Param. columns: a list of columns (("name1", width1), ("name2", width2),...)
        """
        self.DeleteAllColumns()
        i=0
        for col in columns:
            if len(col)==3: # ie col_format has been sent
                name, s, col_format = col
                self.InsertColumn(i, name, col_format)
                self.SetColumnWidth(i, s)
                i+=1
            else:
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
        global vListCurrentID
        self.currentItem = event.m_itemIndex
        vListCurrentID = self.currentItem

        event.Skip()

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        event.Skip()

    def OnItemDeselected(self, evt):
        self.currentItem = 0
    
    def OnGetItemImage(self, item):
        index =self.itemIndexMap[item]
        pass

    def OnGetItemAttr(self, item):
        index=self.itemIndexMap[item]
        try:
            flag=self.itemDataMap[index][2]
            return self.flag_attr_dict[flag]
        except:
            return None
  
    def selectItem(self,idx):
        self.SetItemState(idx, wx.LIST_STATE_SELECTED,wx.LIST_STATE_SELECTED)

       
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
      
        self.panel_filter = wx.Panel(self, -1)
        self.panel_main   = wx.Panel(self, -1)
        
        self.label_group      = wx.StaticText(self.panel_filter, -1, "Group")
        self.choice_group     = wx.Choice(self.panel_filter, -1, choices=["1", "2", "3","4", "5"])
        self.text_ctrl_result = wx.TextCtrl(self.panel_filter, -1, '')

        self.panel_ctrl_holder = wx.ScrolledWindow(self.panel_main, -1)
        self.panel_ctrl_holder.SetScrollbars(1,1,1,1)
        self.text_ctrl_details = VirtualList(self.panel_main)
  
        self.Bind(wx.EVT_CHOICE, self.OnGroup, self.choice_group)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def __set_properties(self):
        self.SetMinSize((1000,400))
        self.Maximize()
 
    def __do_layout(self):
        sizer_base    = wx.BoxSizer(wx.VERTICAL)
        sizer_main    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_filter  = wx.BoxSizer(wx.HORIZONTAL)
        
        self.sizer_listCtrl_holder = wx.BoxSizer(wx.VERTICAL)
        self.panel_ctrl_holder.SetSizer(self.sizer_listCtrl_holder)
        
        sizer_filter.Add(self.label_group,  0, 0, 0)
        sizer_filter.Add(self.choice_group, 0, 0, 0)
        sizer_filter.Add(self.text_ctrl_result, 1, 0, 0)
        self.panel_filter.SetSizer(sizer_filter)
        
        sizer_main.Add(self.panel_ctrl_holder, 1, wx.EXPAND, 0)
        sizer_main.Add(self.text_ctrl_details, 0, 0, 0)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_filter, 0, wx.EXPAND, 0)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
       
    def __do_main(self):
        self.choice_group.Select(0)
     
    def displayData(self):
        global group_number
        group_number= int(self.choice_group.GetStringSelection())
 
        self.purge_listCtrl_holder()

        res = dataset_days[group_number]
        for row in res:
            day, iid = row
            
            # create panel with heading & listCtrl
            newListCtrl = VirtualList(self.panel_ctrl_holder, -1)
            
            #name = " group %d" % group_id
            #newListCtrl.SetName(name)
            
            #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, newListCtrl)
            columns=((str(day),50),('d',50),('c',50))
            newListCtrl.SetColumns(columns)
           
            self.sizer_listCtrl_holder.Add(newListCtrl, 0, wx.ALL | wx.EXPAND, 20)
            
            data = dataset[iid]
            self.text_ctrl_result.SetValue(str(data))
            
            newListCtrl.SetItemMap(data)
            
        self.Layout()
        
    def OnListItemSelected(self, evt):
        obj = evt.GetEventObject()
        print obj.GetName()
        
    def getScheduleData(self, schedule_id):
        data = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        return data
   
    def OnGroup(self, evt):
        self.displayData()
        
    def OnSchool(self, evt):
        self.displayData()
        
    def purge_listCtrl_holder(self):
        self.sizer_listCtrl_holder.DeleteWindows()
        self.Layout()
        
            
if __name__ == "__main__":
    schYr = 2015
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()