import os
import shutil
import topic
import subprocess
import xml_to_html

class resource(object) :
  def __init__(self,description) :
       dlist=description.split()
       self.author=dlist[5].replace("~"," ") # The author of the resource
       del dlist[5] 
       self.linkb=dlist[4]  # The actual web link you are using
       del dlist[4]
       self.module=dlist[3].split("/")
       del dlist[3]
       self.rtype=dlist[2] # What kind of resource is this video etc
       del dlist[2] 
       self.loc=dlist[1]    # Is this an exercise or notes
       del dlist[1]
       self.topic=dlist[0]  # What topic should this be filed under
       del dlist[0]
       self.description=" ".join(dlist)

  def getResourceHTML(self,printmodule):
       table = "<tr> \n"
       if( self.rtype=="VIDEO" ): 
            assert( self.loc=="EXTERNAL" )
            table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td><td><a href="' + self.linkb + '" >' + self.description + '</a></td>'
       elif( self.rtype=="WEBSITE" ):
            assert( self.loc=="EXTERNAL" )
            table += '<td></td><td><i class="fa fa-external-link fa-3x"></i></td><td><a href="' + self.linkb + '" >' + self.description + '</a></td>'
       elif( self.rtype=="PDF" ):
            if not os.path.isfile("html/resources/" + self.linkb):
               shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
            if( self.loc=="EXERCISE"):
                table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td><td>'
            else:
                assert( self.loc=="INTRO" ) 
                table += '<td></td><td><i class="fa fa-book fa-3x"></i></td><td>'

            table += '<a href="resources/' + self.linkb + '">' + self.description + '</a></td>'
       elif( self.rtype=="LATEX" ):
            if not os.path.isfile("html/resources" + self.linkb.replace(".tex",".pdf") ):
               cmd = ['pdflatex', '-interaction', 'nonstopmode', "Resources/" + self.linkb]
               proc = subprocess.Popen(cmd)
               proc.communicate()
               proc = subprocess.Popen(cmd)
               proc.communicate()
               shutil.copy( self.linkb.replace(".tex",".pdf"), "html/resources/" + self.linkb.replace(".tex",".pdf") )                
               if not proc.returncode == 0 :
                  os.unlink( self.linkb )
                  raise ValueError("Error compling latex document entitled " + self.linkb)
               # Delete files we don't need after latex has run  
               for filen in os.listdir("."):
                   if filen.startswith( self.linkb.replace(".tex","") ):
                      os.remove(filen)

            if( self.loc=="EXERCISE"):
                table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td><td>'
            else:
                assert( self.loc=="INTRO" )
                table += '<td></td><td><i class="fa fa-book fa-3x"></i></td><td>'

            table += '<a href="resources/' + self.linkb.replace(".tex",".pdf") + '">' + self.description + '</a></td>'
       elif( self.rtype=="IPYTHON"):
            assert( self.loc=="EXERCISE" )
            if not os.path.isfile("html/resources/" + self.linkb):
               shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
            table += '<td></td><td><i class="fa fa-laptop fa-3x"></i></td><td>' + '<a href="resources/' + self.linkb + '" download="' + self.linkb + '"> ' + self.description + '</a></td>'
       elif( self.rtype=="XML") :
            if not os.path.isfile("html/" + self.linkb + ".html") :
                xml_to_html.build_html_file( self.linkb )
            if self.loc=="INTRO" :
                table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td><td>'
            else :
                table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td><td>' 
            table += '<a href="' + self.linkb + '.html">' + self.description + '</a></td>' 
       elif( self.rtype=="GEOGEBRA"):
            if( self.loc=="EXERCISE"):
                if not os.path.isfile("html/" + self.linkb + ".html") :
                   xml_to_html.build_html_file( self.linkb )
                table += '<td></td><td><i class="fa fa-signal fa-3x"></i></td><td>'
            else:
                assert( self.loc=="INTRO" )
                if not os.path.isfile("html/" + self.linkb + ".html") :
                   xml_to_html.build_html_file( self.linkb )
                table += '<td></td><td><i class="fa fa-signal fa-3x"></i></td><td>'

            table += '<a href="' + self.linkb + '.html">' + self.description + '</a></td>'


       if( printmodule==1 ):
            table += '<td>'
            for mod in self.module :
                table += '<a href="' + mod +'.html">' + mod + "</a>"
                if mod != self.module[-1] :
                   table += ' / '
            table += '</td>'
       elif( printmodule==2 ):
            mytopics = topic.topiclist()
            table += '<td><a href="' + self.topic +'.html">' + mytopics.get(self.topic).label + "</a></td>"

       if ( self.loc!="EXTERNAL" ) :
            table += "<td>" + self.author + "</td>"
       table += "</tr> \n"
       return table

