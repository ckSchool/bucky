import wx
import wx.lib.mixins.listctrl  as  listmix

import sys
import time
        



class vListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, style ):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
  
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, 995)
  
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,   self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,  self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK,       self.OnColClick)
        
        
        
    """def main(self):
        #self.addColours()
        headings = (("Artist", 150), ("Title", 220), ("Genre", 100))
        self.buildColumns(headings)
        self.addArt()
        self.PopulateList(musicdata)
        self.SortListItems(2, 1)
        self.banding()"""
        
        
    def PopulateList(self, data):
        #These two should probably be passed to init more cleanly
        #setting the numbers of items = number of elements in the dictionary
        self.itemDataMap = data
        self.itemIndexMap = data.keys()
        #rint "self.itemIndexMap", self.itemIndexMap
        self.SetItemCount(len(data))
        self.currentItem = 0
        #rint 'len(data)=', len(data)

    def buildColumns(self, headings):
        self.DeleteAllColumns()
        col = 0
        for item in headings:
            self.InsertColumn(col, item[0])
            self.SetColumnWidth(col, item[1])
            col += 1
        listmix.ColumnSorterMixin.__init__(self, len(headings))
            
    def GetColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()
    
    def banding(self, odd=(wx.Colour(255, 255, 255)), even=(wx.Colour(215, 215, 235))):
        c = self.GetItemCount()
        if c: 
            for index in range(c):
                if (index%2)==0:
                    self.SetItemBackgroundColour(index, wx.Colour(255, 255, 255))
                else:
                    self.SetItemBackgroundColour(index, wx.Colour(215, 215, 235))
        
    def addArt(self):
        #adding some art
        self.il = wx.ImageList(16, 16)
        a={"sm_up":"GO_UP","sm_dn":"GO_DOWN","w_idx":"WARNING","e_idx":"ERROR","i_idx":"QUESTION"}
        for k,v in a.items():
            s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (k,v)
            exec(s)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
    def OnColClick(self,event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        #self.currentItem,
        #self.GetItemText(self.currentItem),
        #self.getColumnText(self.currentItem, col),

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        #self.GetItemText(self.currentItem)
        #self.GetTopItem()))

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        pass
        # evt.m_itemIndex)


    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...

    def OnGetItemText(self, item, col):
         
        index = self.itemIndexMap[item]
        #rint "index=", index, 'col=', col
        s = self.itemDataMap[index][col]
        return s


    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items

        self.Refresh()

    def GetListCtrl(self):   return self

    def GetSortImages(self): return (self.sm_dn, self.sm_up)

    def OnGetItemImage(self, item):
        return -1
        """
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]

        if genre=="Rock":      return self.w_idx
        elif genre=="Jazz":    return self.e_idx
        elif genre=="New Age": return self.i_idx
        else:             return -1"""

    def OnGetItemAttr(self, item):
        return None
        """
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]

        if genre=="Rock":        return self.attr2
        elif genre=="Jazz":      return self.attr1
        elif genre=="New Age":   return self.attr3
        else:                    return None"""
               
    def addColours(self):
        #adding some attributes (colourful background for each item rows)
        self.attr1 = wx.ListItemAttr()
        #self.attr1.SetBackgroundColour("yellow")
        self.attr2 = wx.ListItemAttr()
        #self.attr2.SetBackgroundColour("light blue")
        self.attr3 = wx.ListItemAttr()
        #self.attr3.SetBackgroundColour("purple")
#----------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, size, style = wx.DEFAULT_FRAME_STYLE ):
        wx.Frame.__init__(self, parent, id, title, size=size, style=style)
        self.CreateStatusBar(1)
        lst = vListCtrl(self, style=wx.LC_HRULES)
        
        headings = (("Artist", 150), ("Title", 220), ("Genre", 100))
        musicdata = {
                1 : ("Bad English", "The Price Of Love", "Rock"),
                2 : ("DNA featuring Suzanne Vega", "Tom's Diner", "Rock"),
                3 : ("George Michael", "Praying For Time", "Rock"),
                4 : ("Gloria Estefan", "Here We Are", "Rock"),
                5 : ("Linda Ronstadt", "Don't Know Much", "Rock")
                }
        
        lst.buildColumns(headings)
        lst.addArt()
        lst.PopulateList(musicdata)
        lst.SortListItems(2, 1)
        lst.banding()
        

if __name__ == "__main__":
    app = wx.App(redirect=False)
    f = TestFrame(None, -1, "ColumnSorterMixin used with a Virtual ListCtrl",wx.Size(500,300))
    f.Show()
    app.MainLoop()