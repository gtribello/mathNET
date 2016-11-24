import sys
import module

def convert_exercise_to_html( infile ):
    # Read in the exercise template 
    f = open( 'Templates/exercise_template.html', 'r' )
    exercise_page = f.read()
    f.close()

    # Read in the module list
    mymodules=module.listofmodules()
    # Insert the module list on the template page
    exercise_page = exercise_page.replace("INSERT MODULE LIST", mymodules.getModuleMenu() )

    # Now read in the source for the file
    f = open( 'Resources/' + infile + ".ghtml", 'r' )
    ex_input = f.readlines()
    f.close()
    html_string = ""
    insolution=0
    inquestion=0
    egcount=0
    iq=0 
    foundexamples=0
    foundproblems=0
    for item in ex_input :
        if "TITLE:" in item :
           exercise_page = exercise_page.replace( "INSERT TOPIC TITLE", item.replace("TITLE: ", "") )
        elif "DESCRIPTION:" in item :
           if inquestion>0 | insolution==1 :
              sys.error("DESCRIPTION SHOULD APPEAR BEFORE EXAMPLES IN INPUT FILE " + infile)
           html_string += "<H1> Introduction </H1>\n"
        elif "QUESTION_BREAK:" in item :
           if foundexamples==0 :
              html_string += "<H1> Example problems </H1>\n"
              html_string += "<p> Click on the problems to reveal the solution </p> \n" 
              foundexamples=1
           if insolution==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
           insolution=0
           egcount += 1
           html_string += '<h4> Problem ' + str(egcount) + '</h4>'  
        elif "EXAMPLE_QUESTION:" in item :
           if insolution==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
              html_string += '</br>\n'
           inquestion=1
           insolution=0
           html_string += '<div id="accordion" class="panel-group"> \n'
           html_string += '<!-- Start of introductory panel -->\n'
           html_string += '<div class="panel panel-default">\n'
           html_string += '    <div class="panel-heading">\n'
           html_string += '        <h4 class="panel-title">\n'
           html_string += '        <a class="accordion-toggle" href="#collapse-' + str(iq) +'" data-parent="#accordion" data-toggle="collapse">\n'
        elif "WORKED_SOLUTION:" in item :
           insolution=1
           html_string += '        </a>\n'
           html_string += '        </h4>\n'
           html_string += '    </div>\n'
           html_string += '    <div id="collapse-' + str(iq) + '" class="accordion-body collapse">\n'
           html_string += '        <div class="panel-body">\n'
           html_string += '           <div class="row">\n'
           inquestion=0
           iq+=1
        elif "EXERCISE:" in item :
           if inquestion>0 : 
              sys.error("Found EXAMPLE_QUESITON with no solution in input file " + infile )
           if insolution==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
              html_string +='</div>\n'
              insolution=0
           if foundproblems==0 :
              html_string += '<H1> Problems for you to try </H1> \n'
              html_string += '<div id="accordion" class="panel-group"> \n' 
              foundproblems=1
           elif foundproblems==1 :
              html_string +='         </div>\n'
              html_string +='      </div>\n'
              html_string +='   </div>\n'
           iq+=1
           html_string += '    <div class="panel panel-default">\n'
           html_string += '        <div class="panel-heading">\n'
           html_string += '            <h4 class="panel-title">\n'
           html_string += '               <a class="accordion-toggle" href="#collapse-' + str(iq) +'" data-parent="#accordion" data-toggle="collapse">\n'
           html_string += '                  ' + item.replace("EXERCISE: ", "") + '\n'
           html_string += '               </a>\n'
           html_string += '            </h4>\n'
           html_string += '        </div>\n'
           html_string += '        <div id="collapse-' + str(iq) + '" class="accordion-body collapse in">\n'
           html_string += '            <div class="panel-body">\n'
           html_string += '               <div class="row">\n'
        else :
           html_string += item 

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
