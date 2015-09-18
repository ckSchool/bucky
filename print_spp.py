import wx, time, calendar, datetime
import wx.grid as gridlib
import wx.lib.printout as  printout
import wx.lib.mixins.listctrl as listmix
import cPickle
import pyodbc

import win32print
printers = win32print.EnumPrinters(5)
#rint'printers', printers

invoice_date = {1:['NIS: 0123 ______ KELAS: VII A','No. Kwitansi: CK1516/666666'],
                2:['Nama: Akbar Muhammad Amil Siregar ','Tanggal: 1 Januari 2015'],
                        3:['',''],
                        4:['SPP bulan Juli','1475000']        ,
                        5: ['BUS bulan Juli','500000']
                                }

"""
def PrintSPP():
        data = []
        #for i in len(invoice_date):
        #        data.append(invoice_date[i]
        
        data.append(['NIS: 0123 ______ KELAS: VII A','No. Kwitansi: CK1516/666666'])
        data.append(['Nama: Akbar Muhammad Amil Siregar ','Tanggal: 1 Januari 2015'])
        data.append(['',''])
        data.append(['SPP bulan Juli','1475000'])
        data.append(['BUS bulan Juli','500000'])
        
        
        #rintdata
        
        new_data = []
        for val in data:
            new_data.append( [
                              str(val[0]),
                              str(val[1])
                              ])
        #rintnew_data
        
        #prt = printout.PrintTable(self.frame)
        prt = printout.PrintTable()
        #prt.SetHeader(text = txt, type = "text", align=wx.ALIGN_LEFT, indent = 0.5, colour = wx.NamedColour('BLUE'))
        #prt.SetHeader(text = "xxxxxxxxxxxxxxxx", type = "text", align=wx.ALIGN_LEFT, indent = 0.5, colour = wx.NamedColour('BLUE'))
        
        #prt.SetHeader("Name: \nX Late \nX No In \nX No Out \nX No Data At All", type = "Date & Time", align=wx.ALIGN_LEFT, indent = 0.5, colour = wx.NamedColour('BLUE'))
        
        # add Staff Details 
           
        prt.left_margin = 2.4
        prt.right_margin = 0.1    # only used if no column sizes
        
        prt.top_margin  = 0.1
        prt.bottom_margin = 0.4
        prt.cell_left_margin = 0.1
        prt.cell_right_margin = 0.1
        
        
        # table
        for r in range (0,3):
            prt.SetRowLineColour(r,"BLACK")
            prt.SetColumnLineColour(r,"BLACK")
        #new_header = ['Date', 'Day', 'In', 'Out', ' ', 'Late']
        #new_data.insert(0,['Date', 'Day', 'In', 'Out', ' ', 'Late'])
        #prt.label = new_header
        #prt.label_colour="WHITE"
        #prt.SetLabelSpacing(4,4)
        #prt.SetCellText(0,5,"RED")
        #prt.SetCellColour(0,5,"GREY")
        #self.label_font = { "Name": self.default_font_name, "Size": 12, "Colour": [0, 0, 0], "Attr": [0, 0, 0] }
        prt.text_font = { "Name": "ARIAL", "Size": 12, "Colour": [0, 0, 0], "Attr": [0, 0, 0] }
        #prt.SetRowLineSize(1,2)
        prt.SetRowSpacing(4,4)
        prt.data = data #new_data
        prt.set_column = [ 2.7, 2]
        
        prt.SetColAlignment(1, wx.ALIGN_RIGHT)
        #prt.SetColBackgroundColour(0, wx.NamedColour('RED'))
        #prt.SetColTextColour(0, wx.NamedColour('BLACK'))
        #prt.SetCellColour(4, 0, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellColour(4, 1, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellColour(17, 1, wx.NamedColour('LIGHT BLUE'))
        #prt.SetColBackgroundColour(2, wx.NamedColour('LIGHT BLUE'))
        #prt.SetCellText(4, 2, wx.NamedColour('RED'))
        #prt.SetColTextColour(3, wx.NamedColour('RED'))
        
        prt.label_font_colour = wx.NamedColour('BLACK')
        footer = 'Satu juta empat ratus tujuh puluh lima ribu rupiah'
        footer1 = 'Terbilang: ' + footer
        prt.SetFooter(text=footer1, type = 'text', size=14)
        # layout complete
        #prt.page_width = 7.1
        #prt.page_height = 3.6
        #prt.SetPageSize(7,3)
        #prt.SetPaperId(wx.PAPER_LETTER)
        #prt.SetPaperId(wx.PAPER_ENV_MONARCH)
        prt.SetPortrait()
        #prt.pwidth = 7
        #prt.pheight = 3
        
        #psdd = wx.PageSetupDialogData(printData)
        #psdd.CalculatePaperSizeFromId()
       
        #def OnPrintPreview(self, event):
        '''
        psdd = wx.PageSetupDialogData(prt.printData)
        psdd.CalculatePaperSizeFromId()
        dlg = wx.PageSetupDialog(self,psdd)
        dlg.ShowModal()
        prt.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )
        dlg.Destroy()
        '''
        
        #prt.OnPageSetup()
        prt.Preview()
"""        
        
#  PrintFramework
import  wx
import  wx.lib.scrolledpanel as  ScrolledWindow

#----------------------------------------------------------------------


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

    def OnPrintPage(self):
        pdd = wx.PrintDialogData(self.printData)
        pdd.SetToPage(2)
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas, self.log)

        if not printer.Print(self.frame, printout, True):
            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()


#----------------------------------------------------------------------
import  images

# There are two different approaches to drawing, buffered or direct.
# This sample shows both approaches so you can easily compare and
# contrast the two by changing this value.
BUFFERED = 1

#---------------------------------------------------------------------------

class MyCanvas(wx.Panel):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.lines = []
        self.maxWidth  = 900
        self.maxHeight = 400
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False

        #self.SetBackgroundColour("WHITE")
        #self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        """
        bmp = images.Test2.GetBitmap()
        mask = wx.Mask(bmp, wx.BLUE)
        bmp.SetMask(mask)
        self.bmp = bmp
        """

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        #self.SetScrollRate(20,20)

        if BUFFERED:
            # Initialize the buffer bitmap.  No real DC is needed at this point.
            self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DrawInvoice(dc)

        #self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        #self.Bind(wx.EVT_LEFT_UP,   self.OnLeftButtonEvent)
        #self.Bind(wx.EVT_MOTION,    self.OnLeftButtonEvent)
        self.Bind(wx.EVT_PAINT,     self.OnPaint)


    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight


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



    

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_LETTER)
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.canvas = MyCanvas(self)
        self.box.Add(self.canvas, 1, wx.GROW)

        self.SetMinSize((900,400))        
        
        subbox = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, -1, "Page Setup")
        self.Bind(wx.EVT_BUTTON, self.OnPageSetup, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "#rintPreview")
        self.Bind(wx.EVT_BUTTON, self.OnPrintPreview, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        btn = wx.Button(self, -1, "Print")
        self.Bind(wx.EVT_BUTTON, self.OnDoPrint, btn)
        subbox.Add(btn, 1, wx.GROW | wx.ALL, 2)

        self.box.Add(subbox, 0, wx.GROW)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.Layout()
        self.Fit()


    def OnPageSetup(self, evt):
        self.pdata = wx.PrintData()
        
        
        self.pdata.SetPaperId(wx.PAPER_NONE)
        self.pdata.SetBin(wx.PRINTBIN_TRACTOR)
        self.pdata.SetPaperSize((800,200))
        #self.pdata.SetOrientation(wx.LANDSCAPE)


        psdd = wx.PageSetupDialogData(self.printData)
        psdd.SetPrintData(self.pdata)
        
        psdd.EnablePrinter(True)
        psdd.CalculatePaperSizeFromId()
        
        self.margins = (wx.Point(15,15), wx.Point(15,15))
        psdd.SetDefaultMinMargins(True)
        psdd.SetMarginTopLeft(self.margins[0])
        psdd.SetMarginBottomRight(self.margins[1])        
        #dlg = wx.PageSetupDialog(self, psdd) 

        #self.printerPageData.SetMarginBottomRight((25,25))
        #self.printerPageData.SetMarginTopLeft((25,25))
        #self.printerPageData.SetPrintData(psdd)
        
        #dlg = wx.PageSetupDialog(self, psdd)
        #dlg.ShowModal()

        # this makes a copy of the wx.PrintData instead of just saving
        # a reference to the one inside the PrintDialogData that will
        # be destroyed when the dialog is destroyed
        self.printData = wx.PrintData( dlg.GetPageSetupData().GetPrintData() )
        #rint'self.printData',self.printData
        dlg.Destroy()
        
 


    def OnPrintPreview(self, event):
        data      = wx.PrintDialogData(self.printData)
        printout  = MyPrintout(self.canvas)#, self.log)
        printout2 = MyPrintout(self.canvas)#, self.log)
        self.preview = wx.PrintPreview(printout, printout2, data)

        if not self.preview.Ok():
            #self.log.WriteText("Houston, we have a problem...\n")
            return

        pfrm = wx.PreviewFrame(self.preview, self, "This is a #rintpreview")

        pfrm.Initialize()
        pfrm.SetPosition(self.GetPosition())
        pfrm.SetSize(self.GetSize())
        pfrm.Show(True)



    def OnDoPrint(self, event):
        pdd = wx.PrintDialogData(self.printData)
        pdd.SetToPage(2)
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas, self.log)

        if not printer.Print(self.frame, printout, True):
            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()


if __name__ == "__main__":
    app = wx.App(None)
    frame_1 = MyFrame(None, -1)
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop() 


#----------------------------------------------------------------------





overview = """\
<html>
<body>
<h1>PrintFramework</h1>

This is an overview of the classes and methods used to #rintdocuments.
It also demonstrates how to do #rintpreviews and invoke the printer
setup dialog.

<p>Classes demonstrated here:<P>
<ul>
    <li><b>wx.Printout()</b> - This class encapsulates the functionality of printing out 
        an application document. A new class must be derived and members overridden 
        to respond to calls such as OnPrintPage and HasPage. Instances of this class 
        are passed to wx.Printer.Print() or a wx.PrintPreview object to initiate 
        printing or previewing.<P><p>
        
    <li><b>wx.PrintData()</b> - This class holds a variety of information related to 
        printers and printer device contexts. This class is used to create a 
        wx.PrinterDC and a wx.PostScriptDC. It is also used as a data member of 
        wx.PrintDialogData and wx.PageSetupDialogData, as part of the mechanism for 
        transferring data between the #rintdialogs and the application.<p><p>

    <li><b>wx.PrintDialog()</b> - This class represents the #rintand #rintsetup 
        common dialogs. You may obtain a wx.PrinterDC device context from a 
        successfully dismissed #rintdialog.<p><p>
        
    <li><b>wx.PrintPreview()</b> - Objects of this class manage the #rintpreview 
        process. The object is passed a wx.Printout object, and the wx.PrintPreview 
        object itself is passed to a wx.PreviewFrame object. Previewing is started by 
        initializing and showing the preview frame. Unlike wxPrinter.Print, flow of 
        control returns to the application immediately after the frame is shown.<p><p>
</ul>

<p>Other classes are also demonstrated, but this is the gist of the printer interface
framework in wxPython.

</body>
</html>

"""


        