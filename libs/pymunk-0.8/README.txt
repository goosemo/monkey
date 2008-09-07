== pymunk ==

ABOUT

    pymunk is a python wrapper for the 2d physics library Chipmunk
    2007 - 2008, Victor Blomqvist - vb@viblo.se, MIT License

    This dev release is based on the latest pymunk release (0.8), 
    using chipmunk rev 223 (source included)
    
    IRC: #pymunk on irc.freenode.net
    Homepage: http://code.google.com/p/pymunk/
    Forum: http://www.slembcke.net/forums/viewforum.php?f=6
    Email: vb@viblo.se
    
    Getting the latest SVN copy:
        svn checkout http://pymunk.googlecode.com/svn/trunk pymunk-read-only

    Chipmunk: http://wiki.slembcke.net/main/published/Chipmunk

HOW TO USE

    pymunk ships with a number of demos in the examples directory, and the 
    API documentation. There is also a few tutorials on the googlecode page 
    and in the (shared) forum. 
    
    If chipmunk doesnt ship with a chipmunk binary your platform can understand
    (currently MacOSX) you will have to compile chipmunk before install. See 
    section CHIPMUNK in this readme for (very simple) instructions.
    
    To install you can either run
        
        > python setup.py install

    or simply put the pymunk folder where your program/game can find it.
    (like /my_python_scripts/yourgame/pymunk). The chipmunk binary library
    is located in the pymunk folder.

    One easy way to get started is to check out the examples/ directory,
    and run 'python demo_contact.py' and so on, and see what it does :)
    (Note: you will have to place /pymunk in the examples directory if
    you dont install pymunk to site-packages)

EXAMPLE
    
    See the included demos (in examples/)

DEPENDENCIES/REQUIREMENTS

    * ctypes (included in python 2.5)
    * python 2.5 (optional, used by the pymunk.util module)
    * pygame (optional, you need it to run most of the demos)
    * pyglet (optional, you need it to run the moon buggy demo)
    * ctypeslib & GCC_XML (optional, you need them to generate new bindings)
    * chipmunk (pymunk ships with a set of chipmunk libraries)

CHIPMUNK

    Compiled libraries of Chipmunk compatible Windows and Linux are distributed
    with pymun.
    If pymunk doesnt have your particular platform included, you can compile 
    Chipmunk by hand with a custom setup argument:
    
        > python setup.py build_chipmunk
    
    The compiled file goes into the /pymunk folder (same as _chipmunk.py, 
    util.py and others)

HOW TO GENERATE BINDINGS
(optional -- if you want to experiment :)

    You will need the ctypes code generator, it is part of the ctypeslib 
    package. You will also need GCC_XML. See the ctypes wiki for instructions
    on how to set it up: 
    http://starship.python.net/crew/theller/wiki/CodeGenerator
    When ctypeslib (h2xml and xml2py) and gcc_xml is installed then run

        > python generate_bindings.py

    (use --help to display options, you will most probably want to change the include
    path and possibly the lib path) you have now created a _chipmunk.py file with
    generated bindings.

