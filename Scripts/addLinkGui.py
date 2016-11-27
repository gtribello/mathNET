import os 
from topic import topiclist
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class AddLinkDialogue(QDialog):
   def __init__(self, parent=None):
       super(AddLinkDialogue, self).__init__(parent)
       grid = QGridLayout()
       # Create an entry for the page we are linking to
       label = QLabel("Adding link to page about")
       grid.addWidget( label, 1, 0 )
       self.onpage = QTextEdit(self)
       self.onpage.setMaximumHeight(label.sizeHint().height()*2) 
       self.onpage.setReadOnly(True)
       grid.addWidget( self.onpage, 1, 1 )
       # Add type of resource
       label = QLabel("Type")
       grid.addWidget( label, 1, 2 )
       self.typebox = QComboBox(self)
       self.typebox.addItem("unset")
       self.typebox.addItem("WEBSITE")   
       self.typebox.addItem("VIDEO")
       self.typebox.setCurrentIndex(0)
       grid.addWidget( self.typebox, 1, 3 )
       label = QLabel("Link to add")
       grid.addWidget( label, 2, 0 )
       self.linkd = QLineEdit(self)
       grid.addWidget( self.linkd, 2, 1, 1, 3 )
       label = QLabel("Description")
       grid.addWidget( label, 3, 0 )
       self.textBrowser = QTextEdit(self)
       grid.addWidget( self.textBrowser, 4, 0, 1, 4 )
       # Clear button
       self.clearb = QPushButton('clear', self)
       self.clearb.clicked.connect(self.clearcells)
       grid.addWidget(self.clearb, 5, 2 )
       self.okb = QPushButton('save', self)
       self.okb.clicked.connect(self.savedata)
       grid.addWidget(self.okb, 5, 3 )
       self.setLayout(grid)

   def setCurrentPage( self, page ):
       mytopics = topiclist()
       mypage = mytopics.strip( page )
       self.onpage.setText(mypage)
       if( mypage=="invalid" ) :
           return False
       return True

   def clearcells( self ):
       self.linkd.setText("")
       self.typebox.setCurrentIndex(0)
       self.textBrowser.setText("")

   def savedata( self ):
       error = QErrorMessage(self)
       # Check that the type was set
       if self.typebox.currentText()=="unset" :
          error.showMessage("Type of resource was not set")
          error.exec_()
          return 
       # Check link was set
       if "http" not in self.linkd.text() :
          error.showMessage("Link was not set")
          error.exec_()
          return 
       # Check something has been put in the description
       if self.textBrowser.toPlainText()=="" :
          error.showMessage("Description was not set")
          error.exec_()
          return
       # Generate topic list
       mytopics = topiclist() 
       thistopic = self.onpage.toPlainText() 
       if( mytopics.get(thistopic).addResource( "EXTERNAL", self.typebox.currentText(), "module", self.linkd.text(), "blank", self.textBrowser.toPlainText() )==0 ) :
          error.showMessage("This resource has already been added to this page")
          error.exec_()
          return 
       self.clearcells()
       self.close()
