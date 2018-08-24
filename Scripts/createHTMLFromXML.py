# -*- coding: utf-8 -*-
import os
import sys
import shutil
import pageelements
import subprocess
import lxml.etree as ET

def createVideoPage( ftype, name, tree, of ) :
    of.write('<div id="content" class="container">')
    of.write('   <div class="panel panel-blue">')
    of.write('     <div class="panel-heading">')
    of.write('         <div class="row">')
    of.write('            <div class="col-md-8">')
    title = tree.find('TITLE').text + ' : Introductory video'
    if ftype=="geogebra" :
       title = tree.find('TITLE').text + ' : Geogebra exercise'
    of.write('               <h1 class="panel-title">' +  title + '</h1>') 
    of.write('            </div>')
    of.write('            <div class="col-md-4" align="right">')
    of.write('               <a href="' + name.replace(".xml",".pdf") + '" class="btn btn-primary btn-lg active" role="button"> Get worksheet </a>')
    of.write('            </div>')
    of.write('         </div>') 
    of.write('     </div>')
    of.write('   </div>')
    of.write('   <div class="row margin-vert-30">')
    of.write('      <div class="panel panel-primary">')
    of.write('         <div class="panel-heading">')
    of.write('            <h4 class="panel-title">')
    text = 'Before watching the video read the questions below.  As you watch the video try to answer them'
    if ftype=="geogebra" :
       text = "Try to answer the questions below by reading the description and adjusting the geogebra plot" 
    of.write(text)
    of.write('            </h4>')
    of.write('         </div>')
    of.write('         <div class="panel-body">')
    of.write('            <div class="row">')
    of.write('                <p align="center">')
    if ftype=="video" :
       of.write('<iframe width="630" height="472" src="' + tree.find("VIDEO").text + '" frameborder="0" allowfullscreen></iframe>')
    elif ftype=="geogebra" :
       of.write('<center> <iframe scrolling="no" src="' + tree.find("GEOGEBRA").text + '" width="960px" height="450px" style="border:0px;"> </iframe> </center>')
    of.write('                </p>')
    if ftype=="geogebra" :
       of.write('<h1> Description </h3>')
       of.write( tree.find("DESCRIPTION").text )
    of.write('<h1> Questions </h3>')
    of.write('                <ul>')
    of.write( ET.tostring( tree.find("UL"), encoding="unicode", method="xml") )
    of.write('                </ul>')
    of.write('            </div>')
    of.write('         </div>')
    of.write('      </div>')
    of.write('   </div>')
    of.write('</div>')
# And build latex
    generate_pdf_worksheet( tree, name.replace(".xml","") )

def createBlocklyPage( name, tree, of ) :
   # Create modal objects to hold pop up videos
   n = 0
   for lev in tree.findall("LEVEL") :
       if lev.find("VIDEO") is not None :
          of.write('<div id="modl-vid' + str(n) + '" class="modal"> \n')
          of.write('   <div class="modal-content"> \n')
          of.write('        <iframe width="630" height="472" src="' + lev.find("VIDEO").text + '" seamless="" allowfullscreen></iframe> \n')
          of.write('        <span id="modl-close' + str(n) + '"><h2>close</h2></span>')
          of.write('   </div> \n')
          of.write('</div> \n')
       n+=1
   # Modal for final completion tag
   of.write('<div id="modl-review" class="modal"> \n')
   of.write('   <div class="modal-content"> \n')
   of.write(         ET.tostring( tree.find("REVIEW"), encoding="unicode", method="xml" ).replace("<REVIEW>","").replace("</REVIEW>","") + '\n')
   of.write('        <span id="modl-close-review"><h3>close</h3></span>')
   of.write('   </div> \n')
   of.write('</div> \n')
   # Now create blockly page
   of.write('<div id="content" class="container">')
   of.write('   <div class="panel panel-blue">')
   of.write('      <div class="panel-heading">')
   of.write('         <div class="row">')
   of.write('              <h1 class="panel-title">' + tree.find('TITLE').text + ': Blockly exercise </h1>')
   of.write('         </div>')
   of.write('      </div>')
   of.write('   </div>')
   of.write('   <div class="row margin-vert-30">')
   of.write('      <div class="panel panel-primary">')
   of.write('         <div class="panel-heading">')
   of.write('            <h4 class="panel-title">')
   of.write('              Use the blocks in the toolbox to solve the problems described below the exercise')
   of.write('            </h4>')
   of.write('         </div>')
   of.write('         <div class="panel-body">')
   of.write('            <div class="row" id="appPanel">')
   of.write('               <div class="col-md-6">')
   of.write('                 <button onclick="myApp.parseCode(myApp.workspace, initApi)">Show Code </button> \n')
   of.write('                 <button onclick="myApp.runCode()" id="runButton" disabled="disabled">Run Code </button> \n')
   of.write('                 <button onclick="myApp.showAnswer()" id="answerButton">Show answer</button> \n')
   of.write('                 <!-- <button onclick="myApp.save()" id="saveButton">Save workspace</button> \n')
   of.write('                 <button onclick="myApp.load()" id="loadButton">Load solution</button> --> \n')
   of.write('               </div>')
   of.write('                 <div class="col-md-6">')
   of.write('                 <div id="levelIndicator" class="w3-center w3-section w3-large w3-text-black w3-display-topleft" style="width:60%; height:100px" align="right"> </div>')
   of.write('               </div>')
   of.write('               <br/><br/>')
   of.write( ET.tostring( tree.find("WORKSPACE"), encoding="unicode", method="xml").replace("<WORKSPACE>","").replace("</WORKSPACE>","").replace("nbsp;","&nbsp;") )            
   of.write('             <div id="explanation"> </div> \n')
   of.write('             <xml id="toolbox" style="display: none">')
   of.write('             <category name="Variables" custom="VARIABLE"></category>')
   of.write('             </xml>')
   of.write('<script> \n')
   # Buttons to close pop up windows in this app
   n = 0
   for lev in tree.findall("LEVEL") :
       if lev.find("VIDEO") is not None :
          of.write('var span' + str(n) + ' = document.getElementById("modl-close' + str(n) + '");\n')
          of.write('span' + str(n) + '.onclick = function() {\n')
          of.write("    var modal = document.getElementById('modl-vid" + str(n) + "');\n")
          of.write('    modal.style.display = "none";\n')
          of.write("    var currentIframe = modal.querySelector('.modal-content > iframe');\n")
          of.write("    currentIframe.src = currentIframe.src;\n");
          of.write('}\n')
       n += 1
   of.write('var spanreview = document.getElementById("modl-close-review"); \n')
   of.write('spanreview.onclick = function() {\n')
   of.write('     var modal = document.getElementById("modl-review");\n')
   of.write('     modal.style.display = "none"; \n')
   of.write('}\n')
   # Insert Blocks for this app
   of.write( tree.find("BLOCKS").text )
   # Now get the fixed parts of the app
   f = open( 'Templates/blockly-app.html', 'r' )
   page = f.read()
   f.close()
   page = page.replace( "INSERT WORKSPACE STARTUP", tree.find("STARTUP").text )
   page = page.replace( "INSERT API FUNCTIONS", tree.find("APIFUNCTIONS").text )
   page = page.replace( "INSERT LEVEL XML", name )
   of.write( page )
   # Get the custom apps for this app
   of.write( tree.find("SCRIPTS").text.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&") )
   # Script of stuff to do on level load
   of.write('myApp.stuffToDoOnLevelLoad = function(n) {')
   n, levels = 0, tree.findall("LEVEL")
   of.write( tree.find("STARTUP").text )
   of.write("switch( myApp.mylevel ){ \n")
   for lev in levels :
       if lev.find("STARTUP") is not None :
          of.write( "case " + str(n) + ":")
          of.write( lev.find("STARTUP").text.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&") )
          of.write( "break; \n" )
       n += 1
   of.write( "}\n")
   of.write('};')
   # Function of stuff to do on level end
   of.write('myApp.checkLevelEnd = function() {')
   of.write('   levelcomplete = true; video=false;')
   of.write('   switch( myApp.mylevel ){')
   n = 0
   for lev in levels : 
       of.write("case " + str(n) + ":")
       of.write( lev.find("FINISH").text.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&") )
       if lev.find("VIDEO") is not None :
          of.write("if( levelcomplete ) {")
          of.write('alert("Congratulations! Your program is correct.  Close this window for more instructions");')
          of.write("var modal = document.getElementById('modl-vid" + str(n) + "');")
          of.write('modal.style.display = "block";')
          of.write('video=true;')
          of.write("}") 
       of.write("break;")
       n += 1
   of.write('   }')
   of.write('   if( levelcomplete && (myApp.mylevel+1)==myApp.active.length ){')
   of.write('       myApp.answers.push( Blockly.Xml.workspaceToDom(myApp.workspace) );')
   of.write('       var modal = document.getElementById("modl-review");')
   of.write('       modal.style.display = "block";')
   #of.write('       if( !video ) alert("' + ET.tostring( tree.find("REVIEW"), encoding="unicode", method="xml" ) + '");')
   of.write('   } else if( levelcomplete ){')
   of.write('       if( !video ) alert("Congratulations! Your program is correct.  Now see if you can modify your blocks to get through the next level")')
   of.write(        tree.find("STARTUP").text )
   of.write('       if( !myApp.active[myApp.mylevel + 1] ){ myApp.answers.push( Blockly.Xml.workspaceToDom(myApp.workspace) ); }')
   of.write('       myApp.active[myApp.mylevel + 1] = true;')
   of.write('       myApp.setLevel( myApp.mylevel + 1 );')
   of.write('   } else {')
   of.write('       alert("Your program is not quite right.  Have another go and see if you can fix it")')
   of.write(        tree.find("STARTUP").text )
   of.write('       myApp.stuffToDoOnLevelLoad( myApp.mylevel )')
   of.write('   }')
   of.write('};')  
   of.write('</script>')
   # Copy xml to html directory 
   shutil.copy( "Resources/" + name , "html/" + name )

def createExercisePage( name, tree, of ) :
    of.write('<div id="content" class="container">')
    of.write('   <div class="panel panel-blue">')
    of.write('      <div class="panel-heading">')
    of.write('         <div class="row">')
    of.write('            <div class="col-md-8">')
    of.write('                <h1 class="panel-title">' + tree.find('TITLE').text + ': Exercises</h1>')
    of.write('            </div>')
    of.write('            <div class="col-md-4" align="right">')
    of.write('                  <!-- Web2PDF Converter Button BEGIN -->')
    of.write('                   <script type="text/javascript">')
    of.write('                   var')
    of.write('                   pdfbuttonlabel="Save page as PDF"')
    of.write('                   </script>')
    of.write('                   <script src="http://www.web2pdfconvert.com/pdfbutton2.js" id="Web2PDF" type="text/javascript"></script>')
    of.write('                   <!-- Web2PDF Converter Button END -->')
    of.write('            </div>')
    of.write('         </div>')
    of.write('      </div>')
    of.write('      <H1> Introduction </H1>\n')
    of.write( ET.tostring( tree.find("DESCRIPTION"), encoding="unicode", method="xml" ) )
    of.write('<H1> Example problems </H1>\n')
    of.write('<p> Click on the problems to reveal the solution </p> \n')
    root, iq, egcount = tree.getroot(), 0, 0
    for child in root :
        if child.tag=="QUESTION_GROUP" :
           egcount += 1
           of.write('<h4> Problem ' + str(egcount) + '</h4>');
           for sub in child :
               if sub.tag=="EXAMPLE" :
                  exampleToHTML( iq, of, sub )
                  iq += 1
        elif child.tag=="EXAMPLE" :
           exampleToHTML( iq, of, child )
           iq += 1 
        elif child.tag=="EXERCISE" :
           of.write('<H1> Problems for you to try </H1> \n')
           content = ET.tostring( child.find("PROBLEMS"), encoding="unicode", method="xml" )
           pageelements.printPanel( of, "default", 'collapse-' + str(iq), child.find("TITLE").text, content )
           iq+=1
    of.write('   </div>')
    of.write('</div>')

def exampleToHTML( iq, of, child ) :
    question = ET.tostring( child.find("QUESTION"), encoding="unicode", method="xml" )
    answer = ET.tostring( child.find("SOLUTION"), encoding="unicode", method="xml" )
    pageelements.printPanel( of, "default", 'collapse-' + str(iq), question, answer )

def generate_pdf_worksheet( tree, infile ):
    # Read in latex template file
    g = open( 'Templates/latex-template.tex', 'r')
    worksheet = g.read();
    g.close()
    # Generate the latex worksheet 
    worksheet = worksheet.replace( "INSERT TOPIC TITLE", tree.find('TITLE').text )
    latex_questions = "\\begin{itemize}\n"
    for child in tree.find("UL") :
        latex_questions += "\\item "
        latex_questions += ET.tostring( child, encoding="unicode", method="xml" ).replace("<b>","{\\bf").replace("</b>","}").replace("<LI>","").replace("</LI>","").replace("&gt;",">").replace("&lt;","<")
        latex_questions += "\\vspace{4.5cm}\n"
    latex_questions += "\\end{itemize}\n"
    worksheet = worksheet.replace("INSERT QUESTIONS", latex_questions )
    # And output a latex file  
    g = open('latex/' + infile + '.tex', 'w' )
    g.write( worksheet )
    g.close()
    # Run latex to generate pdf files
    pageelements.create_pdf_from_latex( infile )

def buildPage( fname ) :
  tree = ET.parse( "Resources/" + fname )
  root = tree.getroot()
  of = open( "html/" + fname.replace(".xml",".html"), "w" )
  pageelements.printHeader( fname.replace(".xml","") , of )
  pageelements.printTopMenuBar( of )
  done = False
  for child in root :
      if child.tag=="VIDEO" :
         createVideoPage( "video", fname, tree, of )
         done = True
      elif child.tag=="GEOGEBRA" :
         createVideoPage( "geogebra", fname, tree, of )
         done = True
      elif child.tag=="WORKSPACE" :
         createBlocklyPage( fname, tree, of )
         done = True
  if not done :
      createExercisePage( fname, tree, of )
      pageelements.printFooter( of )
      of.close()


if __name__ == "__main__" :
    if len(sys.argv)==2 :
       buildPage( sys.argv[1] )
    elif len(sys.argv)==3 :
       os.chdir(sys.argv[2])
       buildPage( sys.argv[1] ) 
    else :
       print("wrong number of command line arguments expecting 2 found " + str(len(sys.argv)) + " " + str(sys.argv) )
