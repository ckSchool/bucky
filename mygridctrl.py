import wx, fetch

import wx.grid as  gridlib

fixedColCount = 0

def clearGrid(grid):
    grid.ClearGrid()

    rows = grid.NumberRows
    if rows: grid.DeleteRows(0,rows)
    rows = grid.NumberRows

    clearColsBeyond(grid, 2)
    grid.Refresh()

def resizeGrid(grid, r, c):
    clearGrid(grid)
    grid.AppendRows(r)
    grid.AppendCols(c)
    grid.Refresh()

def makeColumnsForData(grid, count):
    clearColsBeyond(grid, 3)

    attr = gridlib.GridCellAttr()
    attr.SetAlignment(wx.ALIGN_CENTER, 0)

    for i in range(count):
        grid.AppendCols()
        grid.SetColAttr(2+i, attr)

    grid.Refresh()

def clearColsBeyond(grid, col_number):
    cols = grid.NumberCols
    if cols > col_number:
        try:   grid.DeleteCols(col_number, (cols - col_number))
        except:pass
        grid.Refresh()

def makeRowsForStudents(grid, studentCount):
    clearRowsBeyond(grid, 0)
    grid.AppendRows(studentCount)
    grid.SetRowSize(0, 20)
    grid.Refresh()

def clearRowsBeyond(grid, row_number):
    rows = grid.NumberRows
    if rows > row_number:
        grid.DeleteRows(row_number, (rows - row_number))
        grid.Refresh()

def changeGridSize(grid, rows_to_append, cols_to_append):
    clearRowsBeyond(grid, 0)
    clearColsBeyond(grid, 2)
    grid.AppendRows(rows_to_append)
    grid.AppendCols(cols_to_append)

def createGrid_forComments(grid):
    grid.CreateGrid(24, 5)
    grid.SetRowMinimalAcceptableHeight(15)

    grid.Refresh()
    attr = gridlib.GridCellAttr()
    attr.SetAlignment(wx.ALIGN_LEFT, 0)
    attr.SetBackgroundColour(wx.WHITE)
    attr.SetReadOnly(True)

    grid.SetColLabelSize(19)

    c = 0
    '''
    grid.SetColSize(c, 0)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,'student_id') ## hidden
    c += 1
    '''
    grid.SetColSize(c, 50)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,"ID")

    c += 1
    grid.SetColSize(c, 220)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,"Name")

    c += 1
    grid.SetColSize(c, 600)
    grid.SetColLabelValue(c,"Comments")

    # change attributes for "Affectives" column
    attr = gridlib.GridCellAttr()
    attr.SetAlignment(wx.ALIGN_CENTER, 0)
    c += 1
    grid.SetColAttr(c, attr)
    grid.SetColSize(c, 40)
    grid.SetColLabelValue(c, "Affective")

    # change attributes for "Average" column
    attr = gridlib.GridCellAttr()
    attr.SetAlignment(wx.ALIGN_CENTER, 0)
    attr.SetReadOnly(True)
    c += 1
    grid.SetColAttr(c, attr)
    grid.SetColSize(c, 40)
    grid.SetColLabelValue(c, "Ave")

    grid.SetRowLabelSize(20)

def createGrid_forGrades(grid):
    grid.CreateGrid(0, 3)

    attr = gridlib.GridCellAttr()
    attr.SetAlignment(wx.ALIGN_LEFT, 0)
    attr.SetBackgroundColour(wx.WHITE)
    attr.SetReadOnly(True)

    grid.SetColLabelSize(19)
    c = 0
    '''
    grid.SetColSize(c, 0)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,'student_id') ## hidden
    c += 1
    '''
    grid.SetColSize(c, 50)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,"ID")
    c += 1
    grid.SetColSize(c, 220)
    grid.SetColAttr(c, attr)
    grid.SetColLabelValue(c,"Name")

    grid.SetRowLabelSize(20)


def listStudents(grid, studentIDs, rowHeight):
    clearRowsBeyond(grid, 0)
    r = 0
    for student_id in studentIDs:
        name = fetch.studentFullName(student_id)
  
        ckid = fetch.ckid(student_id)
        
        grid.AppendRows()
        grid.SetRowSize(r, rowHeight)
        grid.SetCellValue(r, 0, ckid)
        grid.SetCellValue(r, 1, name)
        r += 1
    
def keyHandler(grid, event, gridtype):
    keycode = event.GetKeyCode()
    '''
    Handler for the wx.grid's cell editor widget's keystrokes. Checks for specific
    keystrokes, such as arrow up or arrow down, and responds accordingly. Allows
    all other key strokes to pass through the handler.
    '''
    if   keycode == wx.WXK_UP:    grid.MoveCursorUp(False)
    elif keycode == wx.WXK_DOWN:  grid.MoveCursorDown(False)
    elif keycode == wx.WXK_LEFT:  grid.MoveCursorLeft(False)
    elif keycode == wx.WXK_RIGHT: grid.MoveCursorRight(False)
        
    # If Ctrl+C is pressed...
    if event.ControlDown() and event.GetKeyCode() == 67:
        selection(grid)
        # Call copy method
        copy(grid)

    cursorCol=grid.GetGridCursorCol()
    if gridtype == 'grades':
        # don't allow any editing of first three columns or last
        if cursorCol > 2 and cursorCol < (grid.NumberCols):
            # If Supr is presed
            if event.GetKeyCode() == 127:
                # Call delete method
                delete()
            # If Ctrl+V is pressed...
            if event.ControlDown() and event.GetKeyCode() == 86:
                currentcell(grid)
                # Call paste method
                paste(grid, 'grades')  
        
    if gridtype == 'standards': 
        # don't allow any editing of first three columns
        if cursorCol > 2:
            # If Supr is presed
            if event.GetKeyCode() == 127:
                # Call delete method
                delete()
            # If Ctrl+V is pressed...
            if event.ControlDown() and event.GetKeyCode() == 86:
                currentcell(grid)
                # Call paste method
                paste(grid, 'standards')  
                        
    if gridtype == 'comments': 
        # don't allow any editing of first three or last columns
        if cursorCol > 2 and cursorCol < (grid.NumberCols-1):
            # If Supr is presed
            if event.GetKeyCode() == 127:
                # Call delete method
                delete()
            
            # If Ctrl+V is pressed...
            if event.ControlDown() and event.GetKeyCode() == 86:
                # Call paste method
                if  cursorCol == 2: # any string  
                    currentcell(grid) 
                    paste(grid, 'strings') 
                    
                else:               # Affective codes only 'A' 'B'...'E'
                    paste(grid, 'standards')

    # Skip other Key events
    if event.GetKeyCode():
        event.Skip()
        
            

def currentcell(grid):
    # Show cursor position
    row = grid.GetGridCursorRow()
    col = grid.GetGridCursorCol()
    cell = (row, col)
    ##rint "Current cell " + str(cell)

def selection(grid):
    # Show cell selection
    
    # If selection is cell...
    if grid.GetSelectedCells():pass
        #rint "Selected cells " + str(grid.GetSelectedCells())
    
    # If selection is block...
    if grid.GetSelectionBlockTopLeft():pass
        #rint "Selection block top left " + str(grid.GetSelectionBlockTopLeft())
    if grid.GetSelectionBlockBottomRight():pass
        #rint "Selection block bottom right " + str(grid.GetSelectionBlockBottomRight())

    # If selection is col...
    if grid.GetSelectedCols():pass
        #rint "Selected cols " + str(grid.GetSelectedCols())

    # If selection is row...
    if grid.GetSelectedRows():pass
        #rint "Selected rows " + str(grid.GetSelectedRows())

def copy(grid):
    #rint "Copy method"
    
    # Number of rows and cols
    gsBR = grid.GetSelectionBlockBottomRight()
    gsTL = grid.GetSelectionBlockTopLeft()
    ##rint gsBR ,':',gsTL
    
    rows = gsBR[0][0] - gsTL[0][0] + 1
    cols = gsBR[0][1] - gsTL[0][1] + 1

    if not rows or not cols:  return
    
    # data variable contain text that must be set in the clipboard
    data = ''

    # For each cell in selected range append the cell value in the data variable
    # Tabs '\t' for cols and '\r' for rows
    for r in range(rows):
        for c in range(cols):
            data = data + str(grid.GetCellValue(gsTL[0][0] + r, gsTL[0][1] + c))
            if c < cols - 1:
                data = data + '\t'
        data = data + '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

def paste(grid, pasteType):
    clipboard = wx.TextDataObject()
    if wx.TheClipboard.Open():
        wx.TheClipboard.GetData(clipboard)
        wx.TheClipboard.Close()
    else:
        wx.MessageBox("Can't open the clipboard", "Error")
    data = clipboard.GetText()
    table = []
    y = -1
    rowN = grid.GetGridCursorRow()
    colN = grid.GetGridCursorCol()
    
    ##rint  ' r   c ' , rowN, colN
    # Convert text in a array of lines
    for r in data.splitlines():
        y = y +1
        x = -1
        # Convert c in a array of text separated by tab
        for item in r.split('\t'):
            x = x +1
            rowNo = rowN + y
            colNo = colN + x
            ##rint 'rowNo=', rowNo , '   colNo=', colNo
            if pasteType=='grades' and item.isdigit():
                grid.SetCellValue(rowNo, colNo, str(item))
                
            elif pasteType=='standards' and item in 'ABCDE':
                grid.SetCellValue(rowNo, colNo, str(item))
                
            elif pasteType=='strings':
                grid.SetCellValue(rowNo, colNo, str(item))

def delete(grid):
    ##rint "Delete method"
    gsBR = grid.GetSelectionBlockBottomRight()
    gsTL = grid.GetSelectionBlockTopLeft()
    
    # Number of rows and cols
    rows = gsBR[0][0] - gsTL[0][0] + 1
    cols = gsBR[0][1] - gsTL[0][1] + 1
    
    # Clear cells contents
    for r in range(rows):
        for c in range(cols):
            grid.SetCellValue(gsTL[0][0] + r, gsTL[0][1] + c, '')
