import wx,  gVar, fetch

from panel_student_bio   import panel_student_bio
from panel_guardian_data import panel_guardian_data

class panel_student_details(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_ctrls = wx.Panel(self, -1)
        
        self.button_edit = wx.Button(self.panel_ctrls, -1, "Edit ",  style=wx.NO_BORDER)
        
        self.panel_student_bio = wx.Panel(self, -1)#panel_student_bio(self, -1)
    
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass
        #self.SetBackgroundColour((200,200,200))

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_ctrls = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_ctrls.Add(self.button_edit, 0, wx.RIGHT, 0)
        self.panel_ctrls.SetSizer(sizer_ctrls)
        
        sizer_main.Add(self.panel_ctrls,       0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_student_bio, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.sizer_main = sizer_main
        self.Layout()
        
    def displayData(self, student_id):
        print 'panel_student_details.displayData', student_id
        return
        self.panel_student_bio.displayData(student_id)
        self.contact_panels=[]
        
        if student_id:
            sql = "SELECT mother_id, father_id, guardian_id \
                     FROM students \
                    WHERE id = %d" % int(student_id)
            details = fetch.getOneDict(sql)
            print sql, details
            if not details:
                print 'no guardians'
                return
            mother_id   = details['mother_id']
            father_id   = details['mother_id']
            guardian_id = details['guardian_id']
            
            if father_id:
                sql = "SELECT * \
                         FROM guardians \
                        WHERE id = %d" % int(mother_id)
                details = fetch.getOneDict(sql)
    
                if details['name']:
                    p=self.OnAddGuardian(wx.Event)
                    p.head('FATHER')
                    p.displayData(student_id, mother_id, 'father')
                    
            if mother_id:
                sql = "SELECT * FROM guardians \
                        WHERE id = %d" % int(mother_id)
                details = fetch.getOneDict(sql)
    
                if details['name']:
                    #print details['name']
                    p=self.OnAddGuardian(wx.Event)
                    p.head('MOTHER')
                    #p.labelHead.SetBackgroundColour((255, 200, 255))
                    p.displayData(student_id, mother_id, 'mother')
                    
            if guardian_id:
                sql = "SELECT * \
                         FROM guardians \
                        WHERE id = %d" % int(guardian_id)
                details = fetch.getOneDict(sql)
                
                p = self.OnAddGuardian()
                p.head('GUARDIAN')
                
                p.displayData(student_id, guardian_id, 'guardian')
                
        self.Layout()

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
