import wx, gVar

from wx.lib.pubsub import pub

from myListCtrl import VirtualList

class itemPicker(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        tempheading = (("59 ",10), (" ",15), (" ",10))
        self.panel_source    = wx.Panel(self, -1)
        self.label_pool      = wx.StaticText(self.panel_source, -1, "Item pool")
        self.vlist_ctrl_pool = VirtualList(self.panel_source, tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.label_pool_note = wx.StaticText(self.panel_source, -1, "")

        self.panel_spc = wx.Panel(self, -1, size=((10,10)))

        self.panel_selection      = wx.Panel(self, -1)
        self.label_selection      = wx.StaticText(self.panel_selection, -1, "Items in selection")
        self.vlist_ctrl_selection = VirtualList(self.panel_selection, tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.label_selection_note = wx.StaticText(self.panel_selection, -1, "")
        
        self.vlist_ctrl_selection.Bind(wx.EVT_LEFT_DCLICK, self.OnSelectionDclick)
        self.vlist_ctrl_pool.Bind(wx.EVT_LEFT_DCLICK,      self.OnPoolDclick )

        self.__do_layout()
        self.__do_main()

    def __do_layout(self):
        sizer_main      = wx.BoxSizer(wx.HORIZONTAL)
        sizer_source    = wx.BoxSizer(wx.VERTICAL)
        sizer_selection = wx.BoxSizer(wx.VERTICAL)

        sizer_source.Add(self.label_pool,0,0,0)
        sizer_source.Add(self.vlist_ctrl_pool,1,wx.EXPAND,0)
        sizer_source.Add(self.label_pool_note,0,0,0)
        self.panel_source.SetSizer(sizer_source)

        sizer_selection.Add(self.label_selection,0,0,0)
        sizer_selection.Add(self.vlist_ctrl_selection,1,wx.EXPAND,0)
        sizer_selection.Add(self.label_selection_note,0,0,0)
        self.panel_selection.SetSizer(sizer_selection)

        sizer_main.Add(self.panel_source,1,wx.EXPAND ,0)
        sizer_main.Add(self.panel_spc, 0, 0, 0)
        sizer_main.Add(self.panel_selection,1,wx.EXPAND ,0)

        self.SetSizer(sizer_main)
        self.Layout()
        self.Center()

    def __do_main(self):
        self.parent = self.GetParent()

    def SetLabels(self, label1,label2):
        self.label_pool.SetLabelText(label1)
        self.label_selection.SetLabelText(label2)

    def SetListCtrl(self, h1, h2, sy):
        self.sortCol = 1
        self.symbols = sy
        self.setup_listctrl(self.vlist_ctrl_pool, h1 )
        self.setup_listctrl(self.vlist_ctrl_selection, h2)

    def PopulateLists(self, source_list, selection_list=()):
	#rint'item picker  Source:',source_list, '    Selection:', selection_list
	#rint
        self.initial_selection =  self.sel_list = selection_list

        try:
            self.initial_selection_ids = [i for i, n, m, o in self.initial_selection]

        except:
            self.initial_selection_ids = [i for i, n, m in self.initial_selection]
        self.listPool(source_list)

        self.SortByCol(self.sortCol)
	
    def RepopulateSourceList(self,source_list):
	self.listPool(source_list)
        self.SortByCol(self.sortCol)

    def setup_listctrl(self, list_ctrl, heading):
        list_ctrl.initList(self.symbols, heading)

    def listPool(self, source_list):
        self.pool_list = source_list
        self.SetItems()

    def SetItems(self):
        self.SetSourceItems(self.pool_list)
        self.SetSelectionItems(self.sel_list)

    def SetSourceItems(self, sourse_list):
	#rint'SetSourceItems', sourse_list
        DATA = self.makeDictionary(sourse_list)
        self.vlist_ctrl_pool.SetItemMap(DATA)

        if len(sourse_list)==1:
            txt = "( 1 ) Item in pool"
        else:
            txt = "( %d ) Items in pool" %  len(sourse_list)
        self.label_pool_note.SetLabelText(txt)

    def SetSelectionItems(self, selection_list):
	#rint'SetSelectionItems', selection_list
        self.sel_list = selection_list
        
        if len(selection_list)==1:
            txt = "( 1 ) Course Selected" 
        else:
            txt = "( %d ) Courses Selected" %  len(selection_list)
            
        self.label_selection_note.SetLabelText(txt)

        self.refreshSelection()

    def SortByCol(self, col):
        self.sortColSelec = col
        self.sortColPool  = col
        self.vlist_ctrl_pool.SortListItems(self.sortColPool, 1)
        self.vlist_ctrl_selection.SortListItems(self.sortColSelec, 1)

    def makeDictionary(self, mylist):
        index  = 0
        myDict = {}
        for row in mylist:
            newrow=[]
            for x in row:
                if x: x = str(x)
                else: x = ''
                newrow.append(x)

            newrow[0]     = int(newrow[0])
            newrow        = tuple(newrow)
            myDict[index] = newrow
            index +=1

        return myDict

    def refreshSelection(self):
        DATA = self.makeDictionary(self.sel_list)
        self.vlist_ctrl_selection.SetItemMap(DATA)

    def OnOk(self):
        selection_ids = []
        for row in self.sel_list:
            selection_ids.append(row[0])

        remove = [x for x in self.initial_selection_ids if x not in selection_ids]
        add    = [x for x in selection_ids if x not in self.initial_selection_ids]

        return (add, remove)

    def OnAdd(self, event):
	selected_pool_id    = int(self.vlist_ctrl_pool.GetSelectedID())

        selected_pool_index = self.vlist_ctrl_pool.GetFirstSelected()
        selection_ids       =  self.vlist_ctrl_selection.GetAllIds()

        if selected_pool_id not in selection_ids:
            self.sel_list.append(self.pool_list[selected_pool_index])
            self.refreshSelection()
            self.SetItems()
	    
    def GetAllSelectionIds(self):
	return self.vlist_ctrl_selection.GetAllIds()

    def OnRemove(self, event):
        #rint'OnRemove'
	try:
	    remove_id     =  int(self.vlist_ctrl_selection.GetSelectedID())
	except: return
        remove_index = self.vlist_ctrl_selection.GetFirstSelected()
        
	## on initialisation need to creat list if courses that can not be removed
	courses_with_students = (1,2,3)
	if remove_id in courses_with_students:
	    txt = "failed test that no students associated with this class : id = %d" % remove_id
	    #rinttxt
	    print
	    return
        
        new_sel_list=[]
        
        for item in self.sel_list:
            item_id =   item[0]
            ##rintitem_id, remove_id
            if item_id != remove_id:
                ##rint"append : ", item
                new_sel_list.append(item)


        self.sel_list = new_sel_list

        self.refreshSelection()
        self.SetItems()

    def OnAll(self, event):
        self.vlist_ctrl_pool.SelectAll()

    def OnNone(self, event):
        self.vlist_ctrl_pool.SelectNone()

    def OnPoolDclick(self, event):
        self.OnAdd(event)

    def OnSelectionDclick(self, event):
        self.OnRemove(event)
