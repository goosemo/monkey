import pygame, os
from pygame.locals import *

import menu
import Settings

def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption(Settings.name)
    screen = pygame.display.set_mode((640, 480))
    menu.Menu(screen)
