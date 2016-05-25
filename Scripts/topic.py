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

  def addResource(self,location,programming,module,resource_name,description):
     f = open("Topics/" + self.name, "w")
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
     f.write( self.name + " " + location + " " + programming + " " + module + " " + resource_name + " " +  description + "\n" )
     f.close()
     printTopicPage( self )
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
     indesc=0
     foundend=0
     explanation = ""
     intro_table = ""
     exercise_table = ""
     external_table = "" 
     for line in linesin :
         if "DESCRIPTION:" in line :
            indesc=1
         elif "END:" in line :
            if indesc!=1 :
               sys.error("found END: before DESCRIPTION:")
            indesc=0
            foundend=1
         elif indesc==1 :
            explanation += line
         elif( foundend==1 ):
            if len(line.split())>4 :
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

class topiclist(object) :
  def __init__(self) :
     self.tlist = []
     self.labellist = []
     self.topiclist = os.listdir('Topics')
     for this in self.topiclist :
         newtopic = topic( this )
         newtopic.readName()
         self.labellist.append( newtopic.label )
         self.tlist.append( newtopic )

  def get( self, name ) :
     ind=self.topiclist.index(name)
     return self.tlist[ind]

