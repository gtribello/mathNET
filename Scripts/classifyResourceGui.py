# -*- coding: utf-8 -*-
from topic import topiclist
import os 
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AddResourceDialogue(QDialog):
   def __init__(self, parent=None):
       super(AddResourceDialogue, self).__init__(parent) 
       grid = QGridLayout()
       # Create an entry for the page we are linking to
       label = QLabel("Adding link to page about")
       grid.addWidget( label, 1, 0 )
       self.onpage = QTextEdit(self)
       self.onpage.setMaximumHeight(label.sizeHint().height()*2)
       self.onpage.setReadOnly(True) 
       grid.addWidget( self.onpage, 1, 1 )
       # Add module box
       label = QLabel("Module")
       grid.addWidget( label, 1, 2 )
       self.modbox = QComboBox(self)
       self.modbox.addItem("unset")
       for item in os.listdir("Modules") :
           if not item.startswith('.') :
              self.modbox.addItem(item)
       self.modbox.setCurrentIndex(0)
       grid.addWidget( self.modbox, 1, 3 )  
       # Add resource entry
       label = QLabel("Resource")
       grid.addWidget( label, 2, 0 ) 
       # Entry for filename
       self.resource = QTextEdit(self)
       self.resource.setMaximumHeight(label.sizeHint().height()*2)
       self.resource.setReadOnly(True) 
       grid.addWidget( self.resource, 2, 1, 1, 2 )
       # Add browse button
       self.browse = QPushButton('browse', self )
       self.browse.clicked.connect(self.browsefiles)
       grid.addWidget( self.browse, 2, 3 )
       # Author
       alabel = QLabel("Author")
       grid.addWidget( alabel, 3, 0 )
       self.author = QTextEdit(self)
       self.author.setMaximumHeight(label.sizeHint().height()*2)
       grid.addWidget( self.author, 3, 1 )
       # Descrition
       label = QLabel("Description")
       grid.addWidget( label, 4, 0 )
       self.textBrowser = QTextEdit(self)
       grid.addWidget( self.textBrowser, 5, 0, 1, 4 )
       # Type dropdown
       label = QLabel("Type")
       grid.addWidget( label, 4, 2 )
       self.typebox = QComboBox(self)
       self.typebox.addItem("unset")
       self.typebox.addItem("INTRO")
       self.typebox.addItem("EXERCISE")
       self.typebox.setCurrentIndex(0)
       grid.addWidget( self.typebox, 4, 3 ) 
       # And go button
       self.gobutton = QPushButton('save', self ) 
       self.gobutton.clicked.connect(self.save)
       grid.addWidget( self.gobutton, 6, 3 )
       self.setLayout(grid)

   def setCurrentPage( self, page ):
       mytopics = topiclist()
       mypage = mytopics.strip( page )
       self.onpage.setText(mypage)
       if( mypage=="invalid" ) :
           return False
       return True

   def browsefiles( self ):
       filename = QFileDialog.getOpenFileName(self, 'Add resource file', 'Resources', "Files (*.ipynb *.pdf *.xml *.html *.zip *.tex)" )
       splitup = filename.split("/")
       if splitup[len(splitup)-2] != "Resources" : 
          error = QErrorMessage(self)
          error.showMessage("Cannot add file that is not in Resources directory")
          error.exec_()
          return
       self.resource.setText( splitup[len(splitup)-1] )

   def save( self ):
       error = QErrorMessage(self)
       # Check module was set
       if self.modbox.currentText()=="unset" :
          error.showMessage("Module for resource was not set")
          error.exec_()
          return
       # Check resource was set
       if self.resource.toPlainText()=="" :
          error.showMessage("Resource was not set")
          error.exec_()
          return
       # Check if type was set
       if self.typebox.currentText()=="unset" :
          error.showMessage("Type for resource was not set")
          error.exec_()
          return
       # Check that something has been put in the description
       if self.textBrowser.toPlainText()=="" :
          error.showMessage("Description was not set")
          error.exec_()
          return
       # Put this information in the topic list
       mytopics = topiclist()
       thistopic = self.onpage.toPlainText()
       # Get extension of file
       myfile = self.resource.toPlainText()
       splitup = myfile.split(".")
       ext = splitup[len(splitup)-1]
       ftype = "XML"
       if ext=="ipynb" : 
          ftype = "IPYTHON"
       elif ext=="zip" :
          ftype = "IPYTHON" 
       elif ext=="pdf" :
          ftype = "PDF"
       elif ext=="tex" :
          ftype = "LATEX"
       elif ext=="html" :
          ftype = "HTML"
       elif ext=="xml" :
          f = open( "Resources/" + myfile, "r" )
          m_page = f.read()
          f.close()
          if m_page.find("<GEOGEBRA>") !=-1 :
             ftype = "GEOGEBRA"
          myfile=myfile.replace(".xml","")
       else :
          error.showMessage("Invalid extension on input resource file")
          error.exec_()
          return
       # And add the resource to the page
       author = self.author.toPlainText().replace(" ","~")
       if mytopics.get(thistopic).addResource( self.typebox.currentText(), ftype, self.modbox.currentText(), myfile, author, self.textBrowser.toPlainText())==0 :
          error.showMessage("This resource has already been added to this page")
          error.exec_()
          return
       # Clear all input data
       self.resource.setText("")
       self.modbox.setCurrentIndex(0)
       self.typebox.setCurrentIndex(0) 
       self.textBrowser.setText("")
       # Close the window
       self.close()
