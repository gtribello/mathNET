import os
import sys
import topic
import shutil
import basicgraph
import pageelements

of = open("html/index.html", "w" )
pageelements.printHeader( "mathnet", of )
pageelements.printTopMenuBar( of )
of.write('<div id="content" class="container">\n')
of.write('   <div class="row margin-vert-30">\n')
of.write('<h2> Our Philosophy </h2> \n')
of.write('<p> Mathematics is a language which uses a hierarchy of abstract objects to express meaning.  In other words, it is a language and like any language the best way of learning it')
of.write(' is not to sit in a room listening to someone else talk it but rather to try to use it.  The modules that are on this website embrace this way of teaching maths.  The heart of ')
of.write(' each module is a set of short projects that you can work through.  To help you do these projects you will find short videos that explain the key ideas that you will need ')
of.write(' together with practise questions and exercises that should help you build up to the project.  Furthermore, to help you we try throughout to illustrate the connections between sub topics using ')
of.write(' graphs like the one below. </p>')
of.write('<h2> Graph of connections </h2>\n')
of.write('<!-- Main Text -->\n')
of.write('<object data="main.svg" type="image/svg+xml" width="100%"> </object>\n')
of.write('   </div>\n')
of.write('</div>\n')
pageelements.printFooter( of )
mytopics = topic.topiclist()
mygraph = basicgraph.basicgraph()
mygraph.setNodes(mytopics.topiclist, mytopics.labellist)
mygraph.setConnections()
mygraph.printFullGraph("main")
of.close()
