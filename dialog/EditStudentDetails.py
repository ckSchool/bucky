import wx

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

from panel.guardian_details import panel_guardian_details
from panel.bio              import panel_bio
from panel.education        import panel_education
from panel.medical          import panel_medical
from panel.payment_details  import panel_payment_details as panel_fees

def create(parent):
    return DlgEditStudentDetails(parent)
    
class DlgEditStudentDetails(wx.Dialog):
    _custom_classes = {'wx.Panel': ['NB']}
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        
        tc = []
        
        self.panel_panels     = wx.Panel(self, -1)
        
        self.pane_biodata     = panel_bio(self.panel_panels, -1)
        self.pane_education   = panel_education(self.panel_panels, -1)
        self.pane_medical     = panel_medical(self.panel_panels, -1)
        self.pane_fees        = panel_fees(self.panel_panels, -1)
        self.pane_contacts    = panel_guardian_details(self.panel_panels, -1)

        self.panes =[self.pane_biodata, self.pane_education,
                     self.pane_medical, self.pane_fees, self.pane_contacts]
        
        self.pane_dict = {'pane_biodata': self.pane_biodata, 'pane_education':self.pane_education,
                          'pane_medical': self.pane_medical, 'pane_fees': self.pane_fees, 'pane_contacts':self.pane_contacts}
        
        self.pane_biodata.SetName(  'pane_biodata')
        self.pane_education.SetName('pane_education')
        self.pane_medical.SetName(  'pane_medical')
        self.pane_fees.SetName(     'pane_fees')
        self.pane_contacts.SetName( 'pane_contacts')

        self.panel_buttons = wx.Panel(self,-1)
        self.button_save   = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel = wx.Button(self.panel_buttons, -1, "Cancel")

        self.Bind(wx.EVT_BUTTON, self.OnSave,   self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
    def __set_properties(self):
        
        for pane in self.panes:
            pane.Hide()
            
        self.current_pane = self.pane_biodata
        self.current_pane.Show()
        
        #self.pane_fees.panel_buttons.Show()
        self.SetMinSize((-1,600))
        self.Refresh()

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_btns   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panels = wx.BoxSizer(wx.VERTICAL)
        #sizer_tabs   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        
        sizer_btns.Add(self.button_save,   0, wx.ALIGN_RIGHT, 10)
        sizer_btns.Add(self.button_cancel, 0, wx.ALIGN_RIGHT, 10)
        self.panel_buttons.SetSizer(sizer_btns)

        for pane in self.panes:
            sizer_panels.Add(pane, 1, wx.TOP | wx.EXPAND, 10)
        self.panel_panels.SetSizer(sizer_panels)
        
        line = wx.StaticLine(self, -1)
        sizer_main.Add(self.panel_panels,  1, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(line,               0, wx.ALL | wx.EXPAND, 10)
        sizer_main.Add(self.panel_buttons, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.SetSizer(sizer_main)
        
        self.Layout()
        self.Fit()
        self.Centre()
        
    def __do_main(self):
        self.enableCtrls()
        self.pane_contacts.enableAllCtrls()
    
    def displayData(self):
         
        self.student_id = student_id = gVar.student_id
   
        self.clearCtrls()
        self.enableCtrls()

        for p in self.panes:
            p.displayData(student_id)
    
    def NewData(self):
        #subsc = pub.subscribe("New_bio")
        
        #self.student_id = student_id = gVar.student_id
   
        self.clearCtrls()
        self.enableCtrls()
        
    def setCmb(self, cmb, val):
        if val: cmb.SetSelection(val)
    
    def clearCtrls(self):
        for p in self.panes: p.clearCtrls()
        
    def enableCtrls(self):
        #rint'Dlg enableCtrls'
        for p in self.panes:
            #rint'enable pane >', p.GetName()
            p.enableCtrls()
 
    def disableCtrls(self):
        #rint'Dlg > disableCtrls'
        for p in self.panes:  p.disableCtrls() 

    def OnSave(self, evt):
        #rint'OnSave >>>>>',  self.current_pane.GetName()
        self.current_pane.Save()
        self.OnEdit(wx.Event)
        
    def onlyShow(self , tab):
        #rint'onlyShow tab ', tab
        self.pane_contacts.onlyShow(tab)
        
        if tab == 'f':
            title = 'Editing Father'
        elif  tab == 'm':
            title = 'Editing Mother'
        else:
            title = 'Editing Guardian'
            
        self.SetTitle(title)

    def showPane(self, pane_name):#, btn):
        #rint'Dlg > showPane', pane_name,
        
        self.current_pane = self.pane_dict[pane_name]
 
        for p in self.panes:
            p.Hide()
        self.current_pane.Show()
        
        self.Layout()
        
    def OnCancel(self, evt):
        self.Close()
"""
if __name__ == '__main__':
    app = wx.App(redirect=False)
    dlg = DlgEditStudentDetails(None, -1)
    try:
        gVar.student_id = 5
        dlg.displayData()
        dlg.ShowModal()
    finally:  dlg.Destroy()
    app.MainLoop()"""
