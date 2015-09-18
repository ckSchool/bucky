import wx, lv, gVar, fetch, loadCmb

import wx.lib.scrolledpanel as scrolled 
import wx.lib.inspection

import Dlg_ExculEditor

insertion = ''

class PanelExculViewer(wx.Panel):
    def _init_coll_bxs_mainLayout_Items(self, parent):
        parent.AddWindow(self.p_header, 0, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_mid, 1, border=0, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.p_status, 0, border=0, flag=wx.ALL | wx.EXPAND)

    def _init_coll_gbs_mid_Items(self, parent):
        parent.AddWindow(self.lv1, 0, border=10, flag=wx.ALL | wx.EXPAND)

    def _init_coll_bxs_status_Items(self, parent):
        parent.AddWindow(self.ts1, 1, border=0, flag=0)
        parent.AddWindow(self.ts2, 2, border=0, flag=0)

    def _init_coll_lv1_Columns(self, parent):
        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id',
              width=60)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading='Unallocated students', width=200)

    def __do_layout(self):
        self.bxs_mainLayout = wx.BoxSizer(orient=wx.VERTICAL)
        self.gbs_mid = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.bxs_status = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_bxs_mainLayout_Items(self.bxs_mainLayout)
        self._init_coll_gbs_mid_Items(self.gbs_mid)
        self._init_coll_bxs_status_Items(self.bxs_status)

        self.SetSizer(self.bxs_mainLayout)
        self.p_mid.SetSizer(self.gbs_mid)
        self.p_status.SetSizer(self.bxs_status)

    def _init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANELEXCULVIEWER,
              name='PanelExCulRoster', parent=prnt, pos=wx.Point(382, 230),
              size=wx.Size(1017, 570), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(1009, 542))

        self.p_header = wx.Panel(id=wxID_PANELEXCULVIEWERP_HEADER,
              name='p_header', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1009, 48), style=wx.TAB_TRAVERSAL)
        self.p_header.SetBackgroundColour(wx.Colour(0, 7, 79))

        self.panel111 = wx.Panel(id=wxID_PANELEXCULVIEWERPANEL111,
              name='panel111', parent=self.p_header, pos=wx.Point(0, 0),
              size=wx.Size(496, 48), style=wx.TAB_TRAVERSAL)

        self.l_sch = wx.StaticText(id=wxID_PANELEXCULVIEWERL_SCH,
              label='School year', name='l_sch', parent=self.panel111,
              pos=wx.Point(158, 0), size=wx.Size(57, 13), style=0)
        self.l_sch.SetForegroundColour(wx.Colour(255, 255, 255))

        self.c_day = wx.ComboBox(choices=[], id=wxID_PANELEXCULVIEWERC_DAY,
              name='c_day', parent=self.panel111, pos=wx.Point(342, 19),
              size=wx.Size(130, 21), style=wx.CAPTION, value='')
        self.c_day.SetLabel('')
        self.c_day.Bind(wx.EVT_COMBOBOX, self.OnC_dayCombobox,
              id=wxID_PANELEXCULVIEWERC_DAY)

        self.l_day = wx.StaticText(id=wxID_PANELEXCULVIEWERL_DAY, label='Day:',
              name='l_day', parent=self.panel111, pos=wx.Point(345, 0),
              size=wx.Size(24, 13), style=0)
        self.l_day.SetForegroundColour(wx.Colour(255, 255, 255))

        self.spc_semester = wx.SpinCtrl(id=wxID_PANELEXCULVIEWERSPC_SEMESTER,
              initial=1, max=100, min=0, name='spc_semester',
              parent=self.panel111, pos=wx.Point(280, 16), size=wx.Size(48, 24),
              style=wx.SP_ARROW_KEYS)
        self.spc_semester.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Times New Roman'))
        self.spc_semester.SetRange(1, 2)
        self.spc_semester.Bind(wx.EVT_SPIN, self.OnSpc_semesterSpin,
              id=wxID_PANELEXCULVIEWERSPC_SEMESTER)

        self.staticText2 = wx.StaticText(id=wxID_PANELEXCULVIEWERSTATICTEXT2,
              label='School:', name='staticText2', parent=self.panel111,
              pos=wx.Point(8, 1), size=wx.Size(36, 13), style=0)
        self.staticText2.SetForegroundColour(wx.Colour(255, 255, 255))

        self.staticText1 = wx.StaticText(id=wxID_PANELEXCULVIEWERSTATICTEXT1,
              label='Semester', name='staticText1', parent=self.panel111,
              pos=wx.Point(0, 0), size=wx.Size(46, 13), style=0)
        self.staticText1.SetForegroundColour(wx.Colour(255, 255, 255))

        self.spc_schYr = wx.SpinCtrl(id=wxID_PANELEXCULVIEWERSPC_SCHYR,
              initial=2010, max=2100, min=2000, name='spc_schYr',
              parent=self.panel111, pos=wx.Point(155, 17), size=wx.Size(115,
              23), style=wx.SP_ARROW_KEYS)
        self.spc_schYr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        self.spc_schYr.Bind(wx.EVT_SPIN, self.OnSpc_schYrSpin,
              id=wxID_PANELEXCULVIEWERSPC_SCHYR)

        self.c_schools = wx.ComboBox(choices=[],
              id=wxID_PANELEXCULVIEWERC_SCHOOLS, name='c_schools',
              parent=self.panel111, pos=wx.Point(9, 19), size=wx.Size(135, 21),
              style=wx.CAPTION, value='')
        self.c_schools.SetLabel('')
        self.c_schools.Bind(wx.EVT_COMBOBOX, self.OnC_schoolsCombobox,
              id=wxID_PANELEXCULVIEWERC_SCHOOLS)

        self.p_mid = wx.Panel(id=wxID_PANELEXCULVIEWERP_MID, name='p_mid',
              parent=self, pos=wx.Point(0, 48), size=wx.Size(1009, 469),
              style=wx.TAB_TRAVERSAL)

        self.lv1 = wx.ListView(id=wxID_PANELEXCULVIEWERLV1, name='lv1',
              parent=self.p_mid, pos=wx.Point(10, 10), size=wx.Size(206, 449),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        self.lv1.SetBackgroundColour(wx.Colour(223, 223, 223))
        self._init_coll_lv1_Columns(self.lv1)
        self.lv1.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,
              id=wxID_PANELEXCULVIEWERLV1)

        self.p_status = wx.Panel(id=wxID_PANELEXCULVIEWERP_STATUS,
              name='p_status', parent=self, pos=wx.Point(0, 517),
              size=wx.Size(1009, 25), style=wx.TAB_TRAVERSAL)
        self.p_status.SetBackgroundColour(wx.Colour(0, 0, 160))

        self.ts1 = wx.TextCtrl(id=wxID_PANELEXCULVIEWERTS1, name='ts1',
              parent=self.p_status, pos=wx.Point(0, 0), size=wx.Size(336, 25),
              style=0, value='')
        self.ts1.SetBackgroundColour(wx.Colour(0, 0, 128))

        self.ts2 = wx.TextCtrl(id=wxID_PANELEXCULVIEWERTS2, name='ts2',
              parent=self.p_status, pos=wx.Point(336, 0), size=wx.Size(672, 25),
              style=0, value='')
        self.ts2.SetBackgroundColour(wx.Colour(0, 0, 160))

        self.b_edit = wx.Button(id=wxID_PANELEXCULVIEWERB_EDIT,
              label='Open edititor', name='b_edit', parent=self.p_header,
              pos=wx.Point(515, 22), size=wx.Size(93, 23), style=0)
        self.b_edit.Bind(wx.EVT_BUTTON, self.OnB_editButton,
              id=wxID_PANELEXCULVIEWERB_EDIT)

        self.__do_layout()

    def __init__(self, parent, id):
        self._init_ctrls(parent)
        
        loadCmb.schDiv(self.c_schools)
        loadCmb.days(self.c_day)
             
        self.gbs_excul = wx.GridBagSizer(hgap=0, vgap=0)
        
        self.scrolledPanel = scrolled.ScrolledPanel(self.p_mid, - 1,  size=wx.DefaultSize) 
        self.scrollPanelSizer = self.gbs_excul
        self.scrolledPanel.SetSizer(self.scrollPanelSizer) 
        self.scrolledPanel.SetupScrolling() 

        self.gbs_mid.Add(self.scrolledPanel, 1, wx.EXPAND) 
        self.p_mid.Layout() 
        
        self.displayData()
        
    def start_panel(self):
        self.displayData()
        
    def displayData(self):
        # clear the panel
        self.scrolledPanel.DestroyChildren()
        self.gbs_excul.Clear()
        
        # collect the variables
        #gVar.schYr    = self.spc_schYr.Value
        gVar.semester = self.spc_semester.Value   
        sch_id        = fetch.cmbID(self.c_schools)
        dayNo         = fetch.cmbID(self.c_day)+1
        
        if not sch_id: return
        
        studentIDs_list=[]
        # get the excul list
        exculIDs   = fetch.exculIDs_forSch(dayNo, gVar.semester, sch_id)
        if exculIDs:
            exculCount = len(exculIDs)
            i = 0
            for excul_id in exculIDs:
                myLV = self.createLV(excul_id, i)
                # fill each listView with members
                studentIDs = lv.populateExcul(myLV, excul_id)
                studentIDs_list.extend(studentIDs)
                i += 1
                
        remainingStudents = fetch.exculRemainingStudents(sch_id, studentIDs_list)
        lv.populateExculRemainingStudents(self.lv1, remainingStudents)
        dt1 = TextDropTarget(self.lv1) # Make this control a Drop Target
        self.lv1.SetDropTarget(dt1)         # Link to Control           
        
        self.scrolledPanel.FitInside() 
        self.Layout() 
        
        
    def createLV(self, excul_id, itemNo):
        # create a list view for each activity
        # and place it into the grid-bag-sizer
        r, c = round(itemNo/4), itemNo%4

        wxID = 1000 + int(excul_id)
        nameLV = 'mylv%d' % itemNo
        
        myLV = wx.ListView(id=wxID, name=nameLV, parent=self.scrolledPanel,
              pos=wx.Point(752, 7), size=wx.Size(154, 225),
              style=wx.LC_SINGLE_SEL | wx.LC_REPORT)
        myLV.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='id',width=0)
          
        title = fetch.activityTitle(excul_id) 
        
        myLV.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading=title,width=150)   
        myLV.Bind(wx.EVT_LIST_BEGIN_DRAG, self.beginDrag,id=wxID)        
        self.gbs_excul.AddWindow(myLV, (r, c), border=10, flag=wx.EXPAND | wx.ALL, span=(1, 1))  

        dt1 = TextDropTarget(myLV) # Make this control a Drop Target
        myLV.SetDropTarget(dt1)         # Link to Control
        
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


    def OnB_editButton(self, event):
        dlg = Dlg_ExculEditor.create(None)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()


    def OnC_schoolsCombobox(self, event):
        self.displayData()

    def OnC_dayCombobox(self, event):
        self.displayData()

    def OnSpc_semesterSpin(self, event):
        self.displayData()

    def OnSpc_schYrSpin(self, event):
        self.displayData()
        
     
    def OnB_saveButton(self, event):
        lvs = self.scrolledPanel.GetChildren()
        #rint len(lvs)
        for lview in lvs:
            
            excul_id = lview.GetId()-1000
            #rint excul_id
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
            #rint sql
            
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

