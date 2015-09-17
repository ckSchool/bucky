import wx, gVar

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from myListCtrl import VirtualList

class PanelListSwap(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
	tempheading = ((" ",10), (" ",15), (" ",10))
        self.panel_source    = wx.Panel(self, -1)
        self.label_pool      = wx.StaticText(self.panel_source, -1, "Item pool")
	self.vlist_ctrl_pool = VirtualList(self.panel_source, tempheading, style = wx.LC_HRULES)
	
	self.panel_spc = wx.Panel(self, -1, size=((10,10)))
	
	self.panel_selection = wx.Panel(self, -1)
        self.label_selection = wx.StaticText(self.panel_selection, -1, "Items in selection")
        self.vlist_ctrl_selection = VirtualList(self.panel_selection, tempheading, style = wx.LC_HRULES)
        
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
	self.panel_source.SetSizer(sizer_source)
	
	sizer_selection.Add(self.label_selection,0,0,0)
	sizer_selection.Add(self.vlist_ctrl_selection,1,wx.EXPAND,0)
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
	self.symbols           = sy
	self.setup_listctrl(self.vlist_ctrl_pool,  h1 )
	self.setup_listctrl(self.vlist_ctrl_selection, h2)
	
    def PopulateLists(self, source_list, selection_list=()):
        self.initial_selection =  self.sel_list = selection_list
	
        try:
	    self.initial_selection_ids = [i for i, n, m, o in self.initial_selection]
	    
        except:
	    self.initial_selection_ids = [i for i, n, m in self.initial_selection]
        self.listPool(source_list)
        
        self.vlist_ctrl_pool.SortListItems(1, 1)
        self.vlist_ctrl_selection.SortListItems(1, 1)
                
    def setup_listctrl(self, list_ctrl, heading):
        list_ctrl.initList(self.symbols, heading)
        
    def listPool(self, source_list):
        self.pool_list = source_list
        self.SetItems()
	
    def SetItems(self):
	self.SetSourceItems(self.pool_list)
	self.SetSelectionItems(self.initial_selection)

    def SetSourceItems(self, items):
        DATA = self.makeDictionary(items)
        self.vlist_ctrl_pool.SetItemMap(DATA)
            
        txt = "( %d ) Items in pool" %  len(items)  
        self.label_pool.SetLabelText(txt)

    def SetSelectionItems(self, list):
        self.sel_list = list
            
        self.refreshSelection()
        return self.sel_list  
    
    def makeDictionary(self, mylist):
	# ecpecting (2, ('name', 'etc'))
	#print mylist
	index  = 0
	myDict = {}
	for row in mylist:
	    #print row
	    newrow=[]
	    for x in row:
		if x: x = str(x)
		else: x = ''
		newrow.append(x)
    
	    newrow[0]     = int(newrow[0])
	    newrow        = tuple(newrow)
	    myDict[index] = newrow
	    index +=1
	    
	#print 'myDict ', myDict
	return myDict

    def refreshSelection(self):
        records = len(self.sel_list)
        DATA = self.makeDictionary(self.sel_list)
        self.vlist_ctrl_selection.SetItemMap(DATA)
        self.sel_list_dict = DATA
    
    def OnOk(self):
        selection_ids = []
        for row in self.sel_list:
            selection_ids.append(row[0])
  
        remove = [x for x in self.initial_selection_ids if x not in selection_ids]
        add    = [x for x in selection_ids if x not in self.initial_selection_ids]
        
        return (add, remove)

    def OnAdd(self, event):
        remove_ids = self.vlist_ctrl_pool.GetIds_ofSelectedItems()
        
        new_sel_list=[]
        new_sel_list[:]  = [x for x in self.pool_list if x[0] in remove_ids]
        
        new_pool_list=[]
        new_pool_list[:] = [x for x in self.pool_list if not x[0] in remove_ids]
        
	if not new_sel_list:  new_sel_list=[]
	if not self.sel_list: self.sel_list=[]

        self.sel_list  += new_sel_list
        self.pool_list = new_pool_list
        
        self.refreshSelection()
        self.SetItems()
        
    def OnAll(self, event):
        self.vlist_ctrl_pool.SelectAll()
        
    def OnNone(self, event):
        self.vlist_ctrl_pool.SelectNone()

    def OnPoolDclick(self, event):
        self.OnAdd(event)
    
    def OnRemove(self, event):
        remove_ids = self.vlist_ctrl_selection.GetIds_ofSelectedItems()
        
        new_sel_list=[]
        new_sel_list[:] = [x for x in self.sel_list if not x[0] in remove_ids]
        
        new_pool_list=[]
        new_pool_list[:] = [x for x in self.sel_list if x[0] in remove_ids]
        
        self.sel_list = new_sel_list
        self.pool_list += new_pool_list
        
        self.refreshSelection()
        self.SetItems()
        
    def OnSelectionDclick(self, event):
        self.OnRemove(event)
