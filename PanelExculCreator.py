import wx, lv, gVar, fetch

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

flag_insertion = ''
g_replace_id   = 0

class PanelExculCreator(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        #self.statusbar = self.GetTopLevelParent().statusbar
        
        self.panel_spc_topL          = wx.Panel(self, -1)
        self.label_header            = wx.StaticText(self, -1, "Double click or drag to move items")
        self.panel_spc_topR          = wx.Panel(self, -1)
        
        s = wx.LC_REPORT | wx.LC_AUTOARRANGE | wx.LC_SORT_DESCENDING | wx.SUNKEN_BORDER
        self.list_ctrl_activity_pool = wx.ListCtrl(self, -1, style=s)
        self.list_ctrl_excul         = wx.ListCtrl(self, -1, style=s)
        self.list_ctrl_teacher_pool  = wx.ListCtrl(self, -1, style=s)
        
        self.panel_activity_btns     = wx.Panel(self, -1)
        self.button_add_activity     = wx.Button(self.panel_activity_btns, -1, "Add activity")
        self.button_edit_activity    = wx.Button(self.panel_activity_btns, -1, "Edit activity")
        self.button_delete_activity  = wx.Button(self.panel_activity_btns, -1, "Remove activity")
        self.button_save             = wx.Button(self, -1, "Save List")
        self.panel_teacher_btns      = wx.Panel(self, -1)
        self.button_add_teacher      = wx.Button(self.panel_teacher_btns, -1, "Add Teacher")
        self.button_edit_teacher     = wx.Button(self.panel_teacher_btns, -1, "Edit Teacher")
        self.button_del_teacher      = wx.Button(self.panel_teacher_btns, -1, "Remove Teacher")

        self.__set_properties()
        self.__do_layout()

        pub.subscribe(self.displayData, 'exculFilter.changed')
        
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag, self.list_ctrl_activity_pool)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag, self.list_ctrl_excul)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnBeginDrag, self.list_ctrl_teacher_pool)
        
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnActivities_Dclick, self.list_ctrl_activity_pool)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnExcul_Dclick,      self.list_ctrl_excul)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnTeachers_Dclick,   self.list_ctrl_teacher_pool)
        
        self.Bind(wx.EVT_BUTTON, self.OnAddActivity,    self.button_add_activity)
        self.Bind(wx.EVT_BUTTON, self.OnEditActivity,   self.button_edit_activity)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveActivity, self.button_delete_activity)
        
        self.Bind(wx.EVT_BUTTON, self.OnSave,           self.button_save)
        
        self.Bind(wx.EVT_BUTTON, self.OnAddTeacher,     self.button_add_teacher)
        self.Bind(wx.EVT_BUTTON, self.OnEditTeacher,    self.button_edit_teacher)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveTeacher,  self.button_del_teacher)

        self.__do_main()

    def __set_properties(self):
        self.label_header.SetForegroundColour(wx.Colour(255, 255, 255))
        self.panel_activity_btns.SetMinSize((321, 21))
        self.button_save.SetMinSize((300, 40))
        self.panel_teacher_btns.SetMinSize((-1, 21))

    def __do_layout(self):
        sizer_main = wx.FlexGridSizer(3, 3, 5, 5)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.panel_spc_topL,          1, wx.EXPAND, 0)
        sizer_main.Add(self.label_header,            0, 0, 0)
        sizer_main.Add(self.panel_spc_topR,          1, wx.EXPAND, 0)
        sizer_main.Add(self.list_ctrl_activity_pool, 1, wx.EXPAND, 0)
        sizer_main.Add(self.list_ctrl_excul,         1, wx.EXPAND, 0)
        sizer_main.Add(self.list_ctrl_teacher_pool,  1, wx.EXPAND, 0)
        sizer_5.Add(self.button_add_activity,        1, wx.LEFT | wx.EXPAND, 10)
        sizer_5.Add(self.button_edit_activity,       1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_5.Add(self.button_delete_activity,     1, wx.RIGHT | wx.EXPAND, 10)
        self.panel_activity_btns.SetSizer(sizer_5)
        sizer_main.Add(self.panel_activity_btns,     0, wx.BOTTOM, 10)
        sizer_main.Add(self.button_save,             1, wx.BOTTOM | wx.EXPAND, 10)
        sizer_6.Add(self.button_add_teacher,         1, wx.LEFT | wx.EXPAND, 10)
        sizer_6.Add(self.button_edit_teacher,        1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        sizer_6.Add(self.button_del_teacher,         1, wx.RIGHT | wx.EXPAND, 10)
        self.panel_teacher_btns.SetSizer(sizer_6)
        sizer_main.Add(self.panel_teacher_btns,      0, wx.BOTTOM, 10)
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        sizer_main.AddGrowableRow(1)
        sizer_main.AddGrowableCol(0)
        sizer_main.AddGrowableCol(2)
        
    def __do_main(self):
        self.SetSize(self.GetParent().GetSize())
        self.list_ctrl_activity_pool.InsertColumn(0, "ID", 20)
        self.list_ctrl_activity_pool.InsertColumn(1, "Activity pool", -1)
        
        self.list_ctrl_teacher_pool.InsertColumn(1, "ID", 20)
        self.list_ctrl_teacher_pool.InsertColumn(1, "Teacher pool", -1)
        
        self.list_ctrl_excul.InsertColumn(0, "ID",        20)
        self.list_ctrl_excul.InsertColumn(1, "Activity", 200)
        self.list_ctrl_excul.InsertColumn(2, "ID",        20)
        self.list_ctrl_excul.InsertColumn(3, "Teacher",  200)
        
        dt1 = TextDropTarget(self.list_ctrl_excul) # Make this control a Drop Target
        self.list_ctrl_excul.SetDropTarget(dt1)         # Link to Control

        dt2 = TextDropTarget(self.list_ctrl_excul) # Make this control a Drop Target
        self.list_ctrl_excul.SetDropTarget(dt2)    # Link to Control
    
    def displayData(self):
        #rint'school_id, semester, schYr, day', gVar.school_id, gVar.semester, gVar.schYr, gVar.dayNo
          
        self.insertion   = ''
        self.replace_id  =  0
        self.replaceName = ''

        listOfExcul = fetch.excul_groups_forSchSemYr(gVar.dayNo,  gVar.semester, gVar.school_id )
        #rint 'listOfExcul' , listOfExcul
        return
        lv.populateWithList(self.list_ctrl_excul, listOfExcul)
        
        otherActivities = fetch.excul_activities_otherThan(listOfExcul)
        lv.populateWithList(self.list_ctrl_activity_pool, otherActivities)

        otherTeachers = fetch.excul_teacherIDs_otherThan(listOfExcul)
        lv.populateWithList(self.list_ctrl_teacher_pool, otherTeachers)

    
    def OnActivities_Dclick(self, event):
        self.moveSelectedFromAtoB(self.list_ctrl_activity_pool,self.list_ctrl_excul)
        
    def OnTeachers_Dclick(self, event):
        self.moveSelectedFromAtoB(self.list_ctrl_teacher_pool, self.list_ctrl_excul)
           
    def OnExcul_Dclick(self, event):
        pass
    
    def moveSelectedFromAtoB(self, lvSource, lvDestination):
        selection = lv.GetSelectedItems(lvSource)
        if not selection: return
        # copy selected items to new listview
        for index in selection:
            id = lvSource.GetItemText(index)
            title = lvSource.GetItem(index, 1).GetText()

            indexD = lvDestination.Append(str(id))
            lvDestination.SetStringItem(indexD, 0, str(id))
            lvDestination.SetStringItem(indexD, 1, title)
            
        # finaly remove the selected items  in reverse order 
        selection = fetch.reverseList(selection) 
        for index in selection:  
            lvSource.DeleteItem(index)
            
        lv.decorateBanding(lvSource)
        lv.decorateBanding(lvDestination)
        
    def OnBeginDrag(self, event):
        lvBegin = event.GetEventObject()
        self.insertion = 'fail'
        """ Begin a Drag Operation """
        # Create DataObject to holds text to be dragged
        index  = lv.GetFirstSelected()
        if index < 0: return
        
        item_id = int(lvBegin.GetItemText(index))
        title   = lvBegin.GetItem(index, 1).GetText()
        source  = lvBegin.GetName()
        data    = '%s:%s:%s' % (str(item_id), str(title), source)
        
        todrop = wx.PyTextDataObject(data)

        # Create a DropSourceObject, for Drag operation
        drop_source = wx.DropSource(lvBegin)  # Create a DropSourceObject, for Drag operation
        drop_source.SetData(todrop)           # Associate the Data to be dragged with the Drop Source Object
        drop_source.DoDragDrop(True)          # Intiate the Drag Operation


        # if drop was successful remove item from source
        if self.insertion == 'activityInserted':
            #rint 'inserted'
            lvBegin.DeleteItem(index)
        
        elif self.insertion == 'teacherReplaced':
            lvBegin.DeleteItem(index)

            index2 = self.lv3.Append(str(self.replace_id))
            self.lv3.SetStringItem(index2, 0, str(self.replace_id))
            self.lv3.SetStringItem(index2, 1, self.replaceName)
            
        elif self.insertion == 'teacherInserted':
            lv.DeleteItem(index)

    def OnLv1LeftDclick(self, event):
        lv = event.GetEventObject()
        index = lv.GetFirstSelected()

        if index > -1:
            item_id = lv.GetItem(index, 0).GetText()
            title  = lv.GetItem(index, 1).GetText()
            
            indexD = self.lv2.Append(id + '\n\n')
            self.lv2.SetStringItem(indexD, 0, str(item_id))
            self.lv2.SetStringItem(indexD, 1, title)
            lv.DeleteItem(index)
        
    def OnLv2LeftDclick(self, event):
        lv = event.GetEventObject()
        # display a popup with 3 choices
        # 1: disolve activity
        # 2: remove teacher
        index = lv.GetFirstSelected()
        if index > -1:
            activity_id  = lv.GetItem(index, 0).GetText()
            activityName = lv.GetItem(index, 1).GetText()
            
            teacher_id  = lv.GetItem(index, 2).GetText()
            teacherName = lv.GetItem(index, 3).GetText()
            
            self.showPopupRemoveChoices(activity_id, activityName, teacher_id, teacherName)

        event.Skip() 
             
    def OnMenuDisolveSessionClick(self, event):
        lv = self.lv2
        index = lv.GetFirstSelected()
        if index > -1:
            item_id = lv.GetItem(index, 0).GetText()
            title   = lv.GetItem(index, 1).GetText()
            idT     = lv.GetItem(index, 2).GetText()
            nameT   = lv.GetItem(index, 3).GetText()
            
            indexA = self.lv1.Append(str(item_id))
            self.lv1.SetStringItem(indexA, 0, str(item_id))
            self.lv1.SetStringItem(indexA, 1, title)
            
            indexT = self.lv3.InsertStringItem(0, str(idT))
            self.lv3.SetStringItem(indexT, 0, str(idT))
            self.lv3.SetStringItem(indexT, 1, nameT)
                    
            lv.DeleteItem(index)
    
    def OnMenuReleaseTeacherClick(self, event):
        lv = self.lv2
        index = lv.GetFirstSelected()
        if index > -1:
            idT   = lv.GetItem(index, 2).GetText()
            nameT = lv.GetItem(index, 3).GetText()
            
            indexT = self.lv3.InsertStringItem(0, str(idT))
            self.lv3.SetStringItem(indexT, 0, str(idT))
            self.lv3.SetStringItem(indexT, 1, nameT)
                    
            self.lv2.SetStringItem(index, 2, '')
            self.lv2.SetStringItem(index, 3, '')
                    
    def showPopupRemoveChoices(self, activity_id, activityName, teacher_id='', teacherName=''):
        """
        Create and display a popup menu on dbl-click event
        """
        #if not hasattr(self, "popupID1"):
        self.popupID1 = wx.NewId()
        
        # make a menu
        menu = wx.Menu()
        
        # put an icon in the menu
        #item = wx.MenuItem(menu, self.popupID1,"Disolve session")
        #item.Bind(wx.EVT_LEFT_DCLICK, self.OnMenuDisolveSessionClick) 
        self.popupID1 = wx.NewId()
        item = menu.Append(self.popupID1, "Disolve session")
        self.Bind(wx.EVT_MENU, self.OnMenuDisolveSessionClick, item)
        

        if teacher_id:
            self.popupID2 = wx.NewId()
            item = menu.Append(self.popupID2,"Release teacher")
            self.Bind(wx.EVT_MENU, self.OnMenuReleaseTeacherClick, item)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()
    
    def OnSave(self, event):  
        #rint"Event handler `OnSave' not implemented!"
        event.Skip()

    def OnActivitySelected(self, event): 
        #rint"Event handler `OnActivitySelected' not implemented"
        event.Skip()

    def OnExculSelected(self, event):  
        #rint"Event handler `OnExculSelected' not implemented"
        event.Skip()

    def OnTeacherSelected(self, event): 
        #rint"Event handler `OnTeacherSelected' not implemented"
        event.Skip()

    def OnAddActivity(self, event): 
        #rint"Event handler `OnAddActivity' not implemented"
        event.Skip()

    def OnEditActivity(self, event): 
        #rint"Event handler `OnEditActivity' not implemented"
        event.Skip()

    def OnRemoveActivity(self, event): 
        #rint"Event handler `OnRemoveActivity' not implemented"
        event.Skip()

    def OnAddTeacher(self, event):  
        #rint"Event handler `OnAddTeacher' not implemented"
        event.Skip()

    def OnEditTeacher(self, event):  
        #rint"Event handler `OnEditTeacher' not implemented"
        event.Skip()

    def OnRemoveTeacher(self, event):
        #rint"Event handler `OnRemoveTeacher' not implemented"
        event.Skip()
        
        
class TextDropTarget(wx.TextDropTarget):            
    """ This object implements Drop Target functionality for Text """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped text """
        # Initialize the wx.TextDropTarget Object
        wx.TextDropTarget.__init__(self)
        # Store the Object Reference for dropped text
        self.obj = obj

    def OnDropText(self, x, y, data):
        global flag_insertion, g_replace_id
        self.insertion = 'fail'
        self.replace_id, self.replaceName = '', ''
        
        list_ctrl_drop = self.obj 
                                     
        data = str(data).split(':')
        id, title, source = data[0], data[1], data[2]

        destination = list_ctrl_drop.Name
        
        if source != destination:
              
            """ Implement Text Drop """
            ## When text is dropped, write it into the object specified
            # check to see what is at the drop mouse position
            index, flags = self.obj.HitTest((x, y))
 
            if source == 'lv1': 
                # if data comes from lv_activities              
                # append a new item (write to the first columns)
                index = self.obj.Append(id + '\n\n')
                self.obj.SetStringItem(index, 1, title)
                self.insertion = 'activityInserted'
                
            elif source == 'lv3':  
                # when the data comes from  lv_teachers          
                # if there is an activity at that position
                if index > -1:
                    # store the ID
                    self.replace_id  = self.obj.GetItem(index, 2).GetText()
                    self.replaceName = self.obj.GetItem(index, 3).GetText()
                    if self.replace_id:    
                        # set new details
                        self.obj.SetStringItem(index, 2, data[0])
                        self.obj.SetStringItem(index, 3, data[1]) 
                        
                        self.insertion = 'teacherReplaced'  
                        
                    else:
                        self.obj.SetStringItem(index, 2, data[0])
                        self.obj.SetStringItem(index, 3, data[1])
                        
                        self.insertion = 'teacherInserted' 