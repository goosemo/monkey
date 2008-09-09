'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, pymunk, pygame
from pymunk.vec2d import Vec2d
from pygame.locals import *

class WorldEntity(object):
    _pinjoints = []
    _slidejoints = []

    def __init__(self, world_pos, vertices, mass, friction=0.15, moment = None):
        pymunk_verts = map(Vec2d, vertices)
        
        if not moment:
            moment = pymunk.moment_for_poly(mass, pymunk_verts, (0,0))

        self._body = pymunk.Body(mass, moment)
        self._body.position = world_pos
  
        self._shape = pymunk.Poly(self._body, pymunk_verts, (0,0) )
        self._shape.friction = friction

    def get_shape(self):
        return self._shape

    def get_body(self):
        return self._body

    def get_vertices(self):
        return self._shape.get_points()

    def on_collision(self, other_entity):
#        print "%s hit %s" % (self, other_entity)
        pass

    def tick(self, dt):
        pass

class WorldEntityManager(object):
    _entities = {} 
    _group_count = 0

    def __init__(self, space):
        self._space = space

    def alloc_collision_group(self):
        self._group_count += 1
        return self._group_count

    def add_entity(self, entity, dynamic=True, collision_group=0):
        shape = entity.get_shape()
        shape.group = collision_group
        
        self._entities[shape] = entity

        if dynamic:
            self._space.add(entity.get_body(), shape)
        else:
            self._space.add_static(shape)

    def pinjoin_entities(self, ent_a, ent_b, pos_a, pos_b):
        joint = pymunk.PinJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b)
        ent_a._pinjoints.append(joint)
        ent_b._pinjoints.append(joint)
        self._space.add(joint)

    def slidejoin_entities(self, ent_a, ent_b, pos_a, pos_b, min, max):
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

    def tick(self, dt):
        for entity in self.get_entities():
            entity.tick(dt)


class Player(WorldEntity):
    STOP = 0
    LEFT = -1
    RIGHT = 1

    def __init__(self, power = 100000):
        WorldEntity.__init__(self, (400,400), [(-5,-10),(-5,10),(5,10),(5,-10)], 25, moment=pymunk.inf)
        self._power = power
        self.stop()

    def left(self):
        self._direction = Player.LEFT

    def right(self):
        self._direction = Player.RIGHT

    def stop(self):
        self._direction = Player.STOP

    def jump(self):
        self.get_body().apply_impulse((0,5000), (0,0))

    def tick(self, dt):
        body = self.get_body()
        if abs(body.velocity[0]) < 200:
            self.get_body().apply_impulse((self._direction*self._power*dt, 0),(0,0))

PIX_PER_M = 40 #pixels per meter

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
        entity = WorldEntity((i*(chain_link_len+2), 400), chain_link_poly, mass)
        links.append(entity)
        we_manager.add_entity(entity, collision_group=cgrp)

        if i > 0:
            we_manager.pinjoin_entities(links[i], links[i-1], (0,2.5), (chain_link_len, 2.5))
    
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

    ground_block = WorldEntity((0,-20), [(0,0),(0, 20), (700, 20), (700, 0)], pymunk.inf, friction=15)
    ledge_block = WorldEntity((0,200), [(0,0),(0, 20), (200, 20), (200, 0)], pymunk.inf)
    player = Player()

    we_manager = WorldEntityManager(space)
    we_manager.add_entity(ground_block, dynamic=False)
    we_manager.add_entity(ledge_block, dynamic=False)
    we_manager.add_entity(player)
    
    space.set_default_collisionpair_func(we_manager.on_collision)

    clock = pygame.time.Clock()
    unused_time = 0
    step_size = 0.015

    keydown_map = {K_w: False, K_s: False, K_d: False, K_a: False}
    #pygame event loop
    is_running = True
    while is_running:
        screen.fill((0,0,0))

        #perform physics in uniform steps
        dt = clock.tick()/1000.0
        unused_time += dt
        while(unused_time > step_size):
            space.step(step_size)
            unused_time -= step_size

        #handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False

            elif event.type == KEYDOWN:
                if event.key in keydown_map:
                    keydown_map[event.key] = True

                if event.key == K_ESCAPE:
                    is_running = False
                elif event.key == K_v:
                    make_chain(we_manager, 15, True)
                elif event.key == K_c:
                    make_chain(we_manager, 15, False)
                elif event.key == K_SPACE:
                    player.jump()

            elif event.type == KEYUP:
                if event.key in keydown_map:
                    keydown_map[event.key] = False

        #perframe actions
        if keydown_map[K_a]:
            player.left()
        elif keydown_map[K_d]:
            player.right()
        else:
            player.stop()


        #let entites know how much time has passed
        we_manager.tick(dt)

        #draw entities
        for entity in we_manager.get_entities():
            points = map(to_scr, entity.get_vertices())
            pygame.draw.polygon(screen, (255,255,255), points, 1)

        #render fps
        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (255,0,0))
        screen.blit(text_surf, (5, 5))

#            player.get_body().apply_impulse((10, 0), (0,0))

        pygame.display.flip()

#    print data.load('sample.txt').read()
