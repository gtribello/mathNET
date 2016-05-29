import numpy as np
import shutil
import topic
import os

class module(object):

   def __init__(self, parent):
       self.inlist=parent
       self.wasread=0

   def readin(self,modulename):
       self.wasread=1
       self.name=modulename
       try:
         os.stat('Modules/' + modulename)
       except:
         sys.error("Module " + modulename + " does not appear to have a file")

   def getname(self):
      if( self.wasread==0 ):
         sys.error("Cannot get name as module was not read")
      return self.name

   def addConnectionsToMatrixGraph(self,nodelist,graph):
      self.mygraph = np.zeros( (len(nodelist), len(nodelist) ) )
      if( self.wasread==0 ):
         sys.error("Cannot get name as module was not read")
# Now open the file ane read in the lines
      mfile = open( "Modules/" + self.name, 'r' )
      mtlist = mfile.readlines()
      mfile.close()
# This does the generation of the graph
      ingraph = 0
      clista = []
      for item in mtlist :               # range(1,len(mtlist)):
         if ingraph==1 :
            clistb = item.split()
            if (len(clista)>0) & (len(clistb)>0) :
               assert( (len(clista)==1) & (len(clistb)==1) )
               assert( (clista[0] in nodelist) & (clistb[0] in nodelist) )
               graph[ nodelist.index(clista[0]), nodelist.index(clistb[0]) ] += 1
               self.mygraph[ nodelist.index(clista[0]), nodelist.index(clistb[0]) ]=1
            clista=clistb
         elif "GRAPH:" in item  :
            ingraph=1
            
      return graph

   def printModulePage(self):
      f = open( 'Templates/module_template.html', 'r' )
      outfilecontents = f.read()
      f.close()
      # Now open the file ane read in the lines
      mfile = open( "Modules/" + self.name, 'r' )
      mtlist = mfile.readlines()
      mfile.close()
      indesc = 0
      desc = ""
      inlearn = 0
      ingraph = 0
      learning = "<ul> \n"
      utopics = []
      for item in mtlist : 
          if "TITLE:" in item :
             outfilecontents = outfilecontents.replace("INSERT FULL NAME", item.replace("TITLE:","") )
          elif "LEARNINGOUTCOMES:" in item :
             if indesc!=1 :
                sys.error("found LEARNINGOUTCOMES: before DESCRIPTION:")
             indesc = 0
             inlearn = 1
          elif indesc==1 :
             desc += item 
          elif "GRAPH:" in item  :
             if inlearn!=1 :
                sys.error("found GRAPH: before LEARNINGOUTCOMES:")
             ingraph=1
             inlearn=0
          elif (inlearn==1) & (item[0]=="-") :
             learning += '<li type="square">' + item[1:] + '</li> \n'
          elif "DESCRIPTION:" in item :
             indesc=1
          elif ingraph==1 :
             clista = item.split()
             # Make list of topics in module
             if len(clista)>0 :
                 assert( len(clista)==1 )
                 if clista[0] not in utopics :
                    utopics.append(clista[0]) 

      # Get relevant resources for each topic in module
      topictab = ""
      reslist = []
      mytopics = topic.topiclist()
      for t in utopics :
          tstring, reslist = mytopics.get(t).getResourceForModule( self.name, reslist )
          topictab += tstring 
      
      outfilecontents = outfilecontents.replace("INSERT FULL DESCRIPTION", desc )
      outfilecontents = outfilecontents.replace("INSERT LEARNING OUTCOMES", learning + "</ul>\n" )    
      outfilecontents = outfilecontents.replace("INSERT MODULE LABEL", self.name)
      outfilecontents = outfilecontents.replace("INSERT MODULE LIST", self.inlist.getModuleMenu() )
      outfilecontents = outfilecontents.replace("INSERT STUDY GUIDE", topictab )
      outfile = open('html/' + self.name + '.html', 'w' )
      outfile.write( outfilecontents )
      outfile.close()

   def getTopicList(self):
      # Now open the file ane read in the lines
      mfile = open( "Modules/" + self.name, 'r')
      mtlist = mfile.readlines()
      mfile.close()
      thesetopics = []
      for j in range(0,len(mtlist)):
          clist = mtlist[j].split()
          for k in range(0,len(clist)):
              thesetopics.append( clist[k] )
      return thesetopics

class listofmodules(object):

   def __init__(self):
       self.modules = []
       self.mnames = os.listdir("Modules")
       for mod in self.mnames :
           newmod = module(self)
           newmod.readin( mod )
           self.modules.append( newmod )

   def get(self,name):
       ind=self.mnames.index(name)
       return self.modules[ind]

   def getModuleMenu(self):
       modulemenu = ""
       for module in self.modules :
           modulemenu += '<li><span><a href="' + module.getname() +'.html">' + module.getname() + '</a></span></li>\n'
       return modulemenu

   def createMatrixGraph(self,nodelist):
       graph = np.zeros( (len(nodelist), len(nodelist) ) )
       for module in self.modules :
           graph = module.addConnectionsToMatrixGraph( nodelist, graph )
       return graph
           
