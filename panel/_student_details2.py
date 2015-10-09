import wx,  gVar
import fetchodbc as fetch

from panel_cSiswa_details    import cSiswaDetails as cSiswaDetails
from PanelGuardianData import PanelGuardianData

class student_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_ctrls = wx.Panel(self, -1)
        self.button_back = wx.Button(self.panel_ctrls, -1, "<Back",  style=wx.NO_BORDER)
        self.panel_spc   = wx.Panel(self.panel_ctrls,  -1)
        self.button_edit = wx.Button(self.panel_ctrls, -1, "Edit ",  style=wx.NO_BORDER)
        
        self.panel_student_bio = cSiswaDetails(self, -1)
    
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBack, self.button_back)

    def __set_properties(self):
        self.SetBackgroundColour((200,200,200))

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_ctrls = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_ctrls.Add(self.button_back, 0, wx.LEFT, 0)
        sizer_ctrls.Add(self.panel_spc,   1, 0, 0)
        sizer_ctrls.Add(self.button_edit, 0, wx.RIGHT, 0)
        self.panel_ctrls.SetSizer(sizer_ctrls)
        
        sizer_main.Add(self.panel_ctrls,       0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_student_bio, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        
        sizer_main.Fit(self)
        self.sizer_main = sizer_main
        self.Layout()
        
    def displayData(self, student_id):
        #rint'panel_student_details.displayData', student_id
        
        self.panel_student_bio.displayData(student_id)
        self.contact_panels=[]
        
        if student_id:
            sql = "SELECT KOrangTua, KWali \
                     FROM Siswa \
                    WHERE CKID = %d" % int(student_id)
            details = fetch.getOneDict(sql)
            #rintsql, details
            if not details:
                #rint'no KOrangTua'
                return
            KOrangTua = details['KOrangTua']
            KWali     = details['KWali']
            
            if KOrangTua:
                sql = "SELECT * FROM OrangTua \
                    WHERE Kode = %d" % int(KOrangTua)
                details = fetch.getOneDict(sql)
    
                if details['NamaA']:
                    ##rintdetails['NamaA']
                    p=self.OnAddGuardian(wx.Event)
                    p.head('FATHER')
                    #p.labelHead.SetBackgroundColour((255, 200, 255))
                    p.displayData(student_id, KOrangTua, 'father')
                    
                if details['NamaI']:
                    ##rintdetails['NamaI']
                    p=self.OnAddGuardian(wx.Event)
                    p.head('MOTHER')
                    #p.labelHead.SetBackgroundColour((255, 255, 200))
                    p.displayData(student_id, KOrangTua, 'mother')
                    
            if KWali:
                sql = "SELECT * FROM Wali \
                    WHERE Kode = %d" % int(KWali)
                details = fetch.getOneDict(sql)
                ##rintsql, details
                p = self.OnAddGuardian()
                p.head('GUARDIAN')
                #p.labelHead.SetBackgroundColour((200, 255, 255))
                p.displayData(student_id, KWali, 'guardian')
        self.Layout()

        
    def OnBack(self, event):
        msg = "Close this panel and open bookings"
        ans = wx.MessageBox(msg, "Via Function", wx.YES_NO | wx.ICON_QUESTION)
        

    def OnAddGuardian(self, evt=wx.Event):
        p = PanelGuardianData(self, -1)
        self.contact_panels.Append(p)
        self.sizer_main.Add(p, 1, wx.EXPAND, 0)
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgEditStudentDetails(None, -1)
    try:
        gVar.user_id = 1
        dlg.displayData()
        dlg.ShowModal()
    finally:  dlg.Destroy()
    app.MainLoop()
