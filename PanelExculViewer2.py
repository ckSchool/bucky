#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.5 (standalone edition) on Thu Jul 26 08:49:52 2012

import wx

# begin wxGlade: extracode
# end wxGlade


#Boa:FramePanel:PanelExculViewer


import wx, lv, gVar, fetch, loadCmb

import wx.lib.scrolledpanel as scrolled 
import wx.lib.inspection

import Dlg_ExculEditor

insertion = ''


class PanelExculViewer(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PanelExculViewer.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.panel_selector = wx.Panel(self, -1)
        self.label_school = wx.StaticText(self.panel_selector, -1, "School")
        self.label_semester = wx.StaticText(self.panel_selector, -1, "Semester")
        self.label_day = wx.StaticText(self.panel_selector, -1, "Day")
        self.panel_2 = wx.Panel(self.panel_selector, -1)
        self.choice_school = wx.Choice(self.panel_selector, -1, choices=[])
        self.choice_semester = wx.Choice(self.panel_selector, -1, choices=[])
        self.choice_day = wx.Choice(self.panel_selector, -1, choices=[])
        self.button_open_editor = wx.Button(self.panel_selector, -1, "Open editor")
        self.list_ctrl_pool = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.scrolledPanel = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHOICE, self.OnSchool, self.choice_school)
        self.Bind(wx.EVT_CHOICE, self.OnSemester, self.choice_semester)
        self.Bind(wx.EVT_CHOICE, self.OnDay, self.choice_day)
        self.Bind(wx.EVT_BUTTON, self.OnOpenEditor, self.button_open_editor)
        # end wxGlade
        self.__do_main()
        
    def __set_properties(self):
        # begin wxGlade: PanelExculViewer.__set_properties
        self.SetBackgroundColour(wx.Colour(24, 24, 100))
        self.label_school.SetForegroundColour(wx.Colour(255, 255, 255))
        self.panel_selector.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.scrolledPanel.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.scrolledPanel.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PanelExculViewer.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledPanelSizer = wx.GridBagSizer(hgap=5, vgap=5)
        grid_sizer_1 = wx.FlexGridSizer(2, 4, 0, 10)
        grid_sizer_1.Add(self.label_school, 0, 0, 0)
        grid_sizer_1.Add(self.label_semester, 0, 0, 0)
        grid_sizer_1.Add(self.label_day, 0, 0, 0)
        grid_sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.choice_school, 0, 0, 0)
        grid_sizer_1.Add(self.choice_semester, 0, 0, 0)
        grid_sizer_1.Add(self.choice_day, 0, 0, 0)
        grid_sizer_1.Add(self.button_open_editor, 0, 0, 0)
        self.panel_selector.SetSizer(grid_sizer_1)
        sizer_1.Add(self.panel_selector, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 9)
        sizer_2.Add(self.list_ctrl_pool, 0, wx.EXPAND |wx.LEFT | wx.BOTTOM, 10)
        self.scrolledPanel.SetSizer(self.scrolledPanelSizer)
        sizer_2.Add(self.scrolledPanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 9)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        # end wxGlade
        
    def __do_main(self):
        # temp data
        self.schYr    = 2010
        self.semester =    1
        loadCmb.schDiv(self.choice_school)
        
        self.list_ctrl_pool.InsertColumn(0, 'Activity', 120)
        self.choice_semester.Append('1', 1)
        self.choice_semester.Append('2', 2)
        
        loadCmb.days(self.choice_day)
        
        self.panel_selector.Freeze()
        #
        self.choice_school.Select(2)
        self.choice_day.Select(0)
        self.choice_semester.Select(0)
        #
        self.panel_selector.Thaw()
        
    def OnSchool(self, event):  # wxGlade: PanelExculViewer.<event_handler>
        self.displayData()

    def OnSemester(self, event):  # wxGlade: PanelExculViewer.<event_handler>
        self.displayData()

    def OnDay(self, event):  # wxGlade: PanelExculViewer.<event_handler>
        self.displayData()

    def displayData(self):
        #rint'PanelExculViewer2: displayData'
        self.semester_no = self.choice_semester.GetStringSelection()
        
        # clear the panel
        self.scrolledPanel.DestroyChildren()
        self.scrolledPanelSizer.Clear()
        
        # collect the variables
        #gVar.schYr    = self.spc_schYr.Value
        self.semester = self.choice_semester.GetStringSelection()  
        school_id     = fetch.cmbID(self.choice_school)
        dayNo         = fetch.cmbID(self.choice_day)  
        
        #rint">>>", self.semester, ">>>",school_id,">>>", dayNo 
        
        
        if not (school_id and self.semester and dayNo): return
        
        studentIDs_list=[]
        # get the excul list
        exculIDs   = fetch.exculIDs_forSch(dayNo, self.semester, school_id)
        exculIDs = [1,2,3,5,6,7,8,9,11,112,12,13,14,15,16,17,18,19,21,23,24,25,26,27,28]
        
        if exculIDs:
            exculCount = len(exculIDs)
            i = 0
            for excul_id in exculIDs:
                myLV = self.createLV(excul_id, i)
                #rint'createLV ed:', myLV
                # fill each listView with members
                #studentIDs = lv.populateExcul(myLV, excul_id)
                #studentIDs_list.extend(studentIDs)
                i += 1
                
        remainingStudents = fetch.exculRemainingStudents(school_id, studentIDs_list)
        lv.populateExculRemainingStudents(self.list_ctrl_pool, remainingStudents)
        dt1 = TextDropTarget(self.list_ctrl_pool) # Make this control a Drop Target
        self.list_ctrl_pool.SetDropTarget(dt1)         # Link to Control           
        
        self.scrolledPanel.FitInside() 
        self.Layout() 
        
        
    def createLV(self, excul_id, itemNo):
        # create a list view for each activity
        # and place it into the grid-bag-sizer
        r, c = round(itemNo/4), itemNo%4

        wxID = 1000 + int(excul_id)
        nameLV = 'list_ctrl_%d' % itemNo
        
        myLV = wx.ListView(id=wxID, name=nameLV, parent=self.scrolledPanel,
              pos=wx.Point(0, 0), size=wx.Size(154, 225),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
          
        title = fetch.activityTitle(excul_id) 
        #rint'nameLV', nameLV, 'activityTitle', title
        
        myLV.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,id=wxID)        
        self.scrolledPanelSizer.AddWindow(myLV, (r, c), border=10, flag=wx.EXPAND | wx.ALL, span=(1, 1))  

        dt1 = TextDropTarget(myLV) # Make this control a Drop Target
        myLV.SetDropTarget(dt1)         # Link to Control
        
        myLV.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading = 'id',width=0)
        myLV.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading = title,width=150)
        
        return myLV
        
    def beginDrag(self, event):
        global insertion
        insertion = 'fail'
        lview = event.GetEventObject()
        
        """ Begin a Drag Operation """
        # Create DataObject to holds text to be dragged
        index = lview.GetFirstSelected()
        id = int(lview.GetItemText(index))
        title = lview.GetItem(index, 1).GetText()
        source = lview.GetName()
        data = '%s:%s:%s' % (str(id), str(title), source)
        
        tdo = wx.PyTextDataObject(data)
        
        # Create a DropSourceObject, for Drag operation
        tds = wx.DropSource(lview)
        
        # Associate the Data to be dragged with the Drop Source Object
        tds.SetData(tdo)
        
        # Intiate the Drag Operation
        tds.DoDragDrop(True)
        # if drop was successful remove item from source
        if insertion == 'ok': 
            lview.DeleteItem(index)
            lv.decorateBanding(lview)


    def OnOpenEditor(self, event): 
        dlg = Dlg_ExculEditor.create(None)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()


    def OnB_saveButton(self, event):
        lvs = self.scrolledPanel.GetChildren()
        ##rintlen(lvs)
        for lview in lvs:
            
            excul_id = lview.GetId()-1000
            ##rintexcul_id
            studentsInExcul = lview.ItemCount
            
            studentIDs = []
            if studentsInExcul:    
                for i in range(studentsInExcul):
                    student_id = lview.GetItem(i, 0).GetText()
                    ##rintstudent_id
                    studentIDs.append(student_id)
                studentIDs = "'%s'" % ','.join(studentIDs)
                
                
            if not studentIDs: studentIDs="''"
            sql = "UPDATE excul SET studentIDs=%s WHERE excul_id=%d" % (studentIDs, int(excul_id))
            ##rintsql
            
            updateDB.generic(sql)
            
class TextDropTarget(wx.TextDropTarget):    ## Define Text Drop Target class
    """ This object implements Drop Target functionality for Text """
    def __init__(self, obj):
        """ Initialize the Drop Target, passing in the Object Reference to
            indicate what should receive the dropped text """
        # Initialize the wx.TextDropTarget Object
        wx.TextDropTarget.__init__(self)
        # Store the Object Reference for dropped text
        self.obj = obj

    def OnDropText(self, x, y, data):
        global insertion
        lview = self.obj
        data = str(data).split(':')
        source =  data[2]
        lview.SetFocus()
        destination = lview.Name
        
        if source != destination:
            """ Implement Text Drop """
            # When text is dropped, write it into the object specified
            index = lview.Append(data[0] + '\n\n')
            lview.SetStringItem(index, 1, data[1])
            insertion = 'ok'
            ##rint' insertion = 0k'
            lv.decorateBanding(lview)



# end of class PanelExculViewer
