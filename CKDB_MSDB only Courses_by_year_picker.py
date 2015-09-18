import wx, gVar,  pyodbc

import fetchodbc as fetch

from itemPicker import itemPicker

from wx.lib.itemspicker import ItemsPicker, \
                               EVT_IP_SELECTION_CHANGED, \
                               IP_SORT_CHOICES, IP_SORT_SELECTED,\
                               IP_REMOVE_FROM_CHOICES

import DlgNewEditCourse
"""
dlg = DlgNewEditCourse(None)
    try:
        dlg.displayData(20)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()"""

#----------------------------------------------------------------------

        
def create(parent):
    return ItemsPickerDialog(parent)        
        
class ItemsPickerDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.button_add = wx.Button(self, -1, "Add Course")
        self.button_add.Bind(wx.EVT_BUTTON, self.OnAdd)
        
        style = wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING | wx.LC_NO_HEADER  | wx.LC_VRULES | wx.LC_HRULES
                                 
        self.item_picker = itemPicker(self, -1)                         
                                 
        self.button_save = wx.Button(self, -1, "Save")
        self.button_save.Bind(wx.EVT_BUTTON, self.OnSave)
        
        self.__layout()
        self.__set_properties()
        
        self.main()
        
    def __layout(self):
        sizer =wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.button_add, 0, wx.ALL, 5)
        sizer.Add(self.item_picker, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.button_save, 0, wx.ALL | wx.ALIGN_RIGHT,5)
        self.SetSizer(sizer)
        
    def __set_properties(self):
        self.SetSize((500,700))
        self.Layout()
        #self.Fit()
        self.Center()

    def main(self):
        self.itemCount = 0
        gVar.schYr = 2015
        
        label2 = 'Courses For %s:' % gVar.schYr
        self.item_picker.SetLabels('All Courses', label2)
        
        heading_pool      = (('id',0), ('Course Title',120), ('Age',40))
	heading_selection = (('id',0), ('Course Title',120), ('Age',40))
        sy = {"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR}
	self.item_picker.SetListCtrl(heading_pool, heading_selection, sy)
        
        source_list = self.PopulateSourceList()    
        selection_list = self.populateSelectionList()

        self.item_picker.PopulateLists(source_list, selection_list)
        self.item_picker.SortByCol(2)
	
    def populateSelectionList(self):
	selection_list =[]
        sql = "SELECT courses.id, courses.course_name, courses.course_level \
	         FROM courses \
	   INNER JOIN courses_by_year \
	           ON (int(courses.id) = int(courses_by_year.course_id)) \
		WHERE courses_by_year.schYr = %s" % gVar.schYr
        results = fetch.getAll_dict(sql)
	
        if results:
            self.update = True
            for row  in results:
                course_id, course_name, x    = row
                course_level = "%02d" % row[2]
                selection_list.append((course_id, course_name, course_level))
            
        else:
            self.update = False
	return 	selection_list

        
    def PopulateSourceList(self):
        source_list=[]
        sql = "SELECT id, course_name, course_level FROM courses ORDER BY course_level"
        result = fetch.getAll_col(sql)
        for row in result:
            course_id    = row[0]
            course_name  = row[1]
            course_level = "%02d" % row[2]
            source_list.append((course_id, course_name, course_level))
        return source_list
 
    def OnSave(self, evt):
        course_ids_list = self.item_picker.GetAllSelectionIds()
        course_ids = str(course_ids_list).strip('[]')
        if self.update:
            sql = "UPDATE courses_by_year SET courses = '%s' WHERE schYr =%d" % (course_ids, gVar.schYr)
            fetch.updateDBtransaction(sql)
            txt ="List Saved"
            fetch.msg(txt)
            
        else:
            sql = "SELECT * WHERE schYr = %d" % gVar.schYr
            result = fetch.getCount(sql)
            if not result:
                sql = "INSERT INTO courses_by_year (courses, schYr) VALUES ('%s', %d)" % (course_ids, gVar.schYr)
                fetch.updateDBtransaction(sql)
                self.update=True
            else:
                txt ="Error - check coding"
                fetch.msg(txt)

    def OnAdd(self,evt): # add new course to courses
        txt = "Not Yet Fully Functional : Please ask administrator to assist"
        fetch.msg(txt)
        #return
	
	import wx.grid as gridlib
	
	g = gridlib.Grid(self, -1)
	g.GetNumberRows()
    
        dlg = DlgNewEditCourse.create(None)
        try:
            if dlg.ShowModal():
                #rint'Dlg Created New Course'
                source_list = self.PopulateSourceList()
                self.item_picker.RepopulateSourceList(source_list)
            else:
                #rint'do nothing'
            
        finally:
            dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(redirect=False)
    dlg = ItemsPickerDialog(None, -1, "")
    try:
        #dlg.displayData(1, 0)
        dlg.ShowModal()
        
    finally:
        dlg.Destroy()
        
    app.MainLoop()
