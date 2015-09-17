import  wx, gVar, fetch
import  string, time, images

from accounts_ledger    import panel_ledger
from accounts_suppliers import panel_suppliers 
from accounts_accounts  import panel_accounts
from accounts_journal   import panel_journal
from panel_payments     import panel_payments

import DlgCourses

from wx.lib.pubsub      import setupkwargs
from wx.lib.pubsub      import pub

from panel_payments_registrations import panel_payments_registrations

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-1, -2, -2])
        self.sizeChanged = False
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.SetStatusText("A Custom StatusBar...", 0)

        # This will fall into field 1 (the second field)
        #self.cb = wx.CheckBox(self, 1001, "toggle clock")
        #self.Bind(wx.EVT_CHECKBOX, self.OnToggleClock, self.cb)
        #self.cb.SetValue(True)

        # set the initial position of the checkbox
        #self.Reposition()

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

    """
    # the checkbox was clicked
    def OnToggleClock(self, event):
        if self.cb.GetValue():
            self.timer.Start(1000)
            self.Notify()
        else:
            self.timer.Stop()


    def OnSize(self, evt):
        evt.Skip()
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True


    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()


    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        rect.x += 1
        rect.y += 1
        self.cb.SetRect(rect)
        self.sizeChanged = False"""


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        mnuitem1 = fileMenu.Append(-1, 'Forms',   'Edit Forms')
        mnuitem2 = fileMenu.Append(-1, 'Courses', 'Edit Courses')
        
        menubar.Append(fileMenu, '&Settings')
       
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnForms,   mnuitem1)
        self.Bind(wx.EVT_MENU, self.OnCourses, mnuitem2)
        
        self.sb = CustomStatusBar(self)
        self.SetStatusBar(self.sb)

        self.panel_left  = wx.Panel(self, -1)
        self.logo        = wx.Button(self.panel_left,   -1, '')
        self.button_year = wx.Button(self.panel_left,   -1, '2014/15')
        self.tree        = wx.TreeCtrl(self.panel_left, -1, style=wx.TR_HAS_BUTTONS + wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER)
        
        gVar.schYr = 2015
    
        self.pane_suppliers  = panel_suppliers(self,  -1)
        self.pane_ledger     = panel_ledger(self, -1)
        self.pane_accounts   = panel_accounts(self,  -1)
        self.pane_journal    = panel_journal(self,    -1)
        
        self.pane_payments   = panel_payments(self,             -1)
        self.pane_payments_registrations = panel_payments_registrations(self, -1)

        self.panes_dict = { 'Suppliers' : self.pane_suppliers,
                            'Ledger':     self.pane_ledger,
                            'Accounts':   self.pane_accounts,
                            'Journal':    self.pane_journal,
                            'Student Payments':   self.pane_payments,
                            'Registration Payments':   self.pane_payments_registrations}
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeItemSelected, self.tree)
        
        pub.subscribe(self.lockdown,   'lockdown')
        pub.subscribe(self.unlockdown, 'unlockdown')
        pub.subscribe(self.updateSB,   'accounts.updateSB')

        self.__set_properties()
        self.__do_layout()
        self.__do_main()
    
           
    def __set_properties(self):
        self.logo.SetMinSize((-1, 120))
        self.SetTitle("Accounts")
        self.tree.SetMinSize((150,-1))
        self.Maximize()

    def __do_layout(self):
        sizer_main   = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left   = wx.BoxSizer(wx.VERTICAL)
        
        sizer_left.Add(self.logo,        0, wx.EXPAND, 0)
        sizer_left.Add(self.button_year, 0, wx.EXPAND, 0)
        sizer_left.Add(self.tree,        1, wx.EXPAND, 0)
        self.panel_left.SetSizer(sizer_left)
        
        self.panes = [self.panel_left, self.pane_suppliers, self.pane_ledger,  self.pane_journal, self.pane_accounts,self.pane_payments, self.pane_payments_registrations]
        
        for p in self.panes:
            sizer_main.Add(p,     0, wx.EXPAND | wx.BOTTOM, 5)
        """sizer_main.Add(self.panel_left,     0, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_suppliers, 1, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_ledger,    1, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_journal,   1, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_accounts,  1, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_payments,  1, wx.EXPAND | wx.BOTTOM, 5)
        sizer_main.Add(self.pane_payments_registrations, 1, wx.EXPAND | wx.BOTTOM, 5)"""
        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        
        
    def __do_main(self):
        user = 'admin'
        
        if user == 'admin':
            pass
        else:
            self.pane_payments.viewOnly()
            self.pane_payments_registrations.viewOnly()
        
        self.loadTree()
        self.showPanel(self.pane_journal)
        
        self.tree.SetItemDropHighlight(self.tree_item_ids['Journal'])
        
        
        res = fetch.journal_entries_by_schYr(gVar.schYr)
        #print res

        for row in res:
            print row['id'], row
            
        # clean up db
        # = "DELETE FROM PembayaranD WHERE amount IS Null"
        # fetch.updateDB(sql)
            
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
    def OnForms(self, evt):
        dlg = DlgForms.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
    
    def OnCourses(self, evt):
        dlg = DlgCourses.create(None)
        try:
            dlg.displayData()
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()

    def OnCloseWindow(self, event):
        self.sb.timer.Stop()
        del self.sb.timer
        self.Destroy()
        
    def loadTree(self):
        self.tree_item_ids = {}

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        smileidx    = il.Add(images.Smiles.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il

        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.
        self.Centre()

        self.root = self.tree.AddRoot("")
        self.tree.SetPyData(self.root, None)
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        
        root_items = ['Payments', 'Accounts']
        
        panel_payments_registrations
        
        for root_item in root_items:
            root_child = self.tree.AppendItem(self.root, "%s" % root_item)
            
            self.tree_item_ids[root_item] = root_child
            
            self.tree.SetPyData(   root_child, None)
            self.tree.SetItemImage(root_child, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(root_child, fldropenidx, wx.TreeItemIcon_Expanded)
            
            if root_item == 'Payments':
                payment_pages = [('Student Payments',      'Student Payments'), 
                                 ('Registration Payments', 'Registration Payments')]
                for payment_page in payment_pages:
                    payments_child = self.tree.AppendItem(root_child, "%s" % payment_page[0])
                    
                    self.tree_item_ids[payment_page[0]] = payments_child
                    
                    self.tree.SetPyData(   payments_child, self.panes_dict[  payment_page[1]])
                    self.tree.SetItemImage(payments_child, fldridx,     wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(payments_child, fldropenidx, wx.TreeItemIcon_Expanded)
                    
            if root_item == 'Accounts':
                account_items = ['Accounts', 'Journal', 'Ledger', 'Suppliers']
                for account_item in account_items:
                    account_child = self.tree.AppendItem(root_child, "%s" % account_item)
                    
                    self.tree_item_ids[account_item] = account_child
                    
                    self.tree.SetPyData(   account_child, self.panes_dict[account_item])
                    self.tree.SetItemImage(account_child, fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(account_child, fldropenidx, wx.TreeItemIcon_Expanded)
                
        #self.tree.Expand(self.root)
        
    def OnTreeItemSelected(self, event):
        self.item = event.GetItem()
        self.showPanel(self.tree.GetPyData(self.item))
        #pub.sendMessage('tree.change')
        event.Skip()
        
    def showPanel(self, panel):
        try:
            panel.Show()
            for key in self.panes_dict:
                self.panes_dict[key].Hide()
            panel.Show()
            print 'showPanel panel DisplayData'
            panel.displayData()
        except:
            pass
        self.Layout()
        
    def updateSB(self, val, idx):
        self.sb.SetStatusText(str(val), idx)
    
    def lockdown(self, ):
        self.tree.Enable(False)
        self.panel_left.Enable(False)
        for key in self.panes_dict:
            p = self.panes_dict[key]
            if p.IsShown():
                p.lockdown()
    
    def unlockdown(self, ):
        self.tree.Enable()
        self.panel_left.Enable()
        for key in self.panes_dict:
            p = self.panes_dict[key]
            if p.IsShown():
                p.unlockdown()
        
if __name__ == "__main__":
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
