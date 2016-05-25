import numpy as np
import shutil
import webbrowser
import basicgraph
from topic import topiclist
import module
import Tkinter
import addLinkGui
import classifyResourceGui
import os

class maingui(Tkinter.Tk):
    # Constructor
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.loaded=0

    # Inlialize and create window
    def initialize(self):
        self.loaded=1
        self.grid()
        b1 = Tkinter.Button(self,text="add link", height=10, width=30, command=self.addLink )
        b1.grid(column=0, row=0, padx=10 )
        b2 = Tkinter.Button(self,text="classify new resources", height=10, width=30, command=self.classifyNewResources )
        b2.grid(column=0, row=1, padx=10 )
        b3 = Tkinter.Button(self,text="rebuild website", height=10, width=30, command=self.buildFullWebsite )
        b3.grid(column=0, row=2, padx=10 )

        # Do create stuff
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)

    def addLink(self):
        app = addLinkGui.create_new_links(None)
        app.title('Link creation window')
        app.mainloop()

    def classifyNewResources(self):
        app = classifyResourceGui.classify_resources(None)
        app.title('Add resource link')
        app.mainloop()

    def buildFullWebsite(self):
        if( self.loaded==1 ):
            shutil.rmtree('html')

        # See if the html directory is there and create it 
        # if it isnt
        try:
          os.stat('html')
          try:
             os.stat('html/assets')
          except:
             shutil.copytree('Templates/assets', 'html/assets') 
          try:
             os.stat('html/resources')
          except:
             os.mkdir('html/resources') 
        except:
          os.mkdir('html')
          # Copy the assets to the html directory
          shutil.copytree('Templates/assets', 'html/assets')
          # Make a resources directory
          os.mkdir('html/resources')
        
        # Read in topics
        mytopics = topiclist()
        # Create graph and setup the nodes
        mygraph = basicgraph.basicgraph()
        mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
        # Now read in the modules
        mymodules = module.listofmodules()
        # Create the connections for the graph
        graph = mymodules.createMatrixGraph(mytopics.topiclist)
        # Pass these connections to the graph
        mygraph.setConnections( graph )  
        # Now create all topic pages if not already there
        for topic in mytopics.topiclist :
            if not os.path.isfile('html/' + topic + '.html') :
               mytopics.get( topic ).printTopicPage()
            if not os.path.isfile('html/' + topic + '.svg') :
               mygraph.printNodeGraph( topic )
        # And now build the index
        if not os.path.isfile('html/index.html') :
           f = open( 'Templates/index-template.html', 'r' )
           index_page = f.read()
           f.close()
           ofile = open( 'html/index.html', 'w' )
           ofile.write( index_page.replace("INSERT MODULE LIST", mymodules.getModuleMenu()) )
           ofile.close()
        # And the full graph
        if not os.path.isfile('html/main.svg' ):
           mygraph.printFullGraph("main") 
        
        # Now create all module pages if not already there
        for mod in mymodules.mnames :
            if not os.path.isfile('html/' + mod + '.html') :
               mymodules.get( mod ).printModulePage()
            if not os.path.isfile('html/' + mod + '.svg' ) :
               modtopics = mymodules.get( mod ).getTopicList()
               mygraph.printGraphWithPath( modtopics, mod )

# This is done on start up.  The full website is constructed and the main editor window is opened
if __name__ == "__main__":
   app = maingui(None)
   app.title('Main building window')
   app.buildFullWebsite()
   filename = 'file:///' + os.path.dirname(os.path.realpath(__file__)) + '/../html/index.html' 
   webbrowser.open_new_tab(filename)
   app.initialize()
   app.mainloop()

