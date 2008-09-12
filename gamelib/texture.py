import data, pygame, math
from pymunk.vec2d import Vec2d

class Texture(object):
    def __init__(self, image):
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.center = (self.width/2, self.height/2)

def wrld_to_img(verts, min_v):
    m_x, m_y = min_v
    return [(x-m_x,-(y-m_y)) for x,y in verts]

class TextureManager(object):
    def __init__(self):
        self._textures = {}
        self.clear_texture_maps()

    def register_texture(self, name, filename):
        image = data.load_image(filename)
        self._textures[name] = Texture(image)

    def get_texture(self, name):
        return self._textures[name]

    def get_texture_map(self, entity):
        if entity not in self._texture_maps:
            self.texture_map_entity(entity)

        return self._texture_maps[entity]

    def texture_map_entity(self, entity):
        texture_name = entity.get_texture_name()
        if not texture_name:
            return

        texture = self.get_texture(texture_name)
        min_v,max_v = entity.get_bounding_rect()

        ent_width  = max_v[0] - min_v[0]
        ent_height = max_v[1] - min_v[1]

        texture_sheet = pygame.Surface((int(ent_width), int(ent_height))).convert_alpha()
        texture_sheet.fill((0,0,0,0))

        num_x_copies = int(math.ceil(ent_width / texture.width))
        num_y_copies = int(math.ceil(ent_height / texture.height))
        for i in range(num_x_copies):
            for j in range(num_y_copies):
                dest = (i*texture.width, j*texture.height)
                texture_sheet.blit(texture.image, dest)

        final_texture = Texture(texture_sheet)
        self._texture_maps[entity] = final_texture

        return final_texture
    
    def clear_texture_maps(self):
        self._texture_maps = {}
