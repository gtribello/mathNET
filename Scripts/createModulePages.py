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

def createLiturgy( modname, tree ) :
   of = open( "latex/essential-ideas-" + modname +".tex", "w" )
   of.write("\\documentclass[a4paper]{article}") 
   of.write("\\usepackage{tcolorbox}")
   of.write("\\usepackage{amsmath,amssymb,amsfonts}")
   of.write("\\tcbuselibrary{skins}")
   of.write("\\title{")
   of.write("\\vspace{-3em}")
   of.write("\\begin{tcolorbox}")
   of.write("\\Huge\\sffamily Key Ideas : " + modname )   
   of.write("\\end{tcolorbox}")
   of.write("\\vspace{-3em}")
   of.write("}")
   of.write("\\date{}")
   of.write("\\usepackage{background}")
   of.write("\\SetBgScale{1}")
   of.write("\\SetBgAngle{0}")
   of.write("\\SetBgColor{red}")
   #of.write("\\SetBgContents{\\rule[0em]{0pt}{\\textheight}}")
   of.write("\\SetBgHshift{-2.3cm}")
   of.write("\\SetBgVshift{0cm}")
   of.write("\\usepackage[margin=1.5cm]{geometry}")
   of.write("\\makeatletter")
   of.write("\\def\cornell{\@ifnextchar[{\@with}{\@without}}")
   of.write("\\def\@with[#1]#2#3{")
   of.write("\\begin{tcolorbox}[enhanced,colback=white!15,colframe=white,colupper=gray]")
   of.write("\\begin{tcolorbox}[enhanced,colback=gray,colframe=black,fonttitle=\\large\\bfseries\\sffamily,sidebyside=false, nobeforeafter,colupper=black,sidebyside align=top,opacityframe=0,opacityback=0.3,opacitybacktitle=1, opacitytext=1,segmentation style={black!55,solid,opacity=0,line width=1pt},title=#1]")
   of.write("#3")
   of.write("\\end{tcolorbox}")
   of.write("\\end{tcolorbox}")
   of.write("}")
   of.write("\\def\\@without#1#2{")
   of.write("\\begin{tcolorbox}[enhanced,colback=white!15,colframe=white,fonttitle=\\bfseries,sidebyside=true, nobeforeafter,before=\\vfil,after=\\vfil,colupper=blue,sidebyside align=top, lefthand width=.20\\textwidth, opacityframe=0,opacityback=0,opacitybacktitle=0, opacitytext=1, segmentation style={black!55,solid,opacity=0,line width=3pt} ]")
   of.write("\\begin{tcolorbox}[colback=red!05,colframe=red!25,sidebyside align=top, width=\\textwidth,nobeforeafter]#1\end{tcolorbox}")
   of.write("\\tcblower")
   of.write("\\sffamily")
   of.write("\\begin{tcolorbox}[colback=blue!05,colframe=blue!10,width=1\\textwidth,nobeforeafter]")
   of.write("#2")
   of.write("\\end{tcolorbox}")
   of.write("\\end{tcolorbox}")
   of.write("}")
   of.write("\\makeatother")
   of.write("\\parindent=0pt")
   of.write("\\providecommand{\LyX}{L\kern-.1667em\lower.25em\hbox{Y}\kern-.125emX\@}")
   of.write("\\begin{document}") 
   of.write("\\maketitle \n")
   of.write("The baloons below contain many of the important ideas and theorems that are covered in this module.  If you have a good understanding of what ")
   of.write("everything on this sheet means then you have a good understanding of the module content.  I would recommend that you stick these sheets in the ")
   of.write("first few pages of the hardback book that you keep your notes inside and that you consult these notes regularly as you work through the module.")
   for item in tree.findall("ITEM") :
       of.write("\\cornell{" + item.find("CALL").text + "}{" + item.find("RESPONSE").text.replace("&lt;","<").replace("&gt;",">") + "}")
   of.write("\\end{document}")
   of.close()
   # Run latex to generate pdf files
   pageelements.create_pdf_from_latex( "essential-ideas-" + modname  )

def createWorkloadModel( modname, tree ) :
    of = open( "latex/workload-model-" + modname +".tex", "w" )
    of.write("\\documentclass[a4paper]{article} \n")
    of.write("\\usepackage[margin=2.5cm,headheight=50pt,includeheadfoot]{geometry} \n")
    of.write("\\usepackage{amsfonts} \n")
    of.write("\\usepackage{amsmath} \n")
    of.write("\\usepackage{graphicx} \n")
    of.write("\\usepackage{fancyhdr} \n")
    of.write("\\pagestyle{fancy} \n")
    of.write("\\renewcommand{\headrulewidth}{2pt} \n")
    of.write("\\usepackage{xcolor} \n")
    of.write("\\rhead{\includegraphics[width=5cm]{html/assets/img/logo.png}} \n")
    of.write("\\lhead{\Huge Weekly workload: " + modname + "} \n") 
    of.write("\\begin{document} \n")
    of.write("At the start of the semster you should buy yourself a hardback notebook to keep your notes inside.  Stick the pages of this guide into the first few ")
    of.write("pages of your notebook " )
    of.write("and {\\bf make sure that you bring your notebook to all classes and tutorials}.  Similarly buy a usb memory key or create a folder on a cloud service such as ")
    of.write("google drive or dropbox and use this to store all the word processed reports and python notebooks that you write for this module together with the feedback ")
    of.write("I provide on these assignments.  If you have a laptop or tablet please feel free to bring it to all tutorials, lectures and computer classes. If you have this with ")
    of.write("you it will allow you to access the resources on my website and other online resources.\n \n")
    of.write("All the reports that you hand in to be assessed for this module should:")
    of.write("\\begin{itemize} \n")
    of.write("\\item Have your name written in the top right corner of the first page - if your name is not written on your assignment you will be awarded a mark of zero.\n")
    of.write("\\item Be word processed - hand written assignments will be awarded a mark of zero.\n")
    of.write("\\item Be free of spelling errors and basic grammatical errors - use a spell checker and/or a grammar checker (see www.grammarly.com for a free grammar checker) \n")
    of.write("\\end{itemize} \n")
    of.write( modname + " is a 20 CAT point module and as such you are expected to work for 200 hours on this module.  Over the course of twelve week semester this works out at")
    of.write(" about 16 hours per week.  Subtracting from this the five contact hours a week you have for this module leaves 11 hours per week that you are")
    of.write(" expected to spend doing self study for this module.  The following sections detail what I recommend you spend those 11 hours in each week working on. ")
    of.write("Lastly, notice that the conceptual equivalents for a 2.1 at level 3 state that your work must provide:")
    of.write("\\begin{quotation}\n")
    of.write("Synthesis/integration of material from other modules/experience as well as the current module, well-developed arguments with evidence of independent thought and evidence of wide and relevant use of learning resources")
    of.write("\\end{quotation}\n")
    of.write("This is thus the main thing I am looking for when I mark the portfolio and report assignments for this module. \n")
    of.write("The assessment for this module includes the following components: \n")
    of.write("\\begin{itemize} \n")
    for elem in tree.findall("ASSESSMENT") :
        of.write( "\item " + elem.find("DESCRIPTION").text + ", which counts " + elem.find("WEIGHT").text + " towards you final module mark and which is due in at " + elem.find("WHEN").text + "\n")
    of.write("\\end{itemize} \n \clearpage \n")
    of.write("A recommended work plan for the weeks that follow is given on the following pages\n")
    n = 1
    for elem in tree.findall("WEEK") :
        of.write("\\subsection*{Week " + str(n) + "}" )
        of.write( elem.find("TRY").text )
        of.write("\\paragraph{What we will be doing in the tutorial:}")
        of.write( elem.find("TUTORIAL").text )
        of.write("\\paragraph{What work should I be handing in this week:}")
        for task in elem.findall("HANDIN") :
            of.write( task.find("ITEM").text + ", which is due on " + task.find("DUE").text + ". " ) 
        n += 1
    of.write("\\end{document}")
    of.close()
    # Run latex to generate pdf files
    pageelements.create_pdf_from_latex( "workload-model-" + modname )

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
    of.write( tree.find("DESCRIPTION").text + "\n" )
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
    pageelements.create_pdf_from_latex( "portfolio-assessment-" + modname )


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
    if tree.find("ASSESSMENT") :
       of.write('   <H3> Assessment </H3> <br/> ' )
       of.write('   <p>The module assessment consists of the following activities:</p>')
       of.write("   <table> \n")
       of.write("<tr><td><b> item </b></td><td><b> due date </b></td><td><b>weight</b></td></tr>")
       for assessment in tree.find("HANDBOOK").findall("ASSESSMENT") :
           of.write("<tr><td>" + assessment.find("DESCRIPTION").text + "</td><td>" + assessment.find("WHEN").text + "</td><td>" + assessment.find("WEIGHT").text + "</td></tr>") 
       of.write("   </table> </br>\n")
       of.write("   <p>Details on what you are expected to work on during each week of the semester can be found by clicking <b><a href='workload-model-" + mname + ".pdf'> here </a> </b>.</p>")
    if tree.find("LITURGY") : 
       of.write("   <p>A summary of some of the key ideas and theorems that are introduced in this module can be found by clicking <b><a href='essential-ideas-" + mname + ".pdf'> here </a> </b>.</p>")
    if tree.find("PORTFOLIO") :
       of.write('   <H3> Portfolio projects </H3> <br/> ' )
       of.write('    <p>The final aspect of the assessment for this module is a portfolio for which you must produce projects on the following: </p>')
    of.write('<ul>')
    n = 0
    for chp in tree.findall("CHAPTER") :
        n = n + 1  
        of.write('<li><a href="' + mname + str(n) + '-overview.html"> ' + chp.find("TITLE").text +  '</a></li>')
    of.write('</ul>') 
    if tree.find("PORTFOLIO") :    
       of.write("<p>Details on how your final portfolio will be assessed can be found by clicking <b> <a href='portfolio-assessment-" + mname + ".pdf'> here </a> </b>.</p>")
       of.write("<p>Some questions to think about when writing your weekly reports can be found by clicking <b> <a href='resources/reflective-questions.pdf'> here </a> </b>.</p>")
    of.write('   </div>\n')
    of.write('</div>\n')
    # Run latex to generate pdf files
    pageelements.printFooter( of )
    of.close()
    if tree.find("HANDBOOK") : createWorkloadModel( mname, tree.find("HANDBOOK") )
    if tree.find("PORTFOLIO") : createPortfolioMarkscheme( mname, tree.find("PORTFOLIO") )
    if tree.find("LITURGY") : createLiturgy( mname, tree.find("LITURGY") )
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
        of.write('<a href="https://www.youtube.com/watch?v=qS8ROcnjdpg" class="btn btn-primary">Variables</a> &nbsp;')
        of.write('<a href="https://www.youtube.com/watch?v=gB6Gt7CmPyw" class="btn btn-primary">Functions</a> &nbsp;')
        of.write('<a href="https://www.youtube.com/watch?v=FjPDd0yE90M&t=63s" class="btn btn-primary">Logic</a> &nbsp;')
        of.write('<a href="https://www.youtube.com/watch?v=Te0ysSD4_M8" class="btn btn-primary">Loops</a> &nbsp;')
        of.write('<a href="https://www.youtube.com/watch?v=qozgSqeGdV4" class="btn btn-primary">Lists</button>')
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
