import wx, gVar, fetch, lv

from myListCtrl import VirtualList

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

import wx.lib.scrolledpanel as scrolled

flag_insertion = ''
g_replace_activity_id = ''
g_replace_teacher_id  = ''

def create(parent):
    return DlgExculRoster(parent)

class DlgExculRoster(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.label_heading = wx.StaticText(self, -1, '')
        
        self.panel_middle  = wx.Panel(self, -1)
        
        heading = (('',10), ('',10), ('',10))
        self.vlist_ctrl_pool = VirtualList(self.panel_middle, heading, style = wx.LC_HRULES)
        self.scrolledPanel   = scrolled.ScrolledPanel(self.panel_middle, - 1,  size=wx.DefaultSize)
        self.panel_footer    = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL)
        self.text_ctrl_1     = wx.TextCtrl(self.panel_footer, -1, 'x')
        self.text_ctrl_2     = wx.TextCtrl(self.panel_footer, -1, 'x')

        self.panel_btns_footer_mid = wx.Panel(self.panel_footer,   -1, style=wx.TRANSPARENT_WINDOW | wx.TAB_TRAVERSAL)
        self.panel_save_spc        = wx.Panel(self.panel_footer,   -1, style=wx.TAB_TRAVERSAL)

        self.button_save   = wx.Button(self.panel_save_spc,        -1,  label='Save')
        self.button_delete = wx.Button(self.panel_btns_footer_mid, -1, 'Delete')
        self.button_add    = wx.Button(self.panel_btns_footer_mid, -1, 'Add')
        self.button_edit   = wx.Button(self.panel_btns_footer_mid, -1, 'Edit')
        
        pub.subscribe(self.displayData, 'exculFilter.changed')
        #self.vlist_ctrl_pool.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag)
        
        self.button_save.Bind(wx.EVT_BUTTON,   self.OnSave)
        #self.button_delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        #self.button_add.Bind(wx.EVT_BUTTON,    self.OnAdd)
        #self.button_edit.Bind(wx.EVT_BUTTON,   self.OnEdit)

        self.__do_properties()
        self.__do_layout()
        self.__do_main()
        
    def __do_properties(self):
        self.label_heading.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_heading.SetForegroundColour(gVar.white)

        self.vlist_ctrl_pool.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id',    width=60)
        self.vlist_ctrl_pool.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='title', width=200)

    def __do_layout(self):
        sizer_main         = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_middle       = wx.BoxSizer(orient=wx.HORIZONTAL)
        sizer_footer       = wx.BoxSizer(orient=wx.HORIZONTAL)
        sizer_mid_filter   = wx.BoxSizer(orient=wx.HORIZONTAL)
        sizer_footer_right = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.sizer_excul   = wx.GridBagSizer(hgap=0, vgap=0)
        self.scrolledPanel.SetSizer(self.sizer_excul) 
        self.scrolledPanel.SetupScrolling()
        
        sizer_middle.AddWindow(self.vlist_ctrl_pool,  0, wx.ALL | wx.EXPAND, 10)
        sizer_middle.Add(self.scrolledPanel,         1, wx.ALL | wx.EXPAND, 10)
        self.panel_middle.SetSizer(sizer_middle)
        
        sizer_footer.AddWindow(self.text_ctrl_1,           1, wx.EXPAND | wx.ALL, 0)
        sizer_footer.AddWindow(self.panel_btns_footer_mid, 0, wx.ALL | wx.EXPAND, 1)
        sizer_footer.AddWindow(self.text_ctrl_2,           1, wx.EXPAND | wx.ALL, 0)
        sizer_footer.AddWindow(self.panel_save_spc,        0, wx.EXPAND | wx.ALL, 1)
        self.panel_footer.SetSizer(sizer_footer)
        
        sizer_footer_right.AddWindow(self.button_save,     0, 0, 0)
        self.panel_save_spc.SetSizer(sizer_footer_right)
        
        sizer_mid_filter.AddWindow(self.button_add,        0, 0, 0)
        sizer_mid_filter.AddSpacer(wx.Size(8, 8),             0, 0)
        sizer_mid_filter.AddWindow(self.button_delete,     0, 0, 0)
        sizer_mid_filter.AddSpacer(wx.Size(8, 8),             0, 0)
        sizer_mid_filter.AddWindow(self.button_edit,       0, 0, 0)
        self.panel_btns_footer_mid.SetSizer(sizer_mid_filter)
        
        sizer_main.Add(self.label_heading, 0, wx.EXPAND) 
        sizer_main.Add(self.panel_middle,  1, wx.EXPAND) 
        sizer_main.Add(self.panel_footer,  0, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        
    def __do_main(self):
        """self.list_ctrl_excul.DeleteAllColumns()
        
        self.list_ctrl_excul.InsertColumn(0, "ID",          width=0)
        self.list_ctrl_excul.InsertColumn(1, "activity id", width=0)
        self.list_ctrl_excul.InsertColumn(2, "Activity",    width=200)
        self.list_ctrl_excul.InsertColumn(3, "employee id", width=0)
        self.list_ctrl_excul.InsertColumn(4, "Teacher",     width=197)
        
        dt1 = TextDropTarget(self.list_ctrl_excul) # Make this control a Drop Target
        self.list_ctrl_excul.SetDropTarget(dt1)         # Link to Control"""
        
        symbols={"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR}
        heading = (('id',0,0), ('Name',150,0))
        #self.vlist_ctrl_teacher_pool.initList(symbols,  heading)
        #self.vlist_ctrl_student_pool.initList(symbols, heading)
        
        self.createActivitiesMenu()
        self.createTeachersMenu()
        self.createExculMenu()
    
    def displayData(self, exculset_id):
        self.exculset_id = exculset_id
        return
        school, day, semester, schYr = fetch.exculsetinfo(exculset_id)

        flag_insertion, self.replaceName, self.replace_id = '' , '', 0
        
        txt = "Excul activities for exculset id:%d   >  %s  >  %s, \
               Semester %d, %d" % (self.exculset_id, school, day, semester, schYr)
        
        self.SetTitle(txt)
        self.exculList = fetch.excul_groups_forExculSet(self.exculset_id)
        
        lv.populateWithList(self.list_ctrl_excul, self.exculList)
        
        otherActivities = fetch.excul_activityPool(self.exculList)
        self.activityPoolDATA = fetch.build_dictionary(otherActivities)
        self.vlist_ctrl_student_pool.SetItemMap(self.activityPoolDATA)

        otherTeachers = fetch.excul_teacherPool(self.exculList)
        self.teacherPoolDATA = fetch.build_dictionary(otherTeachers)
        self.vlist_ctrl_teacher_pool.SetItemMap(self.teacherPoolDATA)

    def OnActivities_Dclick(self, event):
        selection = self.vlist_ctrl_student_pool.GetIds_ofSelectedItems()
        if not selection: return
        
        # convert tuple to list
        exculList = list(self.exculList)
    
        for activity_id in selection:
            activity_title = fetch.excul_activityTitle(activity_id)
            self.list_ctrl_excul.Append((0, activity_id, activity_title, 0, '' ))
            
            new_list = []
            for row in self.activityPoolDATA:
                res = self.activityPoolDATA[row]
                item_id = res[0]
                if not item_id == activity_id: new_list.append(res)
                
            self.activityPoolDATA = fetch.build_dictionary(new_list)
            self.vlist_ctrl_student_pool.SetItemMap(self.activityPoolDATA)
            
        self.banding()
    
    def OnBeginDragActivity(self, event):
        index  = self.vlist_ctrl_student_pool.GetFirstSelected()
        if index < 0: return
        
        activity_id = int(self.vlist_ctrl_student_pool.GetItemText(index))
        title       = self.vlist_ctrl_student_pool.GetItem(index, 1).GetText()
        source      = self.vlist_ctrl_student_pool.GetName()
        data        = '%s:%s:%s' % (str(activity_id), str(title), source)
    
        """ Begin a Drag Operation """
        todrop = wx.PyTextDataObject(data)
        drop_source = wx.DropSource(self.list_ctrl_excul) # Create a DropSourceObject, for Drag operation
        drop_source.SetData(todrop)  # Associate the Data to be dragged with the Drop Source Object
        drop_source.DoDragDrop(True) # Intiate the Drag Operation
        
        new_list = self.newActivityList(activity_id)
        if flag_insertion == 'replaced':
            new_list.append((g_replace_activity_id, fetch.excul_activityTitle(g_replace_activity_id)))
            
        self.activityPoolDATA = fetch.build_dictionary(new_list)
        self.vlist_ctrl_student_pool.SetItemMap(self.activityPoolDATA)
            
    def newActivityList(self, activity_id):
        new_list = []
        for row in self.activityPoolDATA:
            res = self.activityPoolDATA[row]
            item_id = res[0]
            if not item_id == activity_id:  new_list.append(res)
        return new_list
          
    def OnBeginDragTeacher(self, event):
        index  = self.vlist_ctrl_teacher_pool.GetFirstSelected()
        if index < 0: return
        
        employee_id = int(self.vlist_ctrl_teacher_pool.GetItemText(index))
        title       = self.vlist_ctrl_teacher_pool.GetItem(index, 1).GetText()
        source      = self.vlist_ctrl_teacher_pool.GetName()
        data        = '%s:%s:%s' % (str(employee_id), str(title), source)
        
        """ Begin a Drag Operation """
        todrop = wx.PyTextDataObject(data)
        
        drop_source = wx.DropSource(self.list_ctrl_excul)  # Create a DropSourceObject, for Drag operation
        drop_source.SetData(todrop)                        # Associate the Data to be dragged with the Drop Source Object
        drop_source.DoDragDrop(True)                       # Intiate the Drag Operation
        
        new_list = self.newTeacherList(employee_id)
        if flag_insertion == 'replaced':
            new_list.append((g_replace_teacher_id, fetch.employeeName(g_replace_teacher_id)))
        self.teacherPoolDATA = fetch.build_dictionary(new_list)
        self.vlist_ctrl_teacher_pool.SetItemMap(self.teacherPoolDATA)

        
    def newTeacherList(self, employee_id):
        new_list = []
        for row in self.teacherPoolDATA:
            res     = self.teacherPoolDATA[row]
            item_id = res[0]
            if not item_id == employee_id: new_list.append(res)
        return new_list
                
    def OnOpenPopupActivity(self, evt): self.PopupMenu(self.mnu_activity)
    def OnOpenPopupTeacher(self, evt):  self.PopupMenu(self.mnu_guru)
    def OnOpenPopupExcul(self, evt):    self.PopupMenu(self.mnu_excul)
        
    def OnSave(self, event):
        ic = self.list_ctrl_excul.GetItemCount()
        for i in range(ic):
            excul_id    = int(self.list_ctrl_excul.GetItemText(i, 0))
            activity_id = int(self.list_ctrl_excul.GetItemText(i, 1))
            employee_id = int(self.list_ctrl_excul.GetItemText(i, 3))
            if excul_id: self.update(excul_id, activity_id, employee_id)
            else:        self.insert(activity_id, employee_id)
                
        self.EndModal(wx.OK)
        
    def update(self, excul_id, activity_id, employee_id=0):
        sql = " SELECT id FROM excul \
                 WHERE id = %d \
                   AND exculset_id = %d \
                   AND activity_id = %d \
                   AND employee_id = %d" % (self.exculset_id, excul_id, activity_id, employee_id)

        if fetch.getAll_dict(sql):
            pass
            #rint'DlgExculRoster > match found = do nothing'
            
        else:
            sql ="UPDATE excul \
                     SET activity_id = %d, employee_id = %d \
                   WHERE id    = %d" % (activity_id, employee_id, excul_id)

            fetch.updateDB(sql)
    
    def insert(self, activity_id, employee_id):
        sql = " INSERT INTO excul \
                   SET exculset_id = %d, activity_id = %d , employee_id = %d" % (
                       self.exculset_id, activity_id,       employee_id)
        fetch.updateDB(sql)
        
    def OnDissolveExcul(self,evt):
        lisc_ctrl = self.list_ctrl_excul
        index = self.list_ctrl_excul.GetFirstSelected()
        if index > -1:
            activity_id = lisc_ctrl.GetItem(index, 1).GetText()
            employee_id = lisc_ctrl.GetItem(index, 3).GetText()

            self.addToActivityPool(activity_id)
            self.addToTeacherPool(employee_id)
            
            self.list_ctrl_excul.DeleteItem(index)
            self.banding()
            
    def banding(self):
        #rint'DlgExculRoster > banding'
        lv.decorateBanding(self.list_ctrl_excul)
        self.vlist_ctrl_student_pool.decorateBanding()
        self.vlist_ctrl_teacher_pool.decorateBanding()
        
    def OnReturnTeacher(self, event): 
        lisc_ctrl = self.list_ctrl_excul
        index = self.list_ctrl_excul.GetFirstSelected()
        if index > -1:
            employee_id = lisc_ctrl.GetItem(index, 3).GetText()
            teacher     = lisc_ctrl.GetItem(index, 4).GetText()
            
            self.addToTeacherPool(employee_id)
                    
            self.list_ctrl_excul.SetStringItem(index, 3, '')
            self.list_ctrl_excul.SetStringItem(index, 4, '')
            
    def addToActivityPool(self, activity_id):
        self.activityPoolDATA[len(self.activityPoolDATA)] = (int(activity_id), fetch.excul_activityTitle(activity_id))
        self.vlist_ctrl_student_pool.SetItemMap(self.activityPoolDATA)
        
    def addToTeacherPool(self, employee_id):
        self.teacherPoolDATA[len(self.teacherPoolDATA)] = (int(employee_id), fetch.employeeName(employee_id))
        self.vlist_ctrl_teacher_pool.SetItemMap(self.teacherPoolDATA)

    def OnNewTeacher(self, event):
        new_id = fetch.openDialog(DlgNewEditEmployee)
        if new_id: self.addToTeacherPool(new_id)
        
    def OnEditTeacher(self, event):
        employee_id = self.vlist_ctrl_teacher_pool.get_selected_id()
        fetch.openDialog(DlgNewEditEmployee, employee_id)
        # in name changed update item
        
    def OnDeleteTeacher(self, event):
        pass
        #rint'DlgExculRoster', self.vlist_ctrl_teacher_pool.GetId()
    
    def OnNewActivity(self,evt):
        new_id = fetch.openDialog(DlgNewEditExculActivity)
        if new_id: self.addToActivityPool(new_id)
    
    def OnEditActivity(self,evt):
        activity_id = self.vlist_ctrl_student_pool.get_selected_id()
        fetch.openDialog(DlgNewEditExculActivity, activity_id)
    
    def OnDeleteActivity(self,evt):pass
 
    
        
        
    def createActivitiesMenu(self):
        self.mnu_activity = wx.Menu()

        item = wx.MenuItem(self.mnu_activity, -1, "New")
        self.Bind(wx.EVT_MENU, self.OnNewActivity, item)
        self.mnu_activity.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_activity, -1, "Edit")
        self.Bind(wx.EVT_MENU, self.OnEditActivity, item)
        self.mnu_activity.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_activity, -1, "Delete")
        self.Bind(wx.EVT_MENU, self.OnDeleteActivity, item)
        self.mnu_activity.AppendItem(item)
        
    def createTeachersMenu(self):
        self.mnu_guru = wx.Menu()

        item = wx.MenuItem(self.mnu_guru, -1, "New")
        self.Bind(wx.EVT_MENU, self.OnNewTeacher, item)
        self.mnu_guru.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_guru, -1, "Edit")
        self.Bind(wx.EVT_MENU, self.OnEditTeacher, item)
        self.mnu_guru.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_guru, -1, "Delete")
        self.Bind(wx.EVT_MENU, self.OnDeleteTeacher, item)
        self.mnu_guru.AppendItem(item)
    
        
    def createExculMenu(self):
        self.mnu_excul = wx.Menu()

        item = wx.MenuItem(self.mnu_excul, -1, "Dissolve")
        self.Bind(wx.EVT_MENU, self.OnDissolveExcul, item)
        self.mnu_excul.AppendItem(item)
        
        item = wx.MenuItem(self.mnu_excul, -1, "Return Teacher")
        self.Bind(wx.EVT_MENU, self.OnReturnTeacher, item)
        self.mnu_excul.AppendItem(item)
        

    
        
class TextDropTarget(wx.TextDropTarget):            
    """ This object implements Drop Target functionality for Text """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped text """
       
        wx.TextDropTarget.__init__(self) # Initialize the wx.TextDropTarget Object
        self.obj = obj# Store the Object Reference for dropped text

    def OnDropText(self, x, y, data):
        global flag_insertion, g_replace_teacher_id, g_replace_activity_id
        flag_insertion = 'fail'
        g_replace_teacher_id, g_replace_activity_id,  self.replaceName = '', '', ''
                                     
        data = str(data).split(':')
        source_id, title, source = data[0], data[1], data[2]
        
        """ Implement Text Drop """
        index, flags = self.obj.HitTest((x, y))
        # data coming from lv_teachers          
        # check there is an activity at that position
        if index > -1:
            if source == "activityPool": # if sourse was activity listCtrl
                g_replace_activity_id  = self.obj.GetItem(index, 1).GetText()
                self.obj.SetStringItem(index, 1, data[0])
                self.obj.SetStringItem(index, 2, data[1]) 
                
                if int(g_replace_activity_id):
                      flag_insertion = 'replaced'
                else: flag_insertion = 'inserted'
                    
            else:# if sourse was teacher listCtrl
                g_replace_teacher_id   = self.obj.GetItem(index, 3).GetText()
                self.obj.SetStringItem(index, 3, data[0])
                self.obj.SetStringItem(index, 4, data[1]) 
                
                if int(g_replace_teacher_id):
                      flag_insertion = 'replaced'
                else: flag_insertion = 'inserted'
 
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

            
 