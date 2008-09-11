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
    def __init__(self, level, player):
        self._space = pymunk.Space()
        self._space.gravity = (0.0, -9.8 * 40)
        self._space.damping = 0.98
        self._space.resize_static_hash(dim=10, count=1000)
        self._space.resize_active_hash(dim=10, count=1000)
        
        self._we_manager = world.EntityManager(self._space)

        self._space.set_default_collisionpair_func(self._we_manager.on_collision)

        self._level = level

        self._player = player
        self._player.get_body().position = self._level[levels.PLAYER_START]
        self._we_manager.add_entity(self._player)
        
        for entity in self._level[levels.ELEMENTS]:
            self._we_manager.add_entity(entity)

        for factory in self._level[levels.FACTORIES]:
            factory(self._we_manager)

    def get_entities(self):
        return self._we_manager.get_entities()

    def tick(self, dt):
        self._we_manager.tick(dt)

    def get_space(self):
        return self._space
       
def main(screen):
    screensize = (screen.get_width(), screen.get_height())

    pymunk.init_pymunk()

    player = game_entities.Player()
    world = WorldInstance(levels.Level2, player)
    view = View(screensize)

    texture_manager = texture.TextureManager()
    texture_manager.register_texture('MUD', 'test.png')
    texture_manager.register_texture('crossPole', 'CrossPoleTexture01.png')

    font = pygame.font.Font(None, 16)

    clock = pygame.time.Clock()
    unused_time = 0
    step_size = 0.001

    keydown_map = {K_w: False, K_d: False, K_a: False, K_LEFT: False, K_RIGHT: False}
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
                elif event.key == K_v:
                    make_chain(we_manager, 8, True)
                elif event.key == K_c:
                    make_chain(we_manager, 8, False)
                elif event.key == K_SPACE or event.key == K_UP:
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
        world.tick(dt)

        #draw entities
        view.set_position(player.get_position())

        for entity in world.get_entities():
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


