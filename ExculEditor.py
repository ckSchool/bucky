import wx
import math

import data.fetch   as fetch
import data.loadCmb as loadCmb
import data.gVar    as gVar
import data.images  as images

import wx.lib.mixins.listctrl as listmix

from ctrl.vList_drag_drop import VirtualList

import dialog._ExculDaysSetter
import dialog._NewEditExculActivityTitle
import dialog._NewEditExculActivity

gVar.schYr = 2014
symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(3)

        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-1, -2, -2])
        self.sizeChanged = False

        # Field 0 ... just text
        self.SetStatusText("A Custom StatusBar...", 0)
        # We're going to use a timer to drive a 'clock' in the last
        # field.
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
        self.SetStatusText(st, 2)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.SetTitle("Club Shuffler")
        self.SetSize((1200, 450))

        menubar  = wx.MenuBar()
        fileMenu = wx.Menu()
        mnuitem_save  = fileMenu.Append(-1, 'Save',  'Save')
        mnuitem_print = fileMenu.Append(-1, 'Print', 'Print')
        menubar.Append(fileMenu, '&File')
        clubMenu = wx.Menu()
        mnuitem_addClub  = clubMenu.Append(-1, 'Add Club',  'Add Club')
        mnuitem_editDays = clubMenu.Append(-1, 'Edit Days', 'Edit Days')
        menubar.Append(clubMenu, '&Clubs')

        self.SetMenuBar(menubar)


        self.Bind(wx.EVT_MENU, self.OnSave,  mnuitem_save)
        self.Bind(wx.EVT_MENU, self.OnPrint, mnuitem_print)

        self.Bind(wx.EVT_MENU, self.OnAddClub,  mnuitem_addClub)
        self.Bind(wx.EVT_MENU, self.OnEditDays, mnuitem_editDays)

        self.panel_filter    = wx.Panel(self, -1)
        self.panel_main      = wx.Panel(self, -1)

        self.choice_school   = wx.Choice(self.panel_filter, -1, choices=[])
        self.choice_semester = wx.Choice(self.panel_filter, -1, choices=[])

        self.rb_mon = wx.RadioButton(self.panel_filter, -1, 'Mon')
        self.rb_tue = wx.RadioButton(self.panel_filter, -1, 'Tue')
        self.rb_wed = wx.RadioButton(self.panel_filter, -1, 'Wed')
        self.rb_thr = wx.RadioButton(self.panel_filter, -1, 'Thur')
        self.rb_fri = wx.RadioButton(self.panel_filter, -1, 'Fri')
        self.rb_xxx = wx.RadioButton(self.panel_filter, -1, 'x')

        self.rbtns = [self.rb_mon, self.rb_tue, self.rb_wed,
                      self.rb_thr, self.rb_fri, self.rb_xxx ]

        self.vList_waiting       = VirtualList(self.panel_main, -1, style=wx.LC_REPORT)
        self.panel_clubListCtrls = wx.ScrolledWindow(self.panel_main, -1)

        self.sizer_clubs = wx.GridSizer(2, 2, 5, 5)
        self.panel_clubListCtrls.SetSizer( self.sizer_clubs)

        for btn in self.rbtns:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnDayChange, btn)
            btn.Hide()

        values = [1,2,3,4,5]
        self.rb_dict = dict(zip(self.rbtns, values))
        self.rb_rev_dict = dict(zip(values, self.rbtns))

        self.Bind(wx.EVT_CHOICE, self.OnFilterChange, self.choice_school)
        self.Bind(wx.EVT_CHOICE, self.OnFilterChange, self.choice_semester)
        #self.Bind(wx.EVT)
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.panel_clubListCtrls.SetScrollbars(1, 1, 1, 1)
        columns=( ('ID', 0), ('Unallocated', 150), ('Form', 50))
        self.vList_waiting.SetColumns(columns)
        self.vList_waiting.SetMinSize((300, -1))

        self.choice_school.Append('Primary',   2)
        self.choice_school.Append('Secondary', 3)

        self.choice_semester.Append('Semester 1', 1)
        self.choice_semester.Append('Semester 2', 2)

    def __do_layout(self):
        sizer_base   = wx.BoxSizer(wx.VERTICAL)
        sizer_filter = wx.BoxSizer(wx.HORIZONTAL)

        sizer_filter.Add(self.choice_semester, 0, wx.ALL, 5)
        sizer_filter.Add(self.choice_school,   0, wx.ALL, 5)

        for btn in self.rbtns:
            sizer_filter.Add(btn,      0, wx.ALL, 5)
        self.panel_filter.SetSizer(sizer_filter)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.vList_waiting,       0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        sizer_main.Add(self.panel_clubListCtrls, 1, wx.EXPAND, 0)
        self.panel_main.SetSizer(sizer_main)

        sizer_base.Add(self.panel_filter, 0, wx.EXPAND , 10)
        sizer_base.Add(self.panel_main,   1, wx.EXPAND ,  10)
        self.SetSizer(sizer_base)

    def __do_main(self):
        self.choice_semester.SetSelection(0)
        self.choice_school.SetSelection(0)
        self.OnFilterChange(wx.Event)

    def OnDayChange(self, event):
        self.displayData()

    def OnPrint(self, event):
        print 'print'

    def OnFilterChange(self, event):
        semester  = fetch.cmbID(self.choice_semester)
        school_id = fetch.cmbID(self.choice_school)
        for btn in self.rb_dict:
            btn.Hide()
        self.rb_xxx.Freeze()
        self.rb_xxx.SetValue(1)
        self.rb_xxx.Thaw()

        schedule = fetch.exculSchedule_forSchSemYr(school_id, semester, gVar.schYr)

        for row in schedule:
            day = row['day']
            rb  = self.rb_rev_dict[day]
            rb.SetValue(1)
            rb.Show()

        try:
            self.Layout()
        except:
            print "-"# can't set size of uninitialized sizer item"
        self.displayData()

    def displayData(self):
        day = 0
        for btn in self.rb_dict:
            if btn.GetValue():
                day = self.rb_dict[btn]
                btn.Show()

        semester  = fetch.cmbID(self.choice_semester)
        school_id = fetch.cmbID(self.choice_school)

        schedule_id = fetch.excul_schedule_id(day, semester, school_id, gVar.schYr)

        self.vList_waiting.DeleteAllItems()
        non_members = fetch.excul_unallocatedDATA(schedule_id)

        self.vList_waiting.SetItemMap(non_members)
        self.init_club_lists(schedule_id)
        self.Layout()

    def OnResize(self, event):
        self.Layout()

    def init_club_lists(self, schedule_id):
        club_dict = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        club_count = len(club_dict)
        rows = math.ceil(club_count/3 + .5)
        #
        if club_count > 0:
            try:
                self.sizer_clubs.DeleteWindows()
                self.sizer_clubs.Destroy()
                self.panel_clubListCtrls.DestroyChildren()
                self.AddNewSizerAndCtrls(schedule_id)
            except:
                self.AddNewSizerAndCtrls(schedule_id)
        else:
            if self.sizer_clubs:
                self.sizer_clubs.DeleteWindows()
        return

    def AddClubList(self, key, club_dict):
        club_id   = int(key)
        club_info = club_dict[club_id]
        club_name = club_info[2]
        members   = fetch.excul_studentList(club_id)
        vList     = VirtualList(self.panel_clubListCtrls, -1, style=wx.LC_REPORT)
        columns   = (('ID', 0), (club_name, 150),('Form', 50))

        vList.SetColumns(columns)
        vList.SetName(str(club_id))
        vList.SetItemMap(members)

        self.club_listCtrls.append(vList)
        self.sizer_clubs.Add(vList, 1, wx.EXPAND | wx.ALL, 5)

        # make list ctrl visable modual wide
        self.vClubListCtrls[key] = vList

        # add bindings
        # for wxMSW
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick, vList)

        # for wxGTK
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick, vList)

        self.Bind(wx.EVT_COMMAND_LEFT_DCLICK, self.OnDblClick, vList)

    def OnRightClick(self, event):
        vList =  event.GetEventObject()
        club_id = int(vList.GetName())

        groupInfo = fetch.excul_groupInfo(club_id)
        subject_name = groupInfo['subject_name']

        self.currentItem = vList.currentItem
        student_id       = vList.GetSelectedID()
        gVar.student_id  = student_id
        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne,   id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo,   id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)

        # make a menu
        menu = wx.Menu()
        # add some items
        title = "%s, %s, %s" % (subject_name, "Teacher", "Population")
        menu.SetTitle(title)
        menu.Append(self.popupID1, "Edit Club")
        menu.Append(self.popupID2, "Delete Club")
        menu.AppendSeparator()

        self.currentItem = vList.currentItem

        student_id = vList.GetSelectedID()
        item_has_focus = vList.GetFirstSelected()
        if item_has_focus > -1:
            menu.Append(self.popupID3, "View Student Details")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        position = self.ScreenToClient(wx.GetMousePosition())
        self.PopupMenu(menu, position)
        menu.Destroy()

    def OnPopupOne(self, event):
        print "OnPopupOne Edit Club"
        item = event.GetEventObject().GetName()

    def OnPopupTwo(self, event):
        print "OnPopupTwo Delete Club"
        item = event.GetEventObject().GetName()

    def OnPopupThree(self, event):
        print 'OnPopup 3 - Student Details'
        print  'gVar.student_id', gVar.student_id

    def OnDblClick(self, event):
        vList = event.GetEventObject()
        selected_item = vList.remove_selected_item()
        self.vList_waiting.AppendItem(selected_item)

    def AddNewSizerAndCtrls(self, schedule_id):
        club_dict = fetch.exculGroupsDATA_forScheduleID(schedule_id)
        number_of_ctrls = len(club_dict)

        rows = math.ceil(number_of_ctrls/3 + .5)
        if rows > 0:
            self.sizer_clubs = wx.GridSizer(rows, 3, 5, 5)
            self.panel_clubListCtrls.SetSizer(self.sizer_clubs)

            self.club_listCtrls = []
            self.vClubListCtrls = {}
            for key in club_dict:
                print 'add club  group id =', club_dict[key][0]
                self.AddClubList(key, club_dict)
            self.Layout()

    def OnSave(self, event):
        print 'OnSave'
        if not self.vClubListCtrls: return
        for key in self.vClubListCtrls:
            vList = self.vClubListCtrls[key]
            excul_id = int(vList.GetName())
            members = vList.itemDataMap

            if members:
                self.updateDB(excul_id, members)

    def updateDB(self, excul_group_id, members):
        sql = "DELETE FROM excul_students \
                WHERE excul_group_id =%d " % excul_group_id
        fetch.updateDB(sql)
        for key in members:
            student_id, name, form = members[key]
            sql = "INSERT INTO excul_students \
                               (student_id, excul_group_id) \
                        VALUES (%d, %d)" % (student_id, excul_group_id)
            fetch.updateDB(sql)

    def OnAddClub(self, ):
        pass
        print 'OnAddClub'


    def OnEditDays(self, ):
        pass
        print 'OnEditDays'

if __name__ == "__main__":
    schYr = 2014
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
