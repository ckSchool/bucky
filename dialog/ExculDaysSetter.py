import wx

import data.fetch   as fetch
import data.gVar    as gVar

def create(parent):
    return DlgExculDaysSetter(parent)

class DlgExculDaysSetter(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.panel_main    = wx.Panel(self, -1)
        self.label_title   = wx.StaticText(self.panel_main, -1, " ")
        self.static_line =   wx.StaticLine(self.panel_main, -1)
        self.checkbox_mon  = wx.CheckBox(self.panel_main,   1001, " ")
        self.checkbox_tue  = wx.CheckBox(self.panel_main,   1002, " ")
        self.checkbox_wed  = wx.CheckBox(self.panel_main,   1003, " ")
        self.checkbox_thur = wx.CheckBox(self.panel_main,   1004, " ")
        self.checkbox_fri  = wx.CheckBox(self.panel_main,   1005, " ")
        self.button_ok     = wx.Button(self.panel_main,     -1, "Done")
        
        self.ckbx_list=[self.checkbox_mon, self.checkbox_tue, self.checkbox_wed, self.checkbox_thur, self.checkbox_fri]

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_ok)
        
    def __set_properties(self):
        self.SetSize((250, -1))
        self.SetTitle("Excul Sessions For:  Primary 2012 semester1")
        self.label_title.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        
        sizer_main.Add(self.label_title, 0, wx.BOTTOM, 10)
        sizer_main.Add(self.static_line, 0 ,wx.EXPAND ,0)
        for ckbx in self.ckbx_list:
                    sizer_main.Add(ckbx, 0, wx.TOP | wx.BOTTOM, 5)
        sizer_main.Add(self.button_ok,   0, wx.TOP | wx.ALIGN_RIGHT, 10)
        self.panel_main.SetSizer(sizer_main)
        
        sizer_base.Add(self.panel_main, 1, wx.ALL | wx.EXPAND, 20)
        self.SetSizer(sizer_base)
        
        self.Layout()
        self.Center()
        
    def displayData(self, school_id=0, semester=1):
        title = '%s %d Semester %d' % ('Primary', gVar.schYr, semester)
        self.label_title.SetLabelText(title)
        
        # create class variables
        self.origional_list_of_days = [0,0,0,0,0] # set all days = 'no scheduled activities'
        self.semester_no = semester
        self.school_id   = school_id
        
        orig_days_list = []
        res = fetch.exculSchedule_forSchSemYr(school_id, semester, gVar.schYr)
        for row in res:
            orig_days_list.append(row['day'])
        
        dayNo = 1
        for chbx in self.ckbx_list:
            day_name = gVar.dayNames[dayNo]
            label_text = "%s (-)" % day_name
            if dayNo in orig_days_list:
                print 'dayno', dayNo, ' in list', orig_days_list
                self.origional_list_of_days[dayNo-1] = True
                chbx.SetValue(True)
                schedule_id = fetch.excul_schedule_id(dayNo, semester, school_id, gVar.schYr)
                res = fetch.exculGroupsDATA_forScheduleID(schedule_id)
                club_count = len(res)
                label_text = "%s (%d) clubs" % (day_name, club_count )
                if club_count:
                    chbx.Disable()
            chbx.SetLabelText(label_text)
            print 'dayno', dayNo
            dayNo += 1
            
    def OnOk(self, event):
        for dayNo in [1,2,3,4,5]:
            print 'dayNo = ', dayNo
            if self.ckbx_list[dayNo-1].GetValue():  # if checkbox is ticked
                if not dayNo in self.origional_list_of_days:
                    self.insert(dayNo)
            else: # if  not ticked 
                if dayNo in self.origional_list_of_days:
                    self.remove(dayNo)
        self.EndModal(wx.OK)
        print 'xxxxxxxxxxxx'
        
    def insert(self, dayNo):
        sql = "INSERT INTO excul_schedule \
                  SET day = %d, semester = %d, school_id = %d, schYr = %d" % (
                      dayNo, self.semester_no, self.school_id, gVar.schYr)

        fetch.updateDB(sql)
        
    def remove(self, dayNo):
        sql = "DELETE FROM excul_schedule \
                WHERE day = %d AND semester = %d AND school_id = %d AND schYr = %d" % (
                      dayNo, self.semester_no, self.school_id, gVar.schYr)
        print sql
        fetch.updateDB(sql)
 
#  to test dialog
if __name__ == '__main__':
    gVar.schYr = 2015
    app = wx.App(redirect=False)
    dlg = create(None)
    try:
        dlg.displayData(2, 1)
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
