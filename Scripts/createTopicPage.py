import shutil
import topic
import basicgraph
import pageelements
import sys
import os   
import lxml.etree as ET

def buildTopicPage( tname ):
    tree = ET.parse( "Topics/" + tname + ".xml" ) 
    # Read in topics
    mytopics = topic.topiclist()
    # Create graph and setup the nodes
    mygraph = basicgraph.basicgraph()
    mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
    # Create the connections for the graph
    mygraph.setConnections()
    of = open( "html/" + tname + ".html", "a" ) 
    # Print header and top menu bar for this page
    pageelements.printHeader( tname, of )
    pageelements.printTopMenuBar( of )
    of.write('<div id="content" class="container">\n')
    of.write('   <div class="panel panel-blue">\n')
    of.write('       <div class="panel-heading">\n')
    of.write('           <h1 class="panel-title"> ' + tree.find("TITLE").text + ' </h1>\n')
    of.write('       </div>\n')
    of.write('   </div>\n')
    content =  '<div class="col-md-7">'
    content += '<h3 class="no-margin no-padding">' + tree.find("TITLE").text + '</h3>'
    content += '<p align="justify">' + tree.find("DESCRIPTION").text + '</p>'
    content += "<H4> Syllabus Aims </H4> \n" 
    content += ET.tostring( tree.find("AIMS"), encoding="unicode", method="xml" )
    content += '</div>'
    content += '<div class="col-md-5"><object data="' + tname + '.svg" type="image/svg+xml" width="100%"></object></div>'
    pageelements.printPanel( of, "primary", "collapse-one", "Short description and context", content )
    of.write('   <div id="accordion" class="panel-group">')
    content = "<table>\n"
    content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "INTRO", reslist )
    content += tstring
    content += "</table>\n"
    pageelements.printPanel( of, "default", "collapse-two", "Introductory Material", content )
    content = "<table>\n"
    content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "EXERCISE", reslist )
    content += tstring
    content += "</table>\n"
    pageelements.printPanel( of, "default", "collapse-three", "Exercises", content )
    content = "<table>\n"
    content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> </tr>'
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "EXTERNAL", reslist )
    content += tstring
    content += "</table>\n"
    pageelements.printPanel( of, "default", "collapse-four", "External Resources", content )
    of.write('   </div>')
    # Print the footer
    of.write("</div>\n")
    pageelements.printFooter( of )
    of.close()

if __name__ == "__main__" :
    if len(sys.argv)==2 :
       buildTopicPage( sys.argv[1] )
    else :
       print("wrong number of command line arguments expecting 2 found " + str(len(sys.argv)) + " " + str(sys.argv) )
