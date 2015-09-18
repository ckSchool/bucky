import pyodbc
import pymysql

connmy = pymysql.connect(db='ckdb',
                         user='root',
                         passwd='andrew',
                         host='localhost',
                         autocommit=True)
curmy = connmy.cursor()

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

sql =  "TRUNCATE TABLE absences"
curmy.execute(sql)

for yr in (2005,2006,2007,2008,2009,2010,2011,2012,2013,2014):
    ##rintyr
    for month in (1,2,3,4,5,6,7,8,9,10,11,12):
        sql = "select * from Absensi where TahunAjaran =%d and Bulan =%d" % (yr,month)
        ##rintsql
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            
            for row in rows:
                ##rintrow
                id = row[0]
                alldays = row[3:]
                day = 0 
                for c in alldays:
                    day += 1
                    if c and c != "X" and c != "-":
                        date = "%d/%d/%d" % ( day, month, yr)
                        code = str(c)
                        sql = "INSERT INTO absences SET id='%s', date='%s', code='%s'" % (id,date,code)
                        #rintsql
                        curmy.execute(sql)
                        #curmy.commit()
        except:
            ##rint' pass'
            pass
#cursor.execute("select * from Absensi")
#row = cursor.fetchone()
#if row:
#    #rintrow
    
    
import wx
import wx.grid as gridlib
 
class ScrollSync(object):
    def __init__(self, panel1, panel2):
        self.panel1 = panel1
        self.panel2 = panel2
        self.panel1.grid.Bind(wx.EVT_SCROLLWIN, self.onScrollWin1)
        self.panel2.grid.Bind(wx.EVT_SCROLLWIN, self.onScrollWin2)
 
    def onScrollWin1(self, event):
        if event.Orientation == wx.SB_HORIZONTAL:
            pass#self.panel2.grid.Scroll(event.Position, -1)
        else:
            self.panel2.grid.Scroll(-1, event.Position)
        event.Skip()
 
    def onScrollWin2(self, event):
        if event.Orientation == wx.SB_HORIZONTAL:
            pass
            #self.panel1.grid.Scroll(event.Position, -1)
        else:
            self.panel1.grid.Scroll(-1, event.Position)
        event.Skip()
 
########################################################################
class RegularPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("pink")
 
 
########################################################################
class GridPanelLeft(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.grid = gridlib.Grid(self, style=wx.BORDER_SUNKEN)
        self.grid.CreateGrid(25,2)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_DEFAULT)
        
        
class GridPanelRight(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.grid = gr = gridlib.Grid(self, style=wx.BORDER_SUNKEN)
        self.grid.CreateGrid(25,8)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.grid.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
        gr.SetRowLabelSize(0)
        gr.SetColMinimalAcceptableWidth(0)
        gr.SetColSize(0,0)
 
 
########################################################################
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
 
        notebook = wx.Notebook(self)
 
        page = wx.SplitterWindow(notebook)
        notebook.AddPage(page, "Splitter")
        hSplitter = wx.SplitterWindow(page)
 
        panelOne = GridPanelLeft(hSplitter)
        panelTwo = GridPanelRight(hSplitter)
        ScrollSync(panelOne, panelTwo)
 
        hSplitter.SplitVertically(panelOne, panelTwo)
        hSplitter.SetSashGravity(0.5)
 
        panelThree = RegularPanel(page)
        page.SplitHorizontally(hSplitter, panelThree)
        page.SetSashGravity(0.5)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Nested Splitters",
                          size=(800,600))
        panel = MainPanel(self)
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()