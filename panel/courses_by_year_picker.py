import wx

import data.fetch   as fetch
import data.gVar    as gVar

from panel.itemPicker import itemPicker

from wx.lib.itemspicker import ItemsPicker, \
                               EVT_IP_SELECTION_CHANGED, \
                               IP_SORT_CHOICES, IP_SORT_SELECTED,\
                               IP_REMOVE_FROM_CHOICES

import dialog.NewEditCourse

        
class panel_courses_picker(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.SetName('panel_courses_picker')
        
	
	self.panel_header   = wx.Panel(self, -1)
	self.panel_header_l = wx.Panel(self.panel_header, -1)
	self.panel_header_r = wx.Panel(self.panel_header, -1)
	
	
	#self.button_back    = wx.Button(self.panel_header_l, -1, "Back")
	#self.panel_spc      = wx.Panel(self.panel_header_l, -1)
        self.button_add     = wx.Button(self.panel_header_l, -1, "Add Course")
        
        
        style = wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING | wx.LC_NO_HEADER  | wx.LC_VRULES | wx.LC_HRULES
                                 
        self.item_picker = itemPicker(self, -1)                         
                                 
        self.button_save = wx.Button(self, -1, "Save")
        self.button_save.Bind(wx.EVT_BUTTON, self.OnSave)
	
	#self.Bind(wx.EVT_BUTTON, self.OnBack,     self.button_back)
	self.button_add.Bind(wx.EVT_BUTTON, self.OnAdd)
        
        self.__layout()
        self.__set_properties()
        
        self.main()
        
    def __layout(self):
	sizer    = wx.BoxSizer(wx.VERTICAL)
	sizer_h  = wx.BoxSizer(wx.HORIZONTAL)
	sizer_h_l = wx.BoxSizer(wx.HORIZONTAL)
	
	#sizer_h_l.Add(self.button_back, 0, 0, 0)
	#sizer_h_l.Add(self.panel_spc,   1, 0, 5)
	sizer_h_l.Add(self.button_add,  0, wx.ALIGN_RIGHT, 0)
	self.panel_header_l.SetSizer(sizer_h_l)
	
	sizer_h.Add(self.panel_header_l,  1, 0, 0)
	sizer_h.Add(self.panel_header_r,  1, 0, 0)
	self.panel_header.SetSizer(sizer_h)
        
        sizer.Add(self.panel_header, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.item_picker,  1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.button_save,  0, wx.ALL | wx.ALIGN_RIGHT,5)
        self.SetSizer(sizer)
        
    def __set_properties(self):
        self.SetSize((500,700))
        self.Layout()
        self.Center()
	
    def OnBack(self, evt):
        self.GetTopLevelParent().goBack()

    def main(self):
        pass
	
    def create_selectionList(self):
	#rint'create_selectionList'
	selection_list =[]
        sql = "SELECT c.id, c.name, c.level \
	         FROM courses c \
	         JOIN courses_by_year cby  ON c.id = cby.course_id \
		WHERE cby.schYr = %s" % gVar.schYr
	
	results = fetch.courses_for_year(gVar.schYr)
	
	#rint'fetch.courses_for_year', results
        if results:
            self.update = True
            for row  in results:
		
                course_id, course_name, course_level    = row['id'], row['name'],row['level']
		#rintcourse_id, course_name, course_level 
                #course_level = "%02d" % level
                selection_list.append((course_id, course_name, course_level))
            
        else:
            self.update = False
	return 	selection_list

        
    def create_sourceList(self):
	##rint'create_sourceList'
        source_list=[]

        result = fetch.courses_byLevel()
        for row in result:
            course_id, course_name, course_level    = row['id'], row['name'],row['level']
	    #rintcourse_id, course_name, course_level 
            source_list.append((course_id, course_name, course_level))

        return source_list
 
    def OnSave(self, evt):
        course_ids_list = self.item_picker.GetAllSelectionIds()
        course_ids = str(course_ids_list).strip('[]')
	
	sql = "DELETE \
		 FROM courses_by_year \
		WHERE schYr = %d" % gVar.schYr
	#rintsql
	#rintfetch.updateDB(sql)
	
	data = ()
	for course_id in course_ids_list:
	    sql = "INSERT INTO courses_by_year (course_id, schYr)  \
                     VALUES (%d, %d)" % (course_id, gVar.schYr)
	    #rintsql
	    fetch.updateDB(sql)
	
	
	
	

    def OnAdd(self,evt): # add new course to courses
	pass
	    
    def displayData(self):
	#rint'panel_courses_by_year_picker > displayData'
	
	label2 = 'Courses For %s:' % gVar.schYr
        self.item_picker.SetLabels('All Courses', label2)
	
	self.itemCount = 0

        heading_pool      = (('id',50), ('Course Title',120), ('Age',40))
	heading_selection = (('id',50), ('Course Title',120), ('Age',40))
        sy = {"w_idx":wx.ART_WARNING,   "e_idx":wx.ART_ERROR}
	self.item_picker.SetListCtrl(heading_pool, heading_selection, sy)
        #rint'SetListCtrl'
	
	
        source_list    = self.create_sourceList()
	print
	#rint'source_list created:', source_list
	print
	
        selection_list = self.create_selectionList()
	#rint'   selection_list created:',selection_list
        self.item_picker.PopulateLists(source_list, selection_list)
        self.item_picker.SortByCol(2)

