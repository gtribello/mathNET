import sys
import module
import xml.etree.ElementTree as ET
import lxml.etree as ET

def build_html_file( infile ):
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

    # content = ""
    # for child in root :
    #    if child.tag=="UL" :
    #       content += ET.tostring( child, encoding="unicode", method="xml") 

    # page = page.replace("INSERT QUESTIONS", content )
    # And output this to an html file
    f = open('html/' + infile + '.html', 'w' )
    f.write( page )
    f.close()
