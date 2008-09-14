'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os, sys, pygame

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

def load_image(name):
    try:
        image = pygame.image.load(load(name))
    except pygame.error, message:
        print "couldn't load %s" % name
        sys.exit(0)

    return image.convert_alpha()


sounds = {}

def play_sound(name):
    if name not in sounds:
        try:
            sounds[name] = pygame.mixer.Sound(filepath(name))
        except:
            print "couldn't load %s" % name
            sys.exit(0)

    sounds[name].play()
