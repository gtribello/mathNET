import shutil
import topic
import basicgraph
import pageelements
import sys
import os   
import lxml.etree as ET

def buildTopicPage( tfile ):
    tree, tname = ET.parse( "Topics/" + tfile ), tfile.replace(".xml","")
    # Read in topics
    mytopics = topic.topiclist()
    # Create graph and setup the nodes
    mygraph = basicgraph.basicgraph()
    mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
    # Create the connections for the graph
    mygraph.setConnections()
    # Create the graph for this topic
    mygraph.printNodeGraph( tname )
    of = open( "html/" + tname + ".html", "w" ) 
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
    # Reading resources
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "READING", reslist, 1 )
    if len(reslist)>0  :
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-two", "Written Notes", content )
       content = "<table>\n"
       content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    # Videos
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "VIDEO", reslist, 1 )
    if len(reslist)>0 :
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-four", "Videos", content )
       content = "<table>\n"
       content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    # Examples
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "EXAMPLES", reslist, 1 )
    if len(reslist)>0 :
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-three", "Worked examples", content )
       content = "<table>\n"
       content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    # Blockly
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "BLOCKLY", reslist, 1 )
    if len(reslist)>0 :
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-five", "Applying your knowledge", content )
       content = "<table>\n"
       content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    # Python 
    reslist = []
    tstring, reslist = mytopics.get(tname).getRelevantResources( "", "PYTHON", reslist, 1 )
    if len(reslist)>0 : 
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-six", "Extending your understanding", content )
       content = "<table>\n"
       content += '<tr> <td width="2%"></td> <td width="10%"> </td> <td width="70%"> <h3> Description and link </h3> </td> <td width="10%"> <h3> Module </h3> </td> <td width="10%"> <h3> Author </h3> </td> </tr>'
    # External resources
    reslist = []
    if len(reslist)>0 :
       tstring, reslist = mytopics.get(tname).getRelevantResources( "", "EXTERNAL", reslist, 1 )
       content += tstring
       content += "</table>\n"
       pageelements.printPanel( of, "default", "collapse-seven", "External Resources", content )
       of.write('   </div>')
    # Print the footer
    of.write("</div>\n")
    pageelements.printFooter( of )
    of.close()

if __name__ == "__main__" :
    if len(sys.argv)==2 :
       buildTopicPage( sys.argv[1] )
    elif len(sys.argv)==3 :
       os.chdir(sys.argv[2])	
       buildTopicPage( sys.argv[1] )  
    else :
       print("wrong number of command line arguments expecting 2 found " + str(len(sys.argv)) + " " + str(sys.argv) )
