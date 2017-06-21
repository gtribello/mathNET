import os
import shutil
import topic
import subprocess
import xml_to_html
import lxml.etree as ET

class resource(object) :
  def __init__(self,tree) :
      self.author, self.linkb = tree.find("AUTHOR").text.strip().replace("~"," "), tree.find("LINK").text.strip()
      self.module, self.rtype = tree.findall("MODULE"), tree.find("TYPE").text.strip()
      self.loc, self.topic = tree.find("LEVEL").text.strip(), tree.find("TOPIC").text.strip()
      self.description = tree.find("DESCRIPTION").text.strip()

  def ofModAndLevel(self, module, level ) :
      if module=="" and level==self.loc : 
         return True
      else :
         for mod in self.module :
            if module==mod.text.strip() and level=="" :
               return True 
            elif module==mod.text.strip() and level==self.loc :
               return True
      return False

  def getResourceHTML(self,printmodule):
       table = "<tr> \n"
       if( self.rtype=="VIDEO" ): 
            assert( self.loc=="EXTERNAL" )
            table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td><td><a href="' + self.linkb + '" ><b>' + self.description + '</b></a></td>'
       elif( self.rtype=="WEBSITE" ):
            assert( self.loc=="EXTERNAL" )
            table += '<td></td><td><i class="fa fa-external-link fa-3x"></i></td><td><a href="' + self.linkb + '" ><b>' + self.description + '</b></a></td>'
       elif( self.rtype=="PDF" ):
            #if not os.path.isfile("html/resources/" + self.linkb):
            #   shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
            if printmodule==1 : 
               if( self.loc=="EXAMPLES"):
                   table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td>'
               else:
                   table += '<td></td><td><i class="fa fa-book fa-3x"></i></td>'
            table += '<td><a href="resources/' + self.linkb + '"><b>' + self.description + '</b></a></td>'
       elif( self.rtype=="LATEX" ):
            #if not os.path.isfile("html/resources" + self.linkb.replace(".tex",".pdf") ):
            #   cmd = ['pdflatex', '-interaction', 'nonstopmode', "Resources/" + self.linkb]
            #   proc = subprocess.Popen(cmd)
            #   proc.communicate()
            #   proc = subprocess.Popen(cmd)
            #   proc.communicate()
            #   #shutil.copy( self.linkb.replace(".tex",".pdf"), "html/resources/" + self.linkb.replace(".tex",".pdf") )                
            #   if not proc.returncode == 0 :
            #      os.unlink( self.linkb )
            #      raise ValueError("Error compling latex document entitled " + self.linkb)
            #   # Delete files we don't need after latex has run  
            #   for filen in os.listdir("."):
            #       if filen.startswith( self.linkb.replace(".tex","") ):
            #          os.remove(filen)

            if printmodule==1 :
               if( self.loc=="EXAMPLES"):
                   table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td>'
               else:
                   table += '<td></td><td><i class="fa fa-book fa-3x"></i></td>'

            table += '<td><a href="resources/' + self.linkb.replace(".tex",".pdf") + '"><b>' + self.description + '</b></a></td>'
       # elif( self.rtype=="IPYTHON"):
       #      assert( self.loc=="EXERCISE" )
       #      if not os.path.isfile("html/resources/" + self.linkb):
       #         shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
       #      table += '<td></td><td><i class="fa fa-laptop fa-3x"></i></td><td>' + '<a href="resources/' + self.linkb + '" download="' + self.linkb + '"> ' + self.description + '</a></td>'
       elif( self.rtype=="XML") :
            #if not os.path.isfile("html/" + self.linkb + ".html") :
                #xml_to_html.build_html_file( self.linkb )
            if printmodule==1 :
               if self.loc=="VIDEO" :
                   table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td>'
               elif self.loc=="EXAMPLES" :
                   table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td>' 
            table += '<td><a href="' + self.linkb + '.html"><b>' + self.description + '</b></a></td>' 
       elif( self.rtype=="HTML") :
            # assert( self.loc=="EXERCISE")
            # if not os.path.isfile("html/" + self.linkb + ".html") :
            #    shutil.copy("Resources/" + self.linkb + ".html", "html/" + self.linkb + ".html")
            if printmodule==1 :
               table += '<td></td><td><i class="fa fa-signal fa-3x"></i></td>'
            table += '<td><a href="' + self.linkb + '.html"><b>' + self.description + '</b></a></td>'
       elif( self.rtype=="GEOGEBRA"):
            if printmodule==1 :
               if( self.loc=="EXERCISE"):
               #    #if not os.path.isfile("html/" + self.linkb + ".html") :
               #       #xml_to_html.build_html_file( self.linkb )
                   table += '<td></td><td><i class="fa fa-signal fa-3x"></i></td>'
               else:
               #    #if not os.path.isfile("html/" + self.linkb + ".html") :
               #       #xml_to_html.build_html_file( self.linkb )
                   table += '<td></td><td><i class="fa fa-signal fa-3x"></i></td>'
            table += '<td><a href="' + self.linkb + '.html"><b>' + self.description + '</b></a></td>'


       if( printmodule==1 ):
            table += '<td>'
            for mod in self.module :
                table += '<a href="' + mod.text +'.html">' + mod.text + "</a>"
                if mod != self.module[-1] :
                   table += ' / '
            table += '</td> <td>' + self.author + "</td></tr> \n"
       elif( printmodule==2 ):
            mytopics = topic.topiclist()
            table += '</tr><tr><td> topic: <a href="' + self.topic +'.html">' + mytopics.get(self.topic).label + '</a></td></tr>'
            table += '<tr><td> author: ' + self.author  + '</td></tr>'
            #table += '<td><a href="' + self.topic +'.html">' + mytopics.get(self.topic).label + "</a></td>"

       # if ( self.loc!="EXTERNAL" ) :
       #      table += "<td>" + self.author + "</td>"
       # table += "</tr> \n"
       return table

