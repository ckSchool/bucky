import wx, gVar,  pyodbc

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
import fetchodbc as fetch
import wx.grid   as gridlib

#---------------------------------------------------------------------------

class panel_bookings(wx.Panel):
    def __init__(self, parent, pid):
        self.parent = parent
        wx.Panel.__init__(self, parent, pid)
        
        self.widgetSizer = sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        
    def set_grid_properties(self):
        grid = self.grid

        grid.CreateGrid(5, 15)#, gridlib.Grid.SelectRows)
        grid.EnableEditing(False)
        grid.EnableGridLines(False)
        grid.EnableDragRowSize(False)

        self.setAttr()
        
        grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK,   self.OnCellLeftClick)
        grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,  self.OnCellRightClick)
        grid.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,  self.OnCellLeftDClick)
        grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
        
        grid.EnableDragColSize(enable=False)
        grid.SetColLabelSize(0)
        grid.SetRowLabelSize(0)
        grid.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
        
    def setColumnLabels(self, columnlabels=[]):
        # set column headings & sizes
        grid = self.grid
        idx=0
        for label in columnlabels:
            grid.SetColLabelValue(idx, label[0])
            grid.SetColSize(idx,       label[1])
            idx += 1
            
    def displayData(self):
        self.number_of_grids = 0
        
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(0)
            self.widgetSizer.Remove(0)
            
        # create a new grid
        grid = self.grid = gridlib.Grid(self)
        self.set_grid_properties()
        self.widgetSizer.Add(grid, 1, wx.EXPAND, 0)
                       
        columnlabels = [("TYPE", 80),        ("ID", 30),
                       ("COURSE NAME", 200), ("NOW", 45),
                       ("OUT", 45),          ("CONT.", 55),
                       ("REDO", 45),         ("TOTAL",85),
                       ("NEW",45),           ("TOTAL",55),
                       ("CLASS SIZE",95),    ("CLASSES",75)]
        self.setColumnLabels(columnlabels)
        self.Layout()

        #grid.DeleteRows(1,r)
        #grid.AppendRows(150)

        sql ="SELECT courses FROM courses_by_year WHERE schYr = %s" % gVar.schYr
        #print sql
        course_ids = fetch.getList(sql)

        sql ="SELECT course_level FROM courses_levels ORDER BY course_level"
        course_levels = fetch.getList(sql)

        row = 0
        for level in range(1,20):
            self.formatRow(row)
  
            if level ==1:
                row = self.displayDataForLowerLevelNextYearsCourses(level, row)

            row = self.dispalyDataForLastYearsKelases (level, row)
            row = self.dispalyDataForNextYearsCourses(level, row)
            
    def formatRow(self, row):
        grid = self.grid
        grid.SetRowMinimalHeight(row, 5)
        grid.SetRowSize(row, 5)
            
    def dispalyDataForNextYearsCourses(self, level, row):
        # courses for the new year
        grid = self.grid
        
        new_year_courses = self.getCourseIDSForNewYear(level+1)
        if new_year_courses:
            self.labelRowNew(row);
            grid.AppendRows(1); row += 1
            #print row, 'B rows=', grid.GetNumberRows()    
            for course in new_year_courses:
                courseid = str(course['id'])
                course_name = course['course_name']
                grid.SetCellValue(row, 0, 'course')
                grid.SetCellValue(row, 1, courseid)
                grid.SetCellValue(row, 2, course_name)
                grid.SetCellAlignment(row, 2, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);  
                grid.SetRowAttr(row, self.attrDetailsNew)
                
                grid.AppendRows(1); row += 1
                print row, 'C rows=', grid.GetNumberRows()
        return row
    
    
    def dispalyDataForLastYearsKelases (self, level, row):
        # last years classes
        grid = self.grid
        sql ="SELECT Kode, Nama, Sekolah FROM Kelas WHERE course_level=%d AND TahunAjaran =%d" % (level, gVar.schYr-1)
        classes = fetch.getAllDict(sql)
        
        if classes:
            self.labelRowKelas(row)
            
            grid.AppendRows(1); row += 1
            print row, 'D rows=', grid.GetNumberRows()        
            tot_now, tot_out, tot_cont, tot_retake, sub_tot, tot_tot = (0, 0, 0, 0, 0, 0) 
            for myClass in classes:
                KKode   = myClass['Kode']
                class_name = myClass['Nama']
                
                now  = fetch.batchPopulation(KKode) #GetClassPopulation
                tot_now    +=now
                cont = fetch.numberOfStudents_reregistering(KKode)
                tot_cont   +=cont
                out  = fetch.numberOfStudents_leaving(KKode)
                tot_out    += out
                retake = fetch.numberOfStudents_retaking(KKode)
                
                tot_retake += retake
                sub_tot = cont + retake
                tot_tot += sub_tot
                
                grid.SetRowAttr(row, self.attrDetailsKelas)
                grid.SetCellValue( row, 0, "Kelas")
                grid.SetCellValue( row, 1, str(KKode))
                grid.SetCellValue( row, 2, class_name)
                grid.SetCellValue( row, 3, str(now))
                grid.SetCellValue( row, 4, str(out))
                grid.SetCellValue( row, 5, str(cont))
                grid.SetCellValue( row, 6, str(retake))
                grid.SetCellValue( row, 7, str(sub_tot))
                
                grid.AppendRows(1); row += 1
                print row, 'E rows=', grid.GetNumberRows()
            
            # display totals
            grid.SetRowAttr(row, self.attrTotalsKelas)
            grid.SetCellValue( row, 0, "totals")
            grid.SetCellValue( row, 3, str(tot_now))
            grid.SetCellValue( row, 4, str(tot_out))
            grid.SetCellValue( row, 5, str(tot_cont))
            grid.SetCellValue( row, 6, str(tot_retake))
            grid.SetCellValue( row, 7, str(tot_tot))
            
            grid.AppendRows(1); row += 1
            print row, 'F rows=', grid.GetNumberRows()
        return row
    
    def displayDataForLowerLevelNextYearsCourses(self, level, row):
        # special for any courses lower than the first Kelas
        # now to check for courses for the new year
        return self.dispalyDataForNextYearsCourses(level, row)
        
        
    def getCourseIDSForNewYear(self, level):
        sql ="SELECT courses.id, courses.course_name \
                FROM courses \
          INNER JOIN courses_by_year ON (int(courses.id) = int(courses_by_year.course_id)) \
               WHERE courses_by_year.schYr=%d \
                 AND courses.course_level=%d" % (gVar.schYr, int(level))
        res = fetch.getAllDict(sql)
        
        #print  sql, res

        return res
    
    def labelRowKelas(self, row):
        print 'labelRowKelas'
        grid = self.grid
        idx=2
        yr = gVar.schYr-1
        txt = "CLASS %d" % yr
        tempheading = (txt,"NOW","OUT", "CONT.","REDO","TOTAL")
        for h in tempheading:
            grid.SetCellValue(row,idx, h)
            idx += 1
        grid.SetRowAttr(row, self.attrHeadingsKelas)
    
    def labelRowNew(self, row):
        txt ="COURSE %d" % gVar.schYr
        grid = self.grid
        #print txt
        grid.SetCellValue(row,2, txt )
        grid.SetCellAlignment(row, 2, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);
        idx=7
        tempheading = ("CONT.","NEW","TOTAL","CLASS SIZE","CLASSES")
        for h in tempheading:
            grid.SetCellValue(row,idx, h)
            idx += 1
        grid.SetRowAttr(row, self.attrHeadingsNew)
        
        
        
    def setAttr(self):
        # attribute objects let you keep a set of formatting values
        # in one spot, and reuse them if needed

        self.attrHeadingsNew = attrHeadingsNew = gridlib.GridCellAttr()
        attrHeadingsNew.SetTextColour(wx.BLACK)
        attrHeadingsNew.SetBackgroundColour((230,230,120))
        attrHeadingsNew.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.attrDetailsNew = attrDetailsNew = gridlib.GridCellAttr()
        attrDetailsNew.SetTextColour(wx.BLACK)
        attrDetailsNew.SetBackgroundColour((240,230,190))
        attrDetailsNew.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.attrTotalsNew = attrTotalsNew = gridlib.GridCellAttr()
        attrTotalsNew.SetTextColour(wx.BLACK)
        attrTotalsNew.SetBackgroundColour((240,220,120))
        attrTotalsNew.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.attrHeadingsKelas = attrHeadingsKelas = gridlib.GridCellAttr()
        attrHeadingsKelas.SetTextColour(wx.BLACK)
        attrHeadingsKelas.SetBackgroundColour((200,240,230))
        attrHeadingsKelas.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
        
        self.attrDetailsKelas = attrDetailsKelas = gridlib.GridCellAttr()
        attrDetailsKelas.SetTextColour(wx.BLACK)
        attrDetailsKelas.SetBackgroundColour((230,240,240))
        attrDetailsKelas.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
        
        self.attrTotalsKelas = attrTotalsKelas = gridlib.GridCellAttr()
        attrTotalsKelas.SetTextColour(wx.BLACK)
        attrTotalsKelas.SetBackgroundColour((200,230,240))
        attrTotalsKelas.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))    


    # grid events ---------------------------------------------------

    def OnCellLeftClick(self, evt):
        txt = "OnCellLeftClick: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition())
        print txt
        r,c = evt.GetRow(), evt.GetCol()
        val1 = self.grid.GetCellValue(r,0)
        val2 = self.grid.GetCellValue(r,1)
        print val1, val2
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        r,c = evt.GetRow(), evt.GetCol()
        val1 = self.grid.GetCellValue(r,0)
        val2 = self.grid.GetCellValue(r,1)
        
        if val1 =="Kelas":
            gVar.KKelas = val2
            print 'gVar.KKelas ', gVar.KKelas, 'openPanel:rereg_list'

            gVar.previousPanel = gVar.lastPanel
            gVar.lastPanel = self
            self.GetTopLevelParent().openPanel('rereg_list','panel_reportGrid')
            
            
        elif val1=="course":
            print 'open course bookings -'
            self.GetTopLevelParent().openPanel('course_bookings','bookings_report')
            
        evt.Skip()
        
    def OnCellRightClick(self, evt):
        evt.Skip()

    def OnCellRightDClick(self, evt):
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        evt.Skip()

    def OnLabelRightClick(self, evt):
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        evt.Skip()


    def OnIdle(self, evt):
        pass


    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'

        # Another way to stay in a cell that has a bad value...
        row = self.grid.GetGridCursorRow()
        col = self.grid.GetGridCursorCol()

        if self.grid.IsCellEditControlEnabled():
            self.grid.HideCellEditControl()
            self.grid.DisableCellEditControl()

        value = self.grid.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection

        evt.Skip()
