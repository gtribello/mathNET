import tkinter
import tkinter.messagebox as messagebox
from topic import topiclist
import os 


class classify_resources(tkinter.Tk):
    # Constructor
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    # Initialize and create window
    def initialize(self):
        self.grid()

# Create a label
        rlabel = tkinter.Label(self, text='Select resource', anchor='w')
        rlabel.grid(column=0, row=0, sticky='w', padx=10)
        ResourceList = os.listdir("Resources")
        ResourceList.insert(0,"unset")
        self.resource = tkinter.StringVar()
        self.resource.set(ResourceList[0])
        menu = tkinter.OptionMenu(self, self.resource, *ResourceList)
        menu.grid(column=2,row=0, sticky='W', padx=10)
         
        self.exercise=1
        wbox = tkinter.Checkbutton(self, text="Notes", variable=self.exercise, onvalue=0, offvalue=1, height=5, width=20)
        wbox.grid(column=0,row=1,sticky='W',padx=10)
        vbox = tkinter.Checkbutton(self, text="Exercise", variable=self.exercise, onvalue=1, offvalue=0, height=5, width=20)
        vbox.grid(column=1,row=1,sticky='W',padx=10)

# Create choice for exercise type
        elabel = tkinter.Label(self, text='Type', anchor="w")
        elabel.grid(column=2,row=1,sticky='W',padx=10)
        EtypeList = [ "unset", "PDF", "IPYTHON", "HTML" ]
        self.programming = tkinter.StringVar()
        self.programming.set(EtypeList[0])
        menu = tkinter.OptionMenu(self, self.programming, *EtypeList)
        menu.grid(column=3,row=1, sticky='W', padx=10) 

# Add entry for topic
        tlabel = tkinter.Label(self, text='Topic', anchor="w")
        tlabel.grid(column=0,row=2,sticky='EW',padx=10)
        TopicList = os.listdir("Topics")
        TopicList.insert(0,"unset")
        self.topic = tkinter.StringVar()
        self.topic.set(TopicList[0])
        menu = tkinter.OptionMenu(self, self.topic, *TopicList)
        menu.grid(column=1,row=2, sticky='W', padx=10) 

# Add entry for module
        mlabel = tkinter.Label(self, text='Module', anchor="w")
        mlabel.grid(column=2,row=2,sticky='EW',padx=10)
        ModuleList = os.listdir("Modules")
        ModuleList.insert(0,"unset")
        self.module = tkinter.StringVar()
        self.module.set(ModuleList[0])
        menu = tkinter.OptionMenu(self, self.module, *ModuleList)
        menu.grid(column=3,row=2, sticky='W',padx=10)

# Add stuff to enter description
        dlabel = tkinter.Label(self, text='Description', anchor="w")
        dlabel.grid(column=0,row=3,sticky='W',padx=10)
# And text box for description
        self.description = tkinter.Text(self, width=100, height=10 )
        self.description.grid(column=0,row=4,columnspan=4,sticky='W',padx=10)

# Add button to create resource
        saveb = tkinter.Button(self,text="save", command=self.OnSaveClick )
        saveb.grid(column=5, row=5, padx=10 )

        # Do create stuff
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)

# This saves everything to the file
    def OnSaveClick(self):
        # Check topic was set  
        if self.topic.get()=="unset" :
           messagebox.showerror("Topic was not set")
           return
        # Check module was set
        if self.module.get()=="unset" :
           messagebox.showerror("Topic was not set")
           return
        # Check if type was set
        if self.programming.get()=="unset" :
           messagebox.showerror("Resource type was not set") 
           return
        # Check that something has been put in the description
        if self.description.get('1.0','end-1c')=="" :
           messagebox.showerror("No descrption was provided")
           return
        # Generate teh link stuff
        location = "INTRO"
        if( self.exercise==1 ) :
            location = "EXERCISE" 
        mytopics = topiclist()
        if( mytopics.get( self.topic.get() ).addResource( location, self.programming.get(), self.module.get(), self.resource.get(), self.description.get('1.0','end-1c') )==0 ):
            tkMessageBox.showerror("Resource has already been added to this topic")
            return
        # Regenerate this page
        os.remove("html/" + self.topic.get() + ".html" )
        mytopics.get( self.topic.get() ).printTopicPage()
        self.destroy()
