'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, pymunk, pygame
from pymunk.vec2d import Vec2d
from pygame.locals import *

PIX_PER_M = 2 #pixels per meter

chain_link_len = 10
chain_link_poly = map(Vec2d, [(0,0), (0,5), (chain_link_len, 5), (chain_link_len, 0)])
print chain_link_poly

def make_chain(space, length):
    links = []
    for i in range(length):
        mass = 5
        inertia = pymunk.moment_for_poly(mass, chain_link_poly, (0,0))
        body = pymunk.Body(mass, inertia)
        shape = pymunk.Poly(body, chain_link_poly, (0,0))
        body.position = (i*(chain_link_len), 400)
        links.append((body, shape))
        space.add(body, shape)

        if i > 0:
            chain_joint = pymunk.PinJoint(body, links[i-1][0], (0,0), (chain_link_len, 0))
            space.add(chain_joint)
    
    return links
        

def main():
    
    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('### OSUGCC PYWEEK PROTOTYPE')

    #init pymunk
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -9.8 * PIX_PER_M)
    space.resize_static_hash()
    space.resize_active_hash()


    ledge_body = pymunk.Body(pymunk.inf, pymunk.inf)
    ledge_body.position = Vec2d(0, 100)
    ledge_line = pymunk.Segment(ledge_body, Vec2d(-100,0), Vec2d(100, 0), 5.0)
    space.add(ledge_line)

    chain = make_chain(space, 15)

    #pygame event loop
    is_running = True
    with_physics = True
    while is_running:
        screen.fill((0,0,0))

        pygame.draw.line(screen, (255,255,255), (-100,100), (100,100), 1)

        for link in chain:
            px, py = (int(link[0].position.x), int(link[0].position.y))
            pygame.draw.polygon(screen, (255,255,255), link[1].get_points(), 1)
#            pygame.draw.rect(screen, (255,255,255), (px-chain_link_len/2.0, py, chain_link_len, 5), 1)

        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False
                elif event.key == K_s:
                    space.step(1/50.0)
                elif event.key == K_SPACE:
                    with_physics = not with_physics

            else:
                print event


        if with_physics:
            space.step(1/50.0)
        pygame.display.flip()

#    print data.load('sample.txt').read()
