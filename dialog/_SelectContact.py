import wx, datetime, gVar, loadCmb, fetch
from myListCtrl import VirtualList

#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process


def create(parent):
    return DlgSelectContact(parent)

class DlgSelectContact(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_contacts = wx.Panel(self, -1)
        self.label_name     = wx.StaticText(self.panel_contacts, -1, "Contact Name")
        self.text_ctrl_name = wx.TextCtrl(self.panel_contacts, -1, "")
        self.button_search  = wx.Button(self.panel_contacts, -1, 'Search')
        
        tempheading = (("ID",0), ("Contact Name",105), ("Type",100), ("Students",100),('',0))
        self.vList  = VirtualList(self, tempheading, style = wx.LC_HRULES | wx.LC_SINGLE_SEL)
        
        #self.list_box_names = wx.ListCtrl(self, -1, choices=[], style = wx.LB_SORT)
        
        self.panel_relation  = wx.Panel(self, -1)
        self.label_relation  = wx.StaticText(self.panel_relation, -1, "Relationship")
        self.choice_relation = wx.Choice(self.panel_relation, -1, choices=['Father','Mother','Guardian'])
        self.panel_bottom    = wx.Panel(self, -1)
        self.spc_4           = wx.Panel(self.panel_bottom, -1)
        self.button_new      = wx.Button(self.panel_bottom, -1, "ADD NEW CONTACT")
        self.button_save     = wx.Button(self.panel_bottom, -1, "SAVE")
        self.button_cancel   = wx.Button(self.panel_bottom, -1, "CANCEL")
        self.spc_5           = wx.Panel(self.panel_bottom, -1)

        self.__set_properties()
        self.__do_layout()

        #self.Bind(wx.EVT_TEXT_ENTER, self.OnDblCheck, self.text_ctrl_name)
        #self.Bind(wx.EVT_TEXT, self.OnEnterText, self.text_ctrl_name)
        #self.Bind(wx.EVT_KEY_DOWN, self.KeyDown, self.text_ctrl_name)
        self.Bind(wx.EVT_COMMAND_LEFT_CLICK,       self.OnSelect, self.vList)
        self.Bind(wx.EVT_COMMAND_LEFT_DCLICK,      self.OnDblCheck, self.vList)
        
        self.Bind(wx.EVT_BUTTON, self.OnSave,      self.button_save)
        self.Bind(wx.EVT_BUTTON, self.OnNew,       self.button_new)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,    self.button_cancel)
        self.Bind(wx.EVT_BUTTON, self.OnEnterText, self.button_search)

        self.main()

    def __set_properties(self):

        self.SetTitle("Select Contact")
        self.text_ctrl_name.SetMinSize((-1, 21))
        self.SetMinSize((500,500))
        self.Center()
        self.Layout()

    def __do_layout(self):
        sizer_contacts = wx.BoxSizer(wx.VERTICAL)
        sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        sizer_relation = wx.BoxSizer(wx.HORIZONTAL)
        sizer_search = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_search.Add(self.label_name, 0, wx.ALL, 5)
        sizer_search.Add(self.text_ctrl_name, 1, wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, 5)
        sizer_search.Add(self.button_search,  0,0,0)
        self.panel_contacts.SetSizer(sizer_search)
        
        sizer_relation.Add(self.label_relation,  0, wx.LEFT, 5)
        sizer_relation.Add(self.choice_relation, 0, 0, 0)
        self.panel_relation.SetSizer(sizer_relation)
        
        sizer_bottom.Add(self.spc_4, 1, wx.EXPAND, 0)
        sizer_bottom.Add(self.button_new,    0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_bottom.Add(self.button_save,   0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_bottom.Add(self.button_cancel, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_bottom.Add(self.spc_5,         1, wx.EXPAND, 0)
        self.panel_bottom.SetSizer(sizer_bottom)
        
        sizer_contacts.Add(self.panel_contacts, 0, wx.EXPAND, 0)
        sizer_contacts.Add(self.vList,          1, wx.ALL | wx.EXPAND, 5)
        sizer_contacts.Add(self.panel_relation, 0, wx.TOP | wx.EXPAND, 5)
        sizer_contacts.Add(self.panel_bottom,   0, wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.SetSizer(sizer_contacts)
        sizer_contacts.Fit(self)
        self.Layout()

    def main(self):
        self.name=''
        heading = (("ID",0), ("Contact Name",105), ("Type",100), ("Students",100),('',0))
        self.vList.SetColumns(heading)
        
        sql = "SELECT Kode, NamaA, NamaI FROM OrangTua"
        res = fetch.getAllDict(sql)
        
        self.contacts = {}

        l = []
        for r in res:
            ##rintr
            k = r['Kode']+10000
            a = r['NamaA']
            i = r['NamaI']
            
            if a:
                l.append((k,a,'Father'))
                self.contacts[k]=a
                
            if i:
                k = k + 10000
                l.append((k,i,'Mother'))
                self.contacts[k]=i

        sql = "SELECT Kode, Nama FROM Wali"
        res = fetch.getAllDict(sql)

        for r in res:
            k = r['Kode']
            n = r['Nama']
            if a:
                l.append((k,n,'Guardian'))
                self.contacts[k] = n

        sorted(l,key=lambda x: x[1])
        self.updateList(self.contacts)
        
    def updateList(self, contacts):    
        # Get Names of Students Related To Guardian
        
        d = {}
        index = 0
        for guardian_id in contacts:
            ##rinti
            #guardian_id = i[0]
            name = contacts[guardian_id]# i[1]
            if not name: name ='-'
            
            gid = 0
            #tup = ( name, students))
            if name:
                if guardian_id > 20000:
                    gid = guardian_id -20000
                    mtype = 'Mother'
                    #self.choice_relation.Select(1)
                    
                elif guardian_id > 10000:
                    gid = guardian_id -10000
                    mtype = 'Father'
                    #self.choice_relation.Select(0)
                    
                else:
                    mtype = 'Guardian'
                    #self.choice_relation.Select(2)
                students = self.getKids(gid)
                if not students : students ='-'
                    
                d[index]=(guardian_id, name, mtype, students)
                index += 1
        ##rintd      
        # (index : (id,'data','data'....))
        self.vList.SetItemMap(d)

    def getKids(self, kode):
        if kode > 10000: kode -= 10000
        sql = "SELECT Nama FROM Siswa WHERE KOrangTua = %d GROUP BY Nama" % kode
        res = fetch.getList(sql)
        l = (',').join(res)
        return l

    def OnNew(self, evt):
        pass

    def OnSelect(self, event):  # wxGlade: DlgSelectContact.<event_handler>
        try:
            contact_id = int(self.vList.GetSelectedID())
            self.real_id = self.getType(contact_id)

        except:
            pass
        
    def getType(self, gid):
        if gid > 20000: # mother
            gid = gid -20000
            self.guardian_type='mother'
            self.choice_relation.SetSelection(1)
            
        elif gid > 10000:# father
            gid = gid -10000
            #rintself.guardian_type
            self.choice_relation.SetSelection(0)
            
        else:
            self.guardian_type='guardian'
            self.choice_relation.SetSelection(2)
        return gid
        
        
    def OnDblCheck(self, event):  # wxGlade: DlgSelectContact.<event_handler>
        self.contact_id = contact_id = int(self.vList.GetSelectedID())
        self.name = self.contacts[contact_id]
        self.text_ctrl_name.SetValue(self.name)
        
        self.real_id = self.getType(contact_id)
        #rint'OnDblCheck'

    def OnSave(self, event):  # wxGlade: DlgSelectContact.<event_handler>
        #rintevent.GetEventObject().GetName()
        name = self.text_ctrl_name.GetValue()
        
        if name == self.name:
            sql = 'update', self.name, self.contact_id , self.guardian_type
            self.flag = ('update', self.contact_id)
                
        else:
            sql = "INSERT INTO %s  %s" % (name, self.guardian_type)
            #get insert_id
            self.flag = ('insert', self.contact_id)
            self.guardian_type =self.choice_type.GetCurrentSelection()
            #rintself.guardian_type
        
        #rintsql

    def OnCancel(self, event):  # wxGlade: DlgSelectContact.<event_handler>
        #rint"Event handler `OnCancel' not implemented!"
        self.Close()
    
    def KeyDown(self, evt):
        #rint'a'
        event.Skip()
        
    def OnEnterText(self, event):  # wxGlade: DlgSelectContact.<event_handler>
        k = self.text_ctrl_name.GetValue().strip(' ')
        #rint'b', k
        event.Skip()
        self.updateList(self.testName(k))
    
    def testName(self, k):    
        if k: 
            new_dict ={}
            for key in self.contacts: 
                name = self.contacts[key]
                if name:
                    pass
                    #x=fuzz.token_set_ratio(k, name)
                    #rintx
                    #if x>75: 
                    ##rintfuzz.token_set_ratio(k, name), k,name
                    #    new_dict[key]=name
                
            return(new_dict)
            
        else:
            return(self.contacts)    

if __name__ == "__main__":
    app = wx.App(redirect=False)

    DlgSelectContact = DlgSelectContact(None, -1, "")
    app.SetTopWindow(DlgSelectContact)
    DlgSelectContact.Show()
    app.MainLoop()
