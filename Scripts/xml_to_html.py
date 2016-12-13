import sys
import module
import xml.etree.ElementTree as ET
import lxml.etree as ET

def build_html_file( infile ):
    print( infile )
    tree = ET.parse( "Resources/" + infile + ".xml" )
    root = tree.getroot()
    # Find appropriate template to use
    template = "exercise"
    for child in root :
        if child.tag=="VIDEO" :
           template = "video" 
        elif child.tag=="GEOGEBRA" :
           template = "geogebra"

    # Read in the video template
    if template=="geogebra" :
        f = open( 'Templates/geogebra-template.html', 'r')
    elif template=="video" :
        f = open( 'Templates/video_template.html', 'r')
    else :
        f = open( 'Templates/exercise_template.html', 'r')

    # Read in the appropriate template file
    page = f.read()
    f.close()

    # Read in the module list
    mymodules=module.listofmodules()
    # Insert the module list on the template page
    page = page.replace("INSERT MODULE LIST", mymodules.getModuleMenu() ) 

    root = tree.getroot() 
    page = page.replace( "INSERT TOPIC TITLE", tree.find('TITLE').text )
    if template=="video" :
       page = page.replace( "INSERT VIDEO", tree.find("VIDEO").text )    
       page = page.replace( "INSERT QUESTIONS", ET.tostring( tree.find("UL"), encoding="unicode", method="xml") )
    elif template=="geogebra" :
       page = page.replace( "INSERT GEOGEBRA", tree.find("GEOGEBRA").text )
       page = page.replace( "INSERT DESCRIPTION", tree.find("DESCRIPTION").text )
       page = page.replace( "INSERT QUESTIONS", ET.tostring( tree.find("UL"), encoding="unicode", method="xml") )
    else : 
       html_string = "<H1> Introduction </H1>\n" 
       html_string += ET.tostring( tree.find("DESCRIPTION"), encoding="unicode", method="xml" ) 
       html_string += "<H1> Example problems </H1>\n"
       html_string += "<p> Click on the problems to reveal the solution </p> \n" 
       root = tree.getroot()
       iq = 0
       egcount=0
       for child in root :
           if child.tag=="QUESTION_GROUP" :
              egcount += 1
              html_string += '<h4> Problem ' + str(egcount) + '</h4>'
              iq, newstr = questionsToHTML( iq, child )
              html_string += newstr 
           elif child.tag=="EXAMPLE" :
              html_string += exampleToHTML( iq, child )
              iq+=1
           elif child.tag=="EXERCISE" :
              html_string += '<H1> Problems for you to try </H1> \n'
              html_string += '<div id="accordion" class="panel-group"> \n'
              html_string += '    <div class="panel panel-default">\n'
              html_string += '        <div class="panel-heading">\n'
              html_string += '            <h4 class="panel-title">\n'
              html_string += '               <a class="accordion-toggle" href="#collapse-' + str(iq) +'" data-parent="#accordion" data-toggle="collapse">\n'
              html_string += '                  ' + child.find("TITLE").text + '\n'
              html_string += '               </a>\n'
              html_string += '            </h4>\n'
              html_string += '        </div>\n'
              html_string += '        <div id="collapse-' + str(iq) + '" class="accordion-body collapse in">\n'
              html_string += '            <div class="panel-body">\n'
              html_string += '               <div class="row">\n'
              html_string += ET.tostring( child.find("PROBLEMS"), encoding="unicode", method="xml" )  
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
              iq+=1
       page = page.replace("INSERT EXERICSE MATERIAL", html_string )

    # And output this to an html file
    f = open('html/' + infile + '.html', 'w' )
    f.write( page )
    f.close()

def exampleToHTML( iq, child ):
    html_string =  '<div id="accordion" class="panel-group"> \n'
    html_string += '<div class="panel panel-default">\n'
    html_string += '    <div class="panel-heading">\n'
    html_string += '        <h4 class="panel-title">\n'
    html_string += '        <a class="accordion-toggle" href="#collapse-' + str(iq) +'" data-parent="#accordion" data-toggle="collapse">\n'
    html_string += ET.tostring( child.find("QUESTION"), encoding="unicode", method="xml" )
    html_string += '        </a>\n'
    html_string += '        </h4>\n'
    html_string += '    </div>\n'
    html_string += '    <div id="collapse-' + str(iq) + '" class="accordion-body collapse">\n'
    html_string += '        <div class="panel-body">\n'
    html_string += '           <div class="row">\n'
    html_string += ET.tostring( child.find("SOLUTION"), encoding="unicode", method="xml" )
    html_string +='         </div>\n'
    html_string +='      </div>\n'
    html_string +='   </div>\n'
    html_string +='</div>\n'
    html_string += '</br>\n'
    return html_string 

def questionsToHTML( iq, child ):
    html_string = ""
    for sub in child :
        if sub.tag=="EXAMPLE" :
           html_string += exampleToHTML( iq, sub )
           iq += 1
    return iq, html_string


