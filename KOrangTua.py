import wx
import fetchodbc  as fetch
from pyodbc import DATETIME

from myListCtrl import VirtualList

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        tempheading = ((" ",10), (" ",15), (" ",10))
        
        self.label_heading = wx.StaticText(self, -1, "Campare and update CSiwa > Siswa KOrangTua KWali\n")
        self.panel_base    = wx.Panel(self, -1)
        
        self.panel_cSiswa     = wx.Panel(self.panel_base, -1)
        self.label_cSiswa     = wx.StaticText(self.panel_cSiswa, -1, "CSiswa")
        self.list_ctrl_cSiswa = VirtualList(self.panel_cSiswa,  tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        self.panel_centre = wx.Panel(self.panel_base, -1)
        self.spcp1 = wx.Panel(self.panel_centre, -1)
        self.button_copy = wx.Button(self.panel_centre, -1, " << Copy \n Kodes")
        self.spcp2 = wx.Panel(self.panel_centre, -1)
        self.button_2 = wx.Button(self.panel_centre, -1, "-")
        self.spcp3 = wx.Panel(self.panel_centre, -1)
        
        self.panel_right      = wx.Panel(self.panel_base, -1)
        self.label_siswa      = wx.StaticText(self.panel_right, -1, "siswa")
        self.list_ctrl_siswa  = VirtualList(self.panel_right,  tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.button_make_same = wx.Button(self.panel_right, -1, "-")

        self.Bind(wx.EVT_BUTTON, self.OnCopy, self.button_copy)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClickCSiswa, self.list_ctrl_cSiswa)
        
        self.Bind(wx.EVT_BUTTON, self.OnMakeSame, self.button_make_same)
        
        # for wxMSW
        self.list_ctrl_siswa.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.OnRightClickSiswa)
        # for wxGTK
        self.list_ctrl_siswa.Bind(wx.EVT_RIGHT_UP, self.OnRightClickSiswa)
        
        # for wxMSW
        self.list_ctrl_cSiswa.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.OnClick_cSiswa)
        # for wxGTK
        self.list_ctrl_cSiswa.Bind(wx.EVT_RIGHT_UP, self.OnClick_cSiswa)
        
        
        
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    


    def __set_properties(self):
        #self.SetSize((1280, 800))
        self.SetTitle("Update CSiswa KOrangTua and KWali")
        
        headingBookings = (('Kode',100), ('Nama',100), ('ThLahir',100))
        self.list_ctrl_cSiswa.SetColumns(headingBookings)
        
        headingBookings = (('id',100), ('Name',100), ('TgLahir',100), ('KParent',100), ('KWali',100))
        self.list_ctrl_siswa.SetColumns(headingBookings)


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        
        sizer_1.Add(self.label_heading, 0, 0, 0)
        sizer_3.Add(self.label_cSiswa, 0, 0, 0)
        sizer_3.Add(self.list_ctrl_cSiswa, 1, wx.EXPAND, 0)
        self.panel_cSiswa.SetSizer(sizer_3)
        
        sizer_2.Add(self.panel_cSiswa, 1, wx.EXPAND, 0)
        sizer_4.Add(self.spcp1, 1, wx.EXPAND, 0)
        sizer_4.Add(self.button_copy, 0, 0, 0)
        sizer_4.Add(self.spcp2, 1, wx.EXPAND, 0)
        sizer_4.Add(self.button_2, 0, 0, 0)
        sizer_4.Add(self.spcp3, 1, wx.EXPAND, 0)
        self.panel_centre.SetSizer(sizer_4)
        
        sizer_2.Add(self.panel_centre, 0, wx.EXPAND, 0)
        sizer_5.Add(self.label_siswa, 0, 0, 0)
        sizer_5.Add(self.list_ctrl_siswa, 1, wx.EXPAND, 0)
        sizer_5.Add(self.button_make_same, 0, 0, 0)
        self.panel_right.SetSizer(sizer_5)
        
        sizer_2.Add(self.panel_right, 1, wx.EXPAND, 0)
        self.panel_base.SetSizer(sizer_2)
        sizer_1.Add(self.panel_base, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        
    def __do_main(self):
        sql = "SELECT Kode, Nama, TgLahir FROM CSiswa WHERE KOrangTua IS Null AND KWali IS Null"
        results = fetch.DATA(sql)
        self.list_ctrl_cSiswa.SetItemMap(results)
        
    def OnMakeSame(self, evt):
        #rint'OnMakeSame'
            
    def OnRightClickSiswa(self, evt):
        #rint'OnRightClickSiswa'
        
    def OnClick_cSiswa(self, evt):
        import time
        from datetime import datetime
        
        self.list_ctrl_siswa.DeleteAllItems()
        sid = self.list_ctrl_cSiswa.get_selected_id()
        sql = "SELECT Nama, TgLahir FROM CSiswa WHERE Kode =%d" % sid
        
        res = fetch.getOneDict(sql)
       
        Nama    = res['Nama']
        TgLahir = res['TgLahir']
        
        
        if TgLahir:
            sql2 = "SELECT id, Nama, TgLahir, KOrangTua, KWali FROM Siswa WHERE Nama = '%s' AND TgLahir = #%s#" % (Nama, TgLahir )
            
        else:    
            sql2 = "SELECT id, Nama, TgLahir, KOrangTua, KWali FROM Siswa WHERE Nama = '%s' " % Nama
        #rintsql2
        results = fetch.DATA(sql2)
        self.list_ctrl_siswa.SetItemMap(results)
        
        
        """            sql2 = "SELECT Siswa.CKID, Siswa.Nama, Siswa.KOrangTua, Siswa.KWali \
                      FROM Siswa INNER JOIN CSiswa \
                        ON (Siswa.TgLahir = CSiswa.TgLahir AND Siswa.Nama = CSiswa.Nama ) \
                      WHERE CSiswa.Kode =%d" % sid # # AND Siswa.Nama = CSiswa.Nama) \ , Siswa.TgLahir Siswa.KOrangTua, Siswa.KWali
            
        """
        

    def OnClickSiswa(self, evt):
        #rint'OnClickSiswa'
    
    def OnClickCSiswa(self, evt):
        #rint'OnClickCSiswa'
        
    def OnCopy(self, evt):
        print'OnClickCSiswa'


if __name__ == "__main__":
    app = wx.App(0)
   
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
