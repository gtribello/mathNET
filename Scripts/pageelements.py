import module
import os

def printHeader( pagename, of ) :
    f = open( 'Templates/header.html', 'r' )
    header = f.read()
    f.close()
    of.write( header.replace( "PAGE NAME", pagename ) )

def printTopMenuBar( of ) :
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

def printPanel( of, ptype, collapse_str, title, content ) :
    if ptype == "primary" :
       of.write('<div class="panel panel-primary">')
    else :
       of.write('<div class="panel panel-default">')
    of.write('    <div class="panel-heading">')
    of.write('        <h4 class="panel-title">')
    of.write('        <a class="accordion-toggle" href="#' + collapse_str + '" data-parent="#accordion" data-toggle="collapse">')
    of.write( title )
    of.write('        </a>')
    of.write('        </h4>')
    of.write('    </div>')
    if ptype == "primary" :
       of.write('    <div id="' + collapse_str + '" class="accordion-body collapse in">')
    else :
       of.write('    <div id="' + collapse_str + '" class="accordion-body collapse">')
    of.write('        <div class="panel-body">')
    of.write('            <div class="row">')
    of.write( content )
    of.write('            </div>')
    of.write('        </div>')
    of.write('    </div>')
    of.write('</div>')

def printFooter( of ) :
    f = open( 'Templates/footer.html', 'r' )
    footer = f.read()
    f.close()
    of.write( footer )
