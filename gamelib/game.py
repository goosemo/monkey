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
        
        for entity in self._level[levels.ELEMENTS]:
            self._we_manager.add_entity(entity())

        for factory in self._level[levels.FACTORIES]:
            factory(self._we_manager)

    def next_level(self):
        self._init_level((self._level_num + 1) % len(levels.Levels))

    def previous_level(self):
        self._init_level((self._level_num - 1) % len(levels.Levels))

    def get_entities(self):
        return self._we_manager.get_entities()

    def tick(self, dt):
        self._we_manager.tick(dt)

    def get_time_passed(self):
        return self._we_manager.get_time_passed()

    def get_space(self):
        return self._space

def main(screen):
    screensize = (screen.get_width(), screen.get_height())
    
    hud = data.load_image("headerCropped.png")
    hud_shift = (screensize[0]  - hud.get_width())/2

    texture_manager = texture.TextureManager()
    texture_manager.register_texture('MUD', 'test.png')
    texture_manager.register_texture('monkey', 'monkey.png')

    texture_manager.register_texture('vertPole', 'VerticalPoleSmall.png')
    texture_manager.register_texture('chain', 'Chain01.png')
    texture_manager.register_texture('balloon', 'Balloon.png')
    texture_manager.register_texture('crate1', 'Crate001.png')
    texture_manager.register_texture('floorBox', 'FloorBox1.png')

    pymunk.init_pymunk()

    player = game_entities.Player()
    world = WorldInstance(player, texture_manager, level_num = 1)
    view = View(screensize)

    font = pygame.font.Font(None, 16)
    timerFont = pygame.font.Font(data.filepath("pointy.ttf"), 24)

    clock = pygame.time.Clock()
    time = pygame.time
    MaxTime = 200
    time_elapsed = 0
    text_timer = timerFont.render("%4i" % MaxTime, 4, (255,255,255))


    unused_time = 0
    step_size = 0.001

    keydown_map = {K_w: False, K_d: False, K_a: False, K_LEFT: False, K_RIGHT: False}

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
                elif event.key == K_s:
                    player.begin_grabbing()
                elif event.key == K_e:
                    player.begin_tagging()
                elif event.key == K_q:
                    player.drop()
                elif event.key == K_LEFTBRACKET:
                    world.previous_level()  
                elif event.key == K_RIGHTBRACKET:
                    world.next_level()


            elif event.type == KEYUP:
                if event.key in keydown_map:
                    keydown_map[event.key] = False
                elif event.key == K_s:
                    player.end_grabbing()
                elif event.key == K_e:
                    player.end_tagging()

            elif event.type == USEREVENT:
                time_elapsed += 1
                pygame.time.set_timer(USEREVENT, 1000)
                time_left = MaxTime - time_elapsed

                if time_left == 0:
                    time_elapsed = 0
                    world.next_level()        
                #render timer
                if (time_left > 10):
                    color = (255,255,255)
                else:
                    color = (255,0,0)
        
                text_timer = timerFont.render("%4i" % time_left, 4, color)


        #perframe actions
        if keydown_map[K_a] or keydown_map[K_LEFT]:
            player.left()
        elif keydown_map[K_d] or keydown_map[K_RIGHT]:
            player.right()
        else:
            player.stop()

        #let entites know how much time has passed
        world.tick(dt)

        #draw entities
        view.set_position(player.get_position())

        for entity in world.get_entities():
            if entity.is_textured():
                tex = texture_manager.get_texture_map(entity)
                image = pygame.transform.rotate(tex.image, entity.get_body().angle * 180/math.pi)
                screen.blit(image, view.to_screen(entity.get_texture_origin()))

#            color = (255, 0, 0)
#            pygame.draw.circle(screen, color, view.to_screen(entity.get_body().position),3)
#            color = (0,0,128,128)
#            points = map(view.to_screen, entity.get_vertices())
#            pygame.draw.polygon(screen, color, points, 1)

        #render hud, fps, & timer
        screen.blit(hud,(hud_shift,0))
        text_surf = font.render("fps: %i" % clock.get_fps(), 1, (255,0,0))
        screen.blit(text_surf, (5, 5))
        screen.blit(text_timer, (370 + hud_shift, 65))

        pygame.display.flip()


