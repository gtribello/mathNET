import shutil
import topic
import basicgraph
import pageelements
import sys
import os
import subprocess
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

def createPortfolioMarkscheme( modname, tree ) :
    of = open( "latex/portfolio-assessment-" + modname +".tex", "w" )
    of.write("\\documentclass[a4paper]{article} \n")
    of.write("\\usepackage[margin=2.5cm,headheight=50pt,includeheadfoot]{geometry} \n")
    of.write("\\usepackage{amsfonts} \n")
    of.write("\\usepackage{amsmath} \n")
    of.write("\\usepackage{graphicx} \n")
    of.write("\\usepackage{fancyhdr} \n")
    of.write("\pagestyle{fancy} \n")
    of.write("\\renewcommand{\headrulewidth}{2pt} \n")
    of.write("\\usepackage{xcolor} \n")
    of.write("\\rhead{\includegraphics[width=5cm]{html/assets/img/logo.png}} \n")
    of.write("\lhead{\Huge Portfolio Marking: " + modname + "} \n")
    of.write("\\begin{document} \n")
    for elem in tree.findall("COMPONENT") :
        of.write("\\section{" + elem.find("TITLE").text + "} \n")
        of.write( elem.find("DESCRIPTION").text + "\n" )
        of.write("\\vspace{0.5cm}\n" )
        of.write("\\begin{tabular}{l | l | p{10 cm} } \n")
        of.write("{\\bf Classification } & {\\bf Range } & {\\bf Quality} \\\\ \\hline \n") 
        for mark in elem.findall("RANGE") :
            of.write( mark.find("CLASSIFICATION").text + "&" + mark.find("MARKS").text + "&" + mark.find("QUALITY").text + "\\\\[0.2cm]  \n" )  
        of.write("\\end{tabular} \n")
    of.write("\\end{document}")
    of.close() 
    # Run latex to generate pdf files
    cmd = ['pdflatex', '-interaction', 'nonstopmode', "latex/portfolio-assessment-" + modname + ".tex" ]
    proc = subprocess.Popen(cmd)
    proc.communicate()
    proc = subprocess.Popen(cmd)
    proc.communicate()
    shutil.copy( "portfolio-assessment-" + modname + ".pdf", "html/portfolio-assessment-" + modname + ".pdf" )
    if not proc.returncode == 0 :
       os.unlink( "latex/portfolio-assessment-" + modname + ".tex" )
       raise ValueError("Error compling latex markscheme for module " + modname )
    # Delete files we don't need after latex has run  
    for filen in os.listdir("."):
        if filen.startswith( "portfolio-assessment-" + modname ):
           os.remove(filen)




def buildModulePage( modn ):
    tree, mname = ET.parse( "Modules/" + modn ), modn.replace(".xml","")
    # Read in topics
    mytopics = topic.topiclist()
    # Create graph and setup the nodes
    mygraph = basicgraph.basicgraph()
    mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
    # Create the connections for the graph
    mygraph.setConnections()
    # Print overview page for module
    of = open( "html/" + mname + ".html", "w" ) 
    pageelements.printHeader( mname + " overview", of ) 
    pageelements.printTopMenuBar( of ) 
    of.write('<div id="content" class="container">\n')
    of.write('   <div class="row margin-vert-30">\n') 
    of.write('   <H2> ' + mname + ': ' + tree.find("TITLE").text + '</H2>')
    of.write('   <H3> Description </H3> <br/> ' )
    of.write( tree.find("DESCRIPTION").text )
    of.write('<br/> <br/>')
    of.write('   <H3> Portfolio projects </H3> <br/> ' )
    of.write('    <p>One aspect of the assessment of this module is a portfolio for which you must produce projects on the following: </p>')
    of.write('<ul>')
    n = 0
    for chp in tree.findall("CHAPTER") :
        n = n + 1  
        of.write('<li><a href="' + mname + str(n) + '-overview.html"> ' + chp.find("TITLE").text +  '</a></li>')
    of.write('</ul>')     
    of.write("<p>Details on how your final portfolio will be assessed can be found by clicking <b> <a href='portfolio-assessment-" + mname + ".pdf'> here </a> </b>.</p>")
    of.write('   </div>\n')
    of.write('</div>\n')
    pageelements.printFooter( of )
    of.close()
    createPortfolioMarkscheme( mname, tree.find("ASSESSMENT") )
    n, chapters = 0, tree.findall("CHAPTER")
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
        of.write('<br/>')
        intro = chp.find("INTRO")
        of.write( ET.tostring( intro.find("DESCRIPTION"), encoding="unicode", method="xml" ) )
        of.write('<h3> Aims </h3>')
        of.write( ET.tostring( intro.find("AIMS"), encoding="unicode", method="xml" ) ) 
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
        proj = chp.find("PROJECT")
        of.write('<br/>') 
        of.write('          <h3> ' + proj.find("TITLE").text + ' </h3>\n')
        of.write( ET.tostring( proj.find("DESCRIPTION"), encoding="unicode", method="xml" ) )
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
        of.write('fully expect you to take advantage of this rich information stream.  Some (brief) introductions to the python notebook system are provided below:')
        of.write('             </p>')
        of.write('<ul>')
        of.write('<li> Introductory videos on <a href="https://mediasite.qub.ac.uk/Mediasite/Play/2925f53ceaf642adb26817ec381b01b61d"> <b> running </b> </a> the notebook and <a href="https://mediasite.qub.ac.uk/Mediasite/Play/10d8830c389c4af89ba16e593aec70891d"> <b> writing </b> </a> in the notebook </li>') 
        of.write('<li> Introductory video on <a href="https://mediasite.qub.ac.uk/Mediasite/Play/3cbca07274744689aeaebd82b94060171d"> <b> writing equations </b> </a> with the notebook, notes on <a href="assets/notebook-writing.html"> <b> the markdown language </b> </a> you can use for writing plain text and <a href="https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf"> <b> a short summary </b> </a> of the key markdown commands. </li>') 
        of.write('<li> <a href="http://artofproblemsolving.com/wiki/index.php?title=LaTeX:Symbols"> <b> List of latex commands </b> </a> that can be used to typeset mathematical equations in the jupyter notebook system </li>')
        of.write('</ul>')
        of.write('<p> In addition the buttons below allow you to access resources on the python syntax for key programming concepts </p>') 
        of.write('<a href="http://introtopython.org/var_string_num.html" class="btn btn-primary">Variables</a> &nbsp;')
        of.write('<a href="https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Functions" type="button" class="btn btn-primary">Functions</a> &nbsp;')
        of.write('<a href="http://introtopython.org/if_statements.html" type="button" class="btn btn-primary">Logic</a> &nbsp;')
        of.write('<a href="http://introtopython.org/while_input.html" type="button" class="btn btn-primary">Loops</a> &nbsp;')
        of.write('<a href="http://introtopython.org/lists_tuples.html" type="button" class="btn btn-primary">Lists</a> &nbsp;')
        of.write('<a href="https://matplotlib.org/users/pyplot_tutorial.html" type="button" class="btn btn-primary">Graphs</a>')
        of.write('<p> If you would like to download the python notebook system onto your own laptop you can find it here:</p>')
        of.write('<a href="https://www.continuum.io/downloads"> https://www.continuum.io/downloads </a>')
        of.write('<p> There are some instructions on how to install it on your computer in <a href="https://mediasite.qub.ac.uk/Mediasite/Play/935be4295e7148dd91d6baf4cd2108281d"> <b> this video </b> </a> </p>')
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
        of.write('<button type="button" class="btn btn-primary">Variables</button> &nbsp;')
        of.write('<button type="button" class="btn btn-primary">Functions</button> &nbsp;')
        of.write('<button type="button" class="btn btn-primary">Logic</button> &nbsp;')
        of.write('<button type="button" class="btn btn-primary">Loops</button> &nbsp;')
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
    if len(sys.argv)==3 :
       os.chdir(sys.argv[2])
       buildModulePage( sys.argv[1] )
    else :
       print("wrong number of command line arguments expecting 2 found " + str(len(sys.argv)) + " " + str(sys.argv) )
