import wx, gVar, fetch, loadCmb

from datetime               import date
from DateCtrl               import DateCtrl

from panel_guardian_details import panel_guardian_details
from panel_bio              import panel_bio
from panel_education        import panel_education
from panel_medical          import panel_medical
from panel_payment_details  import panel_payment_details as panel_fees

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import DlgEditStudentDetails
import DlgNewStudent

tab_selected   = 'white'
tab_unselected = (240,245,250)

class panel_student_bio(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        tc = []
        
        self.panel_tabs       = wx.Panel(self, -1)
        self.panel_panels     = wx.Panel(self, -1)
        self.button_biodata   = wx.Button(self.panel_tabs, -1, 'Biodata',   style=wx.NO_BORDER)
        self.button_education = wx.Button(self.panel_tabs, -1, 'Education', style=wx.NO_BORDER)
        self.button_medical   = wx.Button(self.panel_tabs, -1, 'Medical',   style=wx.NO_BORDER)
        self.button_fees      = wx.Button(self.panel_tabs, -1, 'Fees',      style=wx.NO_BORDER)
        self.button_contacts  = wx.Button(self.panel_tabs, -1, 'Contacts',  style=wx.NO_BORDER)
        
        self.pane_biodata     = panel_bio(self.panel_panels, -1)
        self.pane_education   = panel_education(self.panel_panels, -1)
        self.pane_medical     = panel_medical(self.panel_panels, -1)
        self.pane_fees        = panel_fees(self.panel_panels, -1)
        self.pane_contacts    = panel_guardian_details(self.panel_panels, -1)
        
        self.button_new      = wx.Button(self, -1, "New")
        self.button_edit      = wx.Button(self, -1, "Edit")

        self.panes =[self.pane_biodata, self.pane_education,
                     self.pane_medical, self.pane_fees, self.pane_contacts]
        
        self.pane_biodata.SetName(  'pane_biodata')
        self.pane_education.SetName('pane_education')
        self.pane_medical.SetName(  'pane_medical')
        self.pane_fees.SetName(     'pane_fees')
        self.pane_contacts.SetName( 'pane_contacts')

        self.tabs =[self.button_biodata, self.button_education,
                    self.button_medical, self.button_contacts, self.button_fees]
        
        pub.subscribe(self.displayData, 'student.selected')
        
        self.Bind(wx.EVT_BUTTON, self.OnNew,     self.button_new)
        self.Bind(wx.EVT_BUTTON, self.OnEdit,     self.button_edit)
        
        self.Bind(wx.EVT_BUTTON, self.OnBio,      self.button_biodata)
        self.Bind(wx.EVT_BUTTON, self.OnEdu,      self.button_education)
        self.Bind(wx.EVT_BUTTON, self.OnMedical,  self.button_medical)
        self.Bind(wx.EVT_BUTTON, self.OnContacts, self.button_contacts)
        self.Bind(wx.EVT_BUTTON, self.OnFees,     self.button_fees)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        for tab in self.tabs:
            tab.SetWindowStyle(style=wx.NO_BORDER)
            tab.SetBackgroundColour(tab_unselected)
            
        self.button_biodata.SetBackgroundColour(tab_selected)
        
        for pane in self.panes:
            pane.Hide()
            
        self.pane_fees.SetMinSize((-1, 300))
            
        self.current_pane = self.pane_biodata
        self.current_pane.Show()
        self.SetMinSize((-1, 500))

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_panels = wx.BoxSizer(wx.VERTICAL)
        sizer_tabs   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_main_horz   = wx.BoxSizer(wx.HORIZONTAL)

        for t in self.tabs:
            sizer_tabs.Add(t, 0, wx.RIGHT, 2)
        self.panel_tabs.SetSizer(sizer_tabs)
     
        
        for pane in self.panes:
            sizer_panels.Add(pane, 1, wx.TOP | wx.EXPAND, 10)
        self.panel_panels.SetSizer(sizer_panels)
        
        line = wx.StaticLine(self, -1)
        
        sizer_main.Add(self.panel_tabs,   0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_main.Add(self.panel_panels, 1, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(line,              0, wx.ALL | wx.EXPAND, 10)
        #sizer_main.Add(self.button_edit,  0, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(sizer_main_horz,   0, wx.ALL | wx.EXPAND, 0)
        sizer_main_horz.Add(self.button_new,  0, wx.ALL | wx.EXPAND, 10)
        sizer_main_horz.Add(self.button_edit,  0, wx.ALL | wx.EXPAND, 10)
        
        self.SetSizer(sizer_main)
        
        self.Layout()
        
    def __do_main(self):
        self.editing = False
    
    def displayData(self):
        self.student_id = student_id = gVar.student_id
        self.editing = False
        self.clearCtrls()

        student_details = fetch.studentDetails_id(student_id)
        
        if not student_details:
            return
        else:
            for p in self.panes:
                print p.GetName()
                p.displayData(student_id)
        
    def setCmb(self, cmb, val):
        if val: cmb.SetSelection(val)
    
    def clearCtrls(self):
        for p in self.panes: p.clearCtrls()
        
    def enableCtrls(self):
        for p in self.panes: p.enableCtrls()
 
    def disableCtrls(self):
        for p in self.panes: p.disableCtrls()
 
    def OnEdit(self, evt):
        print 'panel_student_bio >>>  OnEdit'
        
        pane_name = self.current_pane.GetName()
        print 'current_pane  pane_name>',pane_name
        
        
        
        dlg = DlgEditStudentDetails.create(None)
        
        try:
            if  pane_name== 'pane_contacts':
                
                tabname = self.pane_contacts.getCurrentTabname()
                print 'pane_contacts shown only ', tabname
                dlg.onlyShow(tabname)
            dlg.displayData()
            dlg.showPane(pane_name)
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
            
    def OnNew(self, evt):
        print 'panel_student_bio >>>  OnNew'
        
        pane_name = self.current_pane.GetName()
        print 'current_pane  pane_name >> ',pane_name
        #pub.sendMessage("New_bio")
        dlg = DlgEditStudentDetails.create(None)
        
        try:
            if  pane_name== 'pane_contacts':
                
                tabname = self.pane_contacts.getCurrentTabname()
                print 'pane_contacts shown only ', tabname
                dlg.onlyShow(tabname)
            dlg.NewData()
            dlg.showPane(pane_name)
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
        

    def OnSave(self, evt):
        #print 'OnSave >>>>>',
        #print self.current_pane.GetName()
        self.current_pane.Save()
        self.OnEdit(wx.Event)
        
    def Save(self):
        print 'save -------------------'

    def OnBio(self, evt):
        self.current_pane = self.pane_biodata
        self.showPane(self.pane_biodata, self.button_biodata)
        
    def OnEdu(self, evt):
        self.current_pane = self.pane_education
        self.showPane(self.current_pane, self.button_education)
        
    def OnMedical(self, evt):
        self.current_pane = self.pane_medical
        self.showPane(self.current_pane, self.button_medical)
        
    def OnContacts(self, evt):
        print 'OnContacts ..................'
        self.current_pane = self.pane_contacts
        self.showPane(self.current_pane, self.button_contacts)
        
    def OnFees(self, evt):
        self.current_pane = self.pane_fees
        self.showPane(self.current_pane, self.button_fees)
        
    def showPane(self, pane, btn):
        #print 'showPane', self.editing
        
        self.current_pane = pane
        if self.editing: return
        for b in self.tabs:
            b.SetBackgroundColour(tab_unselected)
        btn.SetBackgroundColour(tab_selected)
        for p in self.panes:
            p.Hide()
        pane.Show()
        
        self.Layout()
        