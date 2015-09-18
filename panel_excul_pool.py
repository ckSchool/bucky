import wx, gVar, fetch, loadCmb

import wx.lib.scrolledpanel as scrolled 

from PanelListSwap import PanelListSwap

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class panel_excul_pool(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        
	self.SetName('panel_excul_pool')
	
        self.statusbar    = self.GetTopLevelParent().statusbar
        
        self.panel_main   = wx.Panel(self, -1)
        self.panel_bottom = wx.Panel(self, -1)
        
        self.swap_pool     = PanelListSwap(self.panel_main, -1)
        self.swap_selected = PanelListSwap(self.panel_main, -1)

        self.panel_btnL       = wx.Panel(self.panel_bottom, -1)
        self.button_delete    = wx.Button(self.panel_btnL,  -1, 'Delete')
        self.button_edit      = wx.Button(self.panel_btnL,  -1, 'Edit')
        self.button_new       = wx.Button(self.panel_btnL,  -1, 'New')
        self.panel_spc        = wx.Panel(self.panel_btnL,   -1)
        self.button_save      = wx.Button(self.panel_btnL,  -1, 'Save')
        
        self.panel_activities = wx.Panel(self.panel_main, -1)
        self.panel_teacher    = wx.Panel(self.panel_main, -1)

        '''self.button_add_activity    = wx.Button(self.panel_activities, -1, ">", style=wx.NO_BORDER)
        self.button_remove_activity = wx.Button(self.panel_activities, -1, "X", style=wx.NO_BORDER)
        
        self.button_add_teacher     = wx.Button(self.panel_teacher, -1, '<', style=wx.NO_BORDER)
        self.button_remove_teacher  = wx.Button(self.panel_teacher, -1, 'X', style=wx.NO_BORDER)'''
        
        self.panel_main.heading_pool     = (('id',10), ('name',10), ('',10)) 
        self.panel_main.heading_selected = (('id',10), ('name',10), ('',10))
        
        self.__do_properties()
        self.__do_layout()
        self.__do_binds()
        self.__do_main()
        
    def __do_binds(self):
        pub.subscribe(self.displayData, 'exculFilter.changed')
        
        self.button_delete.Bind(wx.EVT_BUTTON,                  self.OnDelete)
        self.button_edit.Bind(wx.EVT_BUTTON,                    self.OnEdit)
        
        self.button_new.Bind(wx.EVT_BUTTON,                     self.OnNew)
        self.button_save.Bind(wx.EVT_BUTTON,                    self.OnSave)
        
        '''self.button_add_activity.Bind(wx.EVT_BUTTON,            self.OnInA )
        self.button_remove_activity.Bind(wx.EVT_BUTTON,         self.OnOutA)
        
        self.button_add_teacher.Bind(wx.EVT_BUTTON,             self.OnInT)
        self.button_remove_teacher.Bind(wx.EVT_BUTTON,          self.OnOutT)'''

    def __do_properties(self):
        pass
        '''self.button_add_activity.SetMinSize(   (30, -1))
        self.button_remove_activity.SetMinSize((30, -1))
        self.button_add_teacher.SetMinSize(    (30, -1))
        self.button_remove_teacher.SetMinSize( (30, -1))'''
        
    def __do_layout(self):
        sizer_base   = wx.BoxSizer(wx.VERTICAL)
        sizer_main   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btnsL  = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_main.Add(self.swap_pool,     1, wx.EXPAND, 0)
        sizer_main.Add(self.swap_selected, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_btnsL.Add(self.button_delete, 0, 0, 0)
        sizer_btnsL.Add(self.button_new,    0, 0, 0)
        sizer_btnsL.Add(self.button_edit,   0, 0, 0)
        sizer_btnsL.Add(self.panel_spc,     1, 0, 0)
        sizer_btnsL.Add(self.button_save,   0, wx.ALL, 20)
        self.panel_btnL.SetSizer(sizer_btnsL)
        
        sizer_bottom.Add(self.panel_btnL,  1, 0, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_base.Add(self.panel_main,   1, wx.EXPAND, 0)
        sizer_base.Add(self.panel_bottom, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)

    def __do_main(self):
        self.replace_id, self.insertion, self.replaceName = 0, '', ''
        heading = (('id',40), ('name',80))
        
        self.swap_pool.headingPool = heading
        self.swap_pool.headingSelection = heading
        self.symbols = {"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR,  "i_idx":wx.ART_QUESTION}
        #self.swap_pool.initHeadings()
        
        self.swap_selected.headingPool = heading
        self.swap_selected.headingSelection = heading
        self.symbols = {"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR,  "i_idx":wx.ART_QUESTION}
        #self.swap_selected.initHeadings()

    def doList(self, listCtrl, sql):
        DATA = fetch.DATA(sql)
        listCtrl.SetItemMap(DATA)
        
    def displayData(self):
        activityIDs =''
        teacherIDs  =''
        return
    
        if self.exculrange_id:
            activityIDs = fetch.exculActivityIDs_forRange(self.exculrange_id)
            teacherIDs  = fetch.exculTeacherIDs_forRange(self.exculrange_id)
	    #rint'fetch.exculTeacherIDs_forRange(self.exculrange_id)', teacherIDs

        if activityIDs:
            activityIDs = activityIDs.split(',')
        else: activityIDs = []
        return
        lv.populateActivities(self.lv_activitiesSelected, activityIDs)
        
        otherActivities = fetch.excul_activities_otherThan(activityIDs)
        lv.populateWithList(self.lv_activityPool, otherActivities)
        
        #rint '>>>>>>>>teacherIDs befor split ;', teacherIDs
        if teacherIDs:
            teacherIDs = teacherIDs.split(',')
        else:
            teacherIDs  = []
        #rint '>>>>>>>>teacherIDs after split;', teacherIDs
        lv.populateExculTeachers(self.lv_teachersSelected, teacherIDs)
        
        otherTeacherIDs = fetch.excul_teacherIDs_otherThan(teacherIDs)
        #rint 'otherTeacherIDs', otherTeacherIDs
        #lv.populateExculTeachers(self.lv_teacherPool, otherTeacherIDs)

        
    def OnBeginDrag(self, event):
        lview = event.GetEventObject()
        self.insertion = 'fail'
        
        ''' Begin a Drag Operation '''
        #rint lview.GetName()
        
        # Create DataObject to holds text to be dragged
        index  = lview.GetFirstSelected()
        if index < 0: return
        
        # Create a DropSourceObject, for Drag operation
        id     = int(lview.GetItemText(index))
        title  = lview.GetItem(index, 1).GetText()
        
        source = lview.GetName()
        data   = '%s:%s:%s' % (str(id), str(title), source)
        
        tdo = wx.PyTextDataObject(data)
        tds = wx.DropSource(lview)
        
        # Associate the Data to be dragged with the Drop Source Object
        tds.SetData(tdo)
        
        # Intiate the Drag Operation
        tds.DoDragDrop(True)
        
        # if drop was successful remove item from source
        if self.insertion == 'ok':
            lview.DeleteItem(index)
            
        lv.decorateBanding(lview)  
            
    def OnActivityPoolDClick(self, event):
        self.moveSelectedFromAtoB(self.lv_activityPool,self.lv_activitiesSelected)

    def OnActivityDClick(self, event):
        self.moveSelectedFromAtoB(self.lv_activitiesSelected, self.lv_activityPool)
        
    def OnInA(self, event):
        self.moveSelectedFromAtoB(self.lv_activityPool, self.lv_activitiesSelected)

    def OnOutA(self, event):
        self.moveSelectedFromAtoB(self.lv_activitiesSelected, self.lv_activityPool)
        
#-------------------------------------------------------------------------------
    def OnTeacherPoolDClick(self, event):
        self.moveSelectedFromAtoB(self.lv_teacherPool, self.lv_teachersSelected)

    def OnTeacherDClick(self, event):
        self.moveSelectedFromAtoB(self.lv_teachersSelected, self.lv_teacherPool)
        
    def OnInT(self, event):
        self.moveSelectedFromAtoB(self.lv_teacherPool, self.lv_teachersSelected)

    def OnOutT(self, event):
        self.moveSelectedFromAtoB(self.lv_teachersSelected, self.lv_teacherPool)

#-------------------------------------------------------------------------------
    def moveSelectedFromAtoB(self, lvSource, lvDestination):
        selection = lv.GetSelectedItems(lvSource)
        if not selection: return
        # copy selected items to new listview
        for index in selection:
            lvid   = lvSource.GetItemText(index)
            title  = lvSource.GetItem(index, 1).GetText()

            indexD = lvDestination.Append(str(lvid))
            lvDestination.SetStringItem(indexD, 0, str(lvid))
            lvDestination.SetStringItem(indexD, 1, title)
            
        # finaly remove the selected items  in reverse order 
        selection  = fetch.reverseList(selection) 
        for index in selection:  
            lvSource.DeleteItem(index)
            
        lv.decorateBanding(lvSource)
        lv.decorateBanding(lvDestination)
#-------------------------------------------------------------------------------

    def OnC_schoolsCombobox(self, event):
        self.displayData()

    def OnC_dayCombobox(self, event):
        self.displayData()

    def OnSpc_semesterSpin(self, event):
        self.displayData()

    def OnSpc_schYrSpin(self, event):
        self.displayData()

    def OnDelete(self, event):
        event.Skip()

    def OnEdit(self, event):
        event.Skip()

    def OnNew(self, event):
        event.Skip()

    def OnSave(self, event):
        g_sch_id        = fetch.cmbID(self.c_schools)
        g_day_no        = fetch.cmbID(self.c_day)+1
        g_semester_no   = self.spc_semester.Value
        g_schYr         = self.spc_schYr.Value
        
        lvA = self.lv_activitiesSelected
        lvT = self.lv_teachersSelected
        
        tCount, aCount = lvT.ItemCount, lvA.ItemCount
        #rint 'tCount, aCount',tCount, aCount
        listT, listA =[],[]
        
        if aCount: 
            for i in range(aCount):
                #rint 'saving activity index ', i 
                listA.append(lvA.GetItem(i,0).GetText())
        
        if tCount: 
            for i in range(tCount): 
                #rint 'saving teacher index ', i
                listT.append(lvT.GetItem(i,0).GetText())

        
        teacherIDs  = "'%s'" % ','.join(listT)
        activityIDs = "'%s'" % ','.join(listA)
        
        if self.exculrange_id:
            sql = "UPDATE exculrange SET activityIDS=%s, teacherIDs=%s \
                    WHERE exculrange_id=%d" % (activityIDs, teacherIDs, self.exculrange_id)
        else:
            sql = "INSERT INTO exculrange \
                   SET activityIDS=%s, teacherIDs=%s, \
                       sch_id=%d, schYr=%d, semester_no=%d, day_no=%d" % (
                       activityIDs, teacherIDs, g_sch_id, g_schYr, 
                       g_semester_no, g_day_no)
        #rint sql
        updateDB.generic(sql)

class TextDropTarget(wx.TextDropTarget):
    
# Define Text Drop Target class             
    """ This object implements Drop Target functionality for Text """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped text """
        # Initialize the wx.TextDropTarget Object
        wx.TextDropTarget.__init__(self)
        # Store the Object Reference for dropped text
        self.obj = obj

    def OnDropText(self, x, y, data): 
        self.insertion = 'fail'
        lvd = self.obj 
        self.replace_id, self.replaceName = '', ''
            
        data = str(data).split(':')
        id, title, source = data[0], data[1], data[2]

        destination = lvd.Name
        if source.startswith('lv_act') and destination.startswith('lv_act'):
            typeSame = True
        elif source.startswith('lv_tea') and destination.startswith('lv_tea'):
            typeSame = True
        else:
            typeSame = False
            
        if source != destination and typeSame:
            """ Implement Text Drop """
            ## When text is dropped, write it into the object specified
            # check to see what is at the drop mouse position
            index, flags = self.obj.HitTest((x, y))
          
            index = self.obj.Append(id + '\n\n')
            self.obj.SetStringItem(index, 0, data[0])
            self.obj.SetStringItem(index, 1, data[1]) 
                        
            self.insertion = 'ok'
            #rint '  self.insertion = ok'
            lv.decorateBanding(self.obj)
