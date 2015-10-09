import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb
from  wx.lib import masked

#import DlgAddrItemEdit, re

class panel_edit_address_sumut(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_postcode     = wx.StaticText(self, -1, "Postcode")
        self.num_ctrl_postcode  = masked.NumCtrl(self, value=0, integerWidth=5, groupDigits=False, allowNegative=False)#wx.TextCtrl(  self, -1, "")
        self.label_kabupaten    = wx.StaticText(self, -1, "Kabupaten")
        self.combo_box_kab      = wx.ComboBox(  self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_kecamatan    = wx.StaticText(self, -1, "Kecamatan")
        self.combo_box_kec      = wx.ComboBox(  self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.lable_kelurahan    = wx.StaticText(self, -1, "Kelurahan")
        self.combo_box_kel      = wx.ComboBox(  self, -1, choices=[], style=wx.CB_DROPDOWN)
        
        self.combos = (self.combo_box_kab, self.combo_box_kec, self.combo_box_kel)

        self.Bind(wx.EVT_TEXT,     self.OnPostcode, self.num_ctrl_postcode)
        self.Bind(wx.EVT_COMBOBOX, self.OnKab,      self.combo_box_kab)
        self.Bind(wx.EVT_COMBOBOX, self.OnKec,      self.combo_box_kec)
        self.Bind(wx.EVT_COMBOBOX, self.OnKel,      self.combo_box_kel)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.label_postcode.SetMinSize((70, 21))

    def __do_layout(self):
        grid_sizer_pc     = wx.FlexGridSizer(4, 2, 5, 5)

        grid_sizer_pc.Add(self.label_postcode,     0, wx.EXPAND, 0)
        grid_sizer_pc.Add(self.num_ctrl_postcode,  0, 0, 0)
        
        grid_sizer_pc.Add(self.label_kabupaten,    0, wx.EXPAND, 0)
        grid_sizer_pc.Add(self.combo_box_kab,      0, wx.EXPAND, 0)
        
        grid_sizer_pc.Add(self.label_kecamatan,    0, wx.EXPAND, 0)
        grid_sizer_pc.Add(self.combo_box_kec,      0, wx.EXPAND, 0)
        
        grid_sizer_pc.Add(self.lable_kelurahan,    0, wx.EXPAND, 0)
        grid_sizer_pc.Add(self.combo_box_kel,      0, wx.EXPAND, 0)
        
        self.SetSizer(grid_sizer_pc)
        grid_sizer_pc.AddGrowableCol(1)
        
        self.Layout()
        
    def loadAllCombos(self):
        loadCmb.kab(self.combo_box_kab, 'sumut')
        loadCmb.kec(self.combo_box_kec, 'sumut')
        loadCmb.kel(self.combo_box_kel, 'sumut')
        #rint'loaded all'
        
    def displayData(self, postcode=0):
        self.loadAllCombos()
        self.num_ctrl_postcode.SetValue(0)

        if postcode:
            sql = "SELECT * FROM postcodes WHERE postcode =%d" % postcode
            dataSet = fetch.getOneDict(sql)
            self.num_ctrl_postcode.SetValue(dataSet['postcode'])
            kelurahan, kecamatan, kabupaten = (dataSet('kelurahan'), dataSet('kecamatan'), dataSet('kabupaten'))
            
            if kelurahan:
                loadCmb.restore_str(self.combo_box_kab, kabupaten)
                self.loadCmbsUnderKab(kabupaten)
                
            elif kecamatan:
                loadCmb.restore_str(self.combo_box_kec, kecamatan)
                self.loadCmbsUnderKec(kecamatan)
                
            elif kelurahan:
                loadCmb.restore_str(self.combo_box_kel, kelurahan)
                self.loadCmbsUnderKal(kelurahan)
  
    def getValues(self):
        pc = self.num_ctrl_postcode.GetValue()
        kal = fetch.cmbValue(self.combo_box_kel)
        kec = fetch.cmbValue(self.combo_box_kec)
        kab = fetch.cmbValue(self.combo_box_kab)

        values  = "%d, %s, %s, %s" % (pc, kal, kec, kab, 'Sumatra Utara', 'Indonesia')

        return values

        
    def OnPostcode(self, event):
        postcode = self.num_ctrl_postcode.GetValue()
        if postcode:
            for c in self.combos:
                c.SetSelection(-1)
            
            sql = "SELECT kelurahan, kecamatan, kabupaten, province FROM postcodes \
                    WHERE  postcode = %d" % postcode
            
            res = fetch.getOneDict(sql)
            #rintsql, res
            if res:
                province  = res['province']
                kelurahan = res['kelurahan']
                kecamatan = res['kecamatan']
                kabupaten = res['kabupaten']
                if province == 'Sumatera Utara':
                    if kelurahan:
                        loadCmb.restore_str(self.combo_box_kel, kelurahan)
                        self.loadCmbsUnderKel(kelurahan)
                    elif kecamatan:
                        self.loadCmbsUnderKec(kecamatan)
                    elif kabupaten:    
                        self.loadCmbsUnderKab(kabupaten)
                else:
                    #rint'go back to other panel'

    def OnKab(self, event):
        self.num_ctrl_postcode.Clear()
        kabupaten = fetch.cmbValue(self.combo_box_kab)
        self.loadCmbsUnderKab(kabupaten)
        
    def loadCmbsUnderKab(self, kabupaten):
        #rint'loadCmbsUnderKab'
        sql = "SELECT kecamatan FROM postcodes \
                WHERE kabupaten = '%s' \
                GROUP BY (kecamatan) \
                ORDER BY (kecamatan)" % kabupaten
        
        loadCmb.setItems(self.combo_box_kec, sql)
        
        sql = "SELECT kelurahan FROM postcodes \
                WHERE kabupaten = '%s' \
                GROUP BY (kelurahan) \
                ORDER BY (kelurahan)" % kabupaten
        
        loadCmb.setItems(self.combo_box_kel, sql)
        
    def OnKec(self, event):
        self.num_ctrl_postcode.Clear()
        kecamatan = fetch.cmbValue(self.combo_box_kec)
        
        self.loadCmbsUnderKec(kecamatan)
        
    def loadCmbsUnderKec(self, kecamatan):
        #rint'loadCmbsUnderKec'
        sql = "SELECT kelurahan FROM postcodes \
                WHERE kecamatan = '%s' \
                GROUP BY (kelurahan) \
                ORDER BY (kelurahan)" % kecamatan
        self.combo_box_kel.Clear()
        loadCmb.setItems(self.combo_box_kel, sql)
        
        sql = "SELECT kabupaten FROM postcodes \
                WHERE kecamatan = '%s'" % kecamatan
        kabupaten = fetch.getStr(sql)
        loadCmb.restore_str(self.combo_box_kab, kabupaten)
    
    def OnKel(self, event):
        self.num_ctrl_postcode.Clear()
        kelurahan = fetch.cmbValue(self.combo_box_kel)
        
        self.loadCmbsUnderKel(kelurahan)
        
    def loadCmbsUnderKel(self, kelurahan):
        #rint'loadCmbsUnderKel'
        sql = "SELECT kecamatan FROM postcodes \
                WHERE kelurahan = '%s'" % kelurahan
      
        kecamatan = fetch.getStr(sql)
        loadCmb.restore_str(self.combo_box_kec, kecamatan)
        
        sql = "SELECT kabupaten FROM postcodes \
                WHERE kelurahan = '%s'" % kelurahan
      
        kabupaten = fetch.getStr(sql)
        loadCmb.restore_str(self.combo_box_kab, kabupaten)
        
        sql = "SELECT postcode FROM postcodes \
                WHERE kelurahan = '%s'" % kelurahan
        postcode = fetch.getDig(sql)
        
        self.num_ctrl_postcode.Freeze()
        self.num_ctrl_postcode.SetValue(postcode)
        self.num_ctrl_postcode.Thaw()
 
#-------------------------------------------------------------------------------
# address edit button events 
    def OnB_kelEditButton(self, event):
        self.openItemEditor(4)

    def OnB_kecEditButton(self, event):
        self.openItemEditor(5)

    def OnB_kabEditButton(self, event):
        self.openItemEditor(6)
        
    def openItemEditor(self, itemType_id):
        cmb = self.addrCmbs[str(itemType_id)]
        id = int(fetch.cmbID(cmb))
            
        dlg=DlgAddrItemEdit.create(None)
        dlg.displayData(int(itemType_id), int(id))
        try:
            if dlg.ShowModal() == wx.ID_OK:
                pass##rint"ok"
            else:
                pass##rint"cancel"
        finally:    
            dlg.Destroy()

"""            
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1)
        
        p = self.panel_edit_address = panel_edit_address(self, -1)
	p2 = panel_edit_address_sumut(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(p, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Center()
        self.Fit()
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
app = MyApp(redirect=False)
app.MainLoop()"""