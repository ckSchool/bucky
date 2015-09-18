import  os
import  wx, papersize
import  wx.lib.printout as  printout
#import PrintFramework as printout
import print_spp



import win32print, win32api

buttonDefs = {814 : ('PrintSPP',      '#rintSPP')}
#import win32print
#printers = win32print.EnumPrinters(5)
##rintprinters

class MyPrintout(wx.Printout):
    def __init__(self, canvas):
        wx.Printout.__init__(self)
        self.canvas = canvas
        

    def OnBeginDocument(self, start, end):
        return super(MyPrintout, self).OnBeginDocument(start, end)

    def OnEndDocument(self):
        super(MyPrintout, self).OnEndDocument()

    def OnBeginPrinting(self):
        super(MyPrintout, self).OnBeginPrinting()

    def OnEndPrinting(self):
        super(MyPrintout, self).OnEndPrinting()

    def OnPreparePrinting(self):
        super(MyPrintout, self).OnPreparePrinting()

    def HasPage(self, page):
        if page <= 2: return True
        else:         return False

    def GetPageInfo(self):
        return (1, 2, 1, 2)

    def OnPrintPage(self, page):
        dc = self.GetDC()

        #-------------------------------------------
        # One possible method of setting scaling factors...

        maxX = self.canvas.getWidth()
        maxY = self.canvas.getHeight()

        # Let's have at least 50 device units margin
        marginX = 50
        marginY = 50

        # Add the margin to the graphic size
        maxX = maxX + (2 * marginX)
        maxY = maxY + (2 * marginY)

        # Get the size of the DC in pixels
        (w, h) = dc.GetSizeTuple()

        # Calculate a suitable scaling factor
        scaleX = float(w) / maxX
        scaleY = float(h) / maxY

        # Use x or y scaling factor, whichever fits on the DC
        actualScale = min(scaleX, scaleY)

        # Calculate the position on the DC for centering the graphic
        posX = (w - (self.canvas.getWidth() * actualScale)) / 2.0
        posY = (h - (self.canvas.getHeight() * actualScale)) / 2.0

        # Set the scale and origin
        dc.SetUserScale(actualScale, actualScale)
        dc.SetDeviceOrigin(int(posX), int(posY))

        #-------------------------------------------

        self.canvas.DrawInvoice(dc, True)
        dc.DrawText("Page: %d" % page, marginX/2, maxY-marginY)

        return True


class MyCanvas(wx.Panel):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.lines = []
        self.maxWidth  = 900
        self.maxHeight = 400
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False


        self.SetVirtualSize((self.maxWidth, self.maxHeight))
       
        # Initialize the buffer bitmap.  No real DC is needed at this point.
        self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawInvoice(dc)

        self.Bind(wx.EVT_PAINT,     self.OnPaint)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def DrawInvoice(self, dc, printing=False):
        dc.BeginDrawing()
        indent1 = 30
        indent2 = indent1 + 90
        indent3 = indent1 + 105
        
        line_1 = 180
        line_2 = line_1 + 20
        line_3 = line_2 + 20
        
        line_4 = line_3 + 40
        line_5 = line_4 + 20
        
        dc.SetFont(wx.Font(10, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        #te = dc.GetTextExtent("Hello World")
        
        dc.DrawText("--------------------------", indent1, line_1-18)
        
        dc.DrawText("Nama Siswa", indent1, line_1)
        dc.DrawText("No.Induk", indent1, line_2)
        dc.DrawText("Kelas   ", indent1, line_3)
        
        dc.DrawText(":", indent2, line_1)
        dc.DrawText(":", indent2, line_2)
        dc.DrawText(":", indent2, line_3)

        name, NoInduk, form = "Albert","A0451","XII a"
        dc.DrawText(name,    indent3, line_1)
        dc.DrawText(NoInduk, indent3, line_2)
        dc.DrawText(form,    indent3, line_3)
        
        dc.DrawText("--------------------------", indent1, line_3+8)
        
        dc.DrawText("N0 Kwintnsi", indent1, line_4)
        dc.DrawText("Tanggal", indent1, line_5)
        
        dc.DrawText(":", indent2, line_4)
        dc.DrawText(":", indent2, line_5)
        
        ck_ref, invoice_date = 'CK1516/99287', '27 Jul 2015'
        
        dc.DrawText(ck_ref,       indent3, line_4)
        dc.DrawText(invoice_date, indent3, line_5)
        
        indent_inv_itemsQ = 300
        indent_inv_itemsD = 350
        indent_inv_itemsU = 750
        indent_inv_itemsT = 850
        
        line_inv_itemsH = 20
        line_inv_itemsI = 30
        
        line_total    = line_4+20
        line_in_words = line_total + 20
        te_up = dc.GetTextExtent("Unit Price")
        te_tot= dc.GetTextExtent("Total")
                
        dc.DrawText("Qnty.",       indent_inv_itemsQ, line_inv_itemsH)
        dc.DrawText("Description", indent_inv_itemsD, line_inv_itemsH)
        dc.DrawText("Unit Price",  indent_inv_itemsU - te_up[0], line_inv_itemsH)
        dc.DrawText("Total",       indent_inv_itemsT - te_tot[0], line_inv_itemsH)
        dc.DrawText("-------------------------------------------------------------------", indent_inv_itemsQ, line_inv_itemsH+10)
        
        inv_items = [('5','Bulan, Bus: Aug,Sept,Oct,Nov,Des', '150,000', '750,000'),
                (('6','Bulan, SPP: Jly,Aug,Sept,Oct,Nov,Des', '1,250,000', '750,000'))]
        spacing = 20
        line = 1
        for i in inv_items:
                qnty, description, unit_price, total = i
                te_up = dc.GetTextExtent(unit_price)
                te_tot= dc.GetTextExtent(total)
                nl = line_inv_itemsI+line*spacing
                dc.DrawText(qnty,        indent_inv_itemsQ,           nl)
                dc.DrawText(description, indent_inv_itemsD,           nl)
                dc.DrawText(unit_price,  indent_inv_itemsU-te_up[0],  nl)
                dc.DrawText(total,       indent_inv_itemsT-te_tot[0], nl)
                line +=1
        underline = '---------------------'
        te_un =  dc.GetTextExtent(underline)[0]
        te_ju =  dc.GetTextExtent('Jumlah')[0]
        
        dc.DrawText(underline, indent_inv_itemsT - te_un,  line_total-10)
        dc.DrawText('Jumlah',  indent_inv_itemsT - te_un - te_ju - 20,  line_total)
        
        grand_total = '23,455,778'
        te_gt = dc.GetTextExtent(grand_total)[0]
        dc.DrawText(grand_total,  indent_inv_itemsT - te_gt,  line_total)
        
        dc.SetFont(wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        in_words = 'Dua puluh juta, empat ratus lima puluh lima ribu tujuh ratus tujuh puluh delapan rupiah'
        te_iw = dc.GetTextExtent(in_words)[0]
        dc.DrawText(in_words,  indent_inv_itemsT - te_iw ,  line_in_words)
        
        
        #dc.DrawLine(5, indent1+te[1], line_1+te[0], indent1+te[1])

        self.DrawSavedLines(dc)
        dc.EndDrawing()


    def DrawSavedLines(self, dc):
        dc.SetPen(wx.Pen('MEDIUM FOREST GREEN', 4))
        for line in self.lines:
            for coords in line:
                apply(dc.DrawLine, coords)
                
    
    def getWidth(self): # callback
        return self.maxWidth

    def getHeight(self):# callback
        return self.maxHeight


class TablePanel(wx.Panel):
    def __init__(self, parent, log, frame):
        wx.Panel.__init__(self, parent, -1)
        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_ENV_MONARCH)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        
        
        self.canvas = MyCanvas(self)
        

        self.SetMinSize((800,400))        
        
        btn_setup   = wx.Button(self, -1, "Page Setup")
        btn_preview = wx.Button(self, -1, "#rintPreview")
        btn_#rint  = wx.Button(self, -1, "Print")
        
        self.box = wx.BoxSizer(wx.VERTICAL)
        subbox   = wx.BoxSizer(wx.HORIZONTAL)
        
        subbox.Add(btn_setup,   1, wx.GROW | wx.ALL, 2)
        subbox.Add(btn_preview, 1, wx.GROW | wx.ALL, 2)
        subbox.Add(btn_print,   1, wx.GROW | wx.ALL, 2)
        
        self.box.Add(self.canvas, 1, wx.GROW)
        self.box.Add(subbox,      0, wx.GROW)
        
        self.Bind(wx.EVT_BUTTON, self.OnPageSetup, btn_setup)
        self.Bind(wx.EVT_BUTTON, self.OnPrintPreview, btn_preview)
        self.Bind(wx.EVT_BUTTON, self.OnDoPrint, btn_print)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        
        self.quickSetPage()
        
    def quickSetPage(self, ):
        psdd = self.getPsdd()     

        dlg = wx.PageSetupDialog(self, psdd)
        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData())
    
    def getPsdd(self, ):
        self.pdata = wx.PrintData()
        
        self.pdata.SetPaperId(wx.PAPER_NONE)
        self.pdata.SetBin(wx.PRINTBIN_TRACTOR)
        self.pdata.SetPaperSize((600,200))

        psdd = wx.PageSetupDialogData(self.printData)
        psdd.SetPrintData(self.pdata)
        
        psdd.EnablePrinter(True)
        psdd.CalculatePaperSizeFromId()
        
        """
        self.margins = (wx.Point(0,05), wx.Point(05,05))
        psdd.SetDefaultMinMargins(True)
        psdd.SetMarginTopLeft(self.margins[0])
        psdd.SetMarginBottomRight(self.margins[1])   """
        return psdd
    
    def OnPageSetup(self, evt):
        self.psdd = self.getPsdd()

        dlg = wx.PageSetupDialog(self, self.psdd)
        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData())
        
        dlg.ShowModal()
        
        
        # this makes a copy of the wx.PrintData instead of just saving
        # a reference to the one inside the PrintDialogData that will
        # be destroyed when the dialog is destroyed
        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )

        dlg.Destroy()
        
 


    def OnPrintPreview(self, event):
        #data      = wx.PrintDialogData(self.printData)
        printout  = MyPrintout(self.canvas)#, self.log)
        printout2 = MyPrintout(self.canvas)#, self.log)
        self.preview = wx.PrintPreview(printout, printout2, self.printData )#data)

        if not self.preview.Ok():
            #rint"Houston, we have a problem..."
            return

        pfrm = wx.PreviewFrame(self.preview, self.GetParent(), "This is a #rintpreview")

        pfrm.Initialize()
        pfrm.SetPosition(self.GetPosition())
        pfrm.SetSize(self.GetSize())
        pfrm.Center()
        pfrm.Show(True)



    def OnDoPrint(self, event):
        pdd = wx.PrintDialogData(self.printData)
        pdd.SetToPage(2)
        
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas)

        if not printer.Print(self.canvas, printout, True):
            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()
        
        
        
       
 
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.p = TablePanel(self, 1,1)
        self.SetMinSize((1000,500))
        self.Fit()
        self.Centre()
    
if __name__ == "__main__":
    app = wx.App(None)
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()