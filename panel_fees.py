import wx, gVar
import fetchodbc   as fetch
import loadCmbODBC as loadCmb

from datetime               import date
from DateCtrl               import DateCtrl

tab_selected   = 'white'
tab_unselected = (240,245,250)

        
        
class panel_fees(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.text_ctrls   = []
        self.choice_ctrls = []
        
    def enableCtrls(self): 
        for ctrl in self.text_ctrls:   ctrl.SetEditable()
        for ctrl in self.choice_ctrls: ctrl.Enable()
        
    def disableCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetEditable(False)
        for ctrl in self.choice_ctrls: ctrl.Enable(False)
          
    def clearCtrls(self):
        for ctrl in self.text_ctrls:   ctrl.SetLabel('')
        for ctrl in self.choice_ctrls: ctrl.SetSelection(0)
        self.disableCtrls()
        
    def displayData(self, student_details):
        pass
    
    def Save(self):
        print 'save fees'
