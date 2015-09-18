import wx, fetch, gVar
import wx.lib.mixins.listctrl as listmix

#import DlgChangePassword
#import DlgLogin

from wx.lib.pubsub import pub

from PanelMonth     import PanelSemester
#from PanelCourses   import PanelCourses  as nb_courses
from PanelNB_excul  import PanelNB_excul as nb_excul
        
class Frame_Main_For_Teachers(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
    
        self.statusbar        = self.CreateStatusBar(3, 0)
        
        yr = str(gVar.schYr)
        
        self.panel_topbar     = wx.Panel(self, -1)
        self.panel_year       = wx.Panel(self.panel_topbar, -1)
        self.button_last      = wx.Button(self.panel_year,     -1, "<", style=wx.NO_BORDER)
        self.label_year       = wx.StaticText(self.panel_year, -1, yr,  style=wx.NO_BORDER | wx.ALIGN_CENTRE)
        self.button_next      = wx.Button(self.panel_year,     -1, ">", style=wx.NO_BORDER)
        
        self.panel_semester   = PanelSemester(self.panel_topbar, -1)
        self.panel_top_spc    = wx.Panel(self.panel_topbar, -1)
        self.panel_switch     = wx.Panel(self, -1)
        self.bitbut_login     = wx.BitmapButton(self.panel_switch, -1,
                                               wx.Bitmap(".\\images\\48\\ck_logo_mini.png",
                                               wx.BITMAP_TYPE_ANY), style=wx.NO_BORDER)
        self.panel_user       = wx.Panel(self.panel_switch,    -1)
        self.button_username  = wx.Button(self.panel_user,     -1, "",          style=wx.NO_BORDER)
        self.label_title      = wx.StaticText(self.panel_user, -1, "Chandra Kusuma")
        self.button_login     = wx.Button(self.panel_topbar,   -1, "LOGIN",     style=wx.NO_BORDER)
        self.button_help      = wx.Button(self.panel_topbar,   -1, "HELP",      style=wx.NO_BORDER)
        self.button_about     = wx.Button(self.panel_topbar,   -1, "ABOUT",     style=wx.NO_BORDER)
        self.button_recon     = wx.Button(self.panel_topbar,   -1, "RECONNECT", style=wx.NO_BORDER)
        self.button_courses   = wx.Button(self.panel_switch,   -1, "Classes",   style=wx.NO_BORDER)
        self.button_excul     = wx.Button(self.panel_switch,   -1, "Extra Curicular", style=wx.NO_BORDER)
        self.panel_spc31      = wx.Panel(self.panel_switch,    -1)
        
        #self.panel_classes    = nb_courses(self,  -1)
        self.panel_excul      = nb_excul(self,    -1)
        
        self.select_buttons   = [self.button_courses, self.button_excul]
        self.function_buttons = [self.button_login, self.button_help, 
                                 self.button_about,  self.button_recon]
        #self.view_panels      = [self.panel_classes, self.panel_excul]
        self.view_panels      = [self.panel_excul]

        pub.subscribe(self.refresh_child, 'refresh.children')
        
        self.button_username.Bind(wx.EVT_BUTTON,   self.OnUser)
        
        self.Bind(wx.EVT_BUTTON, self.OnLast,      self.button_last)
        self.Bind(wx.EVT_BUTTON, self.OnNext,      self.button_next)
        
        self.Bind(wx.EVT_BUTTON, self.OnLogin,     self.button_login)
        self.Bind(wx.EVT_BUTTON, self.OnHelp,      self.button_help)
        self.Bind(wx.EVT_BUTTON, self.OnAbout,     self.button_about)
        self.Bind(wx.EVT_BUTTON, self.OnReconnect, self.button_recon)
        
        self.Bind(wx.EVT_BUTTON, self.OnCourses,   self.button_courses)
        self.Bind(wx.EVT_BUTTON, self.OnExcul,     self.button_excul)
        
        for btn in self.function_buttons:
            btn.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent )
        
        self.__set_properties()
        self.__do_layout()
        self.__do_main()
        
    def OnMouseEvent(self, event, c = gVar.white):
        btn = event.GetEventObject()
        if event.GetEventType() == 10037: c = gVar.barkleys
        
        btn.SetForegroundColour(c)

    def __set_properties(self):
        white = gVar.white
        
        btn = self.button_last
        btn.SetMinSize((21, -1))
        btn.SetBackgroundColour(gVar.darkGrey)
        btn.SetForegroundColour(gVar.barkleys)
        btn.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.label_year.SetMinSize((32, 16))
        self.label_year.SetForegroundColour(gVar.barkleys)
        self.label_year.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        btn = self.button_next
        btn.SetMinSize((21, -1))
        btn.SetBackgroundColour(gVar.darkGrey)
        btn.SetForegroundColour(gVar.barkleys)
        btn.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        btn = self.button_username
        btn.SetBackgroundColour(gVar.mediumGrey)
        btn.SetForegroundColour(gVar.white)
        btn.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        self.panel_topbar.SetBackgroundColour(gVar.darkGrey)
        self.bitbut_login.SetBackgroundColour(gVar.mediumGrey)
        
        self.bitbut_login.SetSize(self.bitbut_login.GetBestSize())
        self.label_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.button_username.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        
        for btn in self.function_buttons:
            btn.SetBackgroundColour(gVar.darkGrey)
            btn.SetForegroundColour(white)
        
        for btn in self.select_buttons:
            btn.SetMinSize((100, 35))
            btn.SetBackgroundColour(gVar.barkleys)
            btn.SetForegroundColour(gVar.darkGrey)
        
        self.panel_switch.SetBackgroundColour(gVar.mediumGrey)

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.VERTICAL)
        sizer_switch = wx.BoxSizer(wx.HORIZONTAL)
        sizer_user   = wx.BoxSizer(wx.VERTICAL)
        sizer_topbar = wx.BoxSizer(wx.HORIZONTAL)
        sizer_year   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_year.Add(self.button_last, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_year.Add(self.label_year,  0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_year.Add(self.button_next, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 4)
        self.panel_year.SetSizer(sizer_year)
        
        sizer_topbar.Add(self.panel_year,     0, wx.EXPAND, 0)
        sizer_topbar.Add(self.panel_semester, 0, wx.EXPAND, 0)
        sizer_topbar.Add(self.panel_top_spc,  1, wx.EXPAND, 0)
        
        for btn in self.function_buttons:
            sizer_topbar.Add(btn, 0, wx.RIGHT , 5)
        self.panel_topbar.SetSizer(sizer_topbar)
        
        sizer_user.Add(self.button_username, 0, wx.LEFT  | wx.TOP, 10)
        sizer_user.Add(self.label_title,     0, wx.LEFT  , 10)
        self.panel_user.SetSizer(sizer_user)
        
        for btn in self.select_buttons:
            sizer_switch.Add(btn, 0, wx.LEFT  | wx.ALIGN_BOTTOM, 2)
        sizer_switch.Add(self.panel_spc31,      1, 0, 0)
        
        sizer_switch.Add(self.bitbut_login,  0, wx.LEFT  | wx.TOP | wx.RIGHT, 3)
        sizer_switch.Add(self.panel_user,           0, wx.RIGHT | wx.EXPAND, 200)
        self.panel_switch.SetSizer(sizer_switch)
        
        sizer_main.Add(self.panel_topbar, 0, wx.EXPAND, 0)
        sizer_main.Add(self.panel_switch, 0, wx.EXPAND, 0)
        for panel in self.view_panels:
            sizer_main.Add(panel,  1, wx.EXPAND, 0)
        
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
    
    def __do_main(self):
        if fetch.useConnection[0]=='localhost':
            self.SetTitle('Connected to Vostro')
        else:self.SetTitle('Localy connected to main server')
        self.current_panel_idx = 0
        self.SetSizeWH(1200, 900)
        self.Center()
        self.makeAdminPopupMenu()
        #self.login()
        gVar.user_id = 103
        
        self.button_last.Disable()
        self.button_next.Disable()

        txt = 'Loged in as: %s | LOGOUT' % fetch.employeeName(gVar.user_id)
        self.button_login.SetLabel(txt)
        #self.button_admin.Show(fetch.hasPermission('Admin'))
        self.showSemester(False)
        
        self.Layout()
        self.HighlightBtn(0)
        self.changeYear(0)
        
    def login(self):
        if not gVar.user_id > 0:
            self.button_login.SetLabel('Login')
            self.OnLogin(wx.Event)
        
        self.button_admin.Show(fetch.hasPermission('Admin'))
        self.Layout()
            
        self.HighlightBtn(0)
        self.changeYear(0)
        
    def OnCourses(  self, event): self.HighlightBtn(0)
    def OnExcul(    self, event): self.HighlightBtn(1)
        
    def OnGrades(   self, event): self.HighlightBtn(2)
        
    def clearStatusbar(self):
        self.statusbar.SetStatusText('',0)
        self.statusbar.SetStatusText('',1)
        self.statusbar.SetStatusText('',2)
        
    def HighlightBtn(self, idxBtn):
        self.clearStatusbar()
        self.current_panel_idx = idxBtn
        """
        self.panel_semester.Show(idxBtn > 0) 
        for x in range(len(self.select_buttons)):
            btn = self.select_buttons[x]
            btn.Freeze()
            
            if x == idxBtn:
                btn.SetBackgroundColour(gVar.barkleys)
                btn.SetForegroundColour(gVar.darkGrey)
                self.view_panels[x].Show()
                self.childPanel().filterReset()
                self.view_panels[x].displayData()
            
            else:
                btn.SetBackgroundColour(gVar.darkGrey)
                btn.SetForegroundColour(gVar.mediumGrey)
                self.view_panels[x].Hide()
                
            btn.Thaw()"""
        
    def OnLogin(self, event):
        #dlg=DlgLogin.create(None)
        #res = dlg.ShowModal()
        #dlg.Destroy()
        
        if res == wx.ID_OK:
            self.HighlightBtn(0)
            self.button_login.SetLabel('Change User')
            name = fetch.employeeName(gVar.user_id)
            self.button_username.SetLabel(name)

        elif res == wx.ID_CANCEL:
            if not gVar.user_id: self.Close()
        
    def OnHelp(self, event):   event.Skip()
    def OnAbout(self, event): event.Skip()
    def OnReconnect(self, event):  fetch.rc()
    
    def OnManage(self,event):
        dlg=DlgManageUserPrivileges.create(None)
        res = dlg.ShowModal()
        dlg.Destroy()
        
    def OnLast(self, event):  self.changeYear(-1)
    def OnNext(self, event):  self.changeYear(+1)
        
    def changeYear(self, x):
        #return
        gVar.schYr += x
        self.label_year.SetLabelText(str(gVar.schYr))
        self.childPanel().filterReset()
        self.refresh_child()
               
    def refresh_child(self):
        self.clearStatusbar()
        self.childPanel().displayData()
        
    def childPanel(self):
        shownPanel = self.view_panels[self.current_panel_idx]
        return shownPanel
    
    def OnUser(self, evt):
        dlg = DlgChangePassword.create(None)
        res = dlg.ShowModal()
        dlg.Destroy()
        
    def OnAdmin(self, evt):
        self.PopupMenu(self.mnu_admin)
        
    def makeAdminPopupMenu(self): # make a menu
        self.mnu_admin = wx.Menu()

        item = wx.MenuItem(self.mnu_admin, -1, "Manage Accounts")
        self.Bind(wx.EVT_MENU, self.OnManage, item)
        self.mnu_admin.AppendItem(item)
    
    def showSemester(self, show):
        self.panel_semester.Show(show)
        self.panel_topbar.Layout()    

def create(parent):
    return Frame_Main_For_Teachers(parent)
    
if __name__ == '__main__':
    app = wx.App(redirect=False)
    gVar.schYr = 2012
    frame = create(None)
    frame.Show()
    app.MainLoop()