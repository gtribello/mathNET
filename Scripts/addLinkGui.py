import tkinter
import tkinter.messagebox as messagebox
import os 
from topic import topiclist
from os import listdir

class create_new_links(tkinter.Tk):
    # Constructor
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    # Inlialize and create window
    def initialize(self):
        self.grid()

        # Create a label
        label = tkinter.Label(self, text='Link', anchor="w")
        label.grid(column=0,row=0,sticky='W',padx=10)
        # Create an entry next to this
        self.link = tkinter.Entry(self, width=60)
        self.link.grid(column=1,row=0,columnspan=6,sticky='W',padx=10)

        # Add entry for topic
        tlabel = tkinter.Label(self, text='Topic', anchor="w")
        tlabel.grid(column=7,row=0,sticky='EW',padx=10)
        TopicList = listdir("Topics")
        TopicList.insert(0,"unset")
        self.topic = tkinter.StringVar()
        self.topic.set(TopicList[0])
        menu = tkinter.OptionMenu(self, self.topic, *TopicList)
        menu.grid(column=8,row=0, sticky='W', padx=10)

        # Add entry for module
        self.video=1
        wbox = tkinter.Checkbutton(self, text="Website", variable=self.video, onvalue=0, offvalue=1, height=5, width=20)
        wbox.grid(column=1,row=1,sticky='W',padx=10)
        vbox = tkinter.Checkbutton(self, text="Video", variable=self.video, onvalue=1, offvalue=0, height=5, width=20)
        vbox.grid(column=2,row=1,sticky='W',padx=10)
        # Add entry for module
        mlabel = tkinter.Label(self, text='Module', anchor="w")
        mlabel.grid(column=3,row=1,sticky='EW',padx=10)
        ModuleList = listdir("Modules")
        ModuleList.insert(0,"unset")
        # ModuleList = [ "unset", "SOR3012", "AMA4004" ]    # Need to get all modules here
        self.module = tkinter.StringVar()
        self.module.set(ModuleList[0])
        menu = tkinter.OptionMenu(self, self.module, *ModuleList)
        menu.grid(column=4,row=1, sticky='W',padx=10) 

        # Add entry for description
        dlabel = tkinter.Label(self, text='Description', anchor="w")
        dlabel.grid(column=0,row=2,sticky='W',padx=10)
        # Create the entry for the description
        self.description = tkinter.Text(self, width=110, height=10 )
        self.description.grid(column=0,row=3,columnspan=9,sticky='W',padx=10)

        # Create some buttons
        clearb = tkinter.Button(self,text="clearcells", command=self.OnClearClick)
        saveb = tkinter.Button(self,text="save", command=self.OnSaveClick )
        clearb.grid(column=7, row=4, padx=10 )
        saveb.grid(column=8, row=4, padx=10 )
        
        # Do create stuff
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)

    # This clears all the entries and cells
    def OnClearClick(self):
        self.link.delete(0, 'end') 
        self.description.delete('1.0', 'end')

    # This saves everything to the file
    def OnSaveClick(self):
        # Check topic was set  
        if self.topic.get()=="unset" :
           messagebox.showerror("Topic was not set")
           return
        # Check link was set
        if "http" not in self.link.get() :
           messagebox.showerror("Link was not set")
           return
        # Check that something has been put in the description
        if self.description.get('1.0','end-1c')=="" :
           messagebox.showerror("No descrption was provided")
           return
        # Generate the link stuff
        rtype = "WEBSITE" 
        location = "EXTERNAL" 
        if self.video==1 :
           rtype = "VIDEO"
           if self.module.get()!='unset' :
              location = "INTRO"
        mytopics = topiclist()
        if( mytopics.get( self.topic.get() ).addResource( location, self.programming.get(), self.module.get(), self.resource.get(), self.description.get('1.0','end-1c') )==0 ):
            messagebox.showerror("Resource has already been added to this topic")
            return  
        # Regenerate this page
        os.remove("html/" + self.topic.get() + ".html" ) 
        mytopics.get( self.topic.get() ).printTopicPage()
        # And clear ready to add new link
        self.link.delete(0, 'end')
        self.description.delete('1.0', 'end')
        self.destroy()
        
