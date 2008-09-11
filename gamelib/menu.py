#! /usr/bin/env python

import pygame, sys, data
from pygame.locals import *

import main
from ezmenu import *
from data import *

class Menu(object):
 
    def __init__(self, screen):
        self.screen = screen
        self.menu = EzMenu(["New Game", lambda: main.main()], ["Continue", None], ["Quit Game", sys.exit])
        self.menu.set_highlight_color((255, 255, 255))
        self.menu.set_normal_color((10, 10, 10))
        self.menu.center_at(180, 230)
        self.menu.set_font(pygame.font.Font(filepath("pointy.ttf"), 26))
        self.main_loop()
  
    def main_loop(self):
        while 1:
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return
        
            self.screen.fill((255, 255, 255))
            bg = load_image("loadScreen.png")
            self.screen.blit(bg, (0, 0))
            self.menu.draw(self.screen)
            pygame.display.flip()
        

def load_image(name):
    try:
        image = pygame.image.load(data.load(name))
    except pygame.error, message:
        print "couldn't load %s" % name
        sys.exit(0)

    image = image.convert_alpha()
    return image
        
