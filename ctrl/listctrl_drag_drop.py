import wx
import time
import os
import sys
import stat

import  data.images

from wx.lib.mixins.listctrl import ColumnSorterMixin
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin



class FileInfo(object):
    def __init__(self, path, date_created, date_modified, size):
        self.name = os.path.basename(path)
        self.path = path
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size




########################################################################
class MyListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        self.index = 0

    #----------------------------------------------------------------------
    def dropUpdate(self, path):
        file_stats = os.stat(path)
        creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                      time.localtime(file_stats[stat.ST_CTIME]))
        modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                      time.localtime(file_stats[stat.ST_MTIME]))
        file_size = file_stats[stat.ST_SIZE]
        if file_size > 1024:
            file_size = file_size / 1024.0
            file_size = "%.2f KB" % file_size

        pos = self.InsertStringItem(self.index, path)

        self.SetStringItem(pos, 1, creation_time)
        self.SetStringItem(pos, 2, modified_time)
        self.SetStringItem(pos, 3, str(file_size))

        self.index += 1



class FileDrop(wx.FileDropTarget):  #This is the file drop target
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)  #File Drop targets are subsets of windows
        self.window = window

    def OnDropFiles(self, x, y, filenames):   #FileDropTarget now fills in the ListOfFiles

        for DragAndDropFile in filenames:
            self.window.dropUpdate(DragAndDropFile) # update list control
        return True


class FileWindow(wx.Frame, ColumnSorterMixin):

    def __init__(self, parent, id, title):  #This will initiate with an id and a title
        wx.Frame.__init__(self, parent, id, title, size=(550, 300))

        hbox = wx.BoxSizer(wx.HORIZONTAL)  #These are layout items
        panel = wx.Panel(self, -1)  #These are layout items

        self.FileList = MyListCtrl(panel)  #This builds the list control box
        self.FileList.InsertColumn(0,'Filename',width=140)  #Here we build the columns
        self.FileList.InsertColumn(1,'Date Created',width=140)
        self.FileList.InsertColumn(2,'Date Modified',width=140)
        self.FileList.InsertColumn(3,'Size',wx.LIST_FORMAT_RIGHT, width=40)
        
        ColumnSorterMixin.__init__(self, 4)
        # data map used by sorting, needs to get update on drop
        self.itemDataMap = {}

        # up down images stuff
        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())
        self.FileList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        DropTarget = FileDrop(self.FileList)  #Establish the listctrl as a drop target
        self.FileList.SetDropTarget(DropTarget)  #Make drop target.

        hbox.Add(self.FileList, 1, wx.EXPAND)
        panel.SetSizer(hbox)
        self.Show(True)
        
    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.FileList

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

def main():
    ex = wx.App(redirect = True, filename = time.strftime("%Y%m%d%H%M%S.txt"))
    FileWindowObject = FileWindow(None, -1, 'List of Files and Actions')
    ex.MainLoop()

if __name__ == '__main__':
    main()