import wx
from wx.lib.agw import ultimatelistctrl as ULC
import sys
import os
import random
import datetime
import math

import wx.lib.mixins.listctrl as listmix
import wx.lib.colourdb as cdb
import wx.lib.colourselect as csel


data = {'CONTRACT_TERM':'TEST'}

class DataXfervalidator(wx.PyValidator):
    def __init__(self, data, key):
        wx.PyValidator.__init__(self)
        self.data = data
        self.key = key
        #self.TransferFromWindow()
        ##rint"validating"
        #rintdata
        #rint"VALIDATOR CLASS TRIGGRED"
        ##rintkey
        
    def Clone (self):
        #rint"VAL CLONE TRIGGERED"
        return DataXfervalidator(self.data, self.key)
    
    def Validate(self):
        #rint'here we go'
    
    
    def TransferToWindow(self):
        #rint"TransferTO"
        #rintdata
        textCtrl = self.GetWindow()
        textCtrl.SetValue(self.data.get(self.key, ""))
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        #rint"TransferFROM"
        ##rinttextCtrl
        self.data[self.key] = textCtrl.GetValue()
        #rintdata
        return True

class TestUltimateListCtrl(ULC.UltimateListCtrl):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, extraStyle=0):
        
        ULC.UltimateListCtrl.__init__(self, parent, id, pos, size, style, extraStyle)
    
    
class UltimateListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS|wx.SUNKEN_BORDER)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.list = TestUltimateListCtrl(self, -1,
                                         style=wx.LC_REPORT
                                         #| wx.BORDER_SUNKEN
                                         | wx.BORDER_NONE
                                         | wx.LC_EDIT_LABELS
                                         #| wx.LC_SORT_ASCENDING
                                         #| wx.LC_NO_HEADER
                                         | wx.LC_VRULES
                                         | wx.LC_HRULES
                                         )
        sizer.Add(self.list, 1, wx.EXPAND)
        
        self.PopulateList()
        self.TransferDataFromWindow()
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
    
    def PopulateList(self):

        self.list.Freeze()
        
        info = ULC.UltimateListItem()
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_CHECK
        info._image = []
        info._format = 0
        #info._kind = 1
        info._text = "CONTRACT"
        
        self.list.TransferDataToWindow()
        self.list.InsertColumnInfo(0, info)
        index = self.list.InsertStringItem(sys.maxint,'')
        item = self.list.GetItem(0, 0)
        textctrl = wx.TextCtrl(self.list, -1, "", validator=DataXfervalidator(data,'CONTRACT_TERM'))
        ##textctrl = wx.TextCtrl(self.list, -1, "", style=wx.TE_MULTILINE)
        item.SetWindow(textctrl)
        self.list.SetItem(item)
        #self.list.TransferDataFromWindow()
        #textctrl.TransferDataToWindow()
        
        
        
        self.list.SetColumnWidth(0, 100)
 
        self.list.Thaw()
        self.list.Update()
    
    
    
class MiniFrame(wx.MiniFrame):
    def __init__(self):
        wx.MiniFrame.__init__(self, None, -1, 'Mini Frame', size=(800, 600),style=wx.DEFAULT_FRAME_STYLE)
        self.ulc = UltimateListCtrlPanel(self)
        
        #button = wx.Button(self.ulc, -1, "Close Me", pos=(15, 15))
        #self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
    
        
        
    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()    

app = wx.App(None)
MiniFrame().Show()
app.MainLoop()        
        