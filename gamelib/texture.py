import data, pygame

class Texture(object):
    def __init__(self, name, file):
        self._name = name
        self._file = file
        self.image = data.load_image(file)
        self.center = (self.image.get_width()/2, self.image.get_height()/2)

class TextureManager(object):
    _textures = {}

    def register_texture(self, name, filename):
        self._textures[name] = Texture(name, filename)

    def get_texture(self, name):
        return self._textures[name]

