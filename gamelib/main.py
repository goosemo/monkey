'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, pymunk, pygame
from pygame.locals import *

PIX_PER_M = 25 #pixels per meter

#chain_link_poly = [(0,0),(0,1),(1,0),(1,1)]
#def make_chain(space, length):
#    for i in range(length):
#        mass = 5
#        inertia = pymunk.moment_for_poly(mass, 0, chain_link_poly, (0,0))
#        body = py
        

def main():
    
    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('### OSUGCC PYWEEK PROTOTYPE')

    #init pymunk
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -9.8 * PIX_PER_M)
    space.resize_static_hash()
    space.resize_active_hash()

    #pygame event loop
    is_running = True
    while(is_running):
        screen.fill((0,0,0))    
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False

            else:
                print event

        pygame.display.flip()

#    print data.load('sample.txt').read()
