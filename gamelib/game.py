import data, pymunk, pygame, sys, math
import game_entities, texture, world

from pymunk.vec2d import Vec2d
from pygame.locals import *

chain_link_len = 20 
chain_link_poly = [(-chain_link_len/2, -2.5), (-chain_link_len/2,2.5), (chain_link_len/2, 2.5), (chain_link_len/2, -2.5)]

def make_chain(we_manager, length, allow_self_intersection = False):
    cgrp = 0
    if allow_self_intersection:
        cgrp = we_manager.alloc_collision_group()

    links = []
    for i in range(length):
        mass = 1 
        entity = world.BaseEntity((i*(chain_link_len+2), 400), chain_link_poly, mass, grabable=True, taggable = False, friction=0.1)
        links.append(entity)
        we_manager.add_entity(entity, collision_group=cgrp)

        if i > 0:
            we_manager.pin_join_entities(links[i], links[i-1], (-chain_link_len/2,0), (chain_link_len/2, 0))
    
    return links


class View(object):
    _position = (0,0)
    
    def __init__(self, screensize):
        self.set_screensize(screensize)

    def set_screensize(self, screensize):
        self._screensize = screensize

    def get_screensize(self):
        return self._screensize

    def set_position(self, position):
        self._position = position

    def get_position(self, position):
        return self._position

    def to_screen(self, v):
        return (v[0] - self._position[0] + self._screensize[0]/2, (self._screensize[1]/2)-v[1] + self._position[1])

def main(screen):
   
    screensize = (screen.get_width(), screen.get_height())
    pygame.display.init(screensize)
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 16)
    
    texture_manager = texture.TextureManager()
    texture_manager.register_texture('MUD', 'test.png')
    texture_manager.register_texture('crossPole', 'CrossPoleTexture01.png')

    #init pymunk
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -9.8 * 40)
    space.damping = 0.98
    space.resize_static_hash(dim=10, count=1000)
    space.resize_active_hash(dim=10, count=1000)

    #build some objects for our world
    ground_block = world.BaseEntity((0,-20), [(0,0),(0, 20), (700, 20), (700, 0)], pymunk.inf)
    ledge_block = world.BaseEntity((0,200), [(0,0),(0, 20), (200, 20), (200, 0)], pymunk.inf)
    moveable_block_1 = world.BaseEntity((500,200), [(-40,-40),(-40, 40), (40, 40), (40, -40)], 30, texture_name = 'MUD')
    moveable_block_2 = world.BaseEntity((300,200), [(-20,-20),(-20, 20), (20, 20), (20, -20)], 10)
    moveable_block_3 = world.BaseEntity((50,400), [(-20,-20),(-20, 20), (20, 20), (20, -20)], 999)

    player = game_entities.Player()

    #add the entities to the world
    we_manager = world.EntityManager(space)
    we_manager.add_entity(ground_block, dynamic=False)
    we_manager.add_entity(ledge_block, dynamic=False)
    we_manager.add_entity(moveable_block_1)
    we_manager.add_entity(moveable_block_2)
    we_manager.add_entity(moveable_block_3)
    we_manager.add_entity(player)

    #set the collisions to be handeled by the world manager
    space.set_default_collisionpair_func(we_manager.on_collision)

    #create a viewport
    view = View(screensize)

    clock = pygame.time.Clock()
    unused_time = 0
    step_size = 0.001

    keydown_map = {K_w: False, K_d: False, K_a: False, K_LEFT: False, K_RIGHT: False}
    #pygame event loop
    is_running = True
    while is_running:
        screen.fill((0x28,0x08b,0xd7))

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
                    make_chain(we_manager, 8, True)
                elif event.key == K_c:
                    make_chain(we_manager, 8, False)
                elif event.key == K_SPACE:
                    player.jump()
                elif event.key == K_s:
                    player.begin_grabbing()
                elif event.key == K_e:
                    player.begin_tagging()
                elif event.key == K_q:
                    player.drop()

            elif event.type == KEYUP:
                if event.key in keydown_map:
                    keydown_map[event.key] = False
                elif event.key == K_s:
                    player.end_grabbing()
                elif event.key == K_e:
                    player.end_tagging()

        #perframe actions
        if keydown_map[K_a] or keydown_map[K_LEFT]:
            player.left()
        elif keydown_map[K_d] or keydown_map[K_RIGHT]:
            player.right()
        else:
            player.stop()

        #let entites know how much time has passed
        we_manager.tick(dt)

        #draw entities
        view.set_position(player.get_position())

        for entity in we_manager.get_entities():
            if entity.is_textured():
                tex = texture_manager.get_texture(entity.get_texture_name())
                image = pygame.transform.rotate(tex.image, entity.get_body().angle * 180/math.pi)
                shift_vec = Vec2d(-image.get_width()/2, image.get_height()/2)
                screen.blit(image, view.to_screen(entity.get_body().position + shift_vec))

            color = (255, 0, 0)
            pygame.draw.circle(screen, color, view.to_screen(entity.get_body().position),3)
            color = (255,255,255)
            points = map(view.to_screen, entity.get_vertices())
            pygame.draw.polygon(screen, color, points, 1)

        #render fps
        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (255,0,0))
        screen.blit(text_surf, (5, 5))

        pygame.display.flip()


