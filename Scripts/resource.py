import os
import shutil
import generate_html_exercise

class resource(object) :
  def __init__(self,description) :
       dlist=description.split()
       self.linkb=dlist[4]  # The actual web link you are using
       del dlist[4]
       self.module=dlist[3] # What module should this come under
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
            table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td><td><a href="' + self.linkb + '" >' + self.description + '</a></td>'
       elif( self.rtype=="WEBSITE" ):
            table += '<td></td><td><i class="fa fa-external-link fa-3x"></i></td><td><a href="' + self.linkb + '" >' + self.description + '</a></td>'
       elif( self.rtype=="PDF" ):
            if not os.path.isfile("html/resources/" + self.linkb):
               shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
            if( self.loc=="EXERCISE"):
                table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td><td>'
            else:
                table += '<td></td><td><i class="fa fa-book fa-3x"></i></td><td>'

            table += '<a href="resources/' + self.linkb + '">' + self.description + '</a></td>'
       elif( self.rtype=="IPYTHON"):
            if not os.path.isfile("html/resources/" + self.linkb):
               shutil.copy("Resources/" + self.linkb, "html/resources/" + self.linkb)
            table += '<td></td><td><i class="fa fa-laptop fa-3x"></i></td><td>' + '<a href="resources/' + self.linkb + '" download="' + self.linkb + '"> ' + self.description + '</a></td>'
       elif( self.rtype=="HTML"):
            generate_html_exercise.convert_exercise_to_html( self.linkb )
            if( self.loc=="EXERCISE"):
                table += '<td></td><td><i class="fa fa-pencil fa-3x"></i></td><td>'
            else:
                table += '<td></td><td><i class="fa fa-video-camera fa-3x"></i></td><td>'

            table += '<a href="' + self.linkb + '.html">' + self.description + '</a></td>'

       if( printmodule>0 ):
            table += '<td><a href="' + self.module +'.html">' + self.module + "</a></td>"    # Ideally this would be a link to the module

       table += "</tr> \n"
       return table

