import module
import os

def printHeader( pagename, pageout ) :
    f = open( 'Templates/header.html', 'r' )
    header = f.read()
    f.close()
    of = open( pageout, 'w' )
    of.write( header.replace( "PAGE NAME", pagename ) )
    of.close()

def printTopMenuBar( pageout ) :
    of = open( pageout, 'a' )
    of.write('<div id="pre_header" class="visible-lg"></div>\n')
    of.write('<div id="header" class="container">\n')
    of.write('        <div class="row">\n')
    of.write('                <!-- Logo -->\n')
    of.write('                <div class="logo">\n')
    of.write('                        <a href="index.html" title="">\n')
    of.write('                                <img src="assets/img/logo.png" alt="Logo" />\n')
    of.write('                        </a>\n')
    of.write('                </div>\n')
    of.write('                <!-- End Logo -->')
    of.write('                <!-- Top Menu -->')
    of.write('                <div class="col-md-12 margin-top-30">\n')
    of.write('                        <div id="hornav" class="pull-right visible-lg">\n')
    of.write('                                <ul class="nav navbar-nav">\n')
    of.write('                                        <li><a href="index.html">Home</a></li>\n')
    of.write('                                          <li><span>Modules</span>\n')
    of.write('                                          <ul>\n')
    # Read in the module list
    mymodules=module.listofmodules()
    # And get the module menu
    of.write( mymodules.getModuleMenu() )                                           
    of.write('                                          </ul>\n')                         
    of.write('                        </div>\n')
    of.write('                </div>\n')
    of.write('                <div class="clear"></div>\n')
    of.write('                <!-- End Top Menu -->\n')
    of.write('        </div>\n')
    of.write('</div>\n')
    of.write('<!-- === END HEADER === -->\n')
    of.close()

def printFooter( pageout ) :
    f = open( 'Templates/footer.html', 'r' )
    footer = f.read()
    f.close()
    of = open( pageout, 'a') 
    of.write( footer )
    of.close() 
