import resource
import module
import os

class topic(object) :
  def __init__(self,name) :
     self.namewasread=0
     self.name=name
     self.resources = []

  def readName(self):
     self.namewasread=1
     try:
        ifile = open( 'Topics/' + self.name, 'r' )
     except:
        sys.error("could not find input file")
     mystr = ifile.readline()
     ifile.close()
     self.label =  mystr.replace("TITLE: ", "").rstrip('\n') 

  def addResource(self,location,programming,modname,resource_name,author,description):
     f = open("Topics/" + self.name, "r")
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
     
     f = open("Topics/" + self.name, "a+")
     f.write( self.name + " " + location + " " + programming + " " + modname + " " + resource_name + " " + author + " " +  description + "\n" )
     f.close()
     os.remove("html/" + self.name + ".html" )
     self.printTopicPage()
     os.remove("html/" + modname + ".html" )
     mymodules = module.listofmodules()
     mymodules.get(modname).printModulePage()
     return 1

  def printTopicPage( self ):
     f = open( 'Templates/topic_template.html', 'r' )
     template_page = f.read()
     f.close()

# Find the title
     mlist = module.listofmodules()
     modulemenu = mlist.getModuleMenu()
     outfilecontents = template_page.replace("INSERT TOPIC TITLE", self.label)
     outfilecontents = outfilecontents.replace("INSERT MODULE LIST", modulemenu)
     outfilecontents = outfilecontents.replace("INSERT LABEL TITLE", self.name)
# Find the description
     ifile = open( "Topics/" + self.name, 'r' )
     linesin = ifile.readlines()
     ifile.close()
     indesc=0
     foundend=0
     inlearn=0
     explanation = ""
     intro_table = ""
     exercise_table = ""
     external_table = "" 
     for line in linesin :
         if "DESCRIPTION:" in line :
            indesc=1
         elif "LEARNINGOUTCOMES:" in line :
            if indesc!=1 :
               sys.error("found LEARNINGOUTCOMES: before DESCRIPTION:")
            inlearn=1
            indesc=0
            explanation += "<H4> Learning outcomes </H4> \n"
            explanation += "<ul> \n"
         elif "END:" in line :
            if inlearn!=1 :
               sys.error("found END: before LEARNINGOUTCOMES:")
            inlearn=0
            foundend=1
            explanation += "</ul> \n" 
         elif indesc==1 :
            explanation += line
         elif (inlearn==1) & (line[0]=="-") :
            explanation += '<li type="square">' + line[1:] + '</li> \n' 
         elif (foundend==1) &  (len(line.split())>4) :
            if line.split()[0]!=self.name :
               sys.error("found dubious line in input file") 
            res = resource.resource(line)
            if res.loc=="INTRO" :
               intro_table += res.getResourceHTML( 1 )
            elif res.loc=="EXERCISE" :
               exercise_table += res.getResourceHTML( 1 )
            else :
               external_table += res.getResourceHTML( 0 ) 
     # And insert the tables into the html
     outfilecontents = outfilecontents.replace("INSERT INTRODUCTORY TABLE", intro_table)
     outfilecontents = outfilecontents.replace("INSERT EXERCISES TABLE", exercise_table)
     outfilecontents = outfilecontents.replace("INSERT EXTERNAL TABLE", external_table)
     # Write the html file
     ofile = open('html/' + self.name + '.html', 'w' )
     outfilecontents = outfilecontents.replace("INSERT FULL DESCRIPTION", explanation )
     ofile.write( outfilecontents )
     ofile.close()

  def getResourceForModule(self,modname,reslist):
    ifile = open( "Topics/" + self.name, 'r' )
    linesin = ifile.readlines()
    ifile.close()
    foundend=0
    intro_table = ""
    ex_table = ""
    for line in linesin :
        if (foundend==1) & (len(line.split())>4) :
           res = resource.resource(line)
           if res.linkb not in reslist :
              reslist.append(res.linkb)
              inmod=0
              for mm in res.module :
                  if mm==modname :
                     inmod=1
              if (inmod==1) & (res.loc=="INTRO") :
                 intro_table += res.getResourceHTML( 2 )
              elif (inmod==1) & (res.loc=="EXERCISE") :
                 ex_table += res.getResourceHTML( 2 )
        elif "END:" in line :
           foundend=1
    return intro_table + ex_table, reslist

class topiclist(object) :
  def __init__(self) :
     self.tlist = []
     self.labellist = []
     self.topiclist = os.listdir('Topics')
     for this in self.topiclist :
         # Make sure swap files are ignored 
         if not this.startswith('.') : 
            newtopic = topic( this )
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


