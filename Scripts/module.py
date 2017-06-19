import numpy as np
import shutil
import topic
import basicgraph
import os

#class module(object):
#
#   def __init__(self, parent):
#       self.inlist=parent
#       self.wasread=0
#
#   def readin(self,modulename):
#       self.wasread=1
#       self.name=modulename
#       try:
#         os.stat('Modules/' + modulename)
#       except:
#         sys.error("Module " + modulename + " does not appear to have a file")
#
#   def getname(self):
#      if( self.wasread==0 ):
#         sys.error("Cannot get name as module was not read")
#      return self.name

class listofmodules(object):

   def __init__(self):
       self.mnames = []
       for mod in os.listdir("Modules") :
           if mod.endswith('.xml') :
              # newmod = module(self)
              # newmod.readin( mod )
              self.mnames.append( mod.replace(".xml","") )
              # self.modules.append( newmod )

   def get(self,name):
       ind=self.mnames.index(name)
       return self.modules[ind]

   def getModuleMenu(self):
       modulemenu = ""
       for module in self.mnames :
           modulemenu += '<li><span><a href="' + module +'.html">' + module() + '</a></span></li>\n'
       return modulemenu
