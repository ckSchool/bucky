import wx, gVar, fetch, lv

from myListCtrl import VirtualList

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import wx.lib.scrolledpanel as scrolled

import DlgNewEditExculActivity

flag_insertion = False
g_replace_activity_id = ''
g_replace_teacher_id  = ''
drag_list_ctrl = wx.ListCtrl

def create(parent):
    return DlgExculRoster(parent)
 
class TextDropTarget(wx.TextDropTarget):
    def __init__(self, obj):
        wx.TextDropTarget.__init__(self)
        self.obj = obj

    def OnDropText(self, x, y, data):
        global flag_insertion
        data = str(data).split(':')
        source_id, name, batch = data[0], data[1], data[2]
        list_ctrl = self.obj
        if not list_ctrl== drag_list_ctrl:
            flag_insertion = True
      
            item_data = (source_id, name, batch)
            index = list_ctrl.Append(item_data)
            list_ctrl.SetItemData(index, int(source_id)) 

class PanelExculRosterView(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
        self.panel_topbar   = wx.Panel(self, -1)
        self.panel_main     = wx.Panel(self, -1)
        
        self.panel_spc1     = wx.Panel(self.panel_topbar, -1)
        self.button_new     = wx.Button(self.panel_topbar, -1, "New Activity", style = wx.NO_BORDER)
        
        self.list_ctrl_pool = wx.ListCtrl(self.panel_main, -1, style=wx.LC_REPORT |wx.BORDER_SUNKEN)
        self.initListCtrl(self.list_ctrl_pool)
        
        self.panel_list_ctrls = scrolled.ScrolledPanel(self.panel_main, - 1,  size=wx.DefaultSize)#wx.Panel(self.panel_main, -1)
        
        self.button_new.Bind(wx.EVT_BUTTON , self.OnNew)
        
        self.__do_properties()
        self.__do_layout()
        self.__do_main()
        
    def __do_properties(self):
        self.button_new.SetBackgroundColour(gVar.darkGrey)
        self.button_new.SetForegroundColour(gVar.barkleys)
        self.panel_spc1.SetMinSize((200,-1))
        self.panel_topbar.SetBackgroundColour(gVar.darkGrey)
        
    def __do_layout(self):
        sizer_base       = wx.BoxSizer(wx.VERTICAL)
        sizer_main       = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top_bar    = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_excul = wx.GridBagSizer(hgap=5, vgap=5)
        
        self.panel_list_ctrls.SetSizer(self.sizer_excul)
    
        sizer_top_bar.Add(self.panel_spc1,  0, 0, 0)
        sizer_top_bar.Add(self.button_new,  0,wx.ALL,2)
        self.panel_topbar.SetSizer(sizer_top_bar)
        
        sizer_main.Add(self.list_ctrl_pool,   0, wx.EXPAND | wx.ALL, 10)
        sizer_main.Add(self.panel_list_ctrls, 1, wx.EXPAND | wx.ALL, 10)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_topbar, 0, wx.EXPAND, 0)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        
        self.SetMinSize((1024, 600))
        self.SetSize((1024, 600))
        self.Center()
        
    def __do_main(self):
        self.createMenu()
        self.exculset_id = 0
        #self.button_new.Hide()
        
    def displayData(self, exculset_id):
        self.exculset_id = exculset_id
        self.setTitle()
        self.loadStudentPool()
        self.createAndLoad_listCtrls_forEachActivity()
        
    def loadStudentPool(self):
        school_id      = fetch.schoolID_forExculSet(self.exculset_id)
        return
        self.exculList = fetch.excul_groups_forExculSet(self.exculset_id)
        exculID_list   = ','.join([str(x[0]) for x in self.exculList])
        
        sql = "SELECT student_id FROM excul_students WHERE FIND_IN_SET(excul_id , '%s') " % exculID_list
        res = fetch.getAll_col(sql)
        in_excul_list  = ','.join([str(x[0]) for x in res])
        
        sql ="SELECT s.id, s.first_name, b.name \
                FROM students s \
           LEFT JOIN nis n ON s.id = n.student_id \
                JOIN batch_students bs ON s.id = bs.student_id \
                JOIN batches b ON b.id = bs.batch_id \
               WHERE %d BETWEEN n.admission_year AND n.withdrew_year\
                 AND n.school_id = %d \
                 AND NOT FIND_IN_SET(s.id, '%s') \
                 GROUP BY s.id \
                 ORDER BY s.id \
                 LIMIT 90"  % (gVar.schYr, school_id, in_excul_list)

        lv.populate(self.list_ctrl_pool, sql)
          
    def createAndLoad_listCtrls_forEachActivity(self):
        self.panel_list_ctrls.DestroyChildren()
        self.sizer_excul.Clear()
        
        self.exculList = fetch.excul_groups_forExculSet(self.exculset_id)
        if self.exculList:
            exculCount = len(self.exculList)
            
            r, c = round(exculCount/4), exculCount%4
            self.sizer_excul.SetCols(c)
            self.sizer_excul.SetRows(r)
            
            itemNo = 0
            for excul in self.exculList:
                excul_id = excul[0]
                #rint'create list_ctrl for excul_id', excul_id
                exculLV  = self.createListCtrl(excul_id, itemNo)
                self.Bind(wx.EVT_CONTEXT_MENU, self.OnPopup, exculLV)
                #self.Bind(wx.EVT_MOUSE_EVENTS,  self.OnPopup, exculLV)
                itemNo += 1

            self.Layout()
            
    def createListCtrl(self, excul_id, itemNo):#posit, excul_id):
        list_ctrl_id   = 1000 + int(excul_id)
        list_ctrl_name = 'exculid:%d' % excul_id
        list_ctrl      = wx.ListCtrl(self.panel_list_ctrls, list_ctrl_id, size = (200,200), style=wx.LC_REPORT |wx.BORDER_SUNKEN)
        title = fetch.excul_activityTitle_forExcul(excul_id)
        self.initListCtrl(list_ctrl, title)
      
        r, c = round(itemNo/4), itemNo%4
        self.sizer_excul.Add(list_ctrl, (r,c))
      
        sql = "SELECT s.id, s.first_name, b.name \
               FROM students s \
               JOIN batch_students bs ON s.id = bs.student_id \
               JOIN batches b ON b.id = bs.batch_id \
               JOIN excul_students es ON s.id = es.student_id \
              WHERE es.excul_id =%d" % excul_id
        
        lv.populate(list_ctrl, sql)
        return list_ctrl

    def initListCtrl(self, list_ctrl, title="Pool"):
        list_ctrl.SetDropTarget(TextDropTarget(list_ctrl))
      
        list_ctrl.InsertColumn(0, 'id',    width=0)
        list_ctrl.InsertColumn(1, title, width=100)
        list_ctrl.InsertColumn(2, ' ',     width=100)
      
        list_ctrl.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDragInit)
        
    def setTitle(self):
        res = fetch.exculsetinfo(self.exculset_id)
        if not res: return
        school, day, semester, schYr = res
        txt = "Excul activities for exculset id:%d   >  %s  >  %s, \
               Semester %d, %d" % (self.exculset_id, school, day, semester, schYr)
        self.SetTitle(txt)
        
    def OnDragInit(self, event):
        global drag_list_ctrl, flag_insertion
        
        flag_insertion = False
        list_ctrl = event.GetEventObject()
        index = list_ctrl.GetFirstSelected()
        #rint'index=', index
        if index >-1:
            item_id    = list_ctrl.GetItemData(index)
            item_name  = list_ctrl.GetItemText(index, 1)
            item_batch = list_ctrl.GetItemText(index, 2)
         
            data = '%s:%s:%s' % (str(item_id), str(item_name), str(item_batch))
         
            tdo  = wx.PyTextDataObject(data)
            tds  = wx.DropSource(list_ctrl)
            tds.SetData(tdo)
            tds.DoDragDrop(True)
            
            if flag_insertion:
                list_ctrl.DeleteItem(index)
                
    def OnEdit(self, evt):
        dlg = DlgNewEditExculActivity.create(None)
        try:
            dlg.displayData(self.exculset_id, self.excul_id)
            if dlg.ShowModal() == wx.ID_OK:
                self.displayData(self.exculset_id)
        finally:    
            dlg.Destroy()
    
    def OnNew(self,  evt):
        dlg = DlgNewEditExculActivity.create(None)
        try:
            dlg.displayData(self.exculset_id, 0)
            if dlg.ShowModal() == wx.ID_OK:
                self.displayData(self.exculset_id)
        finally:    
            dlg.Destroy()
    
    
    
    def OnDel(self,  evt):pass
    
    def OnPopup(self, event):
        list_ctrl = event.GetEventObject()
        list_ctrl_id = list_ctrl.GetId()

        self.excul_id = list_ctrl_id - 1000
        
        self.mnu_abs.SetTitle(fetch.excul_activityTitle_forExcul(self.excul_id ))
        self.PopupMenu(self.mnu_abs)
        
    def createMenu(self):
        self.mnu_abs = wx.Menu()

        item = wx.MenuItem(self.mnu_abs, -1, "Edit")
        self.Bind(wx.EVT_MENU, self.OnEdit, item)
        self.mnu_abs.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_abs, -1, "Remove")
        self.Bind(wx.EVT_MENU, self.OnDel, item)
        self.mnu_abs.AppendItem(item)

  
 
if __name__ == '__main__':
    gVar.schYr = 2012
    app = wx.App(redirect=False)
    dlg = create(None)
    try:
        dlg.displayData(1)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
 