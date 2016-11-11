import sys
import module

def convert_video_to_html( infile ):
    # Read in the video template
    f = open( 'Templates/video_template.html', 'r')
    video_page = f.read()
    f.close()
        
    # Read in the module list
    mymodules=module.listofmodules()
    # Insert the module list on the template page
    video_page = video_page.replace("INSERT MODULE LIST", mymodules.getModuleMenu() ) 

    # Now read in the source for the file
    f = open( 'Resources/' + infile + ".ghtml", 'r' )
    v_input = f.readlines()
    f.close()
    inquestions = 0
    questions = "" 
    for item in v_input :
        if (inquestions==1) & (item[0]=="-") :
           questions += '<li type="square">' + item[1:] + '</li> \n'
        elif "TITLE:" in item :
           video_page = video_page.replace("INSERT TOPIC TITLE", item.replace("TITLE: ", "") )
        elif "VIDEO:" in item :
           video_page = video_page.replace("INSERT VIDEO", item.replace("VIDEO: ", "") )  
        elif "QUESTIONS:" in item :
           inquestions=1 
    video_page = video_page.replace("INSERT QUESTIONS", questions )
    # And output this to an html file
    f = open('html/' + infile + '.html', 'w' )
    f.write( video_page )
    f.close()

def convert_geogebra_to_html( infile ):
    # Read in the video template
    f = open( 'Templates/geogebra-template.html', 'r')
    g_page = f.read()
    f.close()

    # Read in the module list
    mymodules=module.listofmodules()
    # Insert the module list on the template page
    g_page = g_page.replace("INSERT MODULE LIST", mymodules.getModuleMenu() )

    # Now read in the source for the file
    f = open( 'Resources/' + infile + ".ghtml", 'r' )
    v_input = f.readlines()
    f.close()
    inquestions = 0
    questions = ""
    indescription = 0
    descrip = ""
    for item in v_input :
        if (inquestions==1) & (item[0]=="-") :
           questions += '<li type="square">' + item[1:] + '</li> \n'
        elif "QUESTIONS:" in item :
           inquestions=1
           indescription=0
           g_page = g_page.replace( "INSERT DESCRIPTION", descrip )
        elif indescription==1 :
           descrip += item
        elif "TITLE:" in item :
           g_page = g_page.replace("INSERT TOPIC TITLE", item.replace("TITLE: ", "") )
        elif "GEOGEBRA:" in item :
           g_page = g_page.replace( "INSERT GEOGEBRA", item.replace("GEOGEBRA: ", "") )
        elif "DESCRIPTION:" in item :
           indescription=1

    g_page = g_page.replace("INSERT QUESTIONS", questions )
    # And output this to an html file
    f = open('html/' + infile + '.html', 'w' )
    f.write( g_page )
    f.close()
