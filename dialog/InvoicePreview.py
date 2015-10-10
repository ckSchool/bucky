import wx, os, papersize
import wx.lib.printout as  printout

import data.fetch   as fetch
import data.gVar    as gVar

NUMBER_IN_WORDS = ''

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
        #rint'MyCanvas OnPrintPage'
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

        #self.canvas.DrawInvoice(dc, True)
        dc.DrawText("Page: %d" % page, marginX/2, maxY-marginY)

        return True
    
    
    
ByTen1 = {1:'ten', 2:'twenty',3:'thirty',4:'fourty',5:'fifty',6:'sixty',7:'seventy',8:'eighty',9:'ninty'}
ByTen = {1:'sepuluh', 2:'dua puluh',3:'tiga puluh',4:'empat puluh',5:'lima puluh',6:'enam puluh',7:'tujuh puluh',8:'delapan puluh',9:'sembilan puluh'}

ByOne1 = {1:'one', 2:'two', 3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',0:'zero'}
ByOne = {1:'satu', 2:'dua', 3:'tiga',4:'empat',5:'lima',6:'enam',7:'tujuh',8:'delapan',9:'sembilan',0:''}

class conv_number_to_words(int):
    
    def __init__(self, n):
        global NUMBER_IN_WORDS
        #rint'n', n
        n = int(n)
        #n = 95505896639631893 # int(raw_input("Please enter an integer:\n>> "))
        #expected='ninety-five quadrillion, five hundred and five trillion, eight hundred and ninety-six billion, six hundred and thirty-nine million, six hundred and thirty-one thousand, eight hundred and ninety-three'
        NUMBER_IN_WORDS = self.get_number_as_words(n).capitalize()
        #rint'get_number_as_words;', n,'    got;', NUMBER_IN_WORDS
        
    def subThousand(self, n):
        assert(isinstance(n,(int, long)))
        assert(0 <= n <= 999)
        if n <= 19:
            return ByOne[n]
        
        elif n <= 99:
            q, r = divmod(n, 10)
            return ByTen[q] + (" " + self.subThousand(r) if r else "")
        
        else:
            q, r = divmod(n, 100)
            if q==1: return "seratus" + (" " + self.subThousand(r) if r else "")
            return ByOne[q] + " ratus" + (" " + self.subThousand(r) if r else "")
            #return ByOne[q] + " hundred" + (" " + self.subThousand(r) if r else "")

    
    def thousandUp(self, n):
        assert(isinstance(n,(int, long)))
        assert(0 <= n)
        
        #zGroup = {1:'thousand',2:'million',3:'billion',4:'trillion',5:'quadrillion',6:'f',7:'g',8:'h',9:'i',10:'h'}
        zGroup = {1:'ribu',2:'juta',3:'miliar',4:'triliar',5:'quadrillion',6:'f',7:'g',8:'h',9:'i',10:'h'}
        return ", ".join(reversed([self.subThousand(z) + (" " + zGroup[i] if i else "") if z else "" for i,z in enumerate(self.splitByThousands(n))]))
    
    def splitByThousands(self, n):
        assert(isinstance(n,(int, long)))
        assert(0 <= n)    
        res = []
        while n:
            n, r = divmod(n, 1000)
            res.append(r)
        return res
    
    def get_number_as_words(self, n):
      assert(isinstance(n,(int, long)))
      if n==0:
        return "Zero"
      return ("Minus " if n < 0 else "") + self.thousandUp(abs(n))



class MyCanvas(wx.Panel):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, (0, 0), size=size)
        
        self.maxWidth  = 860
        self.maxHeight = 400
        
        self.SetMinSize((self.maxWidth, self.maxHeight))
        
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
       
        # Initialize the buffer bitmap.  No real DC is needed at this point.
        self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
        self.dc = wx.BufferedDC(None, self.buffer)
        self.dc.SetBackground(wx.Brush(wx.WHITE))
        
        self.dc.Clear()
        #self.DrawInvoice(self.dc)

        self.Bind(wx.EVT_PAINT,     self.OnPaint)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    def DrawInvoice(self, data, printing=False):
        inv_details, item_list = data 
        dc = self.dc
        
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

        dc.DrawText("--------------------------", indent1, line_1-18)
        
        dc.DrawText("Nama Siswa", indent1, line_1)
        dc.DrawText("No.Induk",   indent1, line_2)
        dc.DrawText("Kelas   ",   indent1, line_3)
        
        dc.DrawText(":", indent2, line_1)
        dc.DrawText(":", indent2, line_2)
        dc.DrawText(":", indent2, line_3)

        name           =  inv_details['name']
        NoInduk        =  inv_details['NoInduk'] 
        form           =  inv_details['form_name']
        ck_ref         =  inv_details['ck_ref']
        invoice_date   =  inv_details['date']
        invoice_amount =  inv_details['amount']
    
        #invoice_items = item_list
        """
        name, NoInduk, form, ck_ref, invoice_date, invoice_amount, invoice_items = ("Albert",
                                                                                    "A0451",
                                                                                    "XII a",
                                                                                    "CK1516/99287",
                                                                                    "27 Jul 2015",
                                                                                    23155778,
                                                                                    inv_items)"""
        dc.DrawText(name,    indent3, line_1) 
        dc.DrawText(NoInduk, indent3, line_2)
        dc.DrawText(form,    indent3, line_3)
        
        dc.DrawText("--------------------------", indent1, line_3+8)
        
        dc.DrawText("N0 Kwintnsi", indent1, line_4)
        dc.DrawText("Tanggal", indent1, line_5)
        
        dc.DrawText(":", indent2, line_4)
        dc.DrawText(":", indent2, line_5)
        
        dc.DrawText(ck_ref,       indent3, line_4)
        dc.DrawText(str(invoice_date), indent3, line_5)
        
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
        
        spacing = 20
        line = 1
        for i in item_list:
            qnty, description, unit_price, total = i['qnty'], i['item_name'], i['price'], i['total_amount']
            
            qnty_s       = self.format_number(qnty)
            unit_price_s = self.format_number(unit_price)
            total_s      = self.format_number(total)
            
            te_up = dc.GetTextExtent(unit_price_s)
            te_tot= dc.GetTextExtent(total_s)
            nl = line_inv_itemsI+line*spacing
            dc.DrawText(qnty_s,        indent_inv_itemsQ,           nl)
            dc.DrawText(description,   indent_inv_itemsD,           nl)
            dc.DrawText(unit_price_s,  indent_inv_itemsU-te_up[0],  nl)
            dc.DrawText(total_s,       indent_inv_itemsT-te_tot[0], nl)
            line +=1
        underline = '---------------------'
        te_un =  dc.GetTextExtent(underline)[0]
        te_ju =  dc.GetTextExtent('Jumlah')[0]
        
        dc.DrawText(underline, indent_inv_itemsT - te_un,  line_total-10)
        dc.DrawText('Jumlah',  indent_inv_itemsT - te_un - te_ju - 20,  line_total)
  
        invoice_amount_s = self.format_number(invoice_amount)
        te_gt = dc.GetTextExtent(invoice_amount_s)[0]
        dc.DrawText(invoice_amount_s,  indent_inv_itemsT - te_gt,  line_total)
        
        dc.SetFont(wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        
        in_words = self.convert_to_kata(invoice_amount_s)
        te_iw = dc.GetTextExtent(in_words)[0]
        dc.DrawText(in_words,  indent_inv_itemsT - te_iw ,  line_in_words)
        
        dc.EndDrawing()
        
    def format_number(self, n):
        return format(n, '0,.0f')

    def convert_to_kata(self, no_str): 
        global NUMBER_IN_WORDS
        s = no_str.replace(',','')
        conv_number_to_words(int(s))
        number_in_words = NUMBER_IN_WORDS
        #rints, '  number_to_words', number_in_words
        return number_in_words
    
    def getWidth(self): # callback
        return self.maxWidth

    def getHeight(self):# callback
        return self.maxHeight
    
    
    
    
def create(parent):
    return DlgInvoicePreview(parent)

class DlgInvoicePreview(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_base      = wx.Panel(self, -1)
        self.SetBackgroundColour('Grey')
        self.canvas       = MyCanvas(self.panel_base)

        self.panel_buttons   = wx.Panel(self.panel_base, -1)
        self.button_save     = wx.Button(self.panel_buttons, -1, "Save")
        self.button_cancel   = wx.Button(self.panel_buttons, -1, "Cancel")
 
        self.Bind(wx.EVT_BUTTON, self.OnSave,    self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_cancel)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle(" ")

    def __do_layout(self):
        sizer_base      = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main      = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons   = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_buttons.Add(self.button_save,   0, 0, 0)
        sizer_buttons.Add(self.button_cancel, 0, 0, 0)
        self.panel_buttons.SetSizer(sizer_buttons)
        
        sizer_main.Add(self.canvas,     1, wx.EXPAND, 0)
        sizer_main.Add(self.panel_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        self.panel_base.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_base, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()
        
    def displayData(self, invoice_id):
        inv_details, item_list = self.invoice_details(invoice_id)

        self.canvas.DrawInvoice((inv_details, item_list))
        
    def displayPreview(self, data):
        self.canvas.DrawInvoice(data)
        
    def invoice_details(self, invoice_id):
        sql = "SELECT item_name, qnty, price, total_amount \
                 FROM acc_invoice_items \
                WHERE invoice_id =%d \
                ORDER BY id" % invoice_id
        item_list = fetch.getAllDict(sql)
        
        sql = "SELECT i.amount, i.ck_ref, i.date, i.schYr, s.name, s.NoInduk, f.name AS form_name \
                 FROM acc_invoices i \
                 JOIN students s ON s.id=i.student_id \
                 JOIN students_by_form sbf ON sbf.student_id = s.id \
                 JOIN forms f ON sbf.form_id = f.id \
                WHERE i.id=%d" % invoice_id
        inv_details = fetch.getOneDict(sql)
        
        return (inv_details, item_list)    
        
    def OnSave(self, evt):
        self.printData = wx.PrintData()
        self.printData.SetPaperId( wx.PAPER_ENV_MONARCH)
        
        self.printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        #self.printData.SetBin(wx.TRACTOR_FEED)
        
        pdd = wx.PrintDialogData(self.printData)
        pdd.SetToPage(2)
        printer = wx.Printer(pdd)
        printout = MyPrintout(self.canvas)

        if not printer.Print(self, printout, True):
            wx.MessageBox("There was a problem printing.\nPerhaps your current printer is not set correctly?", "Printing", wx.OK)
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()
        
        
        self.Close()
        
    
    def OnCancel(self, evt):
        self.Close()
    

if __name__ == "__main__":
    app = wx.App(None)
    #dlg = DlgInvoicePreview(None, -1, "")
    dlg = create(None)
    app.SetTopWindow(dlg)
    dlg.displayData(1)
    dlg.Show()
    app.MainLoop()
