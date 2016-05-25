import shutil
import sys
from os import listdir

def convert_exercise_to_html( infile ):
    # Read in the exercise template 
    f = open( 'Templates/exercise_template.html', 'r' )
    exercise_page = f.read()
    f.close()

    # Read in the module list
    mlist = listdir("Modules")
    modulemenu = ""
    for i in range(0,len(mlist)):
        # Add this module to the module menu
        modulemenu += '<li><span><a href="' + mlist[i] +'.html">' + mlist[i] + '</a></span></li>\n'
     
    # Insert the module list on the template page
    exercise_page = exercise_page.replace("INSERT MODULE LIST", modulemenu )

    # Now read in the source for the file
    f = open( 'Resources/' + infile, 'r' )
    ex_input = f.readlines()
    f.close()
    html_string = ""
    insolution=0
    inquestion=0 
    foundexamples=0
    foundproblems=0
    for i in range(0,len(ex_input)) :
        if "TITLE:" in ex_input[i] :
           exercise_page = exercise_page.replace( "INSERT TOPIC TITLE", ex_input[i].replace("TITLE: ", "") )
        elif "DESCRIPTION:" in ex_input[i] :
           if inquestion>0 | insolution==1 :
              sys.error("DESCRIPTION SHOULD APPEAR BEFORE EXAMPLES IN INPUT FILE " + infile)
           html_string += "<H1> Introduction </H1>\n"
        elif "EXAMPLE_QUESTION:" in ex_input[i] :
           if foundexamples==0 : 
              html_string += "<H1> Worked examples </H1>\n"
              html_string += "<p> Click on the problems to reveal the solution </p> \n" 
              foundexamples=1
           if insolution==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
           inquestion=i
           insolution=0
           html_string += '<div id="accordion" class="panel-group"> \n'
           html_string += '<!-- Start of introductory panel -->\n'
           html_string += '<div class="panel panel-default">\n'
           html_string += '    <div class="panel-heading">\n'
           html_string += '        <h4 class="panel-title">\n'
           html_string += '        <a class="accordion-toggle" href="#collapse-' + str(i) +'" data-parent="#accordion" data-toggle="collapse">\n'
        elif "WORKED_SOLUTION:" in ex_input[i] :
           insolution=1
           html_string += '        </a>\n'
           html_string += '        </h4>\n'
           html_string += '    </div>\n'
           html_string += '    <div id="collapse-' + str(inquestion) + '" class="accordion-body collapse">\n'
           html_string += '        <div class="panel-body">\n'
           html_string += '           <div class="row">\n'
           inquestion=0
        elif "EXERCISE:" in ex_input[i] :
           if inquestion>0 : 
              sys.error("Found EXAMPLE_QUESITON with no solution in input file " + infile )
           if insolution==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
           if foundproblems==0 :
              html_string += '<H1> Problems for you to try </H1> \n'
              foundproblems=1
           html_string += '<div id="accordion" class="panel-group"> \n'
           html_string += '    <div class="panel panel-default">\n'
           html_string += '        <div class="panel-heading">\n'
           html_string += '            <h4 class="panel-title">\n'
           html_string += '               <a class="accordion-toggle" href="#collapse-' + str(i) +'" data-parent="#accordion" data-toggle="collapse">\n'
           html_string += '                  ' + ex_input[i].replace("EXERCISE: ", "") + '\n'
           html_string += '               </a>\n'
           html_string += '            </h4>\n'
           html_string += '        </div>\n'
           html_string += '        <div id="collapse-' + str(i) + '" class="accordion-body collapse in">\n'
           html_string += '            <div class="panel-body">\n'
           html_string += '               <div class="row">\n'
        else :
           html_string += ex_input[i]

    # Make sure exercise panel is closed
    html_string +='         </div>\n'
    html_string +='      </div>\n'
    html_string +='   </div>\n'
    html_string +='</div>\n'
    # And finish by substituting above into template html
    exercise_page = exercise_page.replace("INSERT EXERICSE MATERIAL", html_string )
    # And output this to an html file
    f = open('html/' + infile + '.html', 'w' )
    f.write( exercise_page )
    f.close() 
