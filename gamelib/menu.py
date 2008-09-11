#! /usr/bin/env python

import pygame, sys, data
from pygame.locals import *

import game 
from ezmenu import *
from data import *

class Menu(object):
 
    def __init__(self, screen):
        self.screen = screen
        self.menu = EzMenu(["New Game", lambda: game.main(self.screen)], ["Quit Game", sys.exit])
        self.menu.set_highlight_color((255, 255, 255))
        self.menu.set_normal_color((10, 10, 10))
        self.menu.center_at(180, 230)
        self.menu.set_font(pygame.font.Font(filepath("pointy.ttf"), 36))
        self.main_loop()
  
    def main_loop(self):
        while True:
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
        
