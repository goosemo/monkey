import data, pymunk, pygame, sys, math
import game_entities, texture, world, levels

from pymunk.vec2d import Vec2d
from pygame.locals import *

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
        return (int(v[0] - self._position[0] + self._screensize[0]/2), int((self._screensize[1]/2)-v[1] + self._position[1]))

class WorldInstance(object):
    KillDistance = 1000

    def __init__(self, player, texture_manager, level_num=1):
        self._player = player
        self._texture_manager = texture_manager
        self._init_level(level_num)

    def _init_level(self, level_num):
        self._texture_manager.clear_texture_maps()

        self._space = pymunk.Space()
        self._space.gravity = (0.0, -9.8 * 45)
        self._space.damping = 0.98
        self._space.resize_static_hash(dim=10, count=1000)
        self._space.resize_active_hash(dim=10, count=1000)
        
        self._we_manager = world.EntityManager(self._space)
        self._space.set_default_collisionpair_func(self._we_manager.on_collision)

        self._level_num = level_num
        self._level = levels.Levels[level_num - 1]

        self._player.get_body().position = self._level[levels.PLAYER_START]
        self._we_manager.add_entity(self._player)

        self._level_name = self._level[levels.LEVEL_NAME]
        self._level_max_time = self._level[levels.MAXTIME]
        self._time_elapsed = 0

        self._goalbox = game_entities.GoalBox(self._level[levels.GOALBOX_LOCATION])
        self._we_manager.add_entity(self._goalbox)
                
        for entity in self._level[levels.ELEMENTS]:
            ent = entity()
            self._we_manager.add_entity(ent)

        for factory in self._level[levels.FACTORIES]:
            factory(self._we_manager)


        entities = self._we_manager.get_entities()
        min_x, min_y = entities[0].get_body().position
        max_x, max_y = (min_x, min_y)

        for entity in self._we_manager.get_entities():
            x,y = entity.get_body().position
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        self._killbounds = (
            (min_x - WorldInstance.KillDistance, min_y - WorldInstance.KillDistance),
            (max_x + WorldInstance.KillDistance, max_y + WorldInstance.KillDistance)
            )


        #Added this in to update the timer text when level changes
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
 
    def is_outside_world(self, entity):
        min_v, max_v = self._killbounds
        pos = entity.get_body().position
        if pos[0] < min_v[0] or pos[1] < min_v[1] or pos[0] > max_v[0] or pos[1] > max_v[1]:
            return True
        else:
            return False

    def time_left(self):
        return (self._level_max_time - self._time_elapsed)

    def restart_level(self):
        self._init_level((self._level_num))

    def next_level(self):
        self._init_level((self._level_num + 1) % len(levels.Levels))

    def previous_level(self):
        self._init_level((self._level_num - 1) % len(levels.Levels))

    def display_level_name(self, screen, font, pos):
        level_text = font.render("%s" % self._level_name, 4, (25,25,25))
        screen.blit(level_text, pos)

    def display_level_progress(self, screen, font, pos):

        color = (0,0,0)    
        if (self._level[levels.GOAL_VALUE] - self._goalbox.get_value() < 2):
            color = (255,0,0)

        progress_text = font.render("%i:%i" % (self._goalbox.get_value(), self._level[levels.GOAL_VALUE]), 4, color)
        screen.blit(progress_text, pos)


    def get_entities(self):
        return self._we_manager.get_entities()

    def tick(self, dt):
        if self.is_outside_world(self._player):
            self.restart_level()
            return

        for entity in self.get_entities():
            if self.is_outside_world(entity):
                self._we_manager.remove_entity(entity)

        self._we_manager.tick(dt)
        if self._goalbox.get_value() >= self._level[levels.GOAL_VALUE]:
            self.next_level()

        
        #hack to get chain interaction to work w/o collision
        if self._player.is_grabbing():
            min_v, max_v = self._player.get_bounding_rect()
            for entity in self.get_entities():
                if isinstance(entity, game_entities.ChainLink):
                    pos = entity.get_body().position
                    if min_v[0] -7 <= pos[0] and pos[0] <= max_v[0] + 7:
                        if min_v[1] -7  <= pos[1] and pos[1] <= max_v[1] +7:
                            end = entity.get_free_end()
                            if entity.is_single():
                                end = entity
                            if end:
                               self._player.hold(end, self._player.get_body().position)
                               head = entity.get_head()
                               head.chain_untangle(self._we_manager.alloc_collision_group())


    def get_max_time(self):
        return self._max_time

    def get_level_name(self):
        return self._level_name

    def get_space(self):
        return self._space

def main(screen):
    screensize = (screen.get_width(), screen.get_height())
    
    #hud = data.load_image("headerCropped.png")
    hud = data.load_image("header_colored.png")
    hud_shift = (screensize[0]  - hud.get_width())/2
    hud_center = hud_shift + (hud.get_width()/2)

    texture_manager = texture.TextureManager()
    texture_manager.register_texture('MUD', 'test.png')
    texture_manager.register_texture('monkey', 'monkey_resized.png')

    texture_manager.register_texture('vertPole', 'VerticalPoleSmall.png')
    texture_manager.register_texture('chain', 'Chain01.png')
    texture_manager.register_texture('balloon', 'Balloon.png')
    texture_manager.register_texture('crate1', 'Crate001.png')
    texture_manager.register_texture('bananacrate', 'BananaCrate.png')

    texture_manager.register_texture('floorBox', 'FloorBox1.png')
    texture_manager.register_texture('floorBoxRight', 'FloorBoxRight.png')
    texture_manager.register_texture('floorBoxLeft', 'FloorBoxLeft.png')

    texture_manager.register_texture('banana', 'Banana.png')
    texture_manager.register_texture('bananas', 'BananaS.png')
    texture_manager.register_texture('topPole', 'PoleToppers.png')
    texture_manager.register_texture('bottomPole', 'PoleBottoms.png')

    texture_manager.register_texture('MONKEY_L0', 'MonkeyWalk001.png')
    texture_manager.register_texture('MONKEY_L1', 'MonkeyWalk002.png')
    texture_manager.register_texture('MONKEY_L2', 'MonkeyWalk003.png')
    texture_manager.register_texture('MONKEY_L3', 'MonkeyWalk004.png')

    texture_manager.flip_texture('MONKEY_L0', 'MONKEY_R0')
    texture_manager.flip_texture('MONKEY_L1', 'MONKEY_R1')
    texture_manager.flip_texture('MONKEY_L2', 'MONKEY_R2')
    texture_manager.flip_texture('MONKEY_L3', 'MONKEY_R3')

    pymunk.init_pymunk()

    player = game_entities.Player()
    world = WorldInstance(player, texture_manager, level_num = 1)
    view = View(screensize)

    font = pygame.font.Font(None, 16)
    timerFont = pygame.font.Font(data.filepath("pointy.ttf"), 24)
    levelFont = pygame.font.Font(data.filepath("JANIS___.TTF"),50)

    clock = pygame.time.Clock()
    time = pygame.time
    MaxTime = 250
    time_elapsed = 0
    text_timer = timerFont.render("%4i" % world._level_max_time, 4, (0, 0, 0))

    unused_time = 0
    step_size = 0.005

    keydown_map = {K_w: False, K_LEFT: False, K_RIGHT: False}

    #preprime event timers
    pygame.time.set_timer(USEREVENT, 1000)

    #pygame event loop
    is_running = True
    while is_running:
        screen.fill((0x28,0x08b,0xd7))
        #perform physics in uniform steps
        space = world.get_space()
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
                elif event.key == K_SPACE or event.key == K_UP:
                    player.jump()
                elif event.key == K_z:
                    player.begin_grabbing()
                elif event.key == K_c:
                    player.begin_tagging()
                elif event.key == K_x:
                    player.drop()
                elif event.key == K_v:
                    player.begin_untagging()
                elif event.key == K_r:
                    world.restart_level()
                elif event.key == K_LEFTBRACKET:
                    world.previous_level()
                    world.display_level_name(
                            screen, font=levelFont, pos = (70+hud_shift, 165))

                elif event.key == K_RIGHTBRACKET:
                    world.next_level()
                    world.display_level_name(
                            screen, font=levelFont, pos = (70+hud_shift, 165))


            elif event.type == KEYUP:
                if event.key in keydown_map:
                    keydown_map[event.key] = False
                elif event.key == K_z:
                    player.end_grabbing()
                elif event.key == K_c:
                    player.end_tagging()
                elif event.key == K_v:
                    player.end_untagging()

            elif event.type == USEREVENT:
                world._time_elapsed += 1
                pygame.time.set_timer(USEREVENT, 1000)
                time_left = world.time_left()

                if time_left == 0:
                        world.restart_level()    
#                    world.display_level_name(screen, font=levelFont, pos = (70+hud_shift, 165))

                #render timer
                if time_left > 50:
                    color = (0, 0, 0)
                elif time_left > 10:
                    color = (155,0,0)
                else:
                    color = (255,0,0)
        
                text_timer = timerFont.render("%4i" % time_left, 4, color)


        #perframe actions
        if keydown_map[K_LEFT]:
            player.left()
        elif keydown_map[K_RIGHT]:
            player.right()
        else:
            player.stop()

        #let entites know how much time has passed
        world.tick(dt)

        #draw entities
        view.set_position(player.get_position())

        for entity in world.get_entities():
            if entity.is_textured():
                tex = texture_manager.get_texture_map(entity, entity.get_texture_name())
                image = pygame.transform.rotate(tex.image, entity.get_body().angle * 180/math.pi)
                screen.blit(image, view.to_screen(entity.get_texture_origin()))

#            pygame.draw.polygon(screen, (255,255,255), map(view.to_screen, entity.get_vertices()), 1)

        #render hud, fps, & timer
        screen.blit(hud,(hud_shift,0))
        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (25,0,0))
        screen.blit(text_surf, (5, 5))
        #screen.blit(text_timer, (370 + hud_shift, 65))
        screen.blit(text_timer, (hud_center - 30 , hud.get_height()- 34))

        world.display_level_progress(screen, font=levelFont, pos = (700+hud_shift, 55))

        if world._time_elapsed < 5:
            world.display_level_name(screen, font=levelFont, pos = (70+hud_shift, 165))        


        pygame.display.flip()

