import wx, gVar, fetch, lv

#import DlgNewEditEmployee
import DlgNewEditExculActivity

from myListCtrl import VirtualList

days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

flag_insertion = ''
g_replace_activity_id = ''
g_replace_teacher_id  = ''

def create(parent):
    return DlgExculActivityListEditor(parent)

class DlgExculActivityListEditor(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.p = panel_exul_activity_list_editor(self, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.p, 1, 1, 0)
        self.SetSizer(sizer)
        self.Fit()
        self.Centre()
        
class panel_exul_activity_list_editor(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)    
        self.panel_spc_topL          = wx.Panel(self, -1)
        self.label_header            = wx.StaticText(self, -1, "Double click or drag to move items")
        self.panel_spc_topR          = wx.Panel(self, -1)

        self.list_ctrl_excul         = wx.ListCtrl(self, -1, style=wx.LC_REPORT |wx.BORDER_SUNKEN)
        
        heading = (('id',00), ('title',150))
        self.vlist_ctrl_activity_pool = VirtualList(self, heading, style = wx.LC_HRULES)
        self.vlist_ctrl_activity_pool.SetName('activityPool')
        
        self.vlist_ctrl_teacher_pool  = VirtualList(self, heading, style = wx.LC_HRULES)
        self.vlist_ctrl_teacher_pool.SetName('teacherPool')
        
        self.panel_activity_btns     = wx.Panel(self, -1)
        self.button_add_activity     = wx.Button(self.panel_activity_btns, -1, "Add activity")
        self.button_edit_activity    = wx.Button(self.panel_activity_btns, -1, "Edit activity")
        self.button_delete_activity  = wx.Button(self.panel_activity_btns, -1, "Remove activity")
        self.button_save             = wx.Button(self, -1, "Save List")
        #self.panel_teacher_btns      = wx.Panel(self, -1)
        #self.button_add_teacher      = wx.Button(self.panel_teacher_btns, -1, "Add Teacher")
        #self.button_edit_teacher     = wx.Button(self.panel_teacher_btns, -1, "Edit Teacher")
        #self.button_del_teacher      = wx.Button(self.panel_teacher_btns, -1, "Remove Teacher")

        self.__set_properties()
        self.__do_layout()

        self.vlist_ctrl_activity_pool.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnBeginDragActivity)
        self.vlist_ctrl_activity_pool.Bind(wx.EVT_CONTEXT_MENU,    self.OnOpenPopupActivity)
        self.vlist_ctrl_activity_pool.Bind(wx.EVT_LEFT_DCLICK,     self.OnActivities_Dclick)
        
        self.vlist_ctrl_teacher_pool.Bind(wx.EVT_LIST_BEGIN_DRAG,  self.OnBeginDragTeacher)
        self.vlist_ctrl_teacher_pool.Bind(wx.EVT_CONTEXT_MENU,     self.OnOpenPopupTeacher)
    
        self.list_ctrl_excul.Bind(wx.EVT_CONTEXT_MENU,            self.OnOpenPopupExcul)

        self.Bind(wx.EVT_BUTTON, self.OnNewActivity,    self.button_add_activity)
        self.Bind(wx.EVT_BUTTON, self.OnEditActivity,   self.button_edit_activity)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteActivity, self.button_delete_activity)
        
        self.Bind(wx.EVT_BUTTON, self.OnSave,           self.button_save)
        
        #self.Bind(wx.EVT_BUTTON, self.OnNewTeacher,     self.button_add_teacher)
        #self.Bind(wx.EVT_BUTTON, self.OnEditTeacher,    self.button_edit_teacher)
        #self.Bind(wx.EVT_BUTTON, self.OnDeleteTeacher,  self.button_del_teacher)

        self.__do_main()
        self.Center()

    def __set_properties(self):
        self.list_ctrl_excul.SetMinSize((400,600))
        self.label_header.SetForegroundColour(wx.Colour(255, 255, 255))
        self.panel_activity_btns.SetMinSize((321, 21))
        self.button_save.SetMinSize((300, 40))
        self.vlist_ctrl_teacher_pool.SetMinSize((321, -1))
        #self.panel_teacher_btns.SetMinSize((-1, 21))

    def __do_layout(self):
        sizer_main = wx.FlexGridSizer(3, 3, 5, 5)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.panel_spc_topL,          1, wx.EXPAND, 0)
        sizer_main.Add(self.label_header,            0, 0, 0)
        sizer_main.Add(self.panel_spc_topR,          1, wx.EXPAND, 0)
        sizer_main.Add(self.vlist_ctrl_activity_pool, 1, wx.EXPAND, 0)
        sizer_main.Add(self.list_ctrl_excul,          1, wx.EXPAND, 0)
        sizer_main.Add(self.vlist_ctrl_teacher_pool,  1, wx.EXPAND, 0)
        sizer_5.Add(self.button_add_activity,         1, wx.LEFT | wx.EXPAND, 10)
        sizer_5.Add(self.button_edit_activity,        1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_5.Add(self.button_delete_activity,      1, wx.RIGHT | wx.EXPAND, 10)
        self.panel_activity_btns.SetSizer(sizer_5)
        sizer_main.Add(self.panel_activity_btns,      0, wx.BOTTOM, 10)
        sizer_main.Add(self.button_save,              1, wx.BOTTOM | wx.EXPAND, 10)
        #sizer_6.Add(self.button_add_teacher,         1, wx.LEFT | wx.EXPAND, 10)
        #sizer_6.Add(self.button_edit_teacher,        1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        #sizer_6.Add(self.button_del_teacher,         1, wx.RIGHT | wx.EXPAND, 10)
        #self.panel_teacher_btns.SetSizer(sizer_6)
        #sizer_main.Add(self.panel_teacher_btns,      0, wx.BOTTOM, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        sizer_main.AddGrowableRow(1)
        sizer_main.AddGrowableCol(0)
        sizer_main.AddGrowableCol(2)
        
    def __do_main(self):
        self.list_ctrl_excul.DeleteAllColumns()
        
        self.list_ctrl_excul.InsertColumn(0, "ID",          width=0)
        self.list_ctrl_excul.InsertColumn(1, "activity id", width=0)
        self.list_ctrl_excul.InsertColumn(2, "Activity",    width=200)
        self.list_ctrl_excul.InsertColumn(3, "employee id", width=0)
        self.list_ctrl_excul.InsertColumn(4, "Teacher",     width=197)
        
        dt1 = TextDropTarget(self.list_ctrl_excul) # Make this control a Drop Target
        self.list_ctrl_excul.SetDropTarget(dt1)         # Link to Control
        
        symbols={"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR}
        heading = (('id',0,0), ('Name',150,0))
        self.vlist_ctrl_teacher_pool.initList(symbols,  heading)
        self.vlist_ctrl_activity_pool.initList(symbols, heading)
        
        self.createActivitiesMenu()
        self.createTeachersMenu()
        self.createExculMenu()
    
    def displayData(self, exculset_id):
        self.exculset_id = exculset_id
        res = fetch.exculsetinfo(exculset_id)
        if res:
            school, day, semester, schYr = res
        else:
            #rint'DlgExcul fai'
            return

        flag_insertion, self.replaceName, self.replace_id = '' , '', 0
        
        txt = "Excul activities for exculset id:%d   >  %s  >  %s, \
               Semester %d, %d" % (self.exculset_id, school, day, semester, schYr)
        
        self.SetTitle(txt)
        self.exculList = fetch.excul_groups_forExculSet(self.exculset_id)
        
        lv.populateWithList(self.list_ctrl_excul, self.exculList)
        
        otherActivities = fetch.excul_activityPool(self.exculList)
        self.activityPoolDATA = fetch.build_dictionary(otherActivities)
        self.vlist_ctrl_activity_pool.SetItemMap(self.activityPoolDATA)

        otherTeachers = fetch.excul_teacherPool(self.exculList)
        self.teacherPoolDATA = fetch.build_dictionary(otherTeachers)
        self.vlist_ctrl_teacher_pool.SetItemMap(self.teacherPoolDATA)

    def OnActivities_Dclick(self, event):
        selection = self.vlist_ctrl_activity_pool.GetIds_ofSelectedItems()
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
            self.vlist_ctrl_activity_pool.SetItemMap(self.activityPoolDATA)
            
        self.banding()
    
    def OnBeginDragActivity(self, event):
        index  = self.vlist_ctrl_activity_pool.GetFirstSelected()
        if index < 0: return
        
        activity_id = int(self.vlist_ctrl_activity_pool.GetItemText(index))
        title       = self.vlist_ctrl_activity_pool.GetItem(index, 1).GetText()
        source      = self.vlist_ctrl_activity_pool.GetName()
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
        self.vlist_ctrl_activity_pool.SetItemMap(self.activityPoolDATA)
            
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
            #rint'DlgExculActivityListEditor > match found = do nothing'
            
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
        #rint'DlgExculActivityListEditor > banding'
        lv.decorateBanding(self.list_ctrl_excul)
        self.vlist_ctrl_activity_pool.decorateBanding()
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
        self.vlist_ctrl_activity_pool.SetItemMap(self.activityPoolDATA)
        
    def addToTeacherPool(self, employee_id):
        self.teacherPoolDATA[len(self.teacherPoolDATA)] = (int(employee_id), fetch.employeeName(employee_id))
        self.vlist_ctrl_teacher_pool.SetItemMap(self.teacherPoolDATA)

    def OnNewTeacher(self, event):
        #new_id = fetch.openDialog(DlgNewEditEmployee)
        if new_id:
            self.addToTeacherPool(new_id)
        
    def OnEditTeacher(self, event):
        employee_id = self.vlist_ctrl_teacher_pool.get_selected_id()
        fetch.openDialog(DlgNewEditEmployee, employee_id)
        # in name changed update item
        
    def OnDeleteTeacher(self, event):
        pass
        #rint'DlgExculActivityListEditor', self.vlist_ctrl_teacher_pool.GetId()
    
    def OnNewActivity(self,evt):
        new_id = fetch.openDialog(DlgNewEditExculActivity)
        if new_id: self.addToActivityPool(new_id)
    
    def OnEditActivity(self,evt):
        activity_id = self.vlist_ctrl_activity_pool.get_selected_id()
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
        global flag_insertion, g_replace_id
        flag_insertion = 'fail'
        g_replace_id,  self.replaceName = '', ''
                                     
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
        dlg.p.displayData(1)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()

            
 