import shutil
import webbrowser
import basicgraph
from topic import topiclist
import module
import addLinkGui
import classifyResourceGui
import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from PyQt4.QtWebKit import QWebView, QWebPage

class UrlInput(QLineEdit):
   def __init__(self, browser):
       super(UrlInput, self).__init__()
       self.browser = browser
       self.returnPressed.connect(self._return_pressed)

   def _return_pressed(self):
       url = QUrl(self.text())
       self.browser.load(url)

class mainWindow(QWidget):
   def __init__(self):
       QWidget.__init__(self)
       # Create the window that is used for adding links to external pages
       self.addLinkDialogue = addLinkGui.AddLinkDialogue(self)
       # Create the window that is used for adding links to stuff in the resources directory
       self.addResourceDialogue = classifyResourceGui.AddResourceDialogue(self) 
       # This ensures the whole website is not rebuilt on the first call 
       self.loaded=0

   def initialize(self):
       self.loaded=1
       grid = QGridLayout()
       self.browser = QWebView()
       # handle clicking of links
       self.browser.linkClicked.connect(self.handleLinkClicked)
       url = 'file:///' + os.path.dirname(os.path.realpath(__file__)) + '/../html/index.html'
       self.url_input = UrlInput(self.browser)
       # Load the main page of the website
       self.loadIndexPage()
       # This does something for following links
       self.browser.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
       # url_input at row 1 column 0 of our grid
       grid.addWidget( self.url_input, 1, 0 )
       # Button for adding link
       self.lbutton = QPushButton('Add external link', self)
       self.lbutton.clicked.connect(self.lbuttonHandle)
       # Button placed in row 1 column 1 or grid
       grid.addWidget( self.lbutton, 1, 1 )
       # Button for adding link to internal link
       self.nbutton = QPushButton('Add internal link', self)
       self.nbutton.clicked.connect(self.nbuttonHandle)
       # button at row 1 column 2 of our grid
       grid.addWidget( self.nbutton, 1, 2 )
       # Button for rebuilding site
       self.rbutton = QPushButton('Rebuild site', self)
       self.rbutton.clicked.connect(self.rbuttonHandle)
       # button at row 1 column 1 of our grid
       grid.addWidget( self.rbutton, 1, 3 )
       # browser frame below it
       grid.addWidget( self.browser, 2, 0, 1, 4 )
       self.setLayout(grid) 

   def handleLinkClicked(self, url):
       self.url_input.setText(url.toString())
       self.browser.load(url)

   def lbuttonHandle(self):
       if self.addLinkDialogue.setCurrentPage( self.url_input.text() ) :
          self.addLinkDialogue.exec_()
       # Refresh page now that it has new content
       self.browser.load( QUrl(self.url_input.text()) )

   def nbuttonHandle(self):
       if self.addResourceDialogue.setCurrentPage( self.url_input.text() ) :
          self.addResourceDialogue.exec_()
       # Refresh page now that it has new content
       self.browser.load( QUrl(self.url_input.text()) )

   def rbuttonHandle(self):
       self.buildFullWebsite()
       self.loadIndexPage()

   def loadIndexPage(self):
       url = 'file:///' + os.path.dirname(os.path.realpath(__file__)) + '/../html/index.html'
       self.url_input.setText(url)
       self.browser.load(QUrl(url)) 

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
  app = QApplication(sys.argv)
  main_frame = mainWindow()
  main_frame.buildFullWebsite()
  main_frame.initialize()
  main_frame.show()
  # close app when user closes window
  sys.exit(app.exec_())
