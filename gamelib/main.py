import pygame, os
from pygame.locals import *

import menu

def main():
    pygame.init()
    pygame.display.set_caption("Monkey in a Tangle")
    screen = pygame.display.set_mode((800, 600))
    menu.Menu(screen)
