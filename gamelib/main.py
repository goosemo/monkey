'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, pymunk, pygame
from pymunk.vec2d import Vec2d
from pygame.locals import *

class WorldEntity(object):
    _shape = None
    _body = None
    _pinjoints = []
    _slidejoints = []

    def get_shape(self):
        return self._shape

    def get_body(self):
        return self._body

    def get_vertices(self):
        return self._shape.get_points()

    def on_collision(self, other_entity):
#        print "%s hit %s" % (self, other_entity)
        pass

class WorldEntityManager(object):
    _entities = {} 
    _group_count = 0

    def __init__(self, space):
        self._space = space

    def alloc_collision_group(self):
        self._group_count += 1
        return self._group_count

    def create_worldentity(self, world_pos, vertices, mass, dynamic=True, friction = 0.25, collision_group=0):
        pymunk_verts = map(Vec2d, vertices)
        
        inertia = pymunk.moment_for_poly(mass, pymunk_verts, (0,0))
        body = pymunk.Body(mass, inertia)
        body.position = world_pos
  
        shape = pymunk.Poly(body, pymunk_verts, (0,0) )
        shape.friction = friction
        shape.group = collision_group
        
        ent = WorldEntity()
        ent._shape = shape
        ent._body = body

        self._entities[shape] =  ent

        if dynamic:
            self._space.add(body, shape)
        else:
            self._space.add_static(shape)

        return ent

    def pinjoin_worldentities(self, ent_a, ent_b, pos_a, pos_b):
        joint = pymunk.PinJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b)
        ent_a._pinjoints.append(joint)
        ent_b._pinjoints.append(joint)
        self._space.add(joint)

    def slidejoin_worldentities(self, ent_a, ent_b, pos_a, pos_b, min, max):
        joint = pymunk.SlideJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b, min, max)
        ent_a._slidejoints.append(joint)
        ent_b._slidejoints.append(joint)
        self._space.add(joint)

    def on_collision(self, shapeA, shapeB, contacts, normal_coef, data):
        ent_a = self._entities[shapeA]
        ent_b = self._entities[shapeB]

        if ent_a and ent_b:
            ent_a.on_collision(ent_b)
            ent_b.on_collision(ent_a)
        
        return True

    def get_entities(self):
        return [ent for (shape, ent) in self._entities.iteritems()]


PIX_PER_M = 30 #pixels per meter

SCREENSIZE = (800, 600)

chain_link_len = 15
chain_link_poly = [(0,0), (0,5), (chain_link_len, 5), (chain_link_len, 0)]

def make_chain(we_manager, length, allow_self_intersection = False):
    
    cgrp = 0
    if allow_self_intersection:
        cgrp = we_manager.alloc_collision_group()

    links = []
    for i in range(length):
        mass = 5
        links.append(we_manager.create_worldentity((i*(chain_link_len+2), 400), chain_link_poly, mass, collision_group=cgrp))
        if i > 0:
            we_manager.pinjoin_worldentities(links[i], links[i-1], (0,2.5), (chain_link_len, 2.5))
    
    return links


def to_scr(v):
    return (v[0], (SCREENSIZE[1]/2)-v[1])

def main():
    
    #init pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('### OSUGCC PYWEEK PROTOTYPE')

    font = pygame.font.Font(None, 16)

    #init pymunk
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -9.8 * PIX_PER_M)
    space.damping = 0.98
    space.resize_static_hash(dim=10, count=1000)
    space.resize_active_hash(dim=10, count=1000)

    we_manager = WorldEntityManager(space)
    we_manager.create_worldentity((0,-20), [(0,0),(0, 20), (700, 20), (700, 0)], pymunk.inf, dynamic=False)
    we_manager.create_worldentity((0,200), [(0,0),(0, 20), (200, 20), (200, 0)], pymunk.inf, dynamic=False)
    
    space.set_default_collisionpair_func(we_manager.on_collision)

    clock = pygame.time.Clock()
    unused_time = 0
    step_size = 0.015

    #pygame event loop
    is_running = True
    while is_running:
        screen.fill((0,0,0))

        for entity in we_manager.get_entities():
            points = map(to_scr, entity.get_vertices())
            pygame.draw.polygon(screen, (255,255,255), points, 1)

        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (255,0,0))
        screen.blit(text_surf, (5, 5))

        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False
                elif event.key == K_v:
                    make_chain(we_manager, 15, True)
                elif event.key == K_c:
                    make_chain(we_manager, 15, False)

        dt = clock.tick()/1000.0
        unused_time += dt
        while(unused_time > step_size):
            space.step(step_size)
            unused_time -= step_size

        pygame.display.flip()

#    print data.load('sample.txt').read()
