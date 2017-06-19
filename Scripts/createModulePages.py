import shutil
import topic
import basicgraph
import pageelements
import sys
import os
import lxml.etree as ET

def printModuleSidebar( modname, of ):
    of.write('<div class="col-md-2">\n')
    of.write('   <ul class="list-group sidebar-nav" id="sidebar-nav">\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-overview.html">Overview</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-fproject.html">Final project</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-practise.html">Extend</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-apply.html">Apply</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-examples.html">Examples</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-understand.html">Understand</a></li>\n')
    of.write('      <li class="list-group-item"><a href="' + modname + '-content.html">Content</a></li>\n')
    of.write('   </ul>')
    of.write('</div>')


def buildModulePage( mname ):
    tree = ET.parse( "Modules/" + mname + ".xml" )  
    n, chapters = 0, tree.findall("CHAPTER")
    # Read in topics
    mytopics = topic.topiclist()
    # Create graph and setup the nodes
    mygraph = basicgraph.basicgraph()
    mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
    # Create the connections for the graph
    mygraph.setConnections()
    for chp in chapters :
        n = n + 1
        modname, chp_topics_t, chp_topics = mname + str(n), chp.findall("TOPIC"), []
        for tp in chp_topics_t : chp_topics.append( tp.text.strip() )
        # Print overview page for this project
        of = open( "html/" + modname + "-overview.html", "w" )
        pageelements.printHeader( modname + " overview", of ) 
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of )
        of.write('      <div class="col-md-10">\n')
        of.write('         <h2> Overview: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of )
        of.close()
        # Print final project page for this project
        of = open( "html/" + modname + "-fproject.html", "w" )
        pageelements.printHeader( modname + " overview", of )
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of ) 
        of.write('      <div class="col-md-10">\n')
        of.write('         <h2> Final project: ' + chp.find("TITLE").text + '  </h2>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n') 
        pageelements.printFooter( of ) 
        of.close()
        # Print practise exercises for this project
        of = open( "html/" + modname + "-practise.html", "w" )
        pageelements.printHeader( modname + " overview", of ) 
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of ) 
        of.write('      <div class="col-md-6">\n')
        of.write('         <h2> Practise projects: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('             <p>')
        of.write('The panel on the right of this page contains links to some more challenging programming exercises that require you to use the material that is covered in this ')
        of.write('chapter.  You are strongly encouraged to create a new python notebook for each of the problems listed here that you attempt.  Put all the code you write and the ')
        of.write('explanations of the mathematical ideas you use in the notebook. Please note that there is an enormous ammount of information about python available online and we ')
        of.write('fully expect you to take advantage of this rich information stream.  Some (brief) introductions to the python notebook system and python programming in general are ')
        of.write('provided below, however:')
        of.write('             </p>')
        of.write('<p> If you would like to download the python notebook system onto your own laptop you can find it here:</p>')
        of.write('<a href="https://www.continuum.io/downloads"> https://www.continuum.io/downloads </a>')
        of.write('      </div>\n')
        of.write('      <div class="col-md-4">\n')
        of.write('<table>\n')
        #of.write('<tr> <td width="2%"></td> <td width="10%"> </td> <td width="50%"> <h4> Description </h4> </td> <td width="15%"> <h4> Topic </h4> </td> <td> <h4> Author </h4> </td> </tr>\n')
        reslist, topictab  = [], ""
        for top in chp_topics :
            tstring, reslis = mytopics.get(top).getRelevantResources( mname, "PYTHON", reslist, 2 )
            topictab += tstring
        of.write( topictab )
        of.write('</table>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of ) 
        of.close()
        # Print apply page for this project
        of = open( "html/" + modname + "-apply.html", "w" )
        pageelements.printHeader( modname + " overview", of ) 
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of ) 
        of.write('      <div class="col-md-6">\n')
        of.write('         <h2> Applying your knowledge: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('             <p>')
        of.write('The panel on the right of this page contains links to some programming exercises that require you to use the material that is covered in this chapter.  ')
        of.write('You will use a simple programming language called blockly to do these exercises.  These activites should allow you to implement the logical structure of the ')
        of.write('mathematical concepts that have been introduced in the videos and notes on these topics.  Each exercise consists of a number of levels and for each level you ')
        of.write('have a task to complete.  To complete these levels you will need to use some or all of the following five basic concepts:') 
        of.write('             </p>') 
        of.write('<button type="button" class="btn btn-primary">Variables</button>')
        of.write('<button type="button" class="btn btn-primary">Functions</button>')
        of.write('<button type="button" class="btn btn-primary">Logic</button>')
        of.write('<button type="button" class="btn btn-primary">Loops</button>')
        of.write('<button type="button" class="btn btn-primary">Lists</button>')
        of.write('      </div>\n')
        of.write('      <div class="col-md-4">\n')
        of.write('<table>\n')
        #of.write('<tr> <td width="2%"></td> <td width="10%"> </td> <td width="50%"> <h4> Description </h4> </td> <td width="15%"> <h4> Topic </h4> </td> <td> <h4> Author </h4> </td> </tr>\n')
        reslist, topictab  = [], ""
        for top in chp_topics :
            tstring, reslis = mytopics.get(top).getRelevantResources( mname, "BLOCKLY", reslist, 2 )
            topictab += tstring
        of.write( topictab )
        of.write('</table>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of ) 
        of.close()
        # Print examples page for this project
        of = open( "html/" + modname + "-examples.html", "w" )
        pageelements.printHeader( modname + " overview", of )
        pageelements.printTopMenuBar( of )
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of )
        of.write('      <div class="col-md-6">\n')
        of.write('         <h2> Applying your knowledge: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('             <p>')
        of.write('The panel on the right of this page contains links to some example problems that have been solved using the material that is covered in this chapter.  ')
        of.write('You will find the problems and the solutions together on these pages.  However, please try to solve the problem yourself before you consult the solution.')
        of.write('             </p>')
        of.write('      </div>\n')
        of.write('      <div class="col-md-4">\n')
        of.write('<table>\n')
        #of.write('<tr> <td width="2%"></td> <td width="10%"> </td> <td width="50%"> <h4> Description </h4> </td> <td width="15%"> <h4> Topic </h4> </td> <td> <h4> Author </h4> </td> </tr>\n')
        reslist, topictab  = [], ""
        for top in chp_topics :
            tstring, reslis = mytopics.get(top).getRelevantResources( mname, "EXAMPLES", reslist, 2 )
            topictab += tstring
        of.write( topictab )
        of.write('</table>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of )
        of.close()
        # Print understand page for this project
        of = open( "html/" + modname + "-understand.html", "w" )
        pageelements.printHeader( modname + " overview", of ) 
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of ) 
        of.write('      <div class="col-md-6">\n')
        of.write('         <h2> Understanding the content: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('           <p>') 
        of.write('The panel on the right of this page contains links to videos on the topics we are studying as part of this chapter.  ')
        of.write('On the pages for each of these videos you will find a link to a worksheet containing comprehension questions.  You should ')
        of.write('print out the comprehension questions, watch the video and try to answer the comprehension questions based on the ideas that are explained ')
        of.write('in the video.  If you are struggling to answer any question please come and ask.'); 
        of.write('           </p>')                
        of.write('      </div>\n')
        of.write('      <div class="col-md-4">\n')
        of.write('<table>\n')
        #of.write('<tr> <td width="2%"></td> <td width="10%"> </td> <td width="50%"> <h4> Description </h4> </td> <td width="15%"> <h4> Topic </h4> </td> <td> <h4> Author </h4> </td> </tr>\n')
        reslist, topictab  = [], ""
        for top in chp_topics :
            tstring, reslis = mytopics.get(top).getRelevantResources( mname, "VIDEO", reslist, 2 )
            topictab += tstring
        of.write( topictab )
        of.write('</table>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of ) 
        of.close()
        # Print content page for this project
        of = open( "html/" + modname + "-content.html", "w" )
        pageelements.printHeader( modname + " overview", of )
        pageelements.printTopMenuBar( of ) 
        of.write('<div id="content" class="container">\n')
        of.write('   <div class="row margin-vert-30">\n')
        printModuleSidebar( modname, of ) 
        of.write('      <div class="col-md-6">\n')
        of.write('         <h2> Chapter content: ' + chp.find("TITLE").text + '</h2>\n')
        of.write('           <p>')
        of.write('A diagram illustrating the topics you will need to understand for this chapter together with the connections between topics is given below. ')
        of.write('Written notes on these various topics can be found be clicking on the links in the right panel.')
        of.write('      <br/><br/>\n')
        mygraph.printChapterGraph( chp_topics, modname )
        of.write('<object data="' + modname + '.svg" type="image/svg+xml" width="100%"></object>\n')
        of.write('      </div>\n')
        of.write('      <div class="col-md-4">\n')
        of.write('<table>\n')
        #of.write('<tr> <td width="2%"></td> <td width="10%"> </td> <td width="50%"> <h4> Description </h4> </td> <td width="15%"> <h4> Topic </h4> </td> <td> <h4> Author </h4> </td> </tr>\n')
        reslist, topictab  = [], ""
        for top in chp_topics : 
            tstring, reslis = mytopics.get(top).getRelevantResources( mname, "READING", reslist, 2 )
            topictab += tstring
        of.write( topictab )
        of.write('</table>\n')
        of.write('      </div>\n')
        of.write('   </div>\n')
        of.write('</div>\n')
        pageelements.printFooter( of ) 
        of.close() 


if __name__ == "__main__" :
    if len(sys.argv)==2 :
       buildModulePage( sys.argv[1] ) 
    else :
       print("wrong number of command line arguments expecting 2 found " + str(len(sys.argv)) + " " + str(sys.argv) )
