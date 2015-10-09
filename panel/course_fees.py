import wx

import wx.lib.mixins.listctrl as  listmix

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''
 
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        
        
class panel_course_fees(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.label_heading = wx.StaticText(self, -1, 'Courses & Fees For 20014')
        
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_heading, 0, 0, 0)
        sizer.Add(self.list_ctrl, 1,0,0)
        self.SetSizer(sizer)
        
        self.list_ctrl.InsertColumn(0, "id")
        self.list_ctrl.InsertColumn(1, "course_id")
        self.list_ctrl.InsertColumn(2, "course_name")
        self.list_ctrl.InsertColumn(3, "fee_name")
        self.list_ctrl.InsertColumn(3, "fee_amount")
        
        
        
        
        
    def displayData(self):
        self.list_ctrl.DeleteAllItems()
        for school_id in [1,2,3,4]:
            self.list_ctrl.Append(('School','','','',''))
            course_ids = fetch.courses_forSchool_forYear(school_id, gVar.schYr)
            #rint'course_ids ', course_ids
            
            for course_id in course_ids:
                self.list_ctrl.Append(('Course','','','',''))
                sql = "SELECT fee \
                         FROM scgool_fees \
                        WHERE schYr = %d AND %d IN (course_ids)" % ( gVar.schYr, course_id)
                res = fetch.getAllDict(sql)
                #rintsql, res
                for fee in res:
                    self.list_ctrl.Append(('Fee','2','3','4','5'))