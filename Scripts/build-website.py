import fullgui
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from PyQt4.QtWebKit import QWebView, QWebPage


app = QApplication(sys.argv)
main_frame = fullgui.mainWindow()
main_frame.loaded = 1
main_frame.buildFullWebsite()
