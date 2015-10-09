"""DnD demo with listctrl.
- Dragging of multiple selected items.
- Dropping on an empty list.
- Dropping of items on a list with a different number of columns.
- Dropping on a different applications."""

import cPickle
import wx

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# DragList

class DragList(wx.ListCtrl):
    def __init__(self, *arg, **kw):
        wx.ListCtrl.__init__(self, *arg, **kw)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self._startDrag)

        dt = ListDrop(self)
        self.SetDropTarget(dt)

    def getItemInfo(self, idx):
        """Collect all relevant data of a listitem, and put it in a list"""
        l = []
        l.append(idx) # We need the original index, so it is easier to eventualy delete it
        l.append(self.GetItemData(idx)) # Itemdata
        l.append(self.GetItemText(idx)) # Text first column
        for i in range(1, self.GetColumnCount()): # Possible extra columns
            l.append(self.GetItem(idx, i).GetText())
        return l
    
    def _onStripe(self):
        if self.GetItemCount()>0:
            for x in range(self.GetItemCount()):
                if x % 2==0:
                    self.SetItemBackgroundColour(x,wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DLIGHT))
                else:
                    self.SetItemBackgroundColour(x,wx.WHITE)

    def _startDrag(self, e):
        """ Put together a data object for drag-and-drop _from_ this list. """
        l = []
        idx = -1
        while True: # find all the selected items and put them in a list
            idx = self.GetNextItem(idx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if idx == -1:
                break
            l.append(self.getItemInfo(idx))

        # Pickle the items list.
        itemdata = cPickle.dumps(l, 1)
        # create our own data format and use it in a
        # custom data object
        ldata = wx.CustomDataObject("ListCtrlItems")
        ldata.SetData(itemdata)
        # Now make a data object for the  item list.
        data = wx.DataObjectComposite()
        data.Add(ldata)

        # Create drop source and begin drag-and-drop.
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        res = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)

        # If move, we want to remove the item from this list.
        if res == wx.DragMove:
            # It's possible we are dragging/dropping from this list to this list.  In which case, the
            # index we are removing may have changed...

            # Find correct position.
            l.reverse() # Delete all the items, starting with the last item
            for i in l:
                pos = self.FindItem(i[0], i[2])
                self.DeleteItem(pos)

    def _insert(self, x, y, seq):
        """ Insert text at given x, y coordinates --- used with drag-and-drop. """

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

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ListDrop

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
            # convert it back to a list and give it to the viewer
            ldata = self.data.GetData()
            l = cPickle.loads(ldata)
            self.dv._insert(x, y, l)

        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# main

if __name__ == '__main__':
    items1 = [(2,'Aoo'), (4,'Bar'), (6,'Baz'), (7,'Cif'), ( 9,'Caf'), (10, 'Dof')]
    items2 = [(1,'Foo'), (3,'Gar'), (5,'Haz'), (8,'Zif'), (22,'Zaf'), (26, 'Zof')]
    
    class MyApp(wx.App):
        def OnInit(self):
            self.frame = wx.Frame(None, title='Main Frame')
            self.frame.Show(True)
            self.SetTopWindow(self.frame)
            return True

    app = MyApp(redirect=False)
    
    self.activity_dict = {1:'Chess', 2:'z',3:'y',4:'x'}
    self.id_list_dict = {}
    
    for key in self.activity_dict
        self.id_list_dict[key] = self.create_list()
    
    dl1 = DragList(app.frame, style=wx.LC_REPORT)
    dl2 = DragList(app.frame, style=wx.LC_REPORT)
    dl1.InsertColumn(0, "Chess",     0, 200)
    dl1.InsertColumn(1, "Class",     0, 50)
    dl2.InsertColumn(0, "Badminton", 0, 200)
    dl2.InsertColumn(1, "Class",     0, 50)
    sizer = wx.BoxSizer()
    app.frame.SetSizer(sizer)
    sizer.Add(dl1, proportion=1, flag=wx.EXPAND)
    sizer.Add(dl2, proportion=1, flag=wx.EXPAND)

    from random import choice
    from sys import maxint

    for item in items1:
        iid, txt = item
        idx = dl1.InsertStringItem(iid, txt)
        dl1.SetItemData(idx, iid)
        dl1.SetStringItem(idx, 1, 'XI')
        
    for item in items2:
        iid, txt = item
        idx = dl2.InsertStringItem(iid, txt)
        dl2.SetItemData(idx, iid)
        dl2.SetStringItem(idx, 1, 'VII')
        
        #dl2.SetStringItem(idx, 1, choice(items))
        #dl2.SetStringItem(idx, 2, choice(items))
        
    dl1._onStripe()
    dl2._onStripe()
    app.frame.Layout()
    app.MainLoop()