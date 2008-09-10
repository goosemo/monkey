'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, pymunk, pygame, sys, math
from pymunk.vec2d import Vec2d
from pygame.locals import *

class WorldEntity(object):
    _world_entity_manager = None
    _is_dynamic = True
    _is_taggable = True
    _is_grabable = False
    _texture_name = None

    def __init__(self, world_pos, vertices, mass, friction=0.15, moment = None, taggable=True, grabable=False, texture_name=None):
        pymunk_verts = map(Vec2d, vertices)
        
        if not moment:
            moment = pymunk.moment_for_poly(mass, pymunk_verts, (0,0))

        self._body = pymunk.Body(mass, moment)
        self._body.position = world_pos
  
        self._shape = pymunk.Poly(self._body, pymunk_verts, (0,0) )
        self._shape.friction = friction

        self._is_taggable = taggable
        self._is_grabable = grabable
        self._texture_name = texture_name

    def get_texture_name(self):
        return self._texture_name

    def is_textured(self):
        return self._texture_name is not None

    def is_taggable(self):
        return self._is_taggable

    def is_grabable(self):
        return self._is_grabable

    def is_world_bound(self):
        return self._world_entity_manager is not None

    def is_dynamic(self):
        return self._is_dynamic

    def on_bind_world(self, world_entity_manager):
        self._world_entity_manager = world_entity_manager

    def get_world_entity_manager(self):
        return self._world_entity_manager

    def pin_join(self, entity, self_pos, entity_pos):
        if self.is_world_bound():
            return self._world_entity_manager.pin_join_entities(self, entity, self_pos, entity_pos)

        return False

    def tag(self, grabable_ent, wc_taggable_pos):
        if not self.is_taggable() or not grabable_ent.is_grabable():
            return

        grabable_body = grabable_ent.get_body()

        #move the body to the taggable pos
        grabable_body.position = wc_taggable_pos

        #convert world pin coordinates to local body coords
        lc_grabable_pos = grabable_body.world_to_local(wc_taggable_pos)
        lc_taggable_pos = self.get_body().world_to_local(wc_taggable_pos)

        #turn off collision checking between the combined items
        cgrp = self.get_world_entity_manager().alloc_collision_group()
        self.get_shape().group = cgrp
        grabable_ent.get_shape().group = cgrp
        
        #pin it to the taggable
        grabable_ent.pin_join(self, lc_grabable_pos, lc_taggable_pos)


    def unjoin(self, joint_id):
        if self.is_world_bound():
            return self._world_entity_manager.unjoin(joint_id)

        return False

    def get_shape(self):
        return self._shape

    def get_body(self):
        return self._body

    def get_vertices(self):
        return self._shape.get_points()

    def on_collision(self, other_entity, contacts, normal_coef, data):
        pass

    def tick(self, dt):
        pass

class WorldEntityManager(object):
    _entities = {} 
    _group_count = 0
    _joint_count = 0
    _joints = {}

    PINJOINT = 0
    
    JINF_TYPE = 0
    JINF_JOINT = 1
    JINF_ENTA = 2
    JINF_ENTB = 3
    JINF_DATA = 4

    def __init__(self, space):
        self._space = space

    def alloc_collision_group(self):
        self._group_count += 1
        return self._group_count

    def _alloc_joint_id(self):
        self._joint_count += 1
        return self._joint_count

    def _register_joint(self, joint_type, joint, ent_a, ent_b, data):
        joint_id = self._alloc_joint_id()
        self._joints[joint_id] = (joint_type, joint, ent_a, ent_b, data)
        return joint_id
    
    def unjoin(self, joint_id):
        if not joint_id in self._joints:
            return False

        joint_info = self._joints[joint_id]
        self._space.remove(joint_info[WorldEntityManager.JINF_JOINT])
        
        return True

    def add_entity(self, entity, dynamic=True, collision_group=0):
        shape = entity.get_shape()
        shape.group = collision_group

        entity.on_bind_world(self)
        entity._is_dynamic = dynamic
        self._entities[shape] = entity

        if dynamic:
            self._space.add(entity.get_body(), shape)
        else:
            self._space.add_static(shape)

    def pin_join_entities(self, ent_a, ent_b, pos_a, pos_b):
        joint = pymunk.PinJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b)
        self._space.add(joint)
        return self._register_joint(WorldEntityManager.PINJOINT, joint, ent_a, ent_b, (pos_a, pos_b))



    def on_collision(self, shapeA, shapeB, contacts, normal_coef, data):
        ent_a = self._entities[shapeA]
        ent_b = self._entities[shapeB]

        if ent_a and ent_b:
            ent_a.on_collision(ent_b, contacts, normal_coef, data)
            ent_b.on_collision(ent_a, contacts, normal_coef, data)
        
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

    _hold_joint = None
    _held_entity = None
    _held_location = None

    _try_grab = False
    _try_tag = False

    def __init__(self, power = 50000):
        WorldEntity.__init__(self, (400,400), [(-15,-30),(-15,30),(15,30),(15,-30)], 25, moment=pymunk.inf)
        self._power = power
        self._direction = Player.STOP
        self.stop()

    def left(self):
        self._direction = Player.LEFT

    def right(self):
        self._direction = Player.RIGHT

    def stop(self):
        self._direction = Player.STOP

    def jump(self):
        self.get_body().apply_impulse((0,5000), (0,0))

    def begin_grabbing(self):
        self._try_grab = True

    def end_grabbing(self):
        self._try_grab = False

    def begin_tagging(self):
        self._try_tag = True

    def end_tagging(self):
        self._try_tag = False

    def tag(self, target_entity, wc_contact_pos):
        held_entity = self.get_held_entity()
        if held_entity:
            self.drop()
            target_entity.tag(held_entity, wc_contact_pos)

    def drop(self):
        if self._hold_joint:
            self.unjoin(self._hold_joint)
            self._hold_joint = None
            self._held_entity = None

    def hold(self, entity, wc_contact_pos):
        if not entity.is_grabable():
            return

        self.drop()

        lc_for_entity = entity.get_body().world_to_local(wc_contact_pos)
        lc_for_player = self.get_body().world_to_local(wc_contact_pos)
        joint_id = self.pin_join(entity, lc_for_player, lc_for_entity)
        
        self._hold_joint = joint_id
        self._held_entity = entity
        self._held_location = lc_for_entity

    def get_held_entity(self):
        return self._held_entity

    def on_collision(self, entity, contacts, normal_coef, data):
        if not entity.is_dynamic():
            return

        if self._try_grab and entity.is_grabable():
            self.end_grabbing()
            self.hold(entity, contacts[0].position)
        elif self._try_tag and entity.is_taggable() and self.get_held_entity() != entity:
            self.end_tagging()
            self.tag(entity, contacts[0].position)

    def tick(self, dt):
        body = self.get_body()
        if abs(body.velocity[0]) < 200:
            body.apply_impulse((self._direction*self._power*dt, 0),(0,0))

PIX_PER_M = 40 #pixels per meter

SCREENSIZE = (800, 600)

chain_link_len = 20 
chain_link_poly = [(-chain_link_len/2, -2.5), (-chain_link_len/2,2.5), (chain_link_len/2, 2.5), (chain_link_len/2, -2.5)]

def make_chain(we_manager, length, allow_self_intersection = False):
    
    cgrp = 0
    if allow_self_intersection:
        cgrp = we_manager.alloc_collision_group()

    links = []
    for i in range(length):
        mass = 1 
        entity = WorldEntity((i*(chain_link_len+2), 400), chain_link_poly, mass, grabable=True, taggable = False)
        links.append(entity)
        we_manager.add_entity(entity, collision_group=cgrp)

        if i > 0:
            we_manager.pin_join_entities(links[i], links[i-1], (-chain_link_len/2,0), (chain_link_len/2, 0))
    
    return links


def to_scr(v, camera_pos = (0,0)):
    return (v[0] - camera_pos[0], (SCREENSIZE[1]/2)-v[1] + camera_pos[1])

def load_image(name):
    try:
        image = pygame.image.load(data.load(name))
    except pygame.error, message:
        print "couldn't load %s" % name
        sys.exit(0)
   
    image = image.convert_alpha()
    return image

class Texture(object):
    def __init__(self, name, file):
        self._name = name
        self._file = file
        self.image = load_image(file)
        self.center = (self.image.get_width()/2, self.image.get_height()/2)

TEXTURES = {}

def register_texture(name, filename):
    TEXTURES[name] = Texture(name, filename)

def get_texture(name):
    return TEXTURES[name]

def main():
    
    #init pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('### OSUGCC PYWEEK PROTOTYPE')

    font = pygame.font.Font(None, 16)

    register_texture('MUD', 'test.png')

    #init pymunk
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = (0.0, -9.8 * PIX_PER_M)
    space.damping = 0.98
    space.resize_static_hash(dim=10, count=1000)
    space.resize_active_hash(dim=10, count=1000)

    ground_block = WorldEntity((0,-20), [(0,0),(0, 20), (700, 20), (700, 0)], pymunk.inf, friction=15)
    ledge_block = WorldEntity((0,200), [(0,0),(0, 20), (200, 20), (200, 0)], pymunk.inf)
    moveable_block_1 = WorldEntity((500,200), [(-40,-40),(-40, 40), (40, 40), (40, -40)], 30, texture_name = 'MUD')
    moveable_block_2 = WorldEntity((300,200), [(-20,-20),(-20, 20), (20, 20), (20, -20)], 10)
    moveable_block_3 = WorldEntity((50,400), [(-20,-20),(-20, 20), (20, 20), (20, -20)], 999)


    player = Player()

    we_manager = WorldEntityManager(space)
    we_manager.add_entity(ground_block, dynamic=False)
    we_manager.add_entity(ledge_block, dynamic=False)
    we_manager.add_entity(moveable_block_1)
    we_manager.add_entity(moveable_block_2)
    we_manager.add_entity(moveable_block_3)
    we_manager.add_entity(player)
    
    space.set_default_collisionpair_func(we_manager.on_collision)

    clock = pygame.time.Clock()
    unused_time = 0
    step_size = 0.001

    keydown_map = {K_w: False, K_d: False, K_a: False}
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
            if entity.is_textured():
                texture = get_texture(entity.get_texture_name())
                image = pygame.transform.rotate(texture.image, entity.get_body().angle * 180/math.pi)
                shift_vec = Vec2d(-image.get_width()/2, image.get_height()/2)
                screen.blit(image, to_scr(entity.get_body().position + shift_vec))

            color = (255, 0, 0)
            pygame.draw.circle(screen, color, to_scr(entity.get_body().position),3)
            color = (255,255,255)
            points = map(to_scr, entity.get_vertices())
            pygame.draw.polygon(screen, color, points, 1)

        #render fps
        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (255,0,0))
        screen.blit(text_surf, (5, 5))

        pygame.display.flip()

#    print data.load('sample.txt').read()
