import wx
import data.gVar
import data.fetch
import data.loadCmb

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

from panel.base            import panel_base
from panel.course_fees      import panel_course_fees
from panel.edit_school       import panel_edit_school
from panel.edit_booking       import panel_edit_booking
from panel.edit_address        import panel_edit_address
from panel.edit_guardian        import panel_edit_guardian
from panel.student_details        import panel_student_details
from panel.add_edit_course        import panel_add_edit_course
from panel.course_bookings         import panel_course_bookings
from panel.class_reregStatus        import panel_class_reregStatus as panel_rereg_list
from panel.edit_rereg_status         import panel_edit_rereg_status
from panel.edit_booking_status        import panel_edit_booking_status
from panel.courses_by_year_picker      import panel_courses_picker
from panel.edit_booking_student_details import panel_edit_booking_student_details

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1)

        self.CreateStatusBar(1)
        pub.subscribe(self.change_statusbar, "change.statusbar")
        tempheading = ((" ",10), (" ",15), (" ",10))

        self.panel.login                  = panel.login(self, -1)

        self.panes = {}
        self.panes['base']                = self.panel.base                = panel.base(self, -1) # top horizontal ctrls
        self.panes['rereg_list']          = self.panel.rereg_list          = panel.rereg_list(self, -1)
        self.panes['edit_booking']        = self.panel.edit_booking        = panel.edit_booking(self, -1)
        self.panes['edit_courses']        = self.panel.courses             = panel.courses_picker(self, -1)
        self.panes['student_details']     = self.panel.student_details     = panel.student_details(self, -1)
        self.panes['add_edit_course']     = self.panel.add_edit_course     = panel.add_edit_course(self, -1)
        self.panes['course_bookings']     = self.panel.course_bookings     = panel.course_bookings(self,-1)
        self.panes['edit_rereg_status']   = self.panel.edit_rereg_status   = panel.edit_rereg_status(self, -1)
        self.panes['edit_booking_status'] = self.panel.edit_booking_status = panel.edit_booking_status(self, -1)
        self.panes['edit_guardian_data']  = self.panel.guardian_data       = panel.edit_guardian(self, 1)
        self.panes['course_fees']         = self.panel.course_fees         = panel.course_fees(self, -1)
        self.panes['edit_schools']        = self.panel.edit_school         = panel.edit_school(self, -1)
        self.panes['edit_address']        = self.panel.edit_address        = panel.edit_address(self, -1)
        self.panes['edit_booking_student_details'] = self.panel.edit_booking_student_details = panel.edit_booking_student_details(self, -1)

        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.__set_properties()
        self.__do_layout()
        self.__do_main()

    def __set_properties(self):
        self.SetTitle(" ")

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)

        sizer_main.Add(self.panel.login,    1, wx.EXPAND, 0)
        for key in self.panes:
            sizer_main.Add(self.panes[key], 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)

    def __do_main(self):
        gVar.school = "All"
        gVar.schYr  = 2014

        self.setTitle()

        self.SetSize((300,300))
        self.Center()
        self.Layout()
        gVar.panelHistory.append(self.panel.base)
        self.hidePanes()

        self.panel.login.OnLogin(wx.Event)

    def setTitle(self):
        txt = "BOOKINGS FOR %d" % gVar.schYr
        self.SetTitle(txt)

    def hidePanes(self):
        for key in self.panes:
            self.panes[key].Hide()
        self.Layout()

    def change_statusbar(self):
        self.SetStatusText(gVar.msg)

    def loggedIn(self):
        #rint'logged in'

        #self.EnableCloseButton(False)
        self.SetSize((1280,680))
        self.Center()

        self.panel.login.Hide()
        self.panel.base.Show()
        self.Layout()

        gVar.current_view = "bookings"
        self.panel.base.displayData()

    def hidePanes(self):
        for key in self.panes:
            self.panes[key].Hide()

    def goBack(self):
        #rint'gVar.editedFlag = ', gVar.editedFlag
        p = gVar.panelHistory.pop()

        p.Hide()
        last_panel.in_list = gVar.panelHistory[-1]
        #rint'goBack to ', last_panel.in_list.GetName()
        last_panel.in_list.Show()
        if gVar.editedFlag == True:
            #rint'gVar.editedFlag = True'
            last_panel.in_list.displayData()
            gVar.editedFlag == False
        self.Layout()

    def goTo(self, to_panel):
        #rintto_panel
        last_panel.in_list = gVar.panelHistory[-1]
        last_panel.in_list.Hide()

        gVar.editedFlag = False

        panel.to_show = self.panes[to_panel]
        panel.to_show.Show()
        panel.to_show.displayData()

        gVar.panelHistory.append(panel.to_show)
        self.Layout()

    def OnClose(self, evt):
        evt.Skip()
        return

        msg = "Close Now ?"
        caption ="Closing Down"
        style=(wx.YES_NO|wx.YES_DEFAULT|wx.ICON_EXCLAMATION)

        dlg = wx.MessageDialog(parent=None, message=msg, caption=caption, style=style)
        x = dlg.ShowModal()
        #rint(x == wx.ID_NO)
        if x == wx.ID_NO:
            dlg.Destroy()
            evt.Destroy()
        else:
            dlg.Destroy()
            evt.Skip()

class panel_login(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.SetName('panel.login')

        self.label_login        = wx.StaticText(self, -1, "Login")
        self.label_name         = wx.StaticText(self, -1, "Name")
        self.text_ctrl_name     = wx.TextCtrl(self,   -1, "andrew")
        self.label_password     = wx.StaticText(self, -1, "Password")
        self.text_ctrl_password = wx.TextCtrl(self,   -1, "andrew123", style=wx.TE_PASSWORD)
        self.button_login       = wx.Button(self,     -1, "Enter")
        self.panel.spc          = wx.Panel(self,      -1)

        self.label_login.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        sizer_login  = wx.BoxSizer(wx.VERTICAL)

        sizer_login.Add(self.label_login,        1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        sizer_login.Add(self.label_name,         0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_login.Add(self.text_ctrl_name,     0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_login.Add(self.label_password,     0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)
        sizer_login.Add(self.text_ctrl_password, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_login.Add(self.button_login,       0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        sizer_login.Add(self.panel.spc,          1, wx.EXPAND, 0)
        self.SetSizer(sizer_login)

        self.Bind(wx.EVT_BUTTON, self.OnLogin,          self.button_login)


        self.Show()
        self.Layout()

        self.__do_main()

    def __do_main(self):
        import hashlib
        import os

        password = str("andrew123")

        m = hashlib.md5()
        m.update(password)
        x = m.hexdigest()

    def OnLogin(self, evt):
        import hashlib
        import os

        name = self.text_ctrl_name.GetValue()
        password = str(self.text_ctrl_password.GetValue())

        #salt = os.urandom(16)

        m = hashlib.md5()
        m.update(password) # (salt + password)
        x = m.hexdigest()

        sql = "SELECT * FROM users WHERE name ='%s' AND password='%s'" % (name, password)
        #rintsql
        #rintfetch.getAllDict(sql)
        if fetch.getAllDict(sql): # change to check and set up user privilages

            # temp
            gVar.userIsAdmin = True


            self.GetTopLevelParent().loggedIn()


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

app = MyApp(redirect=False)
app.MainLoop()
