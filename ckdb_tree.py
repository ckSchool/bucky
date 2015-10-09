import wx
import gVar
import fetch

import string
import time
import images
import dialog._SchYr

from wx.lib.combotreebox import ComboTreeBox

from accounts_ledger    import panel_ledger
from accounts_suppliers import panel_suppliers
from accounts_accounts  import panel_accounts
from accounts_journal   import panel_journal
from panel.panel_payments     import _payments
from panel_student_list import panel_student_list

from panel_base            import panel_base
from panel_course_fees     import panel_course_fees
from panel_edit_school     import panel_edit_school
from panel_edit_booking    import panel_edit_booking
from panel_edit_address    import panel_edit_address
from panel_edit_guardian   import panel_edit_guardian
from panel_student_details import panel_student_details

from panel_excul           import panel_excul

from panel_course_bookings              import panel_course_bookings
from panel_form_reregStatus             import panel_form_reregStatus
from panel_edit_rereg_status            import panel_edit_rereg_status
from panel_edit_booking_status          import panel_edit_booking_status
from panel_courses_by_year_picker       import panel_courses_picker
from panel_edit_booking_student_details import panel_edit_booking_student_details

#import DlgCourses

from wx.lib.pubsub      import setupkwargs
from wx.lib.pubsub      import pub

from panel_payments_registrations import panel_payments_registrations

payment_pages = ['Student Payments',  'Registration Payments']
account_pages = ['Journal', 'Ledger', 'Accounts', 'Suppliers']
school_pages  = ['Course Fees', 'Schools', 'Course Bookings', 'Courses By Year', 'Excur']
student_pages = ['Form Rereg Status', ]#'Bookings', 'Guardians',  'Booking Student Details'  ]
root_items    = {'Payments':payment_pages, 'Accounts':account_pages,
                 'School':school_pages, 'Students':student_pages}

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

        gVar.schYr = 2015

        menubar  = wx.MenuBar()
        fileMenu = wx.Menu()
        mnuitem1 = fileMenu.Append(-1, 'Forms',   'Edit Forms')
        mnuitem2 = fileMenu.Append(-1, 'Courses', 'Edit Courses')
        menubar.Append(fileMenu, '&Settings')

        self.SetMenuBar(menubar)

        self.statusbar = CustomStatusBar(self)
        self.SetStatusBar(self.statusbar)

        self.panel_tree = wx.Panel(self, -1)

        self.panel_tree_top = wx.Panel(self.panel_tree, -1)

        self.logo        = wx.Button(self.panel_tree_top,   -1, '')
        self.button_year = wx.Button(self.panel_tree_top,   -1, '2015/16')
        self.tree        = self.__createTreeCtrl() #self._createComboTreeBox(0)

        self.panel_main  = wx.Panel(self, -1)

        self.pane_base      = panel_base(self.panel_main, -1)
        self.pane_ledger    = panel_ledger(self.panel_main, -1)
        self.pane_journal   = panel_journal(self.panel_main, -1)
        self.pane_payments  = panel_payments(self.panel_main, -1)
        self.pane_accounts  = panel_accounts(self.panel_main, -1)
        self.pane_suppliers   = panel_suppliers(self.panel_main, -1)
        self.pane_course_fees = panel_course_fees(self.panel_main, -1)
        self.pane_edit_school = panel_edit_school(self.panel_main, -1)
        self.pane_edit_booking  = panel_edit_booking(self.panel_main, -1)
        self.pane_edit_address  = panel_edit_address(self.panel_main, -1)
        self.pane_edit_guardian = panel_edit_guardian(self.panel_main, -1)
        self.pane_student_list  = panel_student_list(self.panel_main, -1)

        self.pane_excul  = panel_excul(self.panel_main, -1)

        self.pane_student_details     = panel_student_details(self.panel_main, -1)
        self.pane_course_bookings     = panel_course_bookings(self.panel_main, -1)
        self.pane_edit_rereg_status   = panel_edit_rereg_status(self.panel_main, -1)
        self.pane_class_rereg_status  = panel_form_reregStatus(self.panel_main, -1)
        self.pane_edit_booking_status = panel_edit_booking_status(self.panel_main, -1)
        self.pane_payments_registrations = panel_payments_registrations(self.panel_main, -1)
        self.pane_courses_by_year_picker = panel_courses_picker(self.panel_main, -1)
        self.pane_edit_booking_student_details = panel_edit_booking_student_details(self.panel_main, -1)

        self.panes_dict = { 'Suppliers' :            self.pane_suppliers,
                            'Ledger':                self.pane_ledger,
                            'Accounts':              self.pane_accounts,
                            'Journal':               self.pane_journal,
                            'Student Payments':      self.pane_payments,
                            'Registration Payments': self.pane_payments_registrations,
                            'Base':                  self.pane_base,
                            'Excur':                 self.pane_excul,
                            'Course Fees':           self.pane_course_fees,
                            'Schools':               self.pane_edit_school ,
                            'Bookings':              self.pane_edit_booking  ,
                            'Address':               self.pane_edit_address  ,
                            'Guardians':             self.pane_edit_guardian ,
                            'Student Details':       self.pane_student_details  ,
                            'Course Bookings':       self.pane_course_bookings  ,
                            'Form Rereg Status':     self.pane_class_rereg_status  ,
                            'Edit Rereg Status':     self.pane_edit_rereg_status   ,
                            'Edit Booking Status':   self.pane_edit_booking_status   ,
                            'Courses By Year':       self.pane_courses_by_year_picker  ,
                            'Booking Student Details':self.pane_edit_booking_student_details,
                            'Students': self.pane_student_list
                            }

        self.Bind(wx.EVT_MENU,   self.OnForms,   mnuitem1)
        self.Bind(wx.EVT_MENU,   self.OnCourses, mnuitem2)
        self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnYear, self.button_year)

        pub.subscribe(self.write_to_statusbar0, 'write.statusbar0')
        pub.subscribe(self.write_to_statusbar1, 'write.statusbar1')
        pub.subscribe(self.write_to_statusbar2, 'write.statusbar2')
        pub.subscribe(self.lockdown,           'lockdown')
        pub.subscribe(self.unlockdown,         'unlockdown')
        pub.subscribe(self.updateSB,           'accounts.updateSB')

        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def write_to_statusbar0(self):
        self.statusbar.SetStatusText(str(gVar.status), 0)

    def write_to_statusbar1(self):
        self.statusbar.SetStatusText(str(gVar.status), 1)

    def write_to_statusbar2(self):
        self.statusbar.SetStatusText(str(gVar.status), 2)

    def __set_properties(self):
        self.SetMinSize((1000,600))
        self.Maximize()
        self.logo.SetMinSize((60, 60))
        self.SetTitle("CKDB")
        self.tree.SetMinSize((200, -1))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_tree = wx.BoxSizer(wx.VERTICAL)

        sizer_tree_top = wx.BoxSizer(wx.HORIZONTAL)

        sizer_tree_top.Add(self.logo, 0, 0,0)
        sizer_tree_top.Add(self.button_year, 0, 0,0)
        self.panel_tree_top.SetSizer(sizer_tree_top)

        sizer_tree.Add(self.panel_tree_top, 0, wx.EXPAND, 0)
        sizer_tree.Add(self.tree,           1, wx.EXPAND, 0)
        self.panel_tree.SetSizer(sizer_tree)

        for key in self.panes_dict:
            sizer_main.Add(self.panes_dict[key], 1, wx.EXPAND | wx.ALL, 5)
        self.panel_main.SetSizer(sizer_main)

        sizer_base.Add(self.panel_tree, 0, wx.EXPAND, 0)
        sizer_base.Add(self.panel_main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)

    def __createTreeCtrl(self):
        tree = wx.TreeCtrl(self.panel_tree)
        self.tree_item_ids = {}

        self.root = tree.AddRoot("The Root Item")
        tree.SetPyData(self.root, None)

        for root_item in root_items:
            root_item_id = tree.AppendItem(self.root, "%s" % root_item)
            tree.SetPyData(root_item_id, None)

            # add to dictionary
            self.tree_item_ids[root_item] = root_item_id

            children = root_items[root_item]

            for child in children:
                print 'child', child
                child_id = tree.AppendItem(root_item_id, "%s" % (child,))
                tree.SetPyData(child_id, None)

                # add to dictionary
                self.tree_item_ids[child] = child_id

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnItemSelected, tree)

        return tree

    def __do_main(self):
        user = 'admin'
        if user == 'admin':
            pass
        else:
            self.pane_payments.viewOnly()
            self.pane_payments_registrations.viewOnly()

        self.showPanel('Students')


    def OnItemSelected(self, event):
        self.item = event.GetItem()
        panel_name = self.tree.GetItemText(self.item)
        if panel_name:
            self.showPanel(panel_name)
            pub.sendMessage('tree.change')
        event.Skip()

    def showPanel(self, panel_name):
        self.current_panel_name = panel_name
        try:
            for key in self.panes_dict:
                self.panes_dict[key].Hide()
            p = self.panes_dict[panel_name]
            p.Show()

            print 'showPanel panel DisplayData'
            p.displayData()
        except:
            pass

        self.Layout()

    def refresh_data(self):
        self.showPanel(self.current_panel_name)

    def lockdown(self, ):
        #self.tree.Enable(False)
        self.panel_tree.Enable(False)
        for key in self.panes_dict:
            p = self.panes_dict[key]
            if p.IsShown():
                p.lockdown()

    def unlockdown(self, ):
        #self.tree.Enable()
        self.panel_tree.Enable()
        for key in self.panes_dict:
            p = self.panes_dict[key]
            if p.IsShown():
                p.unlockdown()

    def updateSB(self, val, idx):
        self.statusbar.SetStatusText(str(val), idx)

    def OnCloseWindow(self, event):
        self.statusbar.timer.Stop()
        del self.statusbar.timer
        self.Destroy()

    def OnYear(self, evt):
        dlg = DlgSchYr.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            if dlg.schYr != gVar.schYr:
                yr = dlg.schYr
                if yr != gVar.schYr:
                    gVar.schYr = yr
                    nxYr = yr+1
                    txt = '%d/%s' % (yr, str(nxYr)[2:4])
                    self.button_year.SetLabel(txt)
                    self.refresh_data()
        finally:
            dlg.Destroy()

    def OnCourses(self, evt):
        dlg = DlgCourses.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()

        finally:
            dlg.Destroy()

    def OnItemEntered(self, event):
        #self.log.WriteText('You entered: %s\n'%event.GetString())
        event.Skip()

    def OnForms(self, evt):
        dlg = DlgForms.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()

        finally:
            dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
