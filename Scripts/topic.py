import resource
import module
import os
import lxml.etree as ET

class topic(object) :
  def __init__(self,name) :
     self.namewasread=0
     self.name=name
     self.resources = []

  def readName(self):
     self.namewasread=1
     tree = ET.parse( "Topics/" + self.name + ".xml" )
     self.label = tree.find("TITLE").text 

  def addResource(self,location,programming,modname,resource_name,author,description):
     f = open("Topics/" + self.name + ".xml", "r")
     lines = f.readlines()
     inresources=0
     for line in lines : 
         if "END:" in line :
            if inresources!=0 :
               sys.error("found END after resource start")
            inresources = 1 
         elif inresources==1 :
            if len(line.split())>4 :
               if line.split()[4]==resource_name :
                  return 0
     
     f = open("Topics/" + self.name + ".xml", "a+")
     f.write( self.name + " " + location + " " + programming + " " + modname + " " + resource_name + " " + author + " " +  description + "\n" )
     f.close()
     os.remove("html/" + self.name + ".html" )
     self.printTopicPage()
     if location!="EXTERNAL" :  
        os.remove("html/" + modname + ".html" )
        mymodules = module.listofmodules()
        mymodules.get(modname).printModulePage()
     return 1

  def getRelevantResources(self,modname,ltype,reslist,pstyle):
    print("GETTING RESOURCES FROM " + self.name )
    tree = ET.parse( "Topics/" + self.name + ".xml" )
    resources, intro_table = tree.findall("RESOURCE"), ""
    for res in resources :
        res_obj = resource.resource( res )
        if (res_obj.ofModAndLevel( modname, ltype )) & (res_obj.linkb not in reslist) : 
            reslist.append(res_obj.linkb) 
            intro_table += res_obj.getResourceHTML( pstyle )  
    return intro_table, reslist

class topiclist(object) :
  def __init__(self) :
     self.tlist = []
     self.topiclist, self.labellist = [], []
     tlist = os.listdir('Topics')
     for this in tlist :
         # Make sure swap files are ignored 
         if this.endswith('.xml') : 
            tname = this.replace(".xml","")
            self.topiclist.append( tname )
            newtopic = topic( tname )
            newtopic.readName()
            self.labellist.append( newtopic.label )
            self.tlist.append( newtopic )

  def get( self, name ) :
     ind=self.topiclist.index(name)
     return self.tlist[ind]

  def strip( self, page ) :
     splitup = page.split("/")
     mytopic = splitup[ len(splitup)-1 ].replace(".html","")
     if mytopic not in self.topiclist :
        return "invalid"
     return mytopic 


